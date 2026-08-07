#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Upgrade PyMySQL to latest version
"""

import subprocess
import sys

print("=" * 60)
print("PyMySQL Upgrade Script")
print("=" * 60)

print("\nUpgrading pymysql to latest version...")
print("Command: pip install --upgrade pymysql")
print("-" * 60)

try:
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pymysql'],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("SUCCESS! PyMySQL upgraded successfully")
        print("=" * 60)
        
        # Check new version
        import pymysql
        print(f"\nNew PyMySQL version: {pymysql.__version__}")
        
        print("\nNext steps:")
        print("1. Restart the application")
        print("2. Run diagnostic.py to verify")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("ERROR: Upgrade failed!")
        print("=" * 60)
        sys.exit(1)
        
except Exception as e:
    print(f"\nERROR: {e}")
    sys.exit(1)
