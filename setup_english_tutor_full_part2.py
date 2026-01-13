#!/usr/bin/env python3
"""
Part 2: Agent, Models and UI generation.
Run after setup_english_tutor_full.py
"""
from pathlib import Path
from textwrap import dedent

def write_file(path: str, content: str):
    """Write content to file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(dedent(content).strip() + '\n', encoding='utf-8')
    print(f"✓ {path}")

def setup_agent_and_ui():
    """Generate agent, models and UI files."""
    
    print("\n🤖 Generating Agent, Models & UI...\n")
    
    # ==================== MODELS (TTS/STT wrappers) ====================
    
    write_file('english_tutor/src/english_tutor/models/__init__.py', '''
    """TTS and STT model integrations."""
    from .stt import get_stt_model, STTModel
    from .tts import get_tts_model, TTSModel
    
    __all__ = ["get_stt_model", "get_tts_model", "STTModel", "TTSModel"]
    ''')
    
    write_file('english_tutor/src/english_tutor/models/stt.py', '''
    """Speech-to-Text model integration."""
    import sys
    from pathlib import Path
    
    # Add parent project to path to import STT models
    parent_src = Path(__file__).parents[4] / "src"
    sys.path.insert(0, str(parent_src))
    
    try:
        from realtime_phone_agents.stt import get_stt_model as get_parent_stt
        from realtime_phone_agents.stt.base import STTModel
    except ImportError:
        # Fallback stub if parent project not available
        class STTModel:
            async def stt(self, audio_data, **kwargs):
                return "Transcribed text placeholder"
        
        def get_parent_stt(model_name: str):
            return STTModel()
    
    
    def get_stt_model(model_name: str = "whisper-groq") -> STTModel:
        """Get STT model from parent project."""
        return get_parent_stt(model_name)
    ''')
    
    write_file('english_tutor/src/english_tutor/models/tts.py', '''
    """Text-to-Speech model integration."""
    import sys
    from pathlib import Path
    
    # Add parent project to path
    parent_src = Path(__file__).parents[4] / "src"
    sys.path.insert(0, str(parent_src))
    
    try:
        from realtime_phone_agents.tts import get_tts_model as get_parent_tts
        from realtime_phone_agents.tts.base import TTSModel
    except ImportError:
        # Fallback stub
        import numpy as np
        
        class TTSModel:
            def tts(self, text: str, **kwargs):
                # Return dummy audio
                return (24000, np.zeros(24000, dtype=np.int16))
            
            def stream_tts(self, text: str, **kwargs):
                yield (24000, np.zeros(4800, dtype=np.int16))
        
        def get_parent_tts(model_name: str):
            return TTSModel()
    
    
    def get_tts_model(model_name: str = "kokoro") -> TTSModel:
        """Get TTS model from parent project."""
        return get_parent_tts(model_name)
    ''')
    
    # ==================== AGENT (LangGraph) ====================
    
    write_file('english_tutor/src/english_tutor/agent/__init__.py', '''
    """LangGraph-based tutor agent."""
    from .tutor_agent import TutorAgent, create_tutor_graph
    
    __all__ = ["TutorAgent", "create_tutor_graph"]
    ''')
    
    write_file('english_tutor/src/english_tutor/agent/state.py', '''
    """Agent state definition."""
    from typing import TypedDict, Annotated, Sequence
    from langchain_core.messages import BaseMessage
    import operator
    
    
    class AgentState(TypedDict):
        """State for tutor agent."""
        messages: Annotated[Sequence[BaseMessage], operator.add]
        current_exercise: str
        student_response: str
        feedback: str
        next_action: str  # "exercise", "conversation", "feedback"
    ''')
    
    write_file('english_tutor/src/english_tutor/agent/tutor_agent.py', '''
    """Tutor agent implementation using LangGraph."""
    from typing import Optional
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_ollama import ChatOllama
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    from loguru import logger
    
    from .state import AgentState
    from ..competencies.models import StudentProfile
    from ..competencies.tracker import CompetencyTracker
    from ..exercises.generator import ExerciseGenerator
    
    
    class TutorAgent:
        """English tutor agent with LangGraph."""
        
        def __init__(
            self,
            profile: StudentProfile,
            llm: ChatOllama,
            tracker: CompetencyTracker,
            exercise_gen: ExerciseGenerator
        ):
            self.profile = profile
            self.llm = llm
            self.tracker = tracker
            self.exercise_gen = exercise_gen
            self.graph = create_tutor_graph(self)
            self.memory = MemorySaver()
        
        def get_system_prompt(self) -> str:
            """Generate system prompt based on student profile."""
            return f"""You are an English tutor AI helping {self.profile.name}.
    
    Student Level: {self.profile.level.value}
    Weakest Area: {self.profile.get_weakest_competency().value}
    
    Your role:
    - Provide clear, encouraging feedback
    - Adapt difficulty to student level
    - Focus on areas needing improvement
    - Use simple English for beginners
    - Be patient and supportive
    
    Always respond in a friendly, educational tone."""
        
        def process_student_input(self, user_input: str, thread_id: str = "default") -> str:
            """Process student input through the agent graph."""
            initial_state = {
                "messages": [
                    SystemMessage(content=self.get_system_prompt()),
                    HumanMessage(content=user_input)
                ],
                "current_exercise": "",
                "student_response": user_input,
                "feedback": "",
                "next_action": "conversation"
            }
            
            config = {"configurable": {"thread_id": thread_id}}
            result = self.graph.invoke(initial_state, config)
            
            # Extract last AI message
            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage):
                    return msg.content
            
            return "I'm here to help you learn English!"
    
    
    def create_tutor_graph(agent: TutorAgent) -> StateGraph:
        """Create LangGraph workflow for tutoring."""
        
        def should_give_exercise(state: AgentState) -> str:
            """Decide if we should give an exercise."""
            last_msg = state["messages"][-1].content.lower() if state["messages"] else ""
            
            if any(word in last_msg for word in ["exercise", "practice", "test", "quiz"]):
                return "exercise"
            return "respond"
        
        def generate_response(state: AgentState) -> AgentState:
            """Generate conversational response."""
            response = agent.llm.invoke(state["messages"])
            state["messages"].append(response)
            return state
        
        def generate_exercise(state: AgentState) -> AgentState:
            """Generate an exercise based on weak areas."""
            weak_competency = agent.profile.get_weakest_competency()
            
            exercise_text = f"""Let's practice {weak_competency.value}!
    
    {agent.exercise_gen.generate_conversation_prompt(agent.profile.level)}
    
    Take your time and do your best!"""
            
            state["messages"].append(AIMessage(content=exercise_text))
            state["current_exercise"] = exercise_text
            state["next_action"] = "feedback"
            return state
        
        def provide_feedback(state: AgentState) -> AgentState:
            """Provide feedback on student response."""
            feedback_prompt = f"""The student was given this exercise:
    {state['current_exercise']}
    
    Their response: {state['student_response']}
    
    Provide encouraging, constructive feedback. Highlight what they did well and suggest one improvement."""
            
            messages = [
                SystemMessage(content=agent.get_system_prompt()),
                HumanMessage(content=feedback_prompt)
            ]
            
            response = agent.llm.invoke(messages)
            state["messages"].append(response)
            state["feedback"] = response.content
            return state
        
        # Build graph
        workflow = StateGraph(AgentState)
        
        workflow.add_node("respond", generate_response)
        workflow.add_node("exercise", generate_exercise)
        workflow.add_node("feedback", provide_feedback)
        
        workflow.set_entry_point("respond")
        
        workflow.add_conditional_edges(
            "respond",
            should_give_exercise,
            {
                "exercise": "exercise",
                "respond": END
            }
        )
        
        workflow.add_edge("exercise", END)
        workflow.add_edge("feedback", END)
        
        return workflow.compile()
    ''')
    
    # ==================== UI (Gradio) ====================
    
    write_file('english_tutor/src/english_tutor/ui/__init__.py', '''
    """Gradio user interface."""
    from .app import create_gradio_interface
    
    __all__ = ["create_gradio_interface"]
    ''')
    
    write_file('english_tutor/src/english_tutor/ui/app.py', '''
    """Gradio interface for English Tutor."""
    import gradio as gr
    import numpy as np
    from typing import Optional
    from loguru import logger
    
    from ..agent.tutor_agent import TutorAgent
    from ..models.stt import get_stt_model
    from ..models.tts import get_tts_model
    from ..competencies.models import StudentProfile
    
    
    def create_gradio_interface(
        agent: TutorAgent,
        profile: StudentProfile,
        stt_model,
        tts_model
    ) -> gr.Blocks:
        """Create Gradio interface for the tutor."""
        
        with gr.Blocks(title="English Tutor", theme=gr.themes.Soft()) as demo:
            gr.Markdown("# 🎓 AI English Tutor")
            gr.Markdown(f"**Student:** {profile.name} | **Level:** {profile.level.value}")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(label="Conversation", height=400)
                    
                    with gr.Tab("Text"):
                        text_input = gr.Textbox(
                            label="Type your message",
                            placeholder="Ask a question or request an exercise...",
                            lines=2
                        )
                        text_submit = gr.Button("Send", variant="primary")
                    
                    with gr.Tab("Voice"):
                        audio_input = gr.Audio(
                            label="Speak your response",
                            sources=["microphone"],
                            type="filepath"
                        )
                        audio_submit = gr.Button("Submit Audio", variant="primary")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Progress")
                    
                    progress_text = gr.Markdown(
                        f"""
                        **Exercises:** {profile.exercises_completed}
                        
                        **Competencies:**
                        """
                    )
                    
                    competency_bars = {}
                    for comp in profile.competencies:
                        score = profile.get_competency_score(comp)
                        competency_bars[comp] = gr.Slider(
                            label=comp.value.title(),
                            value=score,
                            minimum=0,
                            maximum=100,
                            interactive=False
                        )
                    
                    recommendation = gr.Textbox(
                        label="Recommendation",
                        value=agent.tracker.get_recommendation(),
                        interactive=False
                    )
            
            # Chat history
            chat_history = gr.State([])
            
            def respond_text(message: str, history: list) -> tuple:
                """Handle text input."""
                if not message.strip():
                    return history, ""
                
                # Add user message
                history.append((message, None))
                
                # Get agent response
                response = agent.process_student_input(message)
                
                # Add AI response
                history[-1] = (message, response)
                
                return history, ""
            
            async def respond_audio(audio_path: Optional[str], history: list) -> tuple:
                """Handle audio input."""
                if not audio_path:
                    return history, None
                
                try:
                    # Transcribe audio
                    transcription = await stt_model.stt(audio_path)
                    logger.info(f"Transcribed: {transcription}")
                    
                    # Add user message
                    history.append((f"🎤 {transcription}", None))
                    
                    # Get agent response
                    response = agent.process_student_input(transcription)
                    
                    # Generate TTS response
                    sample_rate, audio_data = tts_model.tts(response)
                    
                    # Update history
                    history[-1] = (f"🎤 {transcription}", f"🔊 {response}")
                    
                    return history, (sample_rate, audio_data)
                    
                except Exception as e:
                    logger.error(f"Audio processing error: {e}")
                    history.append(("🎤 [Audio]", f"Sorry, I couldn't process that. Error: {str(e)}"))
                    return history, None
            
            # Connect handlers
            text_submit.click(
                respond_text,
                inputs=[text_input, chat_history],
                outputs=[chatbot, text_input]
            ).then(
                lambda h: h,
                inputs=[chat_history],
                outputs=[chat_history]
            )
            
            audio_submit.click(
                respond_audio,
                inputs=[audio_input, chat_history],
                outputs=[chatbot, audio_input]
            ).then(
                lambda h: h,
                inputs=[chat_history],
                outputs=[chat_history]
            )
            
            # Enter key support
            text_input.submit(
                respond_text,
                inputs=[text_input, chat_history],
                outputs=[chatbot, text_input]
            )
        
        return demo
    ''')
    
    # ==================== MAIN TUTOR CLASS ====================
    
    write_file('english_tutor/src/english_tutor/tutor.py', '''
    """Main English Tutor class."""
    from typing import Optional
    from langchain_ollama import ChatOllama
    from loguru import logger
    
    from .config import settings
    from .competencies.models import StudentProfile, CompetencyLevel
    from .competencies.tracker import CompetencyTracker
    from .exercises.generator import ExerciseGenerator
    from .agent.tutor_agent import TutorAgent
    from .database.storage import StudentDatabase
    from .models.stt import get_stt_model
    from .models.tts import get_tts_model
    from .ui.app import create_gradio_interface
    
    
    class EnglishTutor:
        """Complete English Tutor system."""
        
        def __init__(
            self,
            student_name: Optional[str] = None,
            llm_model: Optional[str] = None,
            stt_model_name: Optional[str] = None,
            tts_model_name: Optional[str] = None
        ):
            """Initialize English Tutor.
            
            Args:
                student_name: Student name (loads existing or creates new)
                llm_model: Ollama model name
                stt_model_name: STT model name
                tts_model_name: TTS model name
            """
            self.student_name = student_name or settings.default_student_name
            
            # Initialize database
            self.db = StudentDatabase(settings.database_path)
            
            # Load or create profile
            self.profile = self.db.load_profile(self.student_name)
            if not self.profile:
                logger.info(f"Creating new profile for {self.student_name}")
                self.profile = StudentProfile(
                    name=self.student_name,
                    level=CompetencyLevel(settings.initial_level)
                )
                self.db.save_profile(self.profile)
            
            # Initialize LLM
            self.llm = ChatOllama(
                model=llm_model or settings.ollama_model,
                base_url=settings.ollama_base_url,
                temperature=0.7
            )
            
            # Initialize components
            self.tracker = CompetencyTracker(self.profile)
            self.exercise_gen = ExerciseGenerator(self.llm)
            self.agent = TutorAgent(
                profile=self.profile,
                llm=self.llm,
                tracker=self.tracker,
                exercise_gen=self.exercise_gen
            )
            
            # Initialize STT/TTS
            self.stt_model = get_stt_model(stt_model_name or settings.stt_model)
            self.tts_model = get_tts_model(tts_model_name or settings.tts_model)
            
            # Create UI
            self.ui = create_gradio_interface(
                agent=self.agent,
                profile=self.profile,
                stt_model=self.stt_model,
                tts_model=self.tts_model
            )
        
        def launch(self, **kwargs):
            """Launch Gradio interface."""
            default_kwargs = {
                "server_port": settings.server_port,
                "share": settings.share_gradio
            }
            default_kwargs.update(kwargs)
            
            logger.info(f"Launching English Tutor for {self.student_name}")
            self.ui.launch(**default_kwargs)
        
        def save_progress(self):
            """Save student progress to database."""
            self.db.save_profile(self.profile)
            logger.info(f"Progress saved for {self.student_name}")
    ''')
    
    # ==================== RUN SCRIPT ====================
    
    write_file('english_tutor/scripts/run_tutor.py', '''
    #!/usr/bin/env python3
    """Run the English Tutor application."""
    import sys
    from pathlib import Path
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
    
    from english_tutor import EnglishTutor
    from loguru import logger
    
    
    def main():
        """Main entry point."""
        logger.info("Starting English Tutor...")
        
        try:
            tutor = EnglishTutor()
            tutor.launch()
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        except Exception as e:
            logger.error(f"Error: {e}")
            raise
    
    
    if __name__ == "__main__":
        main()
    ''')
    
    # Make executable on Unix
    script_path = Path('english_tutor/scripts/run_tutor.py')
    if script_path.exists():
        script_path.chmod(0o755)
    
    print("\n✅ Agent, Models & UI generated!\n")

if __name__ == "__main__":
    setup_agent_and_ui()
    print("🎉 Complete! Now run: cd english_tutor && pip install -e . && python scripts/run_tutor.py")
