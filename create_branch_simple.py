#!/usr/bin/env python3
"""Execute git commands to create tutor_ingles branch."""
import subprocess
import os

os.system('git checkout -b tutor_ingles')
os.system('git add setup_english_tutor_master.py setup_english_tutor_full.py setup_english_tutor_full_part2.py verify_english_tutor_setup.py')
os.system('git add START_HERE_ENGLISH_TUTOR.md INDICE_ENGLISH_TUTOR.txt RESUMEN_ENGLISH_TUTOR.txt QUICKSTART_ENGLISH_TUTOR.txt ENGLISH_TUTOR_README.md ARCHITECTURE_ENGLISH_TUTOR.txt ENGLISH_TUTOR_FILES.txt')
os.system('git commit -m "feat: Add English Tutor AI project - Complete AI-powered English tutoring system"')
os.system('git status')
print("\n✅ Branch 'tutor_ingles' created!")
print("\nNext: git push -u origin tutor_ingles")
