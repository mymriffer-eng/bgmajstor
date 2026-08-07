#!/usr/bin/env python
"""
Create symlink or copy .htaccess to public_html
"""

import os
import shutil

app_root = "/home/bghranac/repositories/bgmajstor"
htaccess_root = os.path.join(app_root, ".htaccess")
htaccess_public = os.path.join(app_root, "public_html", ".htaccess")

print("=" * 60)
print("Fix .htaccess Location")
print("=" * 60)

# Read root .htaccess
print("\n1. Reading .htaccess from root...")
with open(htaccess_root, 'r') as f:
    content = f.read()
print(f"✓ Read {len(content)} bytes")

# Modify paths for public_html context
print("\n2. Modifying paths for public_html context...")
# In public_html, static files are in ./static/ not public_html/static/
new_content = content.replace('public_html/$1/$2', '$1/$2')
print("✓ Paths updated")

# Write to public_html
print(f"\n3. Writing to {htaccess_public}...")
with open(htaccess_public, 'w') as f:
    f.write(new_content)
print("✓ .htaccess created in public_html/")

# Show content
print("\n4. New .htaccess content:")
print("-" * 60)
print(new_content)

print("\n" + "=" * 60)
print("SUCCESS!")
print("=" * 60)
print("\nNext steps:")
print("1. Check if file exists: ls -la /home/bghranac/repositories/bgmajstor/public_html/.htaccess")
print("2. Restart app in Setup Python App")
print("3. Test: https://bgmajstor.eu/static/test.html")
print("4. Test: https://bgmajstor.eu/static/css/style.css")
