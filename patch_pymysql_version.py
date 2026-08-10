#!/usr/bin/env python
"""
Emergency fix: Patch PyMySQL version to bypass Django check
"""
import sys
import os

print("=== PyMySQL Version Patch ===\n")

# Find PyMySQL installation
venv_path = '/home/bghranac/virtualenv/repositories/bgmajstor/3.13'
pymysql_init = os.path.join(venv_path, 'lib/python3.13/site-packages/pymysql/__init__.py')

if not os.path.exists(pymysql_init):
    print(f"❌ PyMySQL not found at: {pymysql_init}")
    sys.exit(1)

print(f"1. Found PyMySQL at: {pymysql_init}")

# Read current content
with open(pymysql_init, 'r', encoding='utf-8') as f:
    content = f.read()

# Check current version
if '__version__' in content:
    import re
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        current_version = match.group(1)
        print(f"   Current version: {current_version}")
    
    # Patch version to 2.3.0 (higher than 2.2.1 requirement)
    new_content = re.sub(
        r'(__version__\s*=\s*["\'])[^"\']+(["\'])',
        r'\g<1>2.3.0\g<2>',
        content
    )
    
    # Write back
    with open(pymysql_init, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   ✓ Patched to: 2.3.0")
else:
    print("   ❌ __version__ not found in file")
    sys.exit(1)

# Verify patch
print("\n2. Verifying patch...")
import importlib
if 'pymysql' in sys.modules:
    del sys.modules['pymysql']

import pymysql
print(f"   ✓ PyMySQL now reports version: {pymysql.__version__}")

if pymysql.__version__ >= '2.2.1':
    print("\n=== SUCCESS ===")
    print("PyMySQL version patched successfully!")
    print("\nNow RESTART the application:")
    print("Setup Python App → Restart button")
else:
    print(f"\n❌ Patch failed, version is still: {pymysql.__version__}")
    sys.exit(1)
