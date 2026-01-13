#!/usr/bin/env python3
"""
Create git branch 'tutor_ingles' with English Tutor files.
"""
import subprocess
import sys

def run_git_command(cmd: list[str], description: str):
    """Run a git command and print result."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✅ {description} - OK")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Create branch and add English Tutor files."""
    print("\n" + "="*70)
    print("  🌿 Creating Git Branch: tutor_ingles")
    print("="*70)
    
    # Check current branch
    print("\n📋 Current git status:")
    subprocess.run(["git", "status", "-sb"])
    
    # Create new branch
    if not run_git_command(
        ["git", "checkout", "-b", "tutor_ingles"],
        "Creating branch 'tutor_ingles'"
    ):
        print("\n⚠️  Branch might already exist. Switching to it...")
        run_git_command(
            ["git", "checkout", "tutor_ingles"],
            "Switching to branch 'tutor_ingles'"
        )
    
    # Add English Tutor files
    files_to_add = [
        # Setup scripts
        "setup_english_tutor_master.py",
        "setup_english_tutor_full.py",
        "setup_english_tutor_full_part2.py",
        "verify_english_tutor_setup.py",
        
        # Documentation
        "START_HERE_ENGLISH_TUTOR.md",
        "INDICE_ENGLISH_TUTOR.txt",
        "RESUMEN_ENGLISH_TUTOR.txt",
        "QUICKSTART_ENGLISH_TUTOR.txt",
        "ENGLISH_TUTOR_README.md",
        "ARCHITECTURE_ENGLISH_TUTOR.txt",
        "ENGLISH_TUTOR_FILES.txt",
    ]
    
    print("\n📦 Adding English Tutor files to git...")
    for file in files_to_add:
        print(f"  • {file}")
    
    run_git_command(
        ["git", "add"] + files_to_add,
        "Adding files to staging"
    )
    
    # Commit
    commit_message = """feat: Add English Tutor AI project

- Complete AI-powered English tutoring system
- 100% local with Ollama + LangGraph + Gradio
- Tracks 6 competencies: Grammar, Vocabulary, Pronunciation, Listening, Speaking, Writing
- Voice and text interaction with STT/TTS
- Adaptive exercises with LLM
- SQLite progress tracking
- Reuses parent project's TTS/STT infrastructure

Setup scripts:
- setup_english_tutor_master.py (main setup)
- setup_english_tutor_full.py (core modules)
- setup_english_tutor_full_part2.py (agent & UI)

Documentation:
- START_HERE_ENGLISH_TUTOR.md (quick start)
- ENGLISH_TUTOR_README.md (complete guide)
- ARCHITECTURE_ENGLISH_TUTOR.txt (technical diagrams)
- QUICKSTART_ENGLISH_TUTOR.txt (quick reference)
"""
    
    run_git_command(
        ["git", "commit", "-m", commit_message],
        "Committing English Tutor files"
    )
    
    # Show status
    print("\n" + "="*70)
    print("  ✅ Branch 'tutor_ingles' created successfully!")
    print("="*70)
    print("\n📊 Current status:")
    subprocess.run(["git", "status"])
    
    print("\n📋 Next steps:")
    print("  1. Review changes: git log -1")
    print("  2. Push to remote: git push -u origin tutor_ingles")
    print("  3. Switch back to main: git checkout main")
    print("\n🎓 English Tutor files are now in branch 'tutor_ingles'!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
