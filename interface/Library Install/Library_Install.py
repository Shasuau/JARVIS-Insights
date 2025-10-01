# install_deps_v4.py
# Installs packages using a REAL Python interpreter (not this EXE).

import os
import sys
import shutil
import subprocess
from typing import List, Optional

PACKAGES: List[str] = [
    "discord.py",
    "PyYAML",
    "requests",
    "google-auth",
    "google-auth-oauthlib",
    "google-api-python-client",
]

CANDIDATES = [
    "python",     # common
    "py",         # Python Launcher
    os.path.expandvars(r"%LocalAppData%\Programs\Python\Python312\python.exe"),
    r"C:\Program Files\Python312\python.exe",
    r"C:\Program Files (x86)\Python312\python.exe",
]

def find_python() -> Optional[str]:
    # 1) PATH lookups
    for c in ("python", "py"):
        if shutil.which(c):
            return c
    # 2) Common install paths
    for p in CANDIDATES:
        if os.path.isfile(p):
            return p
    return None

def run(title: str, args: List[str], check: bool = True) -> int:
    print(f"\n--- {title} ---")
    print("> " + " ".join(f'"{a}"' if " " in a else a for a in args))
    cp = subprocess.run(args)
    if check and cp.returncode != 0:
        print(f"[ERROR] {title} failed with exit {cp.returncode}")
        sys.exit(cp.returncode)
    return cp.returncode

def main():
    print("=== Installing dependencies (using system Python) ===")

    py = find_python()
    if not py:
        print("[ERROR] No system Python found.")
        print("Install Python first, then re-run this installer.")
        print("Tip (PowerShell): winget install -e --id Python.Python.3.12 --silent")
        sys.exit(1)

    # Sanity check
    run("Show Python version", [py, "-V"])
    run("Show pip version", [py, "-m", "pip", "--version"])

    # Upgrade tooling (user site)
    run("Upgrade pip/setuptools/wheel", [py, "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel", "--user"])

    # Install packages (user site)
    for pkg in PACKAGES:
        run(f"Install {pkg}", [py, "-m", "pip", "install", "--user", pkg])

    print("\n[DONE] All packages installed successfully.")


if __name__ == "__main__":
    main()
