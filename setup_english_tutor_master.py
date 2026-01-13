#!/usr/bin/env python3
"""
MASTER SETUP: Complete English Tutor Project Generator
Executes both setup parts in sequence.
"""
import subprocess
import sys
from pathlib import Path

def run_setup_part(script_name: str, description: str):
    """Run a setup script."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {description} - DONE\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} - FAILED")
        print(f"Error: {e}")
        return False
    except FileNotFoundError:
        print(f"\n⚠️  {script_name} not found. Running inline...")
        return None

def main():
    """Execute complete setup."""
    print("\n" + "="*60)
    print("  🚀 ENGLISH TUTOR - MASTER SETUP")
    print("="*60)
    print("\nThis will generate the complete English Tutor project:")
    print("  ✓ Project structure")
    print("  ✓ Configuration files")
    print("  ✓ Competency tracking system")
    print("  ✓ Exercise generator")
    print("  ✓ Database layer")
    print("  ✓ LangGraph agent")
    print("  ✓ STT/TTS integration")
    print("  ✓ Gradio UI")
    print("  ✓ Main application")
    
    input("\nPress ENTER to continue...")
    
    # Part 1: Core modules
    result1 = run_setup_part(
        "setup_english_tutor_full.py",
        "Part 1: Core Modules (Config, Competencies, Exercises, Database)"
    )
    
    if result1 is False:
        print("\n❌ Setup failed at Part 1")
        return 1
    
    # Part 2: Agent and UI
    result2 = run_setup_part(
        "setup_english_tutor_full_part2.py",
        "Part 2: Agent & UI (LangGraph, Models, Gradio)"
    )
    
    if result2 is False:
        print("\n❌ Setup failed at Part 2")
        return 1
    
    # Final instructions
    print("\n" + "="*60)
    print("  ✅ SETUP COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:\n")
    print("1. Navigate to project:")
    print("   cd english_tutor\n")
    print("2. Configure environment:")
    print("   cp .env.example .env")
    print("   # Edit .env with your settings\n")
    print("3. Install dependencies:")
    print("   pip install -e .")
    print("   # or: uv pip install -e .\n")
    print("4. Run the tutor:")
    print("   python scripts/run_tutor.py\n")
    print("="*60)
    print("\n💡 Tips:")
    print("  - Make sure Ollama is running (ollama serve)")
    print("  - Configure GROQ_API_KEY in .env for STT")
    print("  - The tutor uses models from the parent project")
    print("  - Progress is saved in data/students.db")
    print("\n🎓 Happy Learning!\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
