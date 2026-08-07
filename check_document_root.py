#!/usr/bin/env python
"""
Find actual document root by checking cPanel app configuration
"""

import os
import json

print("=" * 60)
print("cPanel Python App Configuration Files")
print("=" * 60)

app_root = "/home/bghranac/repositories/bgmajstor"

# Check for Passengerfile.json
print("\n1. Passengerfile.json:")
print("-" * 60)
passenger_file = os.path.join(app_root, "Passengerfile.json")
if os.path.exists(passenger_file):
    with open(passenger_file, 'r') as f:
        content = f.read()
        print(content)
        config = json.loads(content)
        if 'document_root' in config:
            print(f"\n✓ document_root found: {config['document_root']}")
else:
    print("✗ Passengerfile.json not found")

# Check parent directory for app config
print("\n2. Check parent directory for app files:")
print("-" * 60)
parent = "/home/bghranac/repositories"
if os.path.exists(parent):
    files = os.listdir(parent)
    print(f"Files in {parent}:")
    for f in files:
        print(f"  - {f}")

# Check home directory structure
print("\n3. Home directory structure:")
print("-" * 60)
home = "/home/bghranac"
for item in ['public_html', 'www', 'htdocs', 'repositories']:
    path = os.path.join(home, item)
    if os.path.exists(path):
        print(f"✓ {item}/ exists")
        # List first level
        try:
            subitems = os.listdir(path)[:5]
            for sub in subitems:
                print(f"    - {sub}")
        except:
            pass
    else:
        print(f"✗ {item}/ does not exist")

# Check if there's a separate public_html at user level
print("\n4. Checking user-level public_html:")
print("-" * 60)
user_public = "/home/bghranac/public_html"
if os.path.exists(user_public):
    print(f"✓ Found: {user_public}")
    print("This might be the actual document root!")
    
    # Check what's inside
    items = os.listdir(user_public)
    print(f"\nContents ({len(items)} items):")
    for item in items[:10]:
        item_path = os.path.join(user_public, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
        else:
            print(f"  📄 {item}")
    if len(items) > 10:
        print(f"  ... and {len(items) - 10} more")
else:
    print("✗ Not found")

print("\n" + "=" * 60)
print("SOLUTION RECOMMENDATION:")
print("=" * 60)
print("Option 1: Use WhiteNoise to serve static files from Django")
print("  - No Apache configuration needed")
print("  - Works reliably on shared hosting")
print("  - Add to requirements.txt and settings")
print("\nOption 2: Configure document_root in Passengerfile.json")
print("  - Set document_root to public_html/")
print("  - Requires app restart")
