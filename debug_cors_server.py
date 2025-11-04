#!/usr/bin/env python3
"""
Start backend and debug CORS issue.
"""
import subprocess
import time
import requests
import sys
import os


def main():
    backend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "backend"
    )
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    print("Starting backend server...")
    backend_process = subprocess.Popen(
        [
            venv_python,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
        ],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(3)  # Wait for server to start

    try:
        print("Testing CORS...")

        # Test 1: Request without Origin header
        print("\nTest 1: Request without Origin header")
        response = requests.get("http://localhost:8000/questions")
        print(f"Status: {response.status_code}")
        cors_headers = {
            k: v
            for k, v in response.headers.items()
            if k.lower().startswith("access-control")
        }
        print(f"CORS headers: {cors_headers}")

        # Test 2: Request with Origin header
        print("\nTest 2: Request with Origin header")
        response = requests.get(
            "http://localhost:8000/questions", headers={"Origin": "http://0.0.0.0:5173"}
        )
        print(f"Status: {response.status_code}")
        cors_headers = {
            k: v
            for k, v in response.headers.items()
            if k.lower().startswith("access-control")
        }
        print(f"CORS headers: {cors_headers}")

        # Test 3: OPTIONS preflight request
        print("\nTest 3: OPTIONS preflight request")
        response = requests.options(
            "http://localhost:8000/questions",
            headers={
                "Origin": "http://0.0.0.0:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        print(f"Status: {response.status_code}")
        cors_headers = {
            k: v
            for k, v in response.headers.items()
            if k.lower().startswith("access-control")
        }
        print(f"CORS headers: {cors_headers}")

    finally:
        print("\nStopping backend server...")
        backend_process.terminate()
        backend_process.wait()


if __name__ == "__main__":
    main()
