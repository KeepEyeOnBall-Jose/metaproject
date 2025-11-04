#!/usr/bin/env python3
"""
Integration test script for the Question Tracker API.

This script tests that all backend API endpoints are working correctly
by starting the server and making HTTP requests to verify functionality.

Usage:
    python test_integration.py
"""

import requests
import subprocess
import time
import sys
import os


def test_backend_integration():
    """Test all backend API endpoints work correctly."""

    # Get the backend directory path
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    print("🚀 Starting backend integration test...")
    print("📍 Backend directory:", backend_dir)
    print("🐍 Python executable:", venv_python)

    # Verify virtual environment exists
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found. Please run setup first.")
        return False

    # Start the backend server
    print("🔄 Starting backend server...")
    server = subprocess.Popen(
        [
            venv_python,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=backend_dir,
    )

    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)

    success = True

    try:
        # Test questions endpoint
        print("🧪 Testing questions endpoint...")
        response = requests.get("http://localhost:8000/questions", timeout=5)
        if response.status_code != 200:
            print(f"❌ Questions endpoint failed: {response.status_code}")
            success = False
        else:
            questions = response.json()
            print(f"✅ Questions endpoint: {len(questions)} questions loaded")

        # Test categories endpoint
        print("🧪 Testing categories endpoint...")
        response = requests.get("http://localhost:8000/categories", timeout=5)
        if response.status_code != 200:
            print(f"❌ Categories endpoint failed: {response.status_code}")
            success = False
        else:
            categories = response.json()
            print(f"✅ Categories endpoint: {len(categories)} categories found")

        # Test individual question endpoint (if we have questions)
        if questions:
            print("🧪 Testing individual question endpoint...")
            first_question_id = questions[0]["id"]
            response = requests.get(
                f"http://localhost:8000/questions/{first_question_id}", timeout=5
            )
            if response.status_code != 200:
                print(f"❌ Individual question endpoint failed: {response.status_code}")
                success = False
            else:
                question = response.json()
                if question["id"] == first_question_id:
                    print(
                        f"✅ Individual question endpoint: question {first_question_id} retrieved"
                    )
                else:
                    print("❌ Individual question endpoint returned wrong data")
                    success = False

        # Test 404 for non-existent question
        print("🧪 Testing 404 for non-existent question...")
        response = requests.get(
            "http://localhost:8000/questions/nonexistent", timeout=5
        )
        if response.status_code != 404:
            print(f"❌ 404 test failed: expected 404, got {response.status_code}")
            success = False
        else:
            print("✅ 404 endpoint works correctly")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error during testing: {e}")
        success = False
    except Exception as e:
        print(f"❌ Unexpected error during testing: {e}")
        success = False
    finally:
        # Clean up: terminate the server
        print("🧹 Cleaning up server process...")
        server.terminate()
        try:
            server.wait(timeout=5)
            print("✅ Server terminated successfully")
        except subprocess.TimeoutExpired:
            print("⚠️  Server did not terminate gracefully, force killing...")
            server.kill()
            server.wait()

    if success:
        print("🎉 All backend integration tests passed!")
        return True
    else:
        print("💥 Some integration tests failed!")
        return False


if __name__ == "__main__":
    success = test_backend_integration()
    sys.exit(0 if success else 1)
