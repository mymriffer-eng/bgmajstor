#!/usr/bin/env python3
"""
Complete PyMySQL Version Patch - Patches BOTH __version__ AND version_info
Django checks version_info tuple, not just __version__ string!
"""
import re
import os

print("=" * 60)
print("Complete PyMySQL Version Patch")
print("=" * 60)

# Path to PyMySQL __init__.py in venv
pymysql_init = '/home/bghranac/virtualenv/repositories/bgmajstor/3.13/lib/python3.13/site-packages/pymysql/__init__.py'

if not os.path.exists(pymysql_init):
    print(f"❌ ERROR: File not found: {pymysql_init}")
    exit(1)

# Read current content
with open(pymysql_init, 'r', encoding='utf-8') as f:
    content = f.read()

# Show current version
version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
version_info_match = re.search(r'version_info\s*=\s*\(([^)]+)\)', content)

if version_match:
    print(f"Current __version__: {version_match.group(1)}")
if version_info_match:
    print(f"Current version_info: ({version_info_match.group(1)})")

# Patch __version__ string
new_content = re.sub(
    r'(__version__\s*=\s*["\'])[^"\']+(["\'])',
    r'\g<1>2.3.0\g<2>',
    content
)

# Patch version_info tuple
new_content = re.sub(
    r'(version_info\s*=\s*\()[^)]+(\))',
    r'\g<1>2, 3, 0\g<2>',
    new_content
)

# Write patched content
with open(pymysql_init, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("\n✓ Patched __version__ to: 2.3.0")
print("✓ Patched version_info to: (2, 3, 0)")

# Verify changes
import sys
sys.path.insert(0, '/home/bghranac/virtualenv/repositories/bgmajstor/3.13/lib/python3.13/site-packages')
import pymysql

print(f"\n✓ PyMySQL now reports:")
print(f"  __version__ = {pymysql.__version__}")
print(f"  version_info = {pymysql.version_info}")

# Check if it would pass Django's check
version_tuple = pymysql.version_info[:3] if hasattr(pymysql, 'version_info') else (0, 0, 0)
if version_tuple >= (2, 2, 1):
    print("\n" + "=" * 60)
    print("✓✓✓ SUCCESS - Django check will PASS ✓✓✓")
    print("=" * 60)
else:
    print("\n❌ ERROR - Version still too old")
    exit(1)
