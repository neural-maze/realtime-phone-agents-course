#!/usr/bin/env python3
"""
Verification script - Check if English Tutor can be generated.
"""
import sys
from pathlib import Path

def check_file_exists(filepath: str) -> bool:
    """Check if a file exists."""
    return Path(filepath).exists()

def main():
    """Run verification checks."""
    print("\n" + "="*70)
    print("  🔍 ENGLISH TUTOR PROJECT - VERIFICATION")
    print("="*70 + "\n")
    
    checks = []
    
    # Check setup scripts
    print("📋 Checking setup scripts...")
    scripts = [
        "setup_english_tutor_master.py",
        "setup_english_tutor_full.py",
        "setup_english_tutor_full_part2.py"
    ]
    
    for script in scripts:
        exists = check_file_exists(script)
        status = "✅" if exists else "❌"
        print(f"  {status} {script}")
        checks.append(exists)
    
    # Check documentation
    print("\n📖 Checking documentation files...")
    docs = [
        "ENGLISH_TUTOR_README.md",
        "QUICKSTART_ENGLISH_TUTOR.txt",
        "ARCHITECTURE_ENGLISH_TUTOR.txt",
        "ENGLISH_TUTOR_FILES.txt",
        "RESUMEN_ENGLISH_TUTOR.txt"
    ]
    
    for doc in docs:
        exists = check_file_exists(doc)
        status = "✅" if exists else "❌"
        print(f"  {status} {doc}")
        checks.append(exists)
    
    # Check Python version
    print("\n🐍 Checking Python version...")
    py_version = sys.version_info
    py_ok = py_version >= (3, 11)
    status = "✅" if py_ok else "❌"
    print(f"  {status} Python {py_version.major}.{py_version.minor}.{py_version.micro}")
    if not py_ok:
        print("     ⚠️  Python 3.11+ required")
    checks.append(py_ok)
    
    # Summary
    print("\n" + "="*70)
    if all(checks):
        print("  ✅ ALL CHECKS PASSED!")
        print("="*70)
        print("\n🚀 Ready to generate English Tutor project!\n")
        print("Next step:")
        print("  python setup_english_tutor_master.py\n")
        return 0
    else:
        print("  ❌ SOME CHECKS FAILED")
        print("="*70)
        print("\n⚠️  Please ensure all setup files are present.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
