#!/usr/bin/env python
"""
Download patch script from GitHub and execute it
"""
import urllib.request
import os
import sys
import subprocess

print("=== Download and Patch PyMySQL ===\n")

# GitHub raw URL
github_url = "https://raw.githubusercontent.com/mymriffer-eng/bgmajstor/main/patch_pymysql_version.py"
local_path = "/home/bghranac/repositories/bgmajstor/patch_pymysql_version.py"

print(f"1. Downloading patch script from GitHub...")
try:
    urllib.request.urlretrieve(github_url, local_path)
    print(f"   ✓ Downloaded to: {local_path}")
except Exception as e:
    print(f"   ❌ Download failed: {e}")
    sys.exit(1)

print("\n2. Executing patch script...")
result = subprocess.run([sys.executable, local_path], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)

if result.returncode == 0:
    print("\n=== SUCCESS ===")
    print("PyMySQL patched successfully!")
    print("\nNow RESTART the application in cPanel!")
else:
    print("\n❌ Patch failed")
    sys.exit(1)
