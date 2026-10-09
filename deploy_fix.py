#!/usr/bin/env python3
import os
import subprocess
import sys

PROJECT_DIR = "/home/bghranac/repositories/bgmajstor"
VENV_PYTHON = "/home/bghranac/virtualenv/repositories/bgmajstor/3.13/bin/python"
SETTINGS = "config.settings_production"


def run_command(command):
    print(f"\n>>> {command}")
    result = subprocess.run(command, cwd=PROJECT_DIR, shell=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    print("Starting BGmajstor deploy fix...")
    print(f"Project dir: {PROJECT_DIR}")

    run_command(f'{VENV_PYTHON} manage.py migrate --settings={SETTINGS}')
    run_command(f'{VENV_PYTHON} manage.py collectstatic --settings={SETTINGS} --noinput --clear')

    print("\n✅ BGmajstor deploy fix completed successfully.")
