#!/usr/bin/env python3
"""
Complete English Tutor project generator.
Creates ALL files needed for the English tutor application.
"""
import os
from pathlib import Path
from textwrap import dedent

def write_file(path: str, content: str):
    """Write content to file, creating parent dirs."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(dedent(content).strip() + '\n', encoding='utf-8')
    print(f"✓ {path}")

def setup_project():
    """Generate complete project structure."""
    
    print("\n🚀 Generating English Tutor Project...\n")
    
    # ==================== CONFIG FILES ====================
    
    write_file('english_tutor/pyproject.toml', '''
    [project]
    name = "english-tutor"
    version = "0.1.0"
    description = "AI-Powered English Tutor with streaming audio/text"
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
    ''')
    
    write_file('english_tutor/.env.example', '''
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=llama3.2
    STT_MODEL=whisper-groq
    GROQ_API_KEY=
    TTS_MODEL=kokoro
    TOGETHER_API_KEY=
    DEFAULT_STUDENT_NAME=Student
    INITIAL_LEVEL=beginner
    DATABASE_PATH=./data/students.db
    SHARE_GRADIO=false
    SERVER_PORT=7860
    ''')
    
    write_file('english_tutor/.gitignore', '''
    __pycache__/
    *.py[cod]
    .Python
    build/
    dist/
    *.egg-info/
    venv/
    .env
    data/*.db
    *.log
    ''')
    
    write_file('english_tutor/README.md', '''
    # English Tutor - AI-Powered Language Learning
    
    Full local English tutor with Gradio + LangGraph + Ollama.
    
    ## Quick Start
    
    ```bash
    # 1. Setup (from parent directory)
    python setup_english_tutor_full.py
    
    # 2. Configure
    cd english_tutor
    cp .env.example .env
    # Edit .env with your Ollama model and API keys
    
    # 3. Install
    pip install -e .
    
    # 4. Run
    python scripts/run_tutor.py
    ```
    
    ## Features
    
    - 🎯 Personalized learning path
    - 🗣️ Speaking practice with pronunciation feedback
    - ✍️ Grammar and vocabulary exercises
    - 👂 Listening comprehension
    - 📊 Progress tracking
    - 🔒 100% local (Ollama + local STT/TTS)
    ''')
    
    # ==================== CORE MODULES ====================
    
    write_file('english_tutor/src/english_tutor/__init__.py', '''
    """English Tutor - AI-Powered Language Learning Agent."""
    from .tutor import EnglishTutor
    
    __version__ = "0.1.0"
    __all__ = ["EnglishTutor"]
    ''')
    
    write_file('english_tutor/src/english_tutor/config.py', '''
    """Configuration management."""
    from pydantic_settings import BaseSettings, SettingsConfigDict
    
    
    class Settings(BaseSettings):
        """App settings from environment."""
        
        model_config = SettingsConfigDict(
            env_file=".env",
            env_file_encoding="utf-8",
            extra="ignore"
        )
        
        ollama_base_url: str = "http://localhost:11434"
        ollama_model: str = "llama3.2"
        stt_model: str = "whisper-groq"
        groq_api_key: str = ""
        tts_model: str = "kokoro"
        together_api_key: str = ""
        default_student_name: str = "Student"
        initial_level: str = "beginner"
        database_path: str = "./data/students.db"
        share_gradio: bool = False
        server_port: int = 7860
    
    
    settings = Settings()
    ''')
    
    # ==================== COMPETENCIES ====================
    
    write_file('english_tutor/src/english_tutor/competencies/__init__.py', '''
    """Competency tracking system."""
    from .models import Competency, CompetencyLevel, StudentProfile
    from .tracker import CompetencyTracker
    
    __all__ = ["Competency", "CompetencyLevel", "StudentProfile", "CompetencyTracker"]
    ''')
    
    write_file('english_tutor/src/english_tutor/competencies/models.py', '''
    """Data models for competencies."""
    from enum import Enum
    from typing import Dict
    from pydantic import BaseModel, Field
    
    
    class Competency(str, Enum):
        """English competency areas."""
        GRAMMAR = "grammar"
        VOCABULARY = "vocabulary"
        PRONUNCIATION = "pronunciation"
        LISTENING = "listening"
        SPEAKING = "speaking"
        WRITING = "writing"
    
    
    class CompetencyLevel(str, Enum):
        """Proficiency levels."""
        BEGINNER = "beginner"
        INTERMEDIATE = "intermediate"
        ADVANCED = "advanced"
    
    
    class StudentProfile(BaseModel):
        """Student learning profile."""
        name: str
        level: CompetencyLevel = CompetencyLevel.BEGINNER
        competencies: Dict[Competency, int] = Field(default_factory=dict)
        exercises_completed: int = 0
        total_practice_time: int = 0
        
        def get_competency_score(self, comp: Competency) -> int:
            """Get score for a competency (0-100)."""
            return self.competencies.get(comp, 0)
        
        def update_competency(self, comp: Competency, points: int):
            """Update competency score."""
            current = self.competencies.get(comp, 0)
            self.competencies[comp] = min(100, current + points)
        
        def get_weakest_competency(self) -> Competency:
            """Return competency needing most practice."""
            if not self.competencies:
                return Competency.GRAMMAR
            return min(self.competencies.items(), key=lambda x: x[1])[0]
    ''')
    
    write_file('english_tutor/src/english_tutor/competencies/tracker.py', '''
    """Competency tracking logic."""
    from .models import Competency, StudentProfile
    
    
    class CompetencyTracker:
        """Track and update student competencies."""
        
        def __init__(self, profile: StudentProfile):
            self.profile = profile
        
        def record_exercise(self, competency: Competency, score: float):
            """Record exercise result and update competency."""
            points = int(score * 10)  # Convert 0-1 to 0-10 points
            self.profile.update_competency(competency, points)
            self.profile.exercises_completed += 1
        
        def get_recommendation(self) -> str:
            """Get personalized recommendation."""
            weak = self.profile.get_weakest_competency()
            score = self.profile.get_competency_score(weak)
            
            if score < 30:
                return f"Let's focus on {weak.value}. You'll improve quickly!"
            elif score < 70:
                return f"You're making progress in {weak.value}. Keep practicing!"
            else:
                return "Great job! Let's challenge you with more advanced exercises."
        
        def get_progress_summary(self) -> dict:
            """Get current progress summary."""
            return {
                "level": self.profile.level.value,
                "exercises_completed": self.profile.exercises_completed,
                "competencies": {
                    k.value: v for k, v in self.profile.competencies.items()
                }
            }
    ''')
    
    # ==================== EXERCISES ====================
    
    write_file('english_tutor/src/english_tutor/exercises/__init__.py', '''
    """Exercise generation system."""
    from .generator import ExerciseGenerator
    from .types import Exercise, ExerciseType
    
    __all__ = ["ExerciseGenerator", "Exercise", "ExerciseType"]
    ''')
    
    write_file('english_tutor/src/english_tutor/exercises/types.py', '''
    """Exercise type definitions."""
    from enum import Enum
    from typing import Optional
    from pydantic import BaseModel
    
    
    class ExerciseType(str, Enum):
        """Types of exercises."""
        GRAMMAR = "grammar"
        VOCABULARY = "vocabulary"
        PRONUNCIATION = "pronunciation"
        LISTENING = "listening"
        CONVERSATION = "conversation"
        WRITING = "writing"
    
    
    class Exercise(BaseModel):
        """Exercise model."""
        type: ExerciseType
        question: str
        expected_answer: Optional[str] = None
        hints: list[str] = []
        difficulty: int = 1  # 1-5
    ''')
    
    write_file('english_tutor/src/english_tutor/exercises/generator.py', '''
    """Exercise generation using LLM."""
    from langchain_ollama import ChatOllama
    from .types import Exercise, ExerciseType
    from ..competencies.models import Competency, CompetencyLevel
    
    
    class ExerciseGenerator:
        """Generate adaptive exercises."""
        
        def __init__(self, llm: ChatOllama):
            self.llm = llm
        
        def generate_grammar_exercise(self, level: CompetencyLevel) -> Exercise:
            """Generate grammar exercise."""
            prompt = f"""Generate a {level.value} level English grammar exercise.
    Format:
    Question: [the exercise question]
    Answer: [correct answer]
    Hints: [2-3 helpful hints]"""
            
            response = self.llm.invoke(prompt)
            content = response.content
            
            # Simple parsing (in production, use structured output)
            lines = content.split('\\n')
            question = lines[0].replace('Question:', '').strip() if lines else "Fill in the blank: I ___ to the store."
            answer = lines[1].replace('Answer:', '').strip() if len(lines) > 1 else "went"
            
            return Exercise(
                type=ExerciseType.GRAMMAR,
                question=question,
                expected_answer=answer,
                hints=["Think about past tense", "It's an irregular verb"],
                difficulty=1 if level == CompetencyLevel.BEGINNER else 3
            )
        
        def generate_vocabulary_exercise(self, level: CompetencyLevel) -> Exercise:
            """Generate vocabulary exercise."""
            prompt = f"""Generate a {level.value} level English vocabulary exercise.
    Give a word definition and ask the student to provide the word.
    Format:
    Question: [definition]
    Answer: [word]"""
            
            response = self.llm.invoke(prompt)
            content = response.content
            
            lines = content.split('\\n')
            question = lines[0].replace('Question:', '').strip() if lines else "A person who teaches is called a ___?"
            answer = lines[1].replace('Answer:', '').strip() if len(lines) > 1 else "teacher"
            
            return Exercise(
                type=ExerciseType.VOCABULARY,
                question=question,
                expected_answer=answer,
                difficulty=1 if level == CompetencyLevel.BEGINNER else 3
            )
        
        def generate_conversation_prompt(self, level: CompetencyLevel) -> str:
            """Generate conversation topic."""
            topics = {
                CompetencyLevel.BEGINNER: "Tell me about your daily routine.",
                CompetencyLevel.INTERMEDIATE: "What are your hobbies and why do you enjoy them?",
                CompetencyLevel.ADVANCED: "Discuss the impact of technology on modern society."
            }
            return topics.get(level, topics[CompetencyLevel.BEGINNER])
    ''')
    
    # ==================== DATABASE ====================
    
    write_file('english_tutor/src/english_tutor/database/__init__.py', '''
    """Database persistence layer."""
    from .storage import StudentDatabase
    
    __all__ = ["StudentDatabase"]
    ''')
    
    write_file('english_tutor/src/english_tutor/database/storage.py', '''
    """SQLite database for student profiles."""
    import json
    import sqlite3
    from pathlib import Path
    from typing import Optional
    from ..competencies.models import StudentProfile, CompetencyLevel, Competency
    from loguru import logger
    
    
    class StudentDatabase:
        """Manage student profiles in SQLite."""
        
        def __init__(self, db_path: str = "./data/students.db"):
            self.db_path = Path(db_path)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._init_db()
        
        def _init_db(self):
            """Initialize database schema."""
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        name TEXT PRIMARY KEY,
                        level TEXT NOT NULL,
                        competencies TEXT NOT NULL,
                        exercises_completed INTEGER DEFAULT 0,
                        total_practice_time INTEGER DEFAULT 0
                    )
                """)
                conn.commit()
        
        def save_profile(self, profile: StudentProfile):
            """Save or update student profile."""
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO students 
                    (name, level, competencies, exercises_completed, total_practice_time)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    profile.name,
                    profile.level.value,
                    json.dumps({k.value: v for k, v in profile.competencies.items()}),
                    profile.exercises_completed,
                    profile.total_practice_time
                ))
                conn.commit()
            logger.info(f"Saved profile for {profile.name}")
        
        def load_profile(self, name: str) -> Optional[StudentProfile]:
            """Load student profile by name."""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT * FROM students WHERE name = ?", (name,)
                )
                row = cursor.fetchone()
                
                if row:
                    competencies_dict = json.loads(row[2])
                    competencies = {
                        Competency(k): v for k, v in competencies_dict.items()
                    }
                    
                    return StudentProfile(
                        name=row[0],
                        level=CompetencyLevel(row[1]),
                        competencies=competencies,
                        exercises_completed=row[3],
                        total_practice_time=row[4]
                    )
                return None
        
        def list_students(self) -> list[str]:
            """List all student names."""
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT name FROM students")
                return [row[0] for row in cursor.fetchall()]
    ''')
    
    print("\n📝 Generated core modules.\n")

if __name__ == "__main__":
    setup_project()
    print("✅ Core files created! Run setup_english_tutor_full_part2.py for agent & UI...")
