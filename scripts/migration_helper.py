#!/usr/bin/env python3
"""
Migration helper script for PNCP API Client.
This script helps verify the migration from the old structure to the new clean architecture.
"""

import os
import sys
from pathlib import Path

def check_old_structure():
    """Check if old structure files exist."""
    old_files = [
        'app.py',
        'templates/',
        'static/',
        'test_*.py'
    ]
    
    print("Checking for old structure files...")
    found_old = False
    
    for pattern in old_files:
        if '*' in pattern:
            # Handle glob patterns
            import glob
            matches = glob.glob(pattern)
            if matches:
                print(f"  Found old files matching {pattern}: {len(matches)} files")
                found_old = True
        else:
            if os.path.exists(pattern):
                print(f"  Found old file/directory: {pattern}")
                found_old = True
    
    return found_old

def check_new_structure():
    """Check if new structure is properly set up."""
    required_paths = [
        'app/',
        'app/__init__.py',
        'app/config/',
        'app/api/',
        'app/core/',
        'app/extensions/',
        'app/templates/',
        'app/static/',
        'tests/',
        'docs/',
        'scripts/',
        'wsgi.py',
        'setup.py'
    ]
    
    print("Checking new structure...")
    missing_paths = []
    
    for path in required_paths:
        if not os.path.exists(path):
            print(f"  Missing required path: {path}")
            missing_paths.append(path)
        else:
            print(f"  ✓ Found: {path}")
    
    return len(missing_paths) == 0, missing_paths

def main():
    """Main migration helper function."""
    print("PNCP API Client Migration Helper")
    print("=" * 40)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check for old structure
    old_found = check_old_structure()
    if old_found:
        print("\n⚠️  Old structure files detected")
    else:
        print("\n✓ No old structure files found")
    
    # Check new structure
    new_ok, missing_paths = check_new_structure()
    if new_ok:
        print("\n✓ New structure is properly set up")
    else:
        print(f"\n❌ New structure is incomplete. Missing {len(missing_paths)} paths:")
        for path in missing_paths:
            print(f"  - {path}")
    
    # Provide recommendations
    print("\nRecommendations:")
    if old_found and new_ok:
        print("  - You can now remove old structure files from the root directory")
        print("  - The application is ready to run with the new structure")
    elif not old_found and new_ok:
        print("  - The migration appears to be complete")
        print("  - You can run the application with: python wsgi.py")
    else:
        print("  - The migration is not complete")
        print("  - Please check the missing paths and ensure all files are in place")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())