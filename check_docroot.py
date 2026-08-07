#!/usr/bin/env python
"""
Check cPanel Python App Configuration
"""

import os
import sys

print("=" * 60)
print("Document Root & App Configuration Check")
print("=" * 60)

# Check environment
print("\n1. Python Environment:")
print("-" * 60)
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")

# Check current working directory
print("\n2. Working Directory:")
print("-" * 60)
print(f"CWD: {os.getcwd()}")
print(f"__file__: {__file__}")
print(f"Script dir: {os.path.dirname(os.path.abspath(__file__))}")

# Check if we're running under Passenger
print("\n3. Passenger Environment Variables:")
print("-" * 60)
passenger_vars = {k: v for k, v in os.environ.items() if 'PASSENGER' in k.upper()}
if passenger_vars:
    for key, value in passenger_vars.items():
        print(f"{key}: {value}")
else:
    print("(No Passenger variables found - not running under Passenger)")

# Check Apache document root
print("\n4. Apache/Document Root:")
print("-" * 60)
document_root = os.environ.get('DOCUMENT_ROOT', 'Not set')
print(f"DOCUMENT_ROOT: {document_root}")

# Check script paths
print("\n5. Script Path Variables:")
print("-" * 60)
script_name = os.environ.get('SCRIPT_NAME', 'Not set')
script_filename = os.environ.get('SCRIPT_FILENAME', 'Not set')
print(f"SCRIPT_NAME: {script_name}")
print(f"SCRIPT_FILENAME: {script_filename}")

# Check what the app root should be
print("\n6. Expected Paths:")
print("-" * 60)
app_root = "/home/bghranac/repositories/bgmajstor"
public_html = os.path.join(app_root, "public_html")
print(f"App Root: {app_root}")
print(f"Public HTML: {public_html}")

# Check .htaccess locations
print("\n7. .htaccess Files:")
print("-" * 60)
htaccess_locations = [
    os.path.join(app_root, ".htaccess"),
    os.path.join(public_html, ".htaccess"),
]
for location in htaccess_locations:
    if os.path.exists(location):
        print(f"✓ Found: {location}")
        size = os.path.getsize(location)
        print(f"  Size: {size} bytes")
    else:
        print(f"✗ Not found: {location}")

# Read current .htaccess
print("\n8. Current .htaccess Content:")
print("-" * 60)
htaccess_root = os.path.join(app_root, ".htaccess")
if os.path.exists(htaccess_root):
    with open(htaccess_root, 'r') as f:
        print(f.read())

print("\n" + "=" * 60)
print("Configuration check complete!")
print("=" * 60)

print("\n" + "=" * 60)
print("RECOMMENDATION:")
print("=" * 60)
print("If document root is /home/bghranac/repositories/bgmajstor,")
print("then URL https://bgmajstor.eu/static/css/style.css")
print("should be rewritten to public_html/static/css/style.css")
print("\nCheck in cPanel: Setup Python App -> Application URL")
