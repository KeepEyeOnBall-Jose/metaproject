#!/usr/bin/env python3
"""
Run Playwright end-to-end tests for the question interface.
This script starts both frontend and backend servers, then runs the tests.
"""
import subprocess
import time
import sys
import os


def run_playwright_tests():
    """Run Playwright tests with servers started."""
    frontend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "frontend"
    )
    backend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "backend"
    )
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    print("🚀 Starting servers for Playwright testing...")

    # Start backend server
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
            "--reload",
        ],
        cwd=backend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Start frontend server
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Wait for servers to start
    print("Waiting for servers to start...")
    time.sleep(8)

    try:
        # Run Playwright tests
        print("Running Playwright tests...")
        test_result = subprocess.run(
            ["npx", "playwright", "test", "--reporter=line"],
            cwd=frontend_dir,
            capture_output=False,
        )

        return test_result.returncode == 0

    finally:
        print("Cleaning up servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()


if __name__ == "__main__":
    success = run_playwright_tests()
    sys.exit(0 if success else 1)
