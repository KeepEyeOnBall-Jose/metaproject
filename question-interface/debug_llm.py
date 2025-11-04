#!/usr/bin/env python3
"""
Debug script to see raw LLM response for concept analysis.
"""

import sys
import subprocess
import time
import requests
import json


def start_backend_server():
    """Start the backend server in the background."""
    backend_dir = "/Users/jose/metaproject/question-interface/backend"
    python_exe = f"{backend_dir}/venv/bin/python"

    print("🔄 Starting backend server...")
    try:
        process = subprocess.Popen(
            [
                python_exe,
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
        return process
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None


def wait_for_server():
    """Wait for the server to be ready."""
    print("⏳ Waiting for server to start...")
    for attempt in range(10):
        try:
            response = requests.get("http://localhost:8000/questions", timeout=2)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except:
            pass
        time.sleep(1)
    return False


def debug_llm_response():
    """Debug the LLM response."""
    print("🔍 Debugging LLM response...")

    # Get questions with answers
    response = requests.get("http://localhost:8000/questions", timeout=5)
    questions = response.json()

    test_questions = []
    for q in questions[:2]:  # Just 2 for debugging
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

    print(f"📊 Sending {len(test_questions)} questions to LLM...")

    # Call analysis endpoint
    analysis_response = requests.post(
        "http://localhost:8000/analyze/concepts",
        json={"questions": test_questions},
        timeout=60,
    )

    print(f"📡 Response status: {analysis_response.status_code}")
    print(f"📄 Response headers: {dict(analysis_response.headers)}")

    if analysis_response.status_code == 200:
        result = analysis_response.json()
        print("📋 Full response:")
        print(json.dumps(result, indent=2))

        # Check what we got
        print("\n🔍 Analysis of response:")
        print(f"  - concepts: {len(result.get('concepts', []))} items")
        print(f"  - relationships: {len(result.get('relationships', []))} items")
        print(
            f"  - suggested_clusters: {len(result.get('suggested_clusters', []))} items"
        )

        if result.get("concepts"):
            print(f"  - First concept: {result['concepts'][0]}")

        if result.get("suggested_clusters"):
            print(f"  - First cluster: {result['suggested_clusters'][0]}")
        else:
            print("  ⚠️  No clusters generated - this might indicate LLM parsing issues")
    else:
        print("❌ Error response:")
        print(analysis_response.text)


def cleanup_server(process):
    """Clean up the server process."""
    if process:
        print("🧹 Cleaning up server process...")
        process.terminate()
        process.wait(timeout=5)
        print("✅ Server terminated successfully")


def main():
    """Main function."""
    print("🚀 Starting LLM debug session...")

    server_process = start_backend_server()
    if not server_process:
        sys.exit(1)

    try:
        if not wait_for_server():
            print("❌ Server startup failed")
            sys.exit(1)

        debug_llm_response()

    finally:
        cleanup_server(server_process)


if __name__ == "__main__":
    main()
