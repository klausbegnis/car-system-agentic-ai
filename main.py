"""
File: main.py
Project: Agentic AI example
Created: Thursday, 16th October 2025 10:08:49 pm
Author: Klaus

MIT License
"""

from dotenv import load_dotenv

load_dotenv()

from src.app.main import app  # noqa

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8084)
