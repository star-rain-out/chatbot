#!/usr/bin/env python3
"""
Syntax checker for the Python files
"""
import ast
import sys
import os

def check_syntax(file_path):
    """Check Python syntax of a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse the AST to check syntax
        ast.parse(content)
        print(f"✅ {file_path}: Syntax OK")
        return True
    except SyntaxError as e:
        print(f"❌ {file_path}: Syntax Error at line {e.lineno}: {e.msg}")
        print(f"   Problematic code: {e.text.strip() if e.text else 'N/A'}")
        return False
    except Exception as e:
        print(f"⚠️  {file_path}: Error - {e}")
        return False

def main():
    """Main function"""
    print("🔍 Checking Python syntax...")

    files_to_check = [
        "main.py",
        "routers/tools_travel.py",
        "routers/tools_landmark.py"
    ]

    all_good = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            if not check_syntax(file_path):
                all_good = False
        else:
            print(f"⚠️  {file_path}: File not found")
            all_good = False

    if all_good:
        print("\n🎉 All files have correct syntax!")
        return 0
    else:
        print("\n💥 Some files have syntax errors!")
        return 1

if __name__ == "__main__":
    sys.exit(main())