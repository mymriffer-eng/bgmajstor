#!/usr/bin/env python
"""
Check for errors - show what's breaking
"""
import pymysql
pymysql.install_as_MySQLdb()

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')

try:
    django.setup()
    print("✓ Django setup OK")
    
    # Try to render home view
    from django.test import RequestFactory
    from core.views import home
    
    factory = RequestFactory()
    request = factory.get('/')
    
    response = home(request)
    print(f"✓ Home view OK - Status: {response.status_code}")
    
except Exception as e:
    print(f"❌ ERROR: {type(e).__name__}")
    print(f"Message: {str(e)}")
    import traceback
    traceback.print_exc()
