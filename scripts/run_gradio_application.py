import logging
import os
import warnings
from uuid import uuid4

# Suppress all warnings before importing other modules
warnings.filterwarnings("ignore")

# Set environment variables to suppress model download logs
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Configure logging to suppress debug messages
logging.getLogger("pydantic_settings").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("superlinked").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

# Suppress structlog debug messages if it's being used
try:
    import structlog
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.ERROR),
    )
except (ImportError, AttributeError):
    pass

import sys

import inquirer

from realtime_phone_agents.agent.fastrtc_agent import FastRTCAgent
from realtime_phone_agents.agent.tools.debt_profiling import (
    save_client_data,
    get_client_summary,
    finalize_profile,
)
from realtime_phone_agents.stt.utils import get_stt_model
from realtime_phone_agents.tts.utils import get_tts_model


def print_header():
    """Print a nice header for the application."""
    print("\n" + "=" * 60)
    print("SolucionaMiDeuda - Agente de Perfilado")
    print("=" * 60)
    print()


def print_success(message: str):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message: str):
    """Print an error message."""
    print(f"❌ {message}", file=sys.stderr)


def print_info(message: str):
    """Print an info message."""
    print(f"🔧 {message}")


def main():
    """
    🚀 FastRTC Agent Application
    
    Interactive voice agent with customizable Speech-to-Text and Text-to-Speech models.
    """
    print_header()
    
    # Define model choices with descriptions
    stt_choices = [
        ("Moonshine - Local lightweight Whisper alternative (default)", "moonshine"),
        ("Whisper Groq - Fast cloud-based Whisper via Groq API", "whisper-groq"),
        ("Faster Whisper - Optimized Whisper via RunPod deployment", "faster-whisper"),
    ]
    
    tts_choices = [
        ("MeloTTS - Alta calidad, funciona sin internet (RECOMENDADO)", "melo"),
        ("OpenAI TTS - Calidad profesional (requiere API Key)", "openai"),
        ("Google TTS - Voz basica en espanol, simple", "gtts"),
        ("Edge TTS - Voz natural (requiere DNS estable, puede fallar)", "edge"),
        ("MiniMax Speech 2.6 - Mejor calidad (requiere Together AI API)", "minimax"),
        ("Kokoro - Local TTS en ingles", "kokoro"),
        ("Together AI - Orpheus (ingles)", "together"),
    ]
    
    avatar_choices = [
        ("Carmen - Asesora de deudas (default)", "carmen"),
        ("Leo", "leo"),
        ("Zac", "zac"),
        ("Dan", "dan"),
        ("Jess", "jess"),
        ("Tara", "tara"),
        ("Zoe", "zoe"),
        ("Mia", "mia"),
        ("Leah", "leah"),
    ]
    
    # Create interactive questions
    questions = [
        inquirer.List(
            "stt_model",
            message="Select STT (Speech-to-Text) model",
            choices=stt_choices,
            default="whisper-groq",
        ),
        inquirer.List(
            "tts_model",
            message="Select TTS (Text-to-Speech) model",
            choices=tts_choices,
            default="melo",
        ),
        inquirer.List(
            "avatar",
            message="Select Avatar",
            choices=avatar_choices,
            default="carmen",
        ),
    ]
    
    try:
        answers = inquirer.prompt(questions)
        if not answers:
            print_error("Selection cancelled by user")
            sys.exit(1)
        
        stt_model = answers["stt_model"]
        tts_model = answers["tts_model"]
        avatar = answers["avatar"]
    except KeyboardInterrupt:
        print("\n\n👋 Selection cancelled by user")
        sys.exit(0)
    
    print()
    print("=" * 60)
    print(f"📝 STT Model: {stt_model}")
    print(f"🔊 TTS Model: {tts_model}")
    print(f"🎭 Avatar: {avatar}")
    print("=" * 60)
    print()

    # Para el MVP de SolucionaMiDeuda no necesitamos base de datos de propiedades
    # Las herramientas de perfilado funcionan en memoria
    print_info("Herramientas de perfilado de deudas cargadas")
    print()

    # Get the selected models
    print_info(f"Initializing {stt_model} STT model...")
    try:
        stt_model_instance = get_stt_model(stt_model)
        print_success("STT model initialized")
    except Exception as e:
        print_error(f"Error initializing STT model: {e}")
        sys.exit(1)

    print_info(f"Initializing {tts_model} TTS model...")
    try:
        tts_model_instance = get_tts_model(tts_model)
        
        # Set voice for Together AI or Orpheus RunPod models
        if tts_model in ["together", "orpheus-runpod"]:
            print_info(f"Setting voice to {avatar} for {tts_model} model...")
            tts_model_instance.set_voice(avatar)
        
        print_success("TTS model initialized")
    except Exception as e:
        print_error(f"Error initializing TTS model: {e}")
        sys.exit(1)

    print()

    # Create the FastRTC agent with selected models
    print_info("Creating FastRTC Agent...")
    try:
        agent = FastRTCAgent(
            stt_model=stt_model_instance,
            tts_model=tts_model_instance,
            tools=[save_client_data, get_client_summary, finalize_profile],
            thread_id=str("gradio-application-" + str(uuid4())),
            avatar=avatar,
        )
        print_success("FastRTC Agent created successfully")
    except Exception as e:
        print_error(f"Error creating agent: {e}")
        sys.exit(1)

    print()

    # Launch the application
    print("=" * 60)
    print("🌐 Launching Gradio interface...")
    print("=" * 60)
    print()

    try:
        agent.stream.ui.launch()
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print_error(f"Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
