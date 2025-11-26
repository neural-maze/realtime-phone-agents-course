# src/realtime_phone_agents/agent/fastrtc_agent.py

import asyncio
from typing import AsyncIterator, List, Optional, Tuple

import numpy as np
from fastrtc import ReplyOnPause, Stream, get_stt_model, get_tts_model
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from loguru import logger

from realtime_phone_agents.agent.tools.property_search import search_property_tool
from realtime_phone_agents.agent.utils import model_has_tool_calls
from realtime_phone_agents.config import settings
from realtime_phone_agents.voice import get_sound_effect

AudioChunk = Tuple[int, np.ndarray]  # (sample_rate, samples)

DEFAULT_SYSTEM_PROMPT = """
Your name is Lisa, and you work for The Neural Maze real estate company. 
Your task is to provide information about specific apartments using the `search_property_tool`.
Don't use asterisks or emojis, as you are engaged in a phone call. Just return short and informative responses.
The information you provide to the user should be concrete, summarised and easy to understand. 

This are some examples of good responses:

- "I found one apartment in that area. It features 3 rooms, 2 bathrooms, and a beautifully designed living room!"
- "I have two appartments for you. The first one is a 3 bedroom, 2 bathroom apartment in the center of the city. The second one is a 2 bedroom, 1 bathroom apartment in the suburbs. The first one is 1000 square feet and the second one is 800 square feet."
""".strip()


