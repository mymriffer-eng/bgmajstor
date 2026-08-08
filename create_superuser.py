#!/usr/bin/env python
"""
Create Django superuser for BGMaistor
"""

import os
import sys
import django

print("=" * 60)
print("Create Superuser for BGMaistor Admin")
print("=" * 60)

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
sys.path.insert(0, os.path.dirname(__file__))

try:
    django.setup()
    from django.contrib.auth import get_user_model
    print("✓ Django setup successful!")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

User = get_user_model()

# Superuser credentials
print("\n" + "=" * 60)
print("SUPERUSER CREDENTIALS")
print("=" * 60)
username = "admin"
email = "support@bgmajstor.eu"
password = "BGMaistor2026!Secure"  # ПРОМЕНИ ТОВА СЛЕД ПЪРВИЯ ЛОГИН!

print(f"Username: {username}")
print(f"Email: {email}")
print(f"Password: {password}")
print("\n⚠️  ВАЖНО: Промени паролата след първия логин!")

# Check if user already exists
print("\n" + "=" * 60)
print("Creating Superuser...")
print("=" * 60)

if User.objects.filter(username=username).exists():
    print(f"⚠️  User '{username}' already exists!")
    user = User.objects.get(username=username)
    
    # Update password
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.email = email
    user.save()
    print(f"✓ Updated existing user to superuser with new password")
else:
    # Create new superuser
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✓ Superuser '{username}' created successfully!")

print("\n" + "=" * 60)
print("SUCCESS!")
print("=" * 60)
print(f"\nAdmin Panel: https://bgmajstor.eu/supereto/")
print(f"Username: {username}")
print(f"Password: {password}")
print("\n⚠️  ВАЖНО:")
print("1. Логни се в admin панела")
print("2. Отиди на Users -> admin -> Change password")
print("3. Смени паролата на нещо сигурно!")
print("4. Изтрий този script след това за сигурност")
print("=" * 60)
