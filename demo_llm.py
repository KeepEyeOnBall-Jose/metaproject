#!/usr/bin/env python3
"""
Quick demo of LLM integration with metaproject
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from llm_client import LocalLLMClient, get_available_services

def main():
    print("🤖 Metaproject LLM Integration Demo")
    print("=" * 40)

    # Check available services
    services = get_available_services()
    print(f"Ollama available: {'✅' if services['ollama'] else '❌'}")
    print(f"LM Studio available: {'✅' if services['lmstudio'] else '❌'}")

    if not any(services.values()):
        print("\n❌ No LLM services available. Please start Ollama or LM Studio.")
        return

    # Test Ollama if available
    if services['ollama']:
        print("\n🔍 Testing Ollama...")
        client = LocalLLMClient("ollama")

        print("Available models:")
        models = client.list_models()
        for model in models:
            print(f"  • {model}")

        # Use smaller model if available
        small_model = None
        for model in models:
            if "20b" in model or "7b" in model or "3b" in model:
                small_model = model
                break
        if not small_model and models:
            small_model = models[0]

        if small_model:
            print(f"\n💬 Testing with {small_model}...")
            try:
                response = client.query(
                    "Say hello and tell me what you are in one sentence.",
                    model=small_model,
                    max_tokens=50,
                    temperature=0.3
                )
                if response:
                    print(f"Response: {response.strip()}")
                else:
                    print("❌ No response received")
            except KeyboardInterrupt:
                print("\n⏹️  Query interrupted")
            except Exception as e:
                print(f"❌ Error: {e}")

    # Test LM Studio if available
    if services['lmstudio']:
        print("\n🎭 Testing LM Studio...")
        client = LocalLLMClient("lmstudio")

        print("Available models:")
        models = client.list_models()
        if models:
            for model in models:
                print(f"  • {model}")

            print("\n💬 Testing LM Studio...")
            try:
                response = client.query(
                    "Hello! What can you help me with?",
                    max_tokens=50
                )
                if response:
                    print(f"Response: {response.strip()}")
                else:
                    print("❌ No response received")
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("No models available")

if __name__ == "__main__":
    main()