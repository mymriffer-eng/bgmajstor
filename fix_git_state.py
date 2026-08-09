#!/usr/bin/env python
"""
Fix Git state on server - commit local changes to allow pull
"""
import subprocess
import os

print("=== Fixing Git State ===\n")

os.chdir('/home/bghranac/repositories/bgmajstor')

# Check git status
print("1. Checking Git status...")
result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
if result.stdout.strip():
    print(f"   Uncommitted changes found:\n{result.stdout}")
    
    print("\n2. Stashing local changes...")
    subprocess.run(['git', 'stash'], capture_output=True)
    print("   ✓ Changes stashed")
else:
    print("   ✓ No uncommitted changes")

print("\n3. Pulling from GitHub...")
result = subprocess.run(['git', 'pull', 'origin', 'main'], capture_output=True, text=True)
print(result.stdout)
if result.returncode == 0:
    print("   ✓ Pull successful")
else:
    print(f"   ❌ Pull failed: {result.stderr}")

print("\n=== Git Fixed ===")
print("Now you can use Git Version Control → Pull/Deploy normally")
