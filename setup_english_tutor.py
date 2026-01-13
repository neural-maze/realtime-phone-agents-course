#!/usr/bin/env python3
"""
Complete setup script for English Tutor project.
Generates all files and directory structure.
"""
import os
from pathlib import Path

# File contents as constants
FILES = {
    'english_tutor/README.md': '''# English Tutor - AI-Powered Language Learning Agent

Full local English tutor with streaming audio/text conversation using Gradio + LangGraph + Ollama.

## Features

- 🎯 **Personalized Learning**: Adaptive exercises based on your competencies
- 🗣️ **Speaking Practice**: Real-time pronunciation feedback with STT
- ✍️ **Writing Exercises**: Grammar and vocabulary drills  
- 👂 **Listening Comprehension**: Audio-based exercises
- 📊 **Progress Tracking**: Monitor your skills improvement
- 🤖 **AI Tutor**: Conversational agent that adapts to your level
- 🔒 **100% Local**: All models run locally (Ollama + local TTS/STT)

## Quick Start

```bash
# From parent directory
python setup_english_tutor.py

# Configure environment
cd english_tutor
cp .env.example .env
# Edit .env with your settings

# Install dependencies
pip install -e .

# Run tutor
python scripts/run_tutor.py
```

## Competencies Tracked

1. **Grammar** - Sentence structure, tenses, articles
2. **Vocabulary** - Word knowledge, synonyms, collocations  
3. **Pronunciation** - Phonetics, intonation, fluency
4. **Listening** - Comprehension, dictation
5. **Speaking** - Conversational fluency
6. **Writing** - Written expression, spelling

## License

MIT
''',

    'english_tutor/pyproject.toml': '''[project]
name = "english-tutor"
version = "0.1.0"
description = "AI-Powered English Tutor with streaming audio/text conversation"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "gradio>=5.14.0",
    "langchain>=0.3.15",
    "langchain-ollama>=0.2.2",
    "langgraph>=0.2.67",
    "loguru>=0.7.3",
    "numpy>=1.26.4",
    "pydantic>=2.11.10",
    "pydantic-settings>=2.12.0",
    "soundfile>=0.12.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/english_tutor"]
''',

    'english_tutor/.env.example': '''# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# STT Configuration
STT_MODEL=whisper-groq
GROQ_API_KEY=

# TTS Configuration  
TTS_MODEL=kokoro
TOGETHER_API_KEY=

# Student Configuration
DEFAULT_STUDENT_NAME=Student
INITIAL_LEVEL=beginner

# Database
DATABASE_PATH=./data/students.db

# UI Configuration
SHARE_GRADIO=false
SERVER_PORT=7860
''',

    'english_tutor/.gitignore': '''__pycache__/
*.py[cod]
*.so
.Python
build/
dist/
*.egg-info/
venv/
env/
.env
.env.local
data/
*.db
*.sqlite
*.log
.DS_Store
Thumbs.db
''',

    'english_tutor/src/english_tutor/config.py': '''"""Configuration management for English Tutor."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    
    # STT
    stt_model: str = "whisper-groq"
    groq_api_key: str = ""
    
    # TTS
    tts_model: str = "kokoro"
    together_api_key: str = ""
    
    # Student
    default_student_name: str = "Student"
    initial_level: str = "beginner"
    
    # Database
    database_path: str = "./data/students.db"
    
    # UI
    share_gradio: bool = False
    server_port: int = 7860


settings = Settings()
''',
}

def create_file(path: str, content: str):
    """Create a file with content, creating parent dirs if needed."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')
    print(f"✓ Created: {path}")

def create_init_files():
    """Create __init__.py files."""
    init_dirs = [
        'english_tutor/src/english_tutor',
        'english_tutor/src/english_tutor/agent',
        'english_tutor/src/english_tutor/competencies',
        'english_tutor/src/english_tutor/exercises',
        'english_tutor/src/english_tutor/ui',
        'english_tutor/src/english_tutor/models',
        'english_tutor/src/english_tutor/database',
    ]
    
    for d in init_dirs:
        init_file = Path(d) / '__init__.py'
        init_file.parent.mkdir(parents=True, exist_ok=True)
        init_file.touch(exist_ok=True)
        print(f"✓ Created: {init_file}")

def create_data_dir():
    """Create data directory."""
    Path('english_tutor/data').mkdir(parents=True, exist_ok=True)
    Path('english_tutor/data/.gitkeep').touch(exist_ok=True)
    print("✓ Created: english_tutor/data/")

def main():
    print("\n🚀 Setting up English Tutor project...\n")
    
    # Create all files
    for path, content in FILES.items():
        create_file(path, content)
    
    print()
    create_init_files()
    print()
    create_data_dir()
    
    print("\n✅ Basic structure created!")
    print("\n📝 Next: Run the detailed setup to create all module files:")
    print("   python setup_english_tutor_full.py")

if __name__ == "__main__":
    main()
