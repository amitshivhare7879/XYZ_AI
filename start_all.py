"""
XYZ AI — Unified Multi-Portal & Engine Launcher
Starts the Unified Gateway, FastAPI Backend, and all 4 frontend portals simultaneously.
"""

import subprocess
import sys
import time
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(__file__).parent

def launch():
    print("==================================================================")
    print("🚀 Starting XYZ AI — Human-Like School ERP Assistant Ecosystem")
    print("==================================================================")

    # 1. Start FastAPI Backend (Port 8000)
    print("[1/6] Launching Backend Engine (FastAPI) on http://localhost:8000 ...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "05_xyz_ai.main:app", "--host", "127.0.0.1", "--port", "8000", "--reload"],
        cwd=str(ROOT_DIR)
    )

    time.sleep(2)

    # 2. Start Unified Login Gateway (Port 3000)
    print("[2/6] Launching Unified Login Gateway on http://localhost:3000 ...")
    gateway_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3000", "--directory", str(ROOT_DIR / "unified_login")]
    )

    # 3. Start Student Portal (Port 3001)
    print("[3/6] Launching Student Portal on http://localhost:3001 ...")
    student_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3001", "--directory", str(ROOT_DIR / "01_student_portal")]
    )

    # 4. Start Parent Portal (Port 3002)
    print("[4/6] Launching Parent Portal on http://localhost:3002 ...")
    parent_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3002", "--directory", str(ROOT_DIR / "02_parent_portal")]
    )

    # 5. Start Staff / Teacher Portal (Port 3003)
    print("[5/6] Launching Staff Portal on http://localhost:3003 ...")
    staff_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3003", "--directory", str(ROOT_DIR / "03_staff_portal")]
    )

    # 6. Start Management Portal (Port 3004)
    print("[6/6] Launching Management Portal on http://localhost:3004 ...")
    mgmt_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "3004", "--directory", str(ROOT_DIR / "04_management_portal")]
    )

    print("\n==================================================================")
    print("✅ All 6 Ecosystem Services Are Running!")
    print("------------------------------------------------------------------")
    print("🌟 Unified Login Gateway: http://localhost:3000 (SSO Entry Point)")
    print("• Student Portal:         http://localhost:3001")
    print("• Parent Portal:          http://localhost:3002")
    print("• Staff/Teacher Portal:   http://localhost:3003")
    print("• Management Portal:      http://localhost:3004")
    print("• Backend API & Docs:     http://localhost:8000/docs")
    print("==================================================================")
    print("👉 Open http://localhost:3000 to log in as any user and auto-redirect.\n")
    print("Press Ctrl+C to terminate all services.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down all services...")
        backend_proc.terminate()
        gateway_proc.terminate()
        student_proc.terminate()
        parent_proc.terminate()
        staff_proc.terminate()
        mgmt_proc.terminate()
        print("Shutdown complete.")

if __name__ == "__main__":
    launch()
