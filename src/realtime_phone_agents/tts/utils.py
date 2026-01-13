from realtime_phone_agents.tts.base import TTSModel
from realtime_phone_agents.tts.local.kokoro import KokoroTTSModel
from realtime_phone_agents.tts.runpod import OrpheusTTSModel
from realtime_phone_agents.tts.togetherai import TogetherTTSModel
from realtime_phone_agents.tts.edge import EdgeTTSModel
from realtime_phone_agents.tts.gtts import GoogleTTSModel
from loguru import logger

def get_tts_model(model_name: str) -> TTSModel:
    """Get a TTS model by name.

    Available options:
        - "melo": MeloTTS - High quality Spanish, runs locally on CPU (recommended)
        - "openai": OpenAI TTS - Professional quality, requires API key
        - "gtts": Google TTS with Spanish support (free, reliable fallback)
        - "edge": Edge TTS with Spanish voice (free, requires stable DNS)
        - "kokoro": Local Kokoro TTS via FastRTC (English only)
        - "together": Together AI API (Orpheus - English voices)
        - "minimax": MiniMax Speech 2.6 via Together AI (best quality, requires API key)
        - "orpheus-runpod": Orpheus TTS via RunPod deployment
    """
    if model_name == "melo":
        from realtime_phone_agents.tts.melo import MeloTTSModel
        logger.info("Loading MeloTTS model (this may take a moment on first run)...")
        return MeloTTSModel(language="ES", device="auto")
    elif model_name == "openai":
        from realtime_phone_agents.tts.openai import OpenAITTSModel
        return OpenAITTSModel(voice="nova") # Nova is a good female voice for Carmen
    elif model_name == "kokoro":
        return KokoroTTSModel()
    elif model_name == "orpheus-runpod":
        orpheus_model = OrpheusTTSModel()
        logger.info("Warming up Orpheus TTS model...")
        orpheus_model.tts_blocking("This is just a simple message to warmup the model")
        return orpheus_model
    elif model_name == "together":
        return TogetherTTSModel()
    elif model_name == "minimax":
        # MiniMax Speech 2.6 Turbo via Together AI
        from realtime_phone_agents.tts.togetherai.options import TogetherTTSOptions
        options = TogetherTTSOptions(
            model="minimax/speech-2.6-turbo",
            voice="Spanish_Female_1",  # MiniMax Spanish voice
        )
        return TogetherTTSModel(options=options)
    elif model_name == "edge":
        return EdgeTTSModel(voice="es-ES-AlvaroNeural")  # Spanish male voice
    elif model_name == "gtts":
        return GoogleTTSModel(lang="es", tld="es")  # Spanish Spain accent
    else:
        raise ValueError(
            f"Invalid TTS model name: {model_name}. Available: melo, gtts, edge, kokoro, together, minimax, orpheus-runpod"
        )
