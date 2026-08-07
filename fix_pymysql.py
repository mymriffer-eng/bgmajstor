#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auto-fix script: Add PyMySQL import to settings_production.py
"""

import os
import sys

print("=" * 60)
print("PyMySQL Auto-Fix Script")
print("=" * 60)

settings_file = '/home/bghranac/repositories/bgmajstor/config/settings_production.py'

print(f"\n1. Checking file: {settings_file}")

if not os.path.exists(settings_file):
    print(f"   ✗ File NOT FOUND!")
    sys.exit(1)

print(f"   ✓ File exists")

# Read current content
print(f"\n2. Reading current content...")
with open(settings_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if PyMySQL import already exists
if 'import pymysql' in content:
    print(f"   ✓ PyMySQL import ALREADY EXISTS!")
    print(f"\n   No changes needed.")
    sys.exit(0)

print(f"   ✗ PyMySQL import NOT FOUND")

# Find the position to insert PyMySQL import
# We want to insert it after "from .settings import *"
pymysql_code = """
# PyMySQL support за MySQL database
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
"""

# Find where to insert
insert_marker = "from .settings import *"

if insert_marker not in content:
    print(f"   ✗ Cannot find insertion point: '{insert_marker}'")
    sys.exit(1)

# Split and insert
parts = content.split(insert_marker, 1)
new_content = parts[0] + insert_marker + pymysql_code + parts[1]

# Backup original file
backup_file = settings_file + '.backup'
print(f"\n3. Creating backup: {backup_file}")
with open(backup_file, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"   ✓ Backup created")

# Write new content
print(f"\n4. Writing updated content...")
with open(settings_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"   ✓ File updated successfully!")

# Verify
print(f"\n5. Verifying changes...")
with open(settings_file, 'r', encoding='utf-8') as f:
    verify_content = f.read()

if 'import pymysql' in verify_content and 'pymysql.install_as_MySQLdb()' in verify_content:
    print(f"   ✓ PyMySQL import VERIFIED!")
else:
    print(f"   ✗ Verification FAILED!")
    print(f"   Restoring backup...")
    with open(backup_file, 'r', encoding='utf-8') as f:
        original = f.read()
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(original)
    sys.exit(1)

print("\n" + "=" * 60)
print("SUCCESS! PyMySQL import added to settings_production.py")
print("=" * 60)
print("\nNext steps:")
print("1. Restart the application in Setup Python App")
print("2. Test the website: https://bgmajstor.eu")
print("3. Run diagnostic.py again to verify")
print("=" * 60)
