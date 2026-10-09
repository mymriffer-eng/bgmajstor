#!/usr/bin/env python3
import os
import sys
import subprocess

PROJECT_DIR = "/home/bghranac/repositories/bgmajstor"
VENV_PYTHON = "/home/bghranac/virtualenv/repositories/bgmajstor/3.13/bin/python"
SETTINGS = "config.settings_production"

# Safe emoji list that usually works well with utf8mb4
SAFE_ICONS = {
    "Електричество": "⚡",
    "В и К": "💧",
    "Климатици и термопомпи": "❄️",
    "Строителство": "🧱",
    "Дърводелски услуги": "🔨",
    "Дограма": "🪟",
    "Градинарство": "🌱",
    "Почистване": "🧼",
}


def run_python_command(args):
    command = f'{VENV_PYTHON} {args}'
    print(f"\n>>> {command}")
    result = subprocess.run(command, cwd=PROJECT_DIR, shell=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_sql_fix():
    sql = """
ALTER TABLE core_category
  CONVERT TO CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

ALTER TABLE core_category
  MODIFY icon VARCHAR(50)
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
"""

    print("\n=== Applying MySQL charset fix to core_category ===")
    print(sql)

    # This file is intended to be run in the project environment where Django can reach the DB.
    # The app will use the configured production database credentials from settings_production.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS)
    sys.path.insert(0, PROJECT_DIR)

    import django
    django.setup()

    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("ALTER TABLE core_category CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("ALTER TABLE core_category MODIFY icon VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

    print("\n✅ Charset fix applied to core_category.")


def update_category_icons():
    print("\n=== Updating category icons ===")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS)
    sys.path.insert(0, PROJECT_DIR)

    import django
    django.setup()

    from core.models import Category

    for name, icon in SAFE_ICONS.items():
        Category.objects.filter(name=name).update(icon=icon)
        print(f"Updated: {name} -> {icon}")

    print("\n✅ Category icons updated.")


if __name__ == "__main__":
    print("BGmajstor category icon fix")
    run_sql_fix()
    update_category_icons()
    print("\nDone.")
