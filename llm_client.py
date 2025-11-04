"""
Local LLM Integration for Metaproject
Provides easy access to Ollama and LM Studio APIs
"""

import requests
import json
from typing import Optional, Dict, Any


class LocalLLMClient:
    """Client for interacting with local LLM services (Ollama and LM Studio)"""

    def __init__(self, service: str = "ollama", base_url: Optional[str] = None):
        """
        Initialize the client

        Args:
            service: 'ollama' or 'lmstudio'
            base_url: Custom base URL (optional)
        """
        self.service = service.lower()

        if base_url:
            self.base_url = base_url.rstrip('/')
        elif self.service == "ollama":
            self.base_url = "http://localhost:11434"
        elif self.service == "lmstudio":
            self.base_url = "http://localhost:1234"
        else:
            raise ValueError("Service must be 'ollama' or 'lmstudio'")

    def list_models(self) -> list:
        """List available models"""
        try:
            if self.service == "ollama":
                response = requests.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            elif self.service == "lmstudio":
                response = requests.get(f"{self.base_url}/v1/models")
                response.raise_for_status()
                data = response.json()
                return [model['id'] for model in data.get('data', [])]
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {self.service}: {e}")
            return []

    def query(self, prompt: str, model: str = "", temperature: float = 0.7,
              max_tokens: int = 1000) -> Optional[str]:
        """
        Send a query to the LLM

        Args:
            prompt: The text prompt to send
            model: Model name (required for Ollama, optional for LM Studio)
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response text or None if error
        """
        try:
            if self.service == "ollama":
                if not model:
                    # Use first available model if none specified
                    models = self.list_models()
                    if not models:
                        print("No models available")
                        return None
                    model = models[0]
                    print(f"Using model: {model}")

                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_predict": max_tokens
                    }
                }
                response = requests.post(f"{self.base_url}/api/generate", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get('response', '')

            elif self.service == "lmstudio":
                payload = {
                    "model": model or "local-model",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
                response = requests.post(f"{self.base_url}/v1/chat/completions", json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get('choices', [{}])[0].get('message', {}).get('content', '')

        except requests.exceptions.RequestException as e:
            print(f"Error querying {self.service}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing response from {self.service}: {e}")
            return None

    def is_available(self) -> bool:
        """Check if the service is available"""
        try:
            if self.service == "ollama":
                response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            elif self.service == "lmstudio":
                response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False


# Convenience functions
def query_ollama(prompt: str, model: str = "", **kwargs) -> Optional[str]:
    """Quick function to query Ollama"""
    client = LocalLLMClient("ollama")
    return client.query(prompt, model, **kwargs)


def query_lmstudio(prompt: str, model: str = "", **kwargs) -> Optional[str]:
    """Quick function to query LM Studio"""
    client = LocalLLMClient("lmstudio")
    return client.query(prompt, model, **kwargs)


def get_available_services() -> Dict[str, bool]:
    """Check which services are available"""
    ollama = LocalLLMClient("ollama").is_available()
    lmstudio = LocalLLMClient("lmstudio").is_available()
    return {
        "ollama": ollama,
        "lmstudio": lmstudio
    }


if __name__ == "__main__":
    # Example usage
    print("Checking available services...")
    services = get_available_services()
    print(f"Ollama available: {services['ollama']}")
    print(f"LM Studio available: {services['lmstudio']}")

    if services['ollama']:
        print("\nOllama models:")
        client = LocalLLMClient("ollama")
        models = client.list_models()
        for model in models:
            print(f"  - {model}")

        print("\nTesting Ollama query...")
        response = client.query("Hello! Can you tell me a short joke?", max_tokens=100)
        if response:
            print(f"Response: {response}")

    if services['lmstudio']:
        print("\nLM Studio models:")
        client = LocalLLMClient("lmstudio")
        models = client.list_models()
        for model in models:
            print(f"  - {model}")

        print("\nTesting LM Studio query...")
        response = client.query("Hello! Can you tell me a short joke?", max_tokens=100)
        if response:
            print(f"Response: {response}")