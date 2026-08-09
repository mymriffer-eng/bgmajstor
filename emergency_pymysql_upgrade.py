#!/usr/bin/env python
"""
EMERGENCY FIX: Upgrade PyMySQL directly without Git deploy
"""
import subprocess
import sys
import os

print("=== EMERGENCY PyMySQL Upgrade ===\n")

# Change to venv directory
venv_path = '/home/bghranac/virtualenv/repositories/bgmajstor/3.13'
activate_script = os.path.join(venv_path, 'bin', 'activate_this.py')

print(f"1. Activating venv: {venv_path}")
if os.path.exists(activate_script):
    exec(open(activate_script).read(), {'__file__': activate_script})
    print("   ✓ Venv activated")
else:
    print("   ⚠ Using system Python")

# Upgrade PyMySQL
print("\n2. Upgrading PyMySQL to 2.2.8...")
result = subprocess.run([
    sys.executable, '-m', 'pip', 'install', 
    '--upgrade', 'pymysql==2.2.8'
], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print(result.stderr)

# Verify installation
print("\n3. Verifying installation...")
try:
    import pymysql
    print(f"   ✓ PyMySQL version: {pymysql.__version__}")
    
    if pymysql.__version__ >= '2.2.1':
        print("   ✓ Version is correct!")
    else:
        print(f"   ❌ Version still old: {pymysql.__version__}")
        sys.exit(1)
        
except ImportError as e:
    print(f"   ❌ Cannot import pymysql: {e}")
    sys.exit(1)

print("\n=== SUCCESS ===")
print("Now RESTART the application in cPanel!")
print("Setup Python App → Restart button")
