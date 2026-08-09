#!/usr/bin/env python
"""
Upgrade PyMySQL to correct version
"""
import subprocess
import sys

print("=== Upgrading PyMySQL ===\n")

# Uninstall old version
print("1. Uninstalling old PyMySQL...")
subprocess.run([sys.executable, '-m', 'pip', 'uninstall', '-y', 'pymysql'])

# Install correct version
print("\n2. Installing PyMySQL >= 2.2.1...")
result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'pymysql>=2.2.1'])

if result.returncode == 0:
    print("\n✓ PyMySQL upgraded successfully")
    
    # Verify
    import pymysql
    print(f"✓ New version: {pymysql.__version__}")
else:
    print("\n❌ Upgrade failed")
    sys.exit(1)
