#!/usr/bin/env python3
"""
Comprehensive test script to verify the question interface works end-to-end.
This test catches CORS issues, connectivity problems, and data loading failures.
"""
import subprocess
import time
import sys
import os
import requests
import json


def test_backend_api():
    """Test backend API endpoints directly."""
    print("🧪 Testing backend API endpoints...")

    backend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "backend"
    )
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    # Test data loading
    test_cmd = [
        venv_python,
        "-c",
        """
import sys
sys.path.insert(0, '.')
from main import load_questions, get_categories
questions = load_questions()
categories = get_categories()
print(f"QUESTIONS_LOADED:{len(questions)}")
print(f"CATEGORIES_COUNT:{len(categories)}")
if questions:
    print(f"SAMPLE_QUESTION:{questions[0].question[:50]}...")
""",
    ]

    result = subprocess.run(test_cmd, cwd=backend_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Backend data loading failed: {result.stderr}")
        return False

    output_lines = result.stdout.strip().split("\n")
    questions_count = 0
    categories_count = 0

    for line in output_lines:
        if line.startswith("QUESTIONS_LOADED:"):
            questions_count = int(line.split(":")[1])
        elif line.startswith("CATEGORIES_COUNT:"):
            categories_count = int(line.split(":")[1])
        elif line.startswith("SAMPLE_QUESTION:"):
            print(f"✅ Sample question: {line.split(':', 1)[1]}")

    print(
        f"✅ Backend loaded {questions_count} questions, {categories_count} categories"
    )
    return questions_count > 0 and categories_count > 0


def test_cors_headers():
    """Test CORS headers are properly configured."""
    print("🧪 Testing CORS configuration...")

    backend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "backend"
    )
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

    # Start backend server for CORS testing
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
        # Test CORS by making a request with Origin header
        response = requests.get(
            "http://localhost:8000/questions",
            headers={"Origin": "http://0.0.0.0:5173"},
            timeout=5,
        )

        if "access-control-allow-origin" in response.headers:
            allowed = response.headers["access-control-allow-origin"]
            print(f"✅ CORS configured - allowed origin: {allowed}")
            return True
        else:
            print("❌ CORS headers missing from backend response")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ CORS test request failed: {e}")
        return False
    finally:
        backend_process.terminate()
        backend_process.wait()