class FastRTCAgent:
    """
    Simplified FastRTC agent that encapsulates all dependencies and logic
    for processing audio through speech-to-text, agent reasoning, and text-to-speech.

    This class combines the React agent creation and FastRTC streaming into a single
    cohesive unit, optimized for mobile phone compatibility by avoiding gradio additional_inputs.
    """

    def __init__(
        self,
        tool_use_message: str = "Let me look for that in the system",
        sound_effect_seconds: float = 3.0,
        stt_model=None,
        tts_model=None,
        voice_effect=None,
        thread_id: str = "default",
        fallback_message: str = "I'm sorry, I couldn't find anything useful in the system.",
        system_prompt: str | None = None,
        tools: List | None = None,
    ):
        """
        Initialize the FastRTC agent with all its dependencies.

        Args:
            tool_use_message: Message to speak when using tools
            sound_effect_seconds: Duration for sound effects when using tools (e.g. keyboard sound)
            stt_model: Speech-to-text model (defaults to get_stt_model())
            tts_model: Text-to-speech model (defaults to get_tts_model())
            voice_effect: Voice effect instance (defaults to get_sound_effect())
            thread_id: Thread ID for agent conversation tracking
            fallback_message: Message to return when no answer is found
            system_prompt: Custom system prompt for the agent
            tools: List of tools for the agent (defaults to property search tool)
        """
        # Dependency injection with sensible defaults
        self._stt_model = stt_model or get_stt_model()
        self._tts_model = tts_model or get_tts_model()
        self._voice_effect = voice_effect or get_sound_effect()

        # Create the React agent directly inside the class
        self._react_agent = self._create_react_agent(
            system_prompt=system_prompt,
            tools=tools,
        )

        # Configuration - stored as instance variables to avoid gradio additional_inputs
        self._thread_id = thread_id
        self._fallback_message = fallback_message
        self._tool_use_message = tool_use_message
        self._sound_effect_seconds = sound_effect_seconds

        # Build the FastRTC Stream with the handler
        self._stream = self._build_stream()

    def _create_react_agent(
        self,
        system_prompt: str | None = None,
        tools: List | None = None,
    ):
        """
        Create and return a LangChain agent with Groq + InMemorySaver + tools.

        Args:
            system_prompt: Custom system prompt (defaults to DEFAULT_SYSTEM_PROMPT)
            tools: List of tools (defaults to [search_property_mock_tool])

        Returns:
            Configured LangChain agent
        """
        llm = ChatGroq(
            model=settings.groq.model,
            api_key=settings.groq.api_key,
        )

        system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        tools = tools or [search_property_tool]

        agent = create_agent(
            llm,
            checkpointer=InMemorySaver(),
            system_prompt=system_prompt,
            tools=tools,
        )
        return agent

    def _build_stream(self) -> Stream:
        """
        Build and configure the FastRTC Stream with the agent handler.
        Uses instance variables instead of gradio additional_inputs for mobile compatibility.

        Returns:
            Configured Stream instance
        """

        async def handler_wrapper(audio: AudioChunk) -> AsyncIterator[AudioChunk]:
            """Handler that uses instance variables directly."""
            async for chunk in self._process_audio(audio):
                yield chunk

        return Stream(
            handler=ReplyOnPause(handler_wrapper),
            modality="audio",
            mode="send-receive",
        )

    async def _process_audio(
        self,
        audio: AudioChunk,
    ) -> AsyncIterator[AudioChunk]:
        """
        Process audio input through the complete pipeline:
        STT -> Agent Reasoning -> TTS with effects.
        Uses instance variables for configuration (tool_use_message, sound_effect_seconds).

        Args:
            audio: Input audio chunk (sample_rate, samples)

        Yields:
            Audio chunks to be played back to the user
        """
        # Step 1: Transcribe audio to text
        transcription = await self._transcribe(audio)
        logger.info(f"Transcription: {transcription}")

        # Step 2: Process with agent and stream responses
        async for audio_chunk in self._process_with_agent(transcription):
            if audio_chunk is not None:
                yield audio_chunk

        # Step 3: Speak final answer
        final_response = await self._get_final_response()
        logger.info(f"Final response: {final_response}")

        if final_response:
            async for audio_chunk in self._synthesize_speech(final_response):
                yield audio_chunk

    async def _transcribe(self, audio: AudioChunk) -> str:
        """
        Transcribe audio to text using STT model.

        Args:
            audio: Audio chunk to transcribe

        Returns:
            Transcribed text
        """
        return self._stt_model.stt(audio)

    async def _process_with_agent(
        self,
        transcription: str,
    ) -> AsyncIterator[Optional[AudioChunk]]:
        """
        Process transcription through the agent and handle tool calls.
        Uses instance variables for tool_use_message and sound_effect_seconds.

        Args:
            transcription: User's transcribed message

        Yields:
            Audio chunks for tool use messages and effects
        """
        final_text: str | None = None

        # Stream LangChain agent updates
        async for chunk in self._react_agent.astream(
            {"messages": [{"role": "user", "content": transcription}]},
            {"configurable": {"thread_id": self._thread_id}},
            stream_mode="updates",
        ):
            for step, data in chunk.items():
                # Handle tool calls
                if step == "model" and model_has_tool_calls(data):
                    # Speak tool-use message
                    async for audio_chunk in self._synthesize_speech(
                        self._tool_use_message
                    ):
                        yield audio_chunk

                    # Play sound effect
                    if self._sound_effect_seconds > 0:
                        async for effect_chunk in self._play_sound_effect():
                            yield effect_chunk

                # Capture final text from model response
                if step == "model":
                    final_text = self._extract_final_text(data)

        # Store final text for later retrieval
        self._last_final_text = final_text

    def _extract_final_text(self, model_step_data) -> Optional[str]:
        """
        Extract the final text response from model step data.

        Args:
            model_step_data: Data from the model step

        Returns:
            Extracted text or None
        """
        msgs = model_step_data.get("messages", [])
        if isinstance(msgs, list) and len(msgs) > 0:
            return getattr(msgs[0], "content", None)
        return None

    async def _get_final_response(self) -> str:
        """
        Get the final response text to speak to the user.

        Returns:
            Final response text
        """
        return getattr(self, "_last_final_text", None) or self._fallback_message

    async def _synthesize_speech(self, text: str) -> AsyncIterator[AudioChunk]:
        """
        Convert text to speech audio chunks.

        Args:
            text: Text to synthesize

        Yields:
            Audio chunks
        """
        async for audio_chunk in self._tts_model.stream_tts(text):
            yield audio_chunk

    async def _play_sound_effect(self) -> AsyncIterator[AudioChunk]:
        """
        Play the configured sound effect.

        Yields:
            Audio chunks for the sound effect
        """
        async for effect_chunk in self._voice_effect.stream():
            yield effect_chunk

    @property
    def stream(self) -> Stream:
        """
        Expose the FastRTC Stream instance.

        Returns:
            The configured Stream instance
        """
        return self._stream

    @property
    def stt_model(self):
        """Get the speech-to-text model."""
        return self._stt_model

    @property
    def tts_model(self):
        """Get the text-to-speech model."""
        return self._tts_model

    @property
    def react_agent(self):
        """Get the React agent."""
        return self._react_agent

    @property
    def voice_effect(self):
        """Get the voice effect."""
        return self._voice_effect

    def set_thread_id(self, thread_id: str) -> None:
        """
        Update the thread ID for conversation tracking.

        Args:
            thread_id: New thread ID
        """
        self._thread_id = thread_id

    def set_fallback_message(self, message: str) -> None:
        """
        Update the fallback message.

        Args:
            message: New fallback message
        """
        self._fallback_message = message

    def set_tool_use_message(self, message: str) -> None:
        """
        Update the tool use message.

        Args:
            message: New tool use message
        """
        self._tool_use_message = message

    def set_sound_effect_seconds(self, seconds: float) -> None:
        """
        Update the sound effect duration.

        Args:
            seconds: New sound effect duration
        """
        self._sound_effect_seconds = seconds
