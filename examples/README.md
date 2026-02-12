# Examples: Using Universal Skills

> **🚀 GrumpiFied Enhancement** - These examples and multi-provider demonstrations are custom additions created by Grumpified-OGGVCT.

This directory contains practical examples demonstrating how to use universal skills with different LLM providers.

## 🎯 What You'll Find Here

- **Working code examples** using skills with multiple providers
- **Complete setup instructions** for each provider
- **Best practices** and common patterns
- **Troubleshooting tips** for common issues

## 📋 Prerequisites

Install the required package (Python 3.7+):
```bash
pip install openai
```

The `openai` package works with OpenRouter, Ollama, and any OpenAI-compatible API!

## 🚀 Quick Start

### 1. Choose Your Provider

| Provider | Cost | Setup Time | Best For |
|----------|------|------------|----------|
| **Ollama** | Free | 5 min | Privacy, offline, no API limits |
| **OpenRouter** | Pay-as-you-go | 2 min | Access 100+ models, flexibility |
| **Claude API** | Pay-as-you-go | 2 min | Best quality, official Claude |

### 2. Run the Demo

```bash
# See demo.py for provider setup instructions
python examples/demo.py
```

## 📖 Examples

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

All examples follow this simple pattern:

```python
from openai import OpenAI
from pathlib import Path

# 1. Load a skill (just read a text file!)
skill_path = "universal/tier-1-instruction-only/SKILL_NAME/system-prompt.md"
with open(skill_path) as f:
    system_prompt = f.read()

# 2. Connect to your chosen provider
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # or http://localhost:11434/v1 for Ollama
    api_key="YOUR_KEY"  # or "ollama" for local
)

# 3. Use the skill!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or "llama3.2" for Ollama
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your request here"}
    ]
)

print(response.choices[0].message.content)
```

That's it! The same code works with any OpenAI-compatible provider.

### Provider-Specific Examples

#### OpenRouter (Cloud)

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="sk-or-v1-..."  # Get from openrouter.ai
)

# Use any of 100+ models!
models = [
    "anthropic/claude-3.5-sonnet",     # Highest quality
    "openai/gpt-4o",                    # Fast and capable
    "meta-llama/llama-3.2-90b",        # Budget-friendly
    "google/gemini-pro-1.5",           # Good for long context
]

for model in models:
    response = client.chat.completions.create(
        model=model,
        messages=[...]
    )
    print(f"{model}: {response.choices[0].message.content[:100]}...")
```

#### Ollama (Local)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Doesn't need a real key
)

# Use any downloaded model
# Run: ollama pull llama3.2
response = client.chat.completions.create(
    model="llama3.2",
    messages=[...]
)
```

#### Claude API (Direct)

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

# Upload skill to get skill_id first
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    skills=["skill-id"],
    messages=[{"role": "user", "content": "..."}]
)
```

### Common Patterns

#### Multi-Turn Conversations

```python
messages = [
    {"role": "system", "content": system_prompt}
]

# First exchange
messages.append({"role": "user", "content": "Suggest domain names for my startup"})
response = client.chat.completions.create(model="anthropic/claude-3.5-sonnet", messages=messages)
messages.append({"role": "assistant", "content": response.choices[0].message.content})

# Follow-up
messages.append({"role": "user", "content": "Make them more creative"})
response = client.chat.completions.create(model="anthropic/claude-3.5-sonnet", messages=messages)
```

#### Error Handling

```python
from openai import OpenAIError

try:
    response = client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Your request"}
        ],
        timeout=30.0  # 30 second timeout
    )
    print(response.choices[0].message.content)
except OpenAIError as e:
    print(f"Error: {e}")
```

## 💡 Tips and Best Practices

### Choosing Models

- **High quality needed?** → Claude 3.5 Sonnet or GPT-4o
- **Cost-conscious?** → Llama 3.2 90B or Gemini Flash
- **Privacy-focused?** → Use Ollama locally
- **Speed priority?** → GPT-4o or smaller Ollama models

### Optimizing Performance

1. **Use appropriate models**: Don't use GPT-4o for simple tasks
2. **Cache system prompts**: Load skills once, reuse many times
3. **Stream responses**: Better UX for long outputs
4. **Handle errors gracefully**: Implement retries and fallbacks
5. **Monitor costs**: Track token usage

## 🐛 Troubleshooting

### "Connection refused" with Ollama

Make sure Ollama is running:
```bash
# Check status
ollama list

# If not running, start it
ollama serve
```

### "Invalid API key" with OpenRouter

Verify your key:
```bash
echo $OPENROUTER_API_KEY
# Should start with "sk-or-v1-"
```

### Skill not working as expected

1. Check you're using the right tier (Tier 2 needs tool support)
2. Verify model supports the required features
3. Try a different model to isolate the issue
4. Check the [Model Compatibility Guide](../docs/MODEL-COMPATIBILITY.md)

## 📚 More Resources

- [OpenRouter Setup Guide](../docs/OPENROUTER-SETUP.md) - Detailed OpenRouter examples
- [Ollama Setup Guide](../docs/OLLAMA-SETUP.md) - Local usage examples
- [Model Compatibility Guide](../docs/MODEL-COMPATIBILITY.md) - Model-specific tips
- [Universal Format Spec](../UNIVERSAL-FORMAT.md) - Technical details

## 🤝 Contributing

Have a useful example? Add it here with:

1. **Clear comments** explaining each step
2. **Error handling** for robustness
3. **Setup instructions** in docstring
4. **Expected output** example

Then submit a PR! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Happy coding!** 🎉
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
