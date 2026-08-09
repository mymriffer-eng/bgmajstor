#!/usr/bin/env python
"""
Comprehensive diagnostic - find exact issue
"""

print("=== BGMaistor Diagnostic ===\n")

# 1. Check PyMySQL
print("1. Checking PyMySQL...")
try:
    import pymysql
    print(f"   ✓ PyMySQL installed: {pymysql.__version__}")
except ImportError as e:
    print(f"   ❌ PyMySQL not found: {e}")

# 2. Check settings file
print("\n2. Checking settings_production.py...")
import os
settings_path = '/home/bghranac/repositories/bgmajstor/config/settings_production.py'
if os.path.exists(settings_path):
    with open(settings_path, 'r') as f:
        content = f.read()
        if 'pymysql.install_as_MySQLdb()' in content:
            print("   ✓ PyMySQL import present in settings")
        else:
            print("   ❌ PyMySQL import MISSING from settings")
        
        if 'STATIC_ROOT' in content:
            print("   ✓ STATIC_ROOT defined")
        else:
            print("   ❌ STATIC_ROOT not found")
else:
    print(f"   ❌ Settings file not found: {settings_path}")

# 3. Test database connection
print("\n3. Testing database connection...")
try:
    import pymysql
    conn = pymysql.connect(
        host='localhost',
        user='bghranac_bgmajstor',
        password='(%(yM07{@!S3b2&s',
        database='bghranac_bgmajstor'
    )
    print("   ✓ Database connection OK")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM core_category")
    count = cursor.fetchone()[0]
    print(f"   ✓ Found {count} categories")
    conn.close()
except Exception as e:
    print(f"   ❌ Database error: {e}")

# 4. Test Django setup
print("\n4. Testing Django setup...")
try:
    import pymysql
    pymysql.install_as_MySQLdb()
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
    import django
    django.setup()
    print("   ✓ Django setup successful")
    
    # Try importing models
    from core.models import Category, City
    print("   ✓ Models imported")
    
    # Count objects
    cats = Category.objects.count()
    cities = City.objects.count()
    print(f"   ✓ Database: {cats} categories, {cities} cities")
    
except Exception as e:
    print(f"   ❌ Django setup failed: {type(e).__name__}: {e}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

print("\n=== Diagnostic Complete ===")
