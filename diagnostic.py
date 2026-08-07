#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BGMaistor cPanel Diagnostic Script
Провери какво не работи в deployment-а
"""

import sys
import os

print("=" * 60)
print("BGMaistor Production Diagnostic Script")
print("=" * 60)

# 1. Проверка на Python версия
print("\n1. Python Version:")
print(f"   {sys.version}")
print(f"   Executable: {sys.executable}")

# 2. Проверка на работна директория
print("\n2. Working Directory:")
print(f"   {os.getcwd()}")

# 3. Проверка дали pymysql е инсталиран
print("\n3. PyMySQL Installation:")
try:
    import pymysql
    print(f"   ✓ pymysql version: {pymysql.__version__}")
    print(f"   ✓ Location: {pymysql.__file__}")
except ImportError as e:
    print(f"   ✗ PyMySQL NOT installed: {e}")
    print("   FIX: Run 'pip install pymysql' in Setup Python App")

# 4. Проверка дали Django е инсталиран
print("\n4. Django Installation:")
try:
    import django
    print(f"   ✓ Django version: {django.__version__}")
    print(f"   ✓ Location: {django.__file__}")
except ImportError as e:
    print(f"   ✗ Django NOT installed: {e}")
    print("   FIX: Run 'pip install -r requirements.txt'")

# 5. Проверка на файлова структура
print("\n5. File Structure Check:")
base_dir = os.path.dirname(os.path.abspath(__file__))
critical_files = [
    'manage.py',
    'passenger_wsgi.py',
    'config/settings.py',
    'config/settings_production.py',
    'requirements.txt',
]

for file_path in critical_files:
    full_path = os.path.join(base_dir, file_path)
    if os.path.exists(full_path):
        print(f"   ✓ {file_path}")
    else:
        print(f"   ✗ {file_path} - MISSING!")

# 6. Проверка на config/settings_production.py съдържание
print("\n6. Production Settings Check:")
settings_path = os.path.join(base_dir, 'config', 'settings_production.py')
if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    checks = {
        'DEBUG = False': 'DEBUG mode',
        'ALLOWED_HOSTS': 'Allowed hosts',
        'SECRET_KEY': 'Secret key',
        'DATABASES': 'Database config',
        'pymysql': 'PyMySQL import',
    }
    
    for check_str, check_name in checks.items():
        if check_str in content:
            print(f"   ✓ {check_name} found")
        else:
            print(f"   ✗ {check_name} - MISSING!")
else:
    print(f"   ✗ settings_production.py NOT FOUND!")

# 7. Опит за Django initialization
print("\n7. Django Initialization Test:")
try:
    # Set Django settings
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
    sys.path.insert(0, base_dir)
    
    # Try to setup Django
    import django
    django.setup()
    print("   ✓ Django setup successful!")
    
    # 8. Database connection test
    print("\n8. Database Connection Test:")
    from django.db import connection
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"   ✓ Database connection successful!")
        print(f"   ✓ Query result: {result}")
        
        # Check database name
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        print(f"   ✓ Connected to database: {db_name[0]}")
        
    except Exception as db_err:
        print(f"   ✗ Database connection FAILED!")
        print(f"   Error: {db_err}")
        print("\n   Possible fixes:")
        print("   - Check MySQL database exists in cPanel")
        print("   - Verify database credentials in settings_production.py")
        print("   - Ensure database user has permissions")
    
    # 9. Check for pending migrations
    print("\n9. Database Migrations Check:")
    try:
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        migrations_output = out.getvalue()
        
        if '[ ]' in migrations_output:
            print("   ⚠ Pending migrations found!")
            print("   FIX: Run 'python manage.py migrate --settings=config.settings_production'")
        else:
            print("   ✓ All migrations applied")
            
    except Exception as mig_err:
        print(f"   ? Cannot check migrations: {mig_err}")
    
except Exception as django_err:
    print(f"   ✗ Django initialization FAILED!")
    print(f"   Error Type: {type(django_err).__name__}")
    print(f"   Error: {django_err}")
    
    import traceback
    print("\n   Full Traceback:")
    print("   " + "\n   ".join(traceback.format_exc().split("\n")))

# 10. Environment check
print("\n10. Environment Variables:")
django_settings = os.environ.get('DJANGO_SETTINGS_MODULE', 'NOT SET')
print(f"   DJANGO_SETTINGS_MODULE: {django_settings}")

print("\n" + "=" * 60)
print("Diagnostic Complete!")
print("=" * 60)
print("\nNext steps:")
print("1. Fix any ✗ errors shown above")
print("2. Make sure to update settings_production.py with PyMySQL import")
print("3. Run migrations if needed")
print("4. Restart the application")
print("=" * 60)
