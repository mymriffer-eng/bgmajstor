#!/usr/bin/env python
"""
Download and run emergency PyMySQL upgrade from GitHub
"""
import urllib.request
import os
import sys

print("=== Emergency PyMySQL Fix via GitHub ===\n")

# GitHub raw URL
github_url = "https://raw.githubusercontent.com/mymriffer-eng/bgmajstor/main/emergency_pymysql_upgrade.py"
local_path = "/home/bghranac/repositories/bgmajstor/emergency_pymysql_upgrade.py"

print(f"1. Downloading from GitHub...")
print(f"   URL: {github_url}")

try:
    urllib.request.urlretrieve(github_url, local_path)
    print(f"   ✓ Downloaded to: {local_path}")
except Exception as e:
    print(f"   ❌ Download failed: {e}")
    sys.exit(1)

print("\n2. Executing upgrade script...")
try:
    exec(open(local_path).read())
except Exception as e:
    print(f"   ❌ Execution failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
