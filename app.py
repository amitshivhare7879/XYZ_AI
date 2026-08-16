"""
XYZ AI — Free Hugging Face Spaces Entrypoint (Gradio / FastAPI SDK)
Mounts the FastAPI core engine, AI persona orchestrator, and all 4 School ERP frontend portals.
Runs 100% free on Hugging Face Spaces without any subscription or credit card.
"""

import sys
import os
from pathlib import Path

# Add root and backend modules to Python search path
ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "05_xyz_ai"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Import main FastAPI application from backend
import importlib.util
spec = importlib.util.spec_from_file_location("main_module", str(BACKEND_DIR / "main.py"))
main_module = importlib.util.module_from_spec(spec)
sys.modules["main_module"] = main_module
spec.loader.exec_module(main_module)
fastapi_app = main_module.app

# Compatibility patch for newer huggingface_hub versions where HfFolder was removed
try:
    import huggingface_hub
    if not hasattr(huggingface_hub, "HfFolder"):
        class HfFolder:
            @staticmethod
            def get_token():
                import os
                return os.getenv("HF_TOKEN") or ""
            @staticmethod
            def save_token(token):
                pass
            @staticmethod
            def delete_token():
                pass
        huggingface_hub.HfFolder = HfFolder
except Exception:
    pass

import gradio as gr

# Minimal Gradio interface linking to our full rich portals
with gr.Blocks(title="XYZ AI School ERP Hub", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 XYZ AI — School ERP Assistant Ecosystem")
    gr.Markdown("Welcome to the **Delhi Public Global School ERP**. You can access all portals directly below:")
    with gr.Row():
        gr.Markdown("""
        - 🌟 **[Unified Login Gateway](/login)**: SSO Login with Auto-Role Redirection
        - 👨‍🎓 **[Student Portal](/student)**: Academic Assistant, Attendance (91.2%), Timetable & 3D Avatar
        - 👨‍👩‍👧 **[Parent Portal](/parent)**: Child Progress, Attendance, Report Cards & Fee Invoices
        - 👩‍🏫 **[Staff / Teacher Portal](/staff)**: Class 10-A Roster & Voice Attendance Marker
        - 🏛️ **[Management Portal](/management)**: School Analytics, Fee Recovery & Escalations
        - 📖 **[Interactive Swagger API Docs](/docs)**: FastAPI REST & AI Endpoints
        """)

# Mount Gradio onto FastAPI
app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
