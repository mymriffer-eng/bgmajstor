#!/usr/bin/env python
"""
Static Files Diagnostic Script for cPanel
Checks if static files are properly collected and accessible
"""

import os
import sys

print("=" * 60)
print("Static Files Diagnostic")
print("=" * 60)

# Setup Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_production'
sys.path.insert(0, os.path.dirname(__file__))

try:
    import django
    django.setup()
    from django.conf import settings
    print("✓ Django settings loaded")
except Exception as e:
    print(f"✗ Django setup failed: {e}")
    sys.exit(1)

# Check settings
print("\n1. Django Static Settings:")
print("-" * 60)
print(f"STATIC_URL: {settings.STATIC_URL}")
print(f"STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"STATICFILES_DIRS: {getattr(settings, 'STATICFILES_DIRS', [])}")
print(f"BASE_DIR: {settings.BASE_DIR}")

# Check if STATIC_ROOT exists
print("\n2. STATIC_ROOT Directory Check:")
print("-" * 60)
if os.path.exists(settings.STATIC_ROOT):
    print(f"✓ STATIC_ROOT exists: {settings.STATIC_ROOT}")
    
    # List CSS files
    css_dir = os.path.join(settings.STATIC_ROOT, 'css')
    if os.path.exists(css_dir):
        print(f"✓ CSS directory exists: {css_dir}")
        css_files = os.listdir(css_dir)
        print(f"  CSS files found: {css_files}")
        
        # Check style.css specifically
        style_css = os.path.join(css_dir, 'style.css')
        if os.path.exists(style_css):
            size = os.path.getsize(style_css)
            print(f"  ✓ style.css exists ({size} bytes)")
            
            # Check permissions
            import stat
            st = os.stat(style_css)
            perms = oct(st.st_mode)[-3:]
            print(f"  Permissions: {perms}")
        else:
            print(f"  ✗ style.css NOT FOUND!")
    else:
        print(f"✗ CSS directory NOT FOUND: {css_dir}")
    
    # List all collected files
    print("\n  All collected static files:")
    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        level = root.replace(settings.STATIC_ROOT, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files[:10]:  # Limit to first 10 files per directory
            print(f'{subindent}{file}')
        if len(files) > 10:
            print(f'{subindent}... and {len(files) - 10} more files')
else:
    print(f"✗ STATIC_ROOT does NOT exist: {settings.STATIC_ROOT}")

# Check public_html structure
print("\n3. Public HTML Structure:")
print("-" * 60)
public_html = os.path.join(settings.BASE_DIR, 'public_html')
if os.path.exists(public_html):
    print(f"✓ public_html exists: {public_html}")
    for item in os.listdir(public_html):
        item_path = os.path.join(public_html, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}/")
            # List first level inside
            try:
                subitems = os.listdir(item_path)[:5]
                for sub in subitems:
                    print(f"    - {sub}")
                if len(os.listdir(item_path)) > 5:
                    print(f"    ... and {len(os.listdir(item_path)) - 5} more")
            except PermissionError:
                print(f"    ✗ Permission denied")
        else:
            size = os.path.getsize(item_path)
            print(f"  📄 {item} ({size} bytes)")
else:
    print(f"✗ public_html NOT FOUND: {public_html}")

# Check source static files
print("\n4. Source Static Files:")
print("-" * 60)
source_static = os.path.join(settings.BASE_DIR, 'static')
if os.path.exists(source_static):
    print(f"✓ Source static/ exists: {source_static}")
    css_source = os.path.join(source_static, 'css', 'style.css')
    if os.path.exists(css_source):
        size = os.path.getsize(css_source)
        print(f"  ✓ Source style.css exists ({size} bytes)")
    else:
        print(f"  ✗ Source style.css NOT FOUND")
else:
    print(f"✗ Source static/ NOT FOUND")

# Web accessibility test
print("\n5. Web Path Analysis:")
print("-" * 60)
print(f"Expected URL: https://bgmajstor.eu{settings.STATIC_URL}css/style.css")
print(f"Should map to: {os.path.join(settings.STATIC_ROOT, 'css', 'style.css')}")

# .htaccess check
print("\n6. .htaccess Check:")
print("-" * 60)
htaccess_path = os.path.join(settings.BASE_DIR, 'public_html', '.htaccess')
if os.path.exists(htaccess_path):
    print(f"✓ .htaccess exists in public_html")
    with open(htaccess_path, 'r') as f:
        content = f.read()
        if 'static' in content.lower():
            print("  ✓ Contains 'static' rules")
        else:
            print("  ⚠ No 'static' rules found")
else:
    htaccess_root = os.path.join(settings.BASE_DIR, '.htaccess')
    if os.path.exists(htaccess_root):
        print(f"✓ .htaccess exists in root: {htaccess_root}")
    else:
        print("✗ No .htaccess found")

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
