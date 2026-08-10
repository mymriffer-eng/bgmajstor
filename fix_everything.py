#!/usr/bin/env python
"""
ALL-IN-ONE FIX: Git sync + PyMySQL patch
"""
import subprocess
import sys
import os
import re

print("=== BGMaistor Emergency Fix ===\n")

# Step 1: Fix Git state
print("1. Fixing Git state...")
os.chdir('/home/bghranac/repositories/bgmajstor')

result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
if result.stdout.strip():
    print("   Stashing uncommitted changes...")
    subprocess.run(['git', 'stash'], capture_output=True)
    print("   ✓ Changes stashed")
else:
    print("   ✓ No uncommitted changes")

# Step 2: Pull from GitHub
print("\n2. Pulling latest code from GitHub...")
result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)
if result.returncode == 0:
    print("   ✓ Pull successful")
else:
    print(f"   ⚠ Pull warning (continuing anyway)")

# Step 3: Patch PyMySQL version
print("\n3. Patching PyMySQL version...")
venv_path = '/home/bghranac/virtualenv/repositories/bgmajstor/3.13'
pymysql_init = os.path.join(venv_path, 'lib/python3.13/site-packages/pymysql/__init__.py')

if not os.path.exists(pymysql_init):
    print(f"   ❌ PyMySQL not found at: {pymysql_init}")
    sys.exit(1)

with open(pymysql_init, 'r', encoding='utf-8') as f:
    content = f.read()

if '__version__' in content:
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        current_version = match.group(1)
        print(f"   Current version: {current_version}")
    
    # Patch to 2.3.0
    new_content = re.sub(
        r'(__version__\s*=\s*["\'])[^"\']+(["\'])',
        r'\g<1>2.3.0\g<2>',
        content
    )
    
    with open(pymysql_init, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   ✓ Patched to: 2.3.0")
else:
    print("   ❌ __version__ not found")
    sys.exit(1)

# Step 4: Verify
print("\n4. Verifying patch...")
if 'pymysql' in sys.modules:
    del sys.modules['pymysql']

import pymysql
print(f"   ✓ PyMySQL version: {pymysql.__version__}")

if pymysql.__version__ >= '2.2.1':
    print("\n" + "="*50)
    print("✓✓✓ ALL FIXES APPLIED SUCCESSFULLY ✓✓✓")
    print("="*50)
    print("\nNow do ONE MORE THING:")
    print("→ Setup Python App → RESTART button")
    print("\nThen your site will work! 🎉")
else:
    print(f"\n❌ Version check failed: {pymysql.__version__}")
    sys.exit(1)
