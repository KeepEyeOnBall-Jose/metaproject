#!/usr/bin/env python3
"""
Check Ollama service status and available models.
"""

import subprocess
import sys
import json


def check_ollama_service():
    """Check if Ollama service is running."""
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            print("✅ Ollama service is running")
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:  # Header + at least one model
                print("📦 Available models:")
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if parts:
                            print(f"   - {parts[0]}")
            else:
                print("⚠️  No models installed")
            return True
        else:
            print("❌ Ollama service not responding")
            print("Error:", result.stderr.strip())
            return False

    except FileNotFoundError:
        print("❌ Ollama not installed or not in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama command timed out")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama: {e}")
        return False


def check_ollama_api():
    """Check if Ollama API is accessible."""
    try:
        import requests

        # Try to connect to Ollama API
        response = requests.get("http://localhost:11434/api/tags", timeout=5)

        if response.status_code == 200:
            print("✅ Ollama API is accessible")
            models = response.json().get("models", [])
            if models:
                print("📦 Models via API:")
                for model in models:
                    name = model.get("name", "unknown")
                    size = model.get("size", 0)
                    size_gb = size / (1024**3) if size else 0
                    print(f"   - {name} ({size_gb:.1f} GB)")
            else:
                print("⚠️  No models available via API")
            return True
        else:
            print(f"❌ Ollama API returned status {response.status_code}")
            return False

    except ImportError:
        print("⚠️  requests library not available for API check")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to Ollama API: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking Ollama API: {e}")
        return False


def main():
    """Main function."""
    print("🔍 Checking Ollama status...")

    service_ok = check_ollama_service()
    api_ok = check_ollama_api()

    if service_ok and api_ok:
        print("🎉 Ollama is fully operational!")
        sys.exit(0)
    elif service_ok:
        print("⚠️  Ollama service running but API not accessible")
        sys.exit(1)
    else:
        print("❌ Ollama is not available")
        print("\n💡 To install Ollama:")
        print("   1. Visit https://ollama.ai/download")
        print("   2. Download and install for macOS")
        print("   3. Run: ollama pull llama3.2")
        print("   4. Start Ollama service")
        sys.exit(1)


if __name__ == "__main__":
    main()
