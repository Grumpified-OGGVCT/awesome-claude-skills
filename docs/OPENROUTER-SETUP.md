# OpenRouter Setup Guide

## What is OpenRouter?

OpenRouter provides a unified API for accessing multiple AI models from different providers (OpenAI, Anthropic, Google, Meta, etc.) through a single interface. It uses OpenAI-compatible format, making it easy to work with the universal skills in this repository.

## Getting Started

### 1. Create an OpenRouter Account

1. Visit [openrouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Navigate to **Keys** in your dashboard
4. Generate a new API key

### 2. Install Required Dependencies

```bash
# Python
pip install openai  # OpenRouter uses OpenAI-compatible API

# Node.js
npm install openai
```

### 3. Basic Usage with Universal Skills

#### Python Example

```python
from openai import OpenAI

# Initialize client with OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY"
)

# Load a universal skill's system prompt
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md", "r") as f:
    system_prompt = f.read()

# Make a request
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or any supported model
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I'm building a project management tool for remote teams. Suggest domain names."}
    ]
)

print(response.choices[0].message.content)
```

#### Node.js Example

```javascript
import OpenAI from 'openai';
import fs from 'fs';

// Initialize client with OpenRouter
const client = new OpenAI({
  baseURL: 'https://openrouter.ai/api/v1',
  apiKey: process.env.OPENROUTER_API_KEY,
});

// Load a universal skill's system prompt
const systemPrompt = fs.readFileSync(
  'universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md',
  'utf8'
);

// Make a request
const response = await client.chat.completions.create({
  model: 'anthropic/claude-3.5-sonnet',
  messages: [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: 'I'm building a project management tool for remote teams. Suggest domain names.' }
  ]
});

console.log(response.choices[0].message.content);
```

### 4. Using Skills with Tool Calling (Tier 2)

For skills that include tool definitions:

```python
import json
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_API_KEY"
)

# Load system prompt and tools
with open("universal/tier-2-tool-enhanced/skill-name/system-prompt.md", "r") as f:
    system_prompt = f.read()

with open("universal/tier-2-tool-enhanced/skill-name/tools-schema.json", "r") as f:
    tools = json.load(f)

# Make a request with tools
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Your request here"}
    ],
    tools=tools
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        print(f"Tool: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
        # Execute the tool and send results back...
```

## Available Models

OpenRouter provides access to many models. Here are popular choices for different use cases:

### Recommended Models

| Model | Best For | Context | Speed | Cost |
|-------|----------|---------|-------|------|
| `anthropic/claude-3.5-sonnet` | Complex reasoning, coding | 200K | Medium | $$ |
| `openai/gpt-4o` | General purpose, fast | 128K | Fast | $$ |
| `google/gemini-pro-1.5` | Long context, multimodal | 1M | Medium | $ |
| `meta-llama/llama-3.2-90b-instruct` | Cost-effective, good quality | 128K | Fast | $ |
| `anthropic/claude-3-opus` | Highest quality, deepest reasoning | 200K | Slow | $$$ |

### Free Models (Great for Testing)

- `meta-llama/llama-3.2-3b-instruct:free`
- `google/gemini-flash-1.5:free`
- `mistralai/mistral-7b-instruct:free`

## Model Selection Tips

### For Tier 1 Skills (Instruction-Only)

Most models work well. Choose based on:
- **Budget**: Use Llama or Gemini models
- **Quality**: Use Claude 3.5 Sonnet or GPT-4o
- **Speed**: Use GPT-4o or Gemini Flash

### For Tier 2 Skills (Tool-Enhanced)

Check tool calling support:
- **Full Support**: Claude 3.5, GPT-4o, Gemini 1.5 Pro
- **Partial Support**: Some open-source models
- **Fallback**: Use manual version if tools not supported

## Cost Management

### 1. Set Usage Limits

In your OpenRouter dashboard:
- Set daily/monthly spend limits
- Enable usage alerts
- Monitor per-model costs

### 2. Use Cheaper Models First

```python
# Try cheaper model first, fallback to expensive one
models_to_try = [
    "meta-llama/llama-3.2-90b-instruct",  # Cheaper
    "anthropic/claude-3.5-sonnet"         # More expensive
]

for model in models_to_try:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000
        )
        if is_good_response(response):
            break
    except Exception as e:
        continue
```

### 3. Cache System Prompts

OpenRouter supports prompt caching for some models:

```python
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[
        {"role": "system", "content": system_prompt},  # Will be cached
        {"role": "user", "content": user_message}
    ],
    extra_headers={
        "HTTP-Referer": "https://your-site.com",  # Optional
        "X-Title": "Your App Name"  # Optional
    }
)
```

## Environment Variables

Create a `.env` file:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_APP_URL=https://your-site.com  # Optional, for rankings
OPENROUTER_APP_NAME=YourApp  # Optional, for rankings
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
```

## Advanced Features

### 1. Model Fallbacks

```python
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=messages,
    extra_body={
        "fallback": ["openai/gpt-4o", "meta-llama/llama-3.2-90b-instruct"]
    }
)
```

### 2. Provider Preferences

```python
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=messages,
    extra_body={
        "provider": {
            "order": ["Anthropic", "AWS"],  # Prefer direct Anthropic
            "allow_fallbacks": True
        }
    }
)
```

### 3. Response Streaming

```python
stream = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=messages,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end='')
```

## Troubleshooting

### Rate Limits

If you hit rate limits:
1. Add delay between requests
2. Use exponential backoff
3. Consider upgrading your plan

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def make_request_with_retry():
    return client.chat.completions.create(...)
```

### Invalid Model Names

Check available models:
```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

### Tool Calling Issues

Not all models support tool calling. Check the model's capabilities:
- Use Claude 3.5, GPT-4o, or Gemini 1.5 Pro for best tool support
- Fall back to manual instructions if tools not supported

## Best Practices

1. **Start with free models** for testing
2. **Use prompt caching** for system prompts
3. **Set token limits** to control costs
4. **Monitor usage** in dashboard
5. **Implement fallbacks** for reliability
6. **Test across models** to find the best fit

## Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter Models](https://openrouter.ai/models)
- [OpenRouter Pricing](https://openrouter.ai/models)
- [API Status](https://status.openrouter.ai)

## Next Steps

- Check out [MODEL-COMPATIBILITY.md](MODEL-COMPATIBILITY.md) for skill-specific model recommendations
- Read [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) to convert your own Claude skills
- See [OLLAMA-SETUP.md](OLLAMA-SETUP.md) for local model deployment
