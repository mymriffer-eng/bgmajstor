#!/usr/bin/env python
"""
Install WhiteNoise and recollect static files
"""

import os
import sys
import subprocess

print("=" * 60)
print("WhiteNoise Installation & Static Files Setup")
print("=" * 60)

# 1. Install whitenoise
print("\n1. Installing WhiteNoise...")
print("-" * 60)
try:
    result = subprocess.run(
        [sys.executable, '-m', 'pip', 'install', 'whitenoise==6.7.0'],
        capture_output=True,
        text=True,
        timeout=120
    )
    print(result.stdout)
    if result.returncode == 0:
        print("✓ WhiteNoise installed successfully!")
    else:
        print(f"✗ Installation failed: {result.stderr}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# 2. Setup Django
print("\n2. Setting up Django...")
print("-" * 60)
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
sys.path.insert(0, os.path.dirname(__file__))

try:
    import django
    django.setup()
    from django.core.management import call_command
    print("✓ Django setup successful!")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

# 3. Collect static files with WhiteNoise
print("\n3. Collecting static files with WhiteNoise...")
print("-" * 60)
try:
    call_command('collectstatic', '--noinput', verbosity=2)
    print("\n✓ Static files collected with WhiteNoise!")
except Exception as e:
    print(f"✗ collectstatic failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("SUCCESS! WhiteNoise configured")
print("=" * 60)
print("\nNext steps:")
print("1. Restart the application in Setup Python App")
print("2. Test: https://bgmajstor.eu")
print("3. Static files now served directly by Django via WhiteNoise")
print("4. No Apache .htaccess configuration needed!")
print("\nWhiteNoise benefits:")
print("  ✓ Compression & caching (faster loading)")
print("  ✓ Cache-busting hashes (better browser caching)")
print("  ✓ Works on any hosting platform")
print("=" * 60)
