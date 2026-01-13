#!/usr/bin/env python3
"""
Setup script for English Tutor project.
Creates directory structure and basic files.
"""
import os
from pathlib import Path

def create_directories():
    """Create directory structure"""
    dirs = [
        'english_tutor/src/english_tutor/agent',
        'english_tutor/src/english_tutor/competencies',
        'english_tutor/src/english_tutor/exercises',
        'english_tutor/src/english_tutor/ui',
        'english_tutor/src/english_tutor/models',
        'english_tutor/src/english_tutor/database',
        'english_tutor/scripts',
        'english_tutor/data',
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"✓ Created: {d}")
    
    return dirs

def create_init_files():
    """Create __init__.py files"""
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
        init_file.touch(exist_ok=True)
        print(f"✓ Created: {init_file}")

def main():
    print("\n🚀 Setting up English Tutor project...\n")
    create_directories()
    print()
    create_init_files()
    print("\n✅ Directory structure created successfully!")
    print("\nNext steps:")
    print("1. cd english_tutor")
    print("2. Copy .env.example to .env and configure")
    print("3. pip install -e . (or uv pip install -e .)")
    print("4. python scripts/run_tutor.py\n")

if __name__ == "__main__":
    main()
