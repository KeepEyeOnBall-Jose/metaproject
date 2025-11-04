# LLM Integration for Metaproject

This project now includes integration with local LLM services (Ollama and LM Studio) for simple queries and AI assistance.

## Setup

1. **Install dependencies** (in virtual environment):
   ```bash
   cd /Users/jose/metaproject
   source venv/bin/activate
   pip install requests
   ```

2. **Start your LLM services**:
   - **Ollama**: Run `ollama serve` (already running on your system)
   - **LM Studio**: Start the LM Studio application and load a model

## Available Services

Your system currently has:
- ✅ **Ollama** running with models: `gpt-oss:20b`
- ✅ **LM Studio** running with models: `openai/gpt-oss-20b`, `qwen3-vl-30b-a3b-instruct-mlx`, etc.

## Usage

### Quick Start

```python
from llm_client import query_ollama, query_lmstudio

# Simple query to Ollama
response = query_ollama("Explain quantum physics simply")
print(response)

# Simple query to LM Studio
response = query_lmstudio("Write a short poem about coding")
print(response)
```

### Advanced Usage

```python
from llm_client import LocalLLMClient

# Initialize client
client = LocalLLMClient("lmstudio")  # or "ollama"

# List available models
models = client.list_models()
print("Available models:", models)

# Query with parameters
response = client.query(
    prompt="What are the benefits of functional programming?",
    temperature=0.7,    # creativity (0.0-1.0)
    max_tokens=200      # response length
)
print(response)
```

### Integration with Question Interface

You can enhance your question interface by adding LLM-powered features:

```python
from llm_client import LocalLLMClient

def analyze_question(question_text):
    """Use LLM to analyze and improve questions"""
    client = LocalLLMClient("lmstudio")

    prompt = f"""Analyze this question and suggest improvements:
Question: {question_text}

Provide a clearer version of this question."""

    return client.query(prompt, max_tokens=100)

# Example usage
original = "how do computers work?"
improved = analyze_question(original)
print(f"Improved: {improved}")
```

## Files

- `llm_client.py` - Main client library for LLM services
- `demo_llm.py` - Demo script showing available services
- `llm_examples.py` - Code examples for integration

## Running Demos

```bash
# Test available services
source venv/bin/activate
python demo_llm.py

# Run examples
python llm_examples.py
```

## API Reference

### LocalLLMClient

- `LocalLLMClient(service, base_url)` - Initialize client
- `list_models()` - Get available models
- `query(prompt, model, temperature, max_tokens)` - Send query
- `is_available()` - Check if service is running

### Convenience Functions

- `query_ollama(prompt, model, **kwargs)` - Quick Ollama query
- `query_lmstudio(prompt, model, **kwargs)` - Quick LM Studio query
- `get_available_services()` - Check which services are running

## Troubleshooting

- **Service not available**: Make sure Ollama/LM Studio is running
- **No models**: Load a model in your LLM application first
- **Slow responses**: Large models take longer; try smaller models
- **Connection errors**: Check that services are running on expected ports (Ollama: 11434, LM Studio: 1234)