#!/usr/bin/env python
"""
Fix WhiteNoise middleware in settings_production.py on server
"""

import os
import sys

print("=" * 60)
print("Fix WhiteNoise Middleware in settings_production.py")
print("=" * 60)

settings_file = "/home/bghranac/repositories/bgmajstor/config/settings_production.py"

# Read current file
print("\n1. Reading settings_production.py...")
print("-" * 60)
with open(settings_file, 'r') as f:
    content = f.read()
print(f"✓ Read {len(content)} bytes")

# Check if WhiteNoise is already in MIDDLEWARE
if "'whitenoise.middleware.WhiteNoiseMiddleware'" in content:
    print("\n✓ WhiteNoise middleware already present!")
else:
    print("\n⚠ WhiteNoise middleware NOT found in file")

# Create the correct MIDDLEWARE block
correct_middleware = """# WhiteNoise Middleware - трябва да се дефинира изрично
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Добавено!
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]"""

# Find and replace MIDDLEWARE configuration
print("\n2. Updating MIDDLEWARE configuration...")
print("-" * 60)

# Look for the old insert statement
if "MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')" in content:
    # Remove the old insert line
    content = content.replace(
        "\n# WhiteNoise Middleware - вмъкваме го след SecurityMiddleware\nMIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')",
        "\n" + correct_middleware
    )
    print("✓ Replaced MIDDLEWARE.insert() with explicit MIDDLEWARE list")
elif "MIDDLEWARE = [" not in content:
    # Add MIDDLEWARE after CSRF_TRUSTED_ORIGINS
    csrf_end = content.find("]", content.find("CSRF_TRUSTED_ORIGINS"))
    if csrf_end > 0:
        insert_pos = content.find("\n", csrf_end) + 1
        content = content[:insert_pos] + "\n" + correct_middleware + "\n" + content[insert_pos:]
        print("✓ Added MIDDLEWARE configuration")
else:
    # MIDDLEWARE already defined, check if it has WhiteNoise
    if "'whitenoise.middleware.WhiteNoiseMiddleware'" not in content:
        # Find MIDDLEWARE = [ and insert WhiteNoise after SecurityMiddleware
        mw_start = content.find("MIDDLEWARE = [")
        sec_line = content.find("'django.middleware.security.SecurityMiddleware'", mw_start)
        if sec_line > 0:
            # Find end of that line
            line_end = content.find("\n", sec_line)
            # Insert WhiteNoise on next line
            indent = "    "
            whitenoise_line = f"{indent}'whitenoise.middleware.WhiteNoiseMiddleware',  # Добавено!\n"
            content = content[:line_end+1] + whitenoise_line + content[line_end+1:]
            print("✓ Inserted WhiteNoise into existing MIDDLEWARE list")
    else:
        print("✓ MIDDLEWARE already has WhiteNoise")

# Create backup
print("\n3. Creating backup...")
print("-" * 60)
backup_file = settings_file + ".backup-whitenoise"
with open(backup_file, 'w') as f:
    f.write(content)
print(f"✓ Backup saved: {backup_file}")

# Write updated file
print("\n4. Writing updated settings_production.py...")
print("-" * 60)
with open(settings_file, 'w') as f:
    f.write(content)
print(f"✓ Written {len(content)} bytes")

# Verify
print("\n5. Verifying...")
print("-" * 60)
with open(settings_file, 'r') as f:
    new_content = f.read()

if "'whitenoise.middleware.WhiteNoiseMiddleware'" in new_content:
    print("✓ WhiteNoise middleware verified in file!")
else:
    print("✗ WhiteNoise middleware still NOT in file!")
    sys.exit(1)

print("\n" + "=" * 60)
print("SUCCESS! WhiteNoise middleware added")
print("=" * 60)
print("\nNext steps:")
print("1. Restart application in Setup Python App")
print("2. Run test_whitenoise.py to verify")
print("3. Test website: https://bgmajstor.eu")
print("=" * 60)
