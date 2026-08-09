#!/usr/bin/env python
"""
Fix settings_production.py - add PyMySQL import at the beginning
"""
import os

settings_file = '/home/bghranac/repositories/bgmajstor/config/settings_production.py'

# Read current content
with open(settings_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if PyMySQL import already exists
if 'pymysql.install_as_MySQLdb()' in content:
    print("✓ PyMySQL import already present")
else:
    # Add PyMySQL import at the very beginning
    pymysql_import = """# PyMySQL as MySQLdb replacement
import pymysql
pymysql.install_as_MySQLdb()

"""
    
    # Insert at the beginning
    content = pymysql_import + content
    
    # Write back
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ Added PyMySQL import to settings_production.py")
    print("✓ File updated successfully")

print("\n=== Next step: Restart the application ===")
