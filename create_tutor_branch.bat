@echo off
REM Script to create git branch 'tutor_ingles' for English Tutor

echo.
echo ========================================================================
echo   Creating Git Branch: tutor_ingles
echo ========================================================================
echo.

echo Current git status:
git status -sb
echo.

echo Creating branch 'tutor_ingles'...
git checkout -b tutor_ingles
if errorlevel 1 (
    echo Branch might exist, switching to it...
    git checkout tutor_ingles
)
echo.

echo Adding English Tutor files...
git add setup_english_tutor_master.py
git add setup_english_tutor_full.py
git add setup_english_tutor_full_part2.py
git add verify_english_tutor_setup.py
git add START_HERE_ENGLISH_TUTOR.md
git add INDICE_ENGLISH_TUTOR.txt
git add RESUMEN_ENGLISH_TUTOR.txt
git add QUICKSTART_ENGLISH_TUTOR.txt
git add ENGLISH_TUTOR_README.md
git add ARCHITECTURE_ENGLISH_TUTOR.txt
git add ENGLISH_TUTOR_FILES.txt
echo.

echo Committing files...
git commit -m "feat: Add English Tutor AI project - Complete AI-powered English tutoring system with Ollama + LangGraph + Gradio"
echo.

echo ========================================================================
echo   Branch 'tutor_ingles' created successfully!
echo ========================================================================
echo.

echo Current status:
git status
echo.

echo Next steps:
echo   1. Push to remote: git push -u origin tutor_ingles
echo   2. Switch back: git checkout main
echo.

pause
