"""Entry point for the packaged backend executable (built with PyInstaller).

The dev workflow still uses `uvicorn app.main:app --reload`; this module exists
so PyInstaller has a static import graph to analyze.
"""
import multiprocessing
import os

import uvicorn

from app.main import app

if __name__ == "__main__":
    multiprocessing.freeze_support()
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "5000"))
    uvicorn.run(app, host=host, port=port)
