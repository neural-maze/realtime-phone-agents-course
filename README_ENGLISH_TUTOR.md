# English Tutor - AI-Powered Language Learning Agent

Full local English tutor with streaming audio/text conversation using Gradio + LangGraph + Ollama.

## Features

- 🎯 **Personalized Learning**: Adaptive exercises based on your competencies
- 🗣️ **Speaking Practice**: Real-time pronunciation feedback with STT
- ✍️ **Writing Exercises**: Grammar and vocabulary drills
- 👂 **Listening Comprehension**: Audio-based exercises
- 📊 **Progress Tracking**: Monitor your skills improvement
- 🤖 **AI Tutor**: Conversational agent that adapts to your level
- 🔒 **100% Local**: All models run locally (Ollama + local TTS/STT)

## Architecture

- **LLM**: Ollama (llama3.2, qwen2.5, or any model you have installed)
- **TTS**: Kokoro (local English TTS) or Together AI
- **STT**: Whisper-based models (Groq, Moonshine, Faster Whisper)
- **Agent Framework**: LangGraph for stateful conversation workflows
- **UI**: Gradio with streaming audio + text chat
- **Database**: SQLite for progress tracking

## Competencies Tracked

1. **Grammar** - Sentence structure, tenses, articles, etc.
2. **Vocabulary** - Word knowledge, synonyms, collocations
3. **Pronunciation** - Phonetics, intonation, fluency
4. **Listening** - Comprehension, dictation, audio understanding
5. **Speaking** - Conversational fluency, spontaneity
6. **Writing** - Written expression, spelling, coherence

## Installation

First, create the directory structure:
```bash
python create_dirs.py
```

Then install dependencies:
```bash
cd english_tutor
pip install -e .
```

Or with uv:
```bash
cd english_tutor
uv pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Edit `.env` with your settings (Ollama model, API keys if using cloud STT/TTS).

## Usage

```bash
cd english_tutor
python scripts/run_tutor.py
```

Or from parent directory:
```bash
uv run python english_tutor/scripts/run_tutor.py
```

## Project Structure

```
english_tutor/
├── src/english_tutor/
│   ├── agent/              # LangGraph agent workflow
│   ├── competencies/       # Skills tracking system
│   ├── exercises/          # Exercise generators
│   ├── ui/                 # Gradio interface
│   ├── models/             # TTS/STT/LLM wrappers
│   └── database/           # SQLite persistence
├── scripts/
│   └── run_tutor.py        # Main entry point
├── data/                   # Student progress database
└── pyproject.toml
```

## License

MIT
