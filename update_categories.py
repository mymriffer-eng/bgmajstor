#!/usr/bin/env python
"""
Update existing categories - remove icon letters
Direct MySQL update without Django
"""
import pymysql

def main():
    print("=== Updating Categories (Direct MySQL) ===\n")
    
    # Connect to database
    connection = pymysql.connect(
        host='localhost',
        user='bghranac_bgmajstor',
        password='(%(yM07{@!S3b2&s',
        database='bghranac_bgmajstor',
        charset='utf8mb4'
    )
    
    try:
        cursor = connection.cursor()
        
        # Get current categories
        cursor.execute("SELECT id, name, icon FROM core_category")
        categories = cursor.fetchall()
        
        print(f"Found {len(categories)} categories:\n")
        for cat_id, name, icon in categories:
            print(f"  ID {cat_id}: {name} (icon: '{icon}')")
        
        # Update all icons to empty string
        cursor.execute("UPDATE core_category SET icon = ''")
        connection.commit()
        
        print(f"\n✓ Updated {cursor.rowcount} categories - all icons removed")
        
    finally:
        connection.close()

if __name__ == "__main__":
    main()
