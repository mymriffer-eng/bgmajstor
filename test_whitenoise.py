#!/usr/bin/env python
"""
Test WhiteNoise Static Files
"""

import os
import sys

print("=" * 60)
print("WhiteNoise Static Files Test")
print("=" * 60)

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
sys.path.insert(0, os.path.dirname(__file__))

try:
    import django
    django.setup()
    from django.conf import settings
    print("✓ Django loaded")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

# Check middleware
print("\n1. Middleware Configuration:")
print("-" * 60)
middleware = settings.MIDDLEWARE
for i, mw in enumerate(middleware):
    marker = "  ← WhiteNoise!" if 'whitenoise' in mw.lower() else ""
    print(f"  {i+1}. {mw}{marker}")

whitenoise_found = any('whitenoise' in mw.lower() for mw in middleware)
if whitenoise_found:
    print("\n✓ WhiteNoise middleware IS configured")
else:
    print("\n✗ WhiteNoise middleware NOT found!")

# Check static settings
print("\n2. Static Files Settings:")
print("-" * 60)
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'default')}")

# Check if WhiteNoise can find files
print("\n3. Test Static File Access:")
print("-" * 60)
style_css = os.path.join(settings.STATIC_ROOT, 'css', 'style.css')
if os.path.exists(style_css):
    size = os.path.getsize(style_css)
    print(f"✓ style.css found: {size} bytes")
    print(f"  Path: {style_css}")
    print(f"  URL: {settings.STATIC_URL}css/style.css")
else:
    print(f"✗ style.css NOT found at: {style_css}")

# Test WhiteNoise import
print("\n4. WhiteNoise Module:")
print("-" * 60)
try:
    import whitenoise
    print(f"✓ WhiteNoise version: {whitenoise.__version__}")
    from whitenoise.middleware import WhiteNoiseMiddleware
    print("✓ WhiteNoiseMiddleware can be imported")
except ImportError as e:
    print(f"✗ WhiteNoise import failed: {e}")

# Simulate HTTP request
print("\n5. Simulate Static File Request:")
print("-" * 60)
try:
    from django.test import RequestFactory
    from django.core.handlers.wsgi import WSGIHandler
    
    # Create a test request for static file
    factory = RequestFactory()
    request = factory.get('/static/css/style.css')
    
    print("✓ Test request created: GET /static/css/style.css")
    print("  (WhiteNoise should handle this in production)")
    
except Exception as e:
    print(f"⚠ Could not simulate request: {e}")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)
print("\nIf WhiteNoise is configured correctly but CSS still not loading:")
print("1. Check browser Network tab for 404/403 errors")
print("2. Try accessing: https://bgmajstor.eu/static/css/style.css directly")
print("3. Check Passenger error logs")
print("4. Clear browser cache (Ctrl+Shift+R)")
print("=" * 60)