def test_console_warnings():
    """Test that no console warnings appear during page load and interaction."""
    print("🖥️  Testing for console warnings...")

    # Create a temporary test to check for warnings
    test_content = """
import { test, expect } from '@playwright/test';

test('check for console warnings', async ({ page }) => {
  const warnings = [];
  const errors = [];

  page.on('console', msg => {
    if (msg.type() === 'warning') {
      warnings.push(msg.text());
    } else if (msg.type() === 'error') {
      errors.push(msg.text());
    }
  });

  await page.goto('http://0.0.0.0:5173');
  await page.waitForTimeout(5000);

  // Interact with the page
  const canvas = page.locator('canvas');
  if (await canvas.isVisible()) {
    await canvas.click();
  }

  await page.locator('li').first().waitFor();
  await page.waitForTimeout(3000);

  // Check for React key warnings
  const reactKeyWarnings = warnings.filter(w =>
    w.includes('Encountered two children with the same key')
  );

  // Check for WebGL performance warnings
  const webglWarnings = warnings.filter(w =>
    w.includes('GL Driver Message') || w.includes('GPU stall')
  );

  // These should be zero
  console.log(`React key warnings: ${reactKeyWarnings.length}`);
  console.log(`WebGL warnings: ${webglWarnings.length}`);

  // Fail if any warnings found
  if (reactKeyWarnings.length > 0 || webglWarnings.length > 0) {
    throw new Error(`Found ${reactKeyWarnings.length} React key warnings and ${webglWarnings.length} WebGL warnings`);
  }
});
"""

    test_file = os.path.join(
        os.path.dirname(__file__),
        "question-interface",
        "frontend",
        "tests",
        "warning-check.spec.js",
    )

    try:
        with open(test_file, "w") as f:
            f.write(test_content)

        # Run the test
        result = subprocess.run(
            [
                "cd",
                "question-interface/frontend",
                "&&",
                "npx",
                "playwright",
                "test",
                "warning-check.spec.js",
                "--reporter=json",
            ],
            cwd=os.path.dirname(__file__),
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            print("❌ Console warning test failed - warnings detected")
            print("STDOUT:", result.stdout[-1000:])  # Last 1000 chars
            print("STDERR:", result.stderr[-1000:])  # Last 1000 chars
            return False
        else:
            print("✅ No console warnings detected")
            return True

    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
    """Test for browser console errors using the feedback loop."""
    print("🖥️  Testing browser console for errors...")

    result = subprocess.run(
        ["python", "console_feedback_loop.py"],
        cwd=os.path.dirname(__file__),
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        print("❌ Console error check failed")
        print("STDOUT:", result.stdout[-500:])  # Last 500 chars
        print("STDERR:", result.stderr[-500:])  # Last 500 chars
        return False

    # Check if the output indicates success
    output = result.stdout
    if "✅ CONSOLE IS CLEAN" in output and "🎉 All console checks passed!" in output:
        print("✅ Browser console is clean - no errors detected")
        return True
    else:
        print("❌ Browser console errors detected")
        # Print relevant parts of the output
        lines = output.split("\n")
        for line in lines:
            if any(
                keyword in line
                for keyword in ["❌", "🚨", "Errors:", "React Errors:", "CORS Errors:"]
            ):
                print(f"   {line}")
        return False


def test_full_integration():
    print("🧪 Testing full integration (frontend + backend)...")

    backend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "backend"
    )
    frontend_dir = os.path.join(
        os.path.dirname(__file__), "question-interface", "frontend"
    )
    venv_python = os.path.join(backend_dir, "venv", "bin", "python")

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
    time.sleep(8)

    try:
        # Test backend API directly
        try:
            response = requests.get("http://localhost:8000/questions", timeout=5)
            if response.status_code != 200:
                print(f"❌ Backend API returned status {response.status_code}")
                return False

            questions_data = response.json()
            if not questions_data or len(questions_data) == 0:
                print("❌ Backend returned no questions")
                return False

            print(f"✅ Backend API returned {len(questions_data)} questions")

        except requests.exceptions.RequestException as e:
            print(f"❌ Backend API request failed: {e}")
            return False

        # Test CORS headers
        try:
            # Test preflight request
            response = requests.options(
                "http://localhost:8000/questions",
                headers={
                    "Origin": "http://0.0.0.0:5173",
                    "Access-Control-Request-Method": "GET",
                },
                timeout=5,
            )

            cors_headers = response.headers
            if "access-control-allow-origin" not in cors_headers:
                print("❌ CORS headers missing from backend response")
                return False

            allowed_origin = cors_headers.get("access-control-allow-origin")
            if allowed_origin not in ["http://0.0.0.0:5173", "*"]:
                print(f"❌ CORS origin not allowed: {allowed_origin}")
                return False

            print("✅ CORS headers properly configured")

        except requests.exceptions.RequestException as e:
            print(f"❌ CORS test failed: {e}")
            return False

        # Test frontend page loads
        try:
            response = requests.get("http://0.0.0.0:5173", timeout=5)
            if response.status_code != 200:
                print(f"❌ Frontend returned status {response.status_code}")
                return False

            content = response.text.lower()
            if "react is not defined" in content:
                print("❌ React not defined error in frontend")
                return False

            if "question" not in content and "interface" not in content:
                print("❌ Frontend content missing expected text")
                return False

            print("✅ Frontend page loads without React errors")

        except requests.exceptions.RequestException as e:
            print(f"❌ Frontend request failed: {e}")
            return False

        # Test frontend can fetch data (simulate browser request)
        try:
            # Test with proper Origin header to trigger CORS
            headers = {"Origin": "http://0.0.0.0:5173"}
            response = requests.get(
                "http://localhost:8000/questions", headers=headers, timeout=5
            )

            if response.status_code != 200:
                print(f"❌ Frontend API call failed with status {response.status_code}")
                return False

            # Check CORS headers in response
            if "access-control-allow-origin" not in response.headers:
                print("❌ CORS headers missing in API response")
                return False

            data = response.json()
            if not isinstance(data, list) or len(data) == 0:
                print("❌ API returned invalid or empty data")
                return False

            print(f"✅ Frontend can successfully fetch {len(data)} questions via API")
            return True

        except requests.exceptions.RequestException as e:
            print(f"❌ Frontend API call failed: {e}")
            return False

    finally:
        # Clean up processes
        print("Cleaning up servers...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.wait()
        frontend_process.wait()


def main():
    """Run all tests."""
    print("🚀 Running comprehensive question interface tests...\n")

    tests = [
        ("Backend API", test_backend_api),
        ("CORS Configuration", test_cors_headers),
        ("Console Warnings", test_console_warnings),
        ("Full Integration", test_full_integration),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print("=" * 50)

        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"\n{test_name}: {status}")
        except Exception as e:
            print(f"\n{test_name}: ❌ FAILED with exception: {e}")
            results.append((test_name, False))

    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print("=" * 50)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    if all_passed:
        print("\n🎉 All tests passed! The question interface is working correctly.")
        return True
    else:
        print("\n💥 Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
