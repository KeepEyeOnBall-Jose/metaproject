#!/usr/bin/env python3
"""
Test script for LLM analysis endpoint (/analyze/concepts)
Tests the AI-powered concept clustering functionality.
"""

import sys
import os
import subprocess
import time
import requests
import json
from pathlib import Path


def start_backend_server():
    """Start the backend server in the background."""
    backend_dir = Path(__file__).parent / "backend"
    python_exe = backend_dir / "venv" / "bin" / "python"

    print("📍 Backend directory:", backend_dir)
    print("🐍 Python executable:", python_exe)

    if not python_exe.exists():
        print("❌ Python virtual environment not found. Run setup first.")
        return None

    print("🔄 Starting backend server...")
    try:
        process = subprocess.Popen(
            [
                str(python_exe),
                "-m",
                "uvicorn",
                "main:app",
                "--host",
                "0.0.0.0",
                "--port",
                "8000",
            ],
            cwd=str(backend_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None


def wait_for_server(max_attempts=10):
    """Wait for the server to be ready."""
    print("⏳ Waiting for server to start...")
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/questions", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")

    print("❌ Server failed to start within timeout")
    return False


def test_llm_analysis():
    """Test the LLM analysis endpoint."""
    print("🧠 Testing LLM analysis endpoint...")

    try:
        # First get some questions to analyze
        response = requests.get("http://localhost:8000/questions", timeout=5)
        response.raise_for_status()
        questions = response.json()

        if not questions:
            print("❌ No questions found to analyze")
            return False

        # Take first 3 questions and get their answers
        test_questions = []
        for q in questions[:3]:
            # Get answer for this question
            answer_response = requests.get(
                f"http://localhost:8000/questions/{q['id']}/answer", timeout=5
            )
            answer_data = (
                answer_response.json()
                if answer_response.status_code == 200
                else {"has_answer": False, "answer": None}
            )

            test_questions.append(
                {
                    "id": q["id"],
                    "question": q["question"],
                    "answer": answer_data.get("answer"),
                    "category": q["category"],
                }
            )

        print(f"📊 Analyzing {len(test_questions)} questions...")
        questions_with_answers = sum(1 for q in test_questions if q["answer"])
        print(f"   {questions_with_answers} have answers available")

        # Test the analysis endpoint
        analysis_response = requests.post(
            "http://localhost:8000/analyze/concepts",
            json={"questions": test_questions},
            timeout=30,  # LLM calls can take time
        )

        if analysis_response.status_code == 200:
            result = analysis_response.json()
            print("✅ LLM analysis successful!")

            # Validate response structure
            if "suggested_clusters" in result:
                clusters = result["suggested_clusters"]
                print(f"📈 Found {len(clusters)} AI-generated clusters")

                # Check cluster structure
                for i, cluster in enumerate(clusters):
                    if "name" in cluster and "question_ids" in cluster:
                        print(
                            f"   Cluster {i+1}: '{cluster['name']}' ({len(cluster['question_ids'])} questions)"
                        )
                    else:
                        print(f"   ❌ Cluster {i+1} missing required fields")

                return True
            else:
                print("❌ Response missing 'suggested_clusters' field")
                print("Response:", json.dumps(result, indent=2))
                return False

        elif analysis_response.status_code == 503:
            print("⚠️  LLM service unavailable (expected in some environments)")
            result = analysis_response.json()
            if "fallback" in result and result["fallback"]:
                print("✅ Fallback logic working correctly")
                return True
            else:
                print("❌ Fallback not triggered properly")
                return False

        else:
            print(f"❌ LLM analysis failed with status {analysis_response.status_code}")
            try:
                error = analysis_response.json()
                print("Error response:", json.dumps(error, indent=2))
            except:
                print("Error response:", analysis_response.text)
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def cleanup_server(process):
    """Clean up the server process."""
    if process:
        print("🧹 Cleaning up server process...")
        try:
            process.terminate()
            process.wait(timeout=5)
            print("✅ Server terminated successfully")
        except subprocess.TimeoutExpired:
            print("⚠️  Server didn't terminate gracefully, force killing...")
            process.kill()
        except Exception as e:
            print(f"⚠️  Error during cleanup: {e}")


def main():
    """Main test function."""
    print("🚀 Starting LLM analysis integration test...")

    # Start backend server
    server_process = start_backend_server()
    if not server_process:
        print("❌ Failed to start backend server")
        sys.exit(1)

    try:
        # Wait for server to be ready
        if not wait_for_server():
            print("❌ Server startup failed")
            sys.exit(1)

        # Test LLM analysis
        if test_llm_analysis():
            print("🎉 LLM analysis integration test PASSED!")
            sys.exit(0)
        else:
            print("❌ LLM analysis integration test FAILED!")
            sys.exit(1)

    finally:
        cleanup_server(server_process)


if __name__ == "__main__":
    main()
