# Examples: Using Universal Skills

This directory contains practical examples demonstrating how to use universal skills with different LLM providers.

## Prerequisites

Install the required package:
```bash
pip install openai
```

## Examples

### demo.py - Multi-Provider Demo

Demonstrates using the same skill with both OpenRouter and Ollama.

**Run it:**
```bash
python examples/demo.py
```

**What it does:**
- Loads a universal skill (domain-name-brainstormer)
- Tests it with OpenRouter (cloud, Claude 3.5 Sonnet)
- Tests it with Ollama (local, Llama 3.2)
- Shows that the same skill works with both!

**Setup:**

For OpenRouter:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

For Ollama:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download a model
ollama pull llama3.2
```

## Creating Your Own Examples

### Basic Pattern

```python
from openai import OpenAI
from pathlib import Path

# 1. Load a skill
with open("universal/tier-1-instruction-only/SKILL_NAME/system-prompt.md") as f:
    system_prompt = f.read()

# 2. Choose provider
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # or http://localhost:11434/v1
    api_key="YOUR_KEY"
)

# 3. Use it!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or "llama3.2"
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your request"}
    ]
)

print(response.choices[0].message.content)
```

### With Streaming

```python
stream = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your request"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='', flush=True)
```

### With Tool Calling (Tier 2 Skills)

```python
import json

# Load skill and tools
with open("universal/tier-2-tool-enhanced/SKILL/system-prompt.md") as f:
    system_prompt = f.read()

with open("universal/tier-2-tool-enhanced/SKILL/tools-schema.json") as f:
    tools = json.load(f)

# Use with tool support
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your request"}
    ],
    tools=tools
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        # Execute your function here
        result = execute_tool(function_name, arguments)
        # Send result back to model...
```

## More Examples

Want to see more? Check out:
- [OpenRouter Setup Guide](../docs/OPENROUTER-SETUP.md) - Detailed examples
- [Ollama Setup Guide](../docs/OLLAMA-SETUP.md) - Local usage examples
- [Model Compatibility Guide](../docs/MODEL-COMPATIBILITY.md) - Model-specific tips

## Contributing

Have a useful example? Add it here with:
1. Clear comments
2. Error handling
3. Setup instructions
4. Expected output

Then submit a PR!
