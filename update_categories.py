#!/usr/bin/env python
"""
Update existing categories - remove icon letters
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
django.setup()

from core.models import Category

def main():
    print("=== Updating Categories ===\n")
    
    categories = Category.objects.all()
    
    if not categories:
        print("❌ No categories found in database")
        return
    
    updated = 0
    for category in categories:
        old_icon = category.icon
        category.icon = ""
        category.save()
        print(f"✓ Updated: {category.name} (was: '{old_icon}' → now: '')")
        updated += 1
    
    print(f"\n=== Summary ===")
    print(f"Updated: {updated} categories")

if __name__ == "__main__":
    main()
