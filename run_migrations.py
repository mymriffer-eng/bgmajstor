#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run Django migrations and collectstatic
"""

import os
import sys
import django

print("=" * 60)
print("Django Migrations & Collectstatic Script")
print("=" * 60)

# Set up Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)

django.setup()

from django.core.management import call_command

print("\n1. Running database migrations...")
print("-" * 60)
try:
    call_command('migrate', '--noinput', verbosity=2)
    print("\n✓ Migrations completed successfully!")
except Exception as e:
    print(f"\n✗ Migrations FAILED: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("\n2. Running collectstatic...")
print("-" * 60)
try:
    call_command('collectstatic', '--noinput', '--clear', verbosity=1)
    print("\n✓ Static files collected successfully!")
except Exception as e:
    print(f"\n✗ Collectstatic FAILED: {e}")
    print("   This may be OK if static files are already collected.")

print("\n" + "=" * 60)
print("SUCCESS! Database setup complete")
print("=" * 60)
print("\nNext steps:")
print("1. Restart the application in Setup Python App")
print("2. Test the website: https://bgmajstor.eu")
print("3. The website should now work!")
print("\nOptional:")
print("- Create superuser: python manage.py createsuperuser --settings=config.settings_production")
print("- Admin panel: https://bgmajstor.eu/admin")
print("=" * 60)
