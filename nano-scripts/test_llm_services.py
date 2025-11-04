#!/usr/bin/env python3
"""test_llm_services.py

Test direct connectivity to Ollama and LMStudio services.

This script tests if the LLM services are running and responding
before testing the full analysis pipeline.

Usage:
  ./test_llm_services.py
"""

import sys
import requests
import json


def test_ollama():
    """Test Ollama service connectivity."""
    try:
        print("Testing Ollama (port 11434)...")

        # Test basic connectivity
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(
                f"✓ Ollama responding. Available models: {len(models.get('models', []))}"
            )

            # Try a simple generate request
            test_payload = {
                "model": "llama2",  # Try default model
                "prompt": "Say 'Hello' in one word.",
                "stream": False,
            }

            gen_response = requests.post(
                "http://localhost:11434/api/generate", json=test_payload, timeout=10
            )

            if gen_response.status_code == 200:
                result = gen_response.json()
                response_text = result.get("response", "").strip()
                print(f"✓ Ollama generation works. Response: '{response_text}'")
                return True
            else:
                print(f"✗ Ollama generation failed: {gen_response.status_code}")
                return False
        else:
            print(f"✗ Ollama not responding: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("✗ Ollama not running (connection refused)")
        return False
    except Exception as e:
        print(f"✗ Ollama error: {e}")
        return False


def test_lmstudio():
    """Test LMStudio service connectivity."""
    try:
        print("Testing LMStudio (port 1234)...")

        # Test basic connectivity - LMStudio uses OpenAI-compatible API
        response = requests.get("http://localhost:1234/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(
                f"✓ LMStudio responding. Available models: {len(models.get('data', []))}"
            )
            if models.get("data"):
                model_names = [
                    m.get("id", "unknown") for m in models["data"][:3]
                ]  # Show first 3
                print(f"  Available models: {', '.join(model_names)}")

            # Try a simple chat completion
            test_payload = {
                "model": (
                    models["data"][0]["id"] if models.get("data") else "local-model"
                ),  # Use first available model
                "messages": [{"role": "user", "content": "Say 'Hello' in one word."}],
                "max_tokens": 10,
            }

            chat_response = requests.post(
                "http://localhost:1234/v1/chat/completions",
                json=test_payload,
                timeout=15,
            )

            if chat_response.status_code == 200:
                result = chat_response.json()
                response_text = (
                    result.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                    .strip()
                )
                print(f"✓ LMStudio chat works. Response: '{response_text}'")
                return True
            else:
                print(
                    f"✗ LMStudio chat failed: {chat_response.status_code} - {chat_response.text}"
                )
                return False
        else:
            print(f"✗ LMStudio not responding: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("✗ LMStudio not running (connection refused)")
        return False
    except Exception as e:
        print(f"✗ LMStudio error: {e}")
        return False


def main():
    print("Testing LLM Service Connectivity")
    print("=" * 40)

    ollama_ok = test_ollama()
    print()
    lmstudio_ok = test_lmstudio()

    print("\n" + "=" * 40)
    print("Summary:")
    print(f"Ollama: {'✓ Working' if ollama_ok else '✗ Not working'}")
    print(f"LMStudio: {'✓ Working' if lmstudio_ok else '✗ Not working'}")

    if ollama_ok or lmstudio_ok:
        print("\nAt least one LLM service is working.")
        print("If analysis is still failing, check the prompts or response parsing.")
    else:
        print("\nNo LLM services are working.")
        print("Start Ollama or LMStudio before testing analysis.")

    sys.exit(0 if (ollama_ok or lmstudio_ok) else 1)


if __name__ == "__main__":
    main()
