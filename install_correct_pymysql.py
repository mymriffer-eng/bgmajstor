#!/usr/bin/env python
"""
Install correct PyMySQL version that actually exists
"""
import subprocess
import sys

print("=== Installing Correct PyMySQL ===\n")

print("1. Installing PyMySQL 1.1.1 (the version that works)...")
result = subprocess.run([
    sys.executable, '-m', 'pip', 'install', 
    'pymysql==1.1.1', '--force-reinstall'
], capture_output=True, text=True)

print(result.stdout)
if result.stderr:
    print(result.stderr)

# Verify
print("\n2. Verifying installation...")
try:
    import importlib
    if 'pymysql' in sys.modules:
        del sys.modules['pymysql']
    
    import pymysql
    print(f"   ✓ PyMySQL version: {pymysql.__version__}")
    
    # Test connection
    print("\n3. Testing database connection...")
    conn = pymysql.connect(
        host='localhost',
        user='bghranac_bgmajstor',
        password='(%(yM07{@!S3b2&s',
        database='bghranac_bgmajstor'
    )
    print("   ✓ Database connection OK")
    conn.close()
    
    print("\n=== SUCCESS ===")
    print("Now RESTART the application!")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)
