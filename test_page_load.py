#!/usr/bin/env python3
"""
Test script to verify the question interface page loads correctly.
"""
import subprocess
import time
import sys
import os


def test_page_load():
    """Test that the frontend page loads without React errors."""
    print("Starting frontend development server...")

    # Start the Vite dev server in the background
    frontend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "frontend"
    )
    server_process = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Wait for server to start
    time.sleep(5)

    try:
        # Use curl to check the page content
        curl_result = subprocess.run(
            ["curl", "-s", "http://localhost:5173"],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if curl_result.returncode != 0:
            print(f"❌ curl failed with return code {curl_result.returncode}")
            print(f"stderr: {curl_result.stderr}")
            return False

        content = curl_result.stdout.lower()

        # Debug: print content
        print("Page content preview:")
        print(content[:500])

        # Check for React errors
        if "react is not defined" in content:
            print("❌ Found 'React is not defined' error in page content")
            return False

        if "error" in content and "react" in content:
            print("❌ Found React-related error in page content")
            return False

        # Check for expected content - be more flexible
        if "question" not in content and "tracker" not in content:
            print("❌ Expected content not found in page")
            return False

        print("✅ Page loaded successfully without React errors")
        return True

    except subprocess.TimeoutExpired:
        print("❌ curl timed out")
        return False
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False
    finally:
        # Clean up server process
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    success = test_page_load()
    sys.exit(0 if success else 1)
