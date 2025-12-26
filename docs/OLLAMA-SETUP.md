# Ollama Setup Guide

## What is Ollama?

Ollama allows you to run large language models locally on your machine or in the cloud. It provides an OpenAI-compatible API, making it work seamlessly with the universal skills in this repository.

## Installation

### macOS and Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows

Download and run the installer from [ollama.com/download](https://ollama.com/download)

### Verify Installation

```bash
ollama --version
```

## Quick Start

### 1. Download a Model

```bash
# Download popular models
ollama pull llama3.2       # Meta's Llama 3.2 (3B or 70B)
ollama pull qwen2.5        # Alibaba's Qwen 2.5
ollama pull mistral        # Mistral 7B
ollama pull granite3       # IBM's Granite 3
ollama pull phi3           # Microsoft's Phi-3
```

### 2. Test the Model

```bash
# Run interactive chat
ollama run llama3.2

# Exit with /bye or Ctrl+D
```

### 3. Start the API Server

Ollama starts automatically on installation. The API runs at:
```
http://localhost:11434
```

## Using Universal Skills with Ollama

### Python Example

```python
from openai import OpenAI

# Connect to local Ollama instance
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but unused for local Ollama
)

# Load a universal skill's system prompt
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md", "r") as f:
    system_prompt = f.read()

# Make a request
response = client.chat.completions.create(
    model="llama3.2",  # Use any model you've pulled
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "I'm building a project management tool for remote teams. Suggest domain names."}
    ]
)

print(response.choices[0].message.content)
```

### Node.js Example

```javascript
import OpenAI from 'openai';
import fs from 'fs';

// Connect to local Ollama instance
const client = new OpenAI({
  baseURL: 'http://localhost:11434/v1',
  apiKey: 'ollama',  // Required but unused
});

// Load system prompt
const systemPrompt = fs.readFileSync(
  'universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md',
  'utf8'
);

// Make a request
const response = await client.chat.completions.create({
  model: 'llama3.2',
  messages: [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: 'I'm building a project management tool for remote teams. Suggest domain names.' }
  ]
});

console.log(response.choices[0].message.content);
```

### Direct HTTP API

```bash
# Using curl
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

## Recommended Models

### For Most Skills (General Purpose)

| Model | Size | RAM Needed | Best For |
|-------|------|------------|----------|
| `llama3.2:3b` | 2GB | 4GB | Fast, lightweight tasks |
| `llama3.2` | 4.7GB | 8GB | Balanced quality/speed |
| `qwen2.5:7b` | 4.7GB | 8GB | Coding, reasoning |
| `mistral` | 4.1GB | 8GB | General purpose |
| `phi3` | 2.3GB | 4GB | Fast, efficient |

### For Complex Reasoning

| Model | Size | RAM Needed | Best For |
|-------|------|------------|----------|
| `llama3.2:70b` | 40GB | 64GB | Highest quality |
| `qwen2.5:14b` | 9GB | 16GB | Better reasoning |
| `granite3:8b` | 4.9GB | 8GB | Enterprise use |

### For Coding

| Model | Size | RAM Needed | Best For |
|-------|------|------------|----------|
| `qwen2.5-coder:7b` | 4.7GB | 8GB | Code generation |
| `codellama` | 3.8GB | 8GB | Code completion |
| `deepseek-coder-v2` | 8.9GB | 16GB | Advanced coding |

### Model Selection Guide

```bash
# List available models
ollama list

# Check model details
ollama show llama3.2

# Pull specific size variant
ollama pull llama3.2:3b     # 3 billion parameters
ollama pull llama3.2:7b     # 7 billion parameters  
ollama pull llama3.2:70b    # 70 billion parameters
```

## Performance Optimization

### 1. GPU Acceleration

Ollama automatically uses your GPU if available:
- **NVIDIA**: CUDA support built-in
- **Apple Silicon**: Metal support built-in
- **AMD**: ROCm support on Linux

Check GPU usage:
```bash
# macOS
ollama ps

# Linux with nvidia-smi
nvidia-smi
```

### 2. Model Quantization

Use quantized models for faster inference and less memory:

```bash
# Q4 quantization (4-bit, smaller, faster)
ollama pull llama3.2:7b-q4_0

# Q8 quantization (8-bit, balanced)
ollama pull llama3.2:7b-q8_0

# Full precision (larger, slower, highest quality)
ollama pull llama3.2:7b-fp16
```

### 3. Concurrent Requests

Ollama handles multiple requests efficiently:

```python
import asyncio
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

async def process_request(prompt):
    response = await client.chat.completions.create(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process multiple requests concurrently
async def main():
    tasks = [
        process_request("Question 1"),
        process_request("Question 2"),
        process_request("Question 3")
    ]
    results = await asyncio.gather(*tasks)
    return results
```

### 4. Keep Model in Memory

```bash
# Keep model loaded in memory (faster subsequent requests)
ollama run llama3.2 --keepalive 24h

# Or set default keepalive
export OLLAMA_KEEP_ALIVE=24h
```

## Tool Calling Support

Some Ollama models support OpenAI-style tool calling:

### Supported Models
- `llama3.2` (with tool calling)
- `qwen2.5:7b` (good tool support)
- `mistral` (basic tool support)

### Example with Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "What's the weather in SF?"}],
    tools=tools
)

# Check for tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        print(f"Calling: {tool_call.function.name}")
        print(f"Args: {tool_call.function.arguments}")
```

**Note**: If tool calling doesn't work, use the manual version of Tier 2 skills.

## Cloud Deployment

### Deploy on a Server

```bash
# On your server
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2

# Expose to network (be careful with security!)
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

### Access Remotely

```python
client = OpenAI(
    base_url="http://your-server-ip:11434/v1",
    api_key="ollama"
)
```

### Docker Deployment

```bash
# Pull Ollama Docker image
docker pull ollama/ollama

# Run container
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama

# Pull a model inside container
docker exec -it ollama ollama pull llama3.2
```

### With GPU Support

```bash
docker run -d \
  --gpus all \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

## Configuration

### Environment Variables

```bash
# Change host/port
export OLLAMA_HOST=0.0.0.0:11434

# Set data directory
export OLLAMA_MODELS=/path/to/models

# Number of parallel requests
export OLLAMA_NUM_PARALLEL=4

# Keep alive duration
export OLLAMA_KEEP_ALIVE=5m

# Max model loading time
export OLLAMA_LOAD_TIMEOUT=5m
```

### Model File Customization

Create custom model configurations:

```bash
# Create a Modelfile
cat > Modelfile <<EOF
FROM llama3.2

# Set temperature
PARAMETER temperature 0.7

# Set system message
SYSTEM You are a helpful coding assistant specialized in Python.

# Set context window
PARAMETER num_ctx 4096
EOF

# Create custom model
ollama create my-custom-model -f Modelfile
ollama run my-custom-model
```

## Troubleshooting

### Model Download Issues

```bash
# Check available space
df -h

# Clear unused models
ollama rm unused-model

# Re-download model
ollama pull llama3.2 --insecure  # If SSL issues
```

### Memory Issues

```bash
# Use smaller model
ollama pull llama3.2:3b

# Use quantized version
ollama pull llama3.2:7b-q4_0

# Reduce context window
# In Modelfile:
PARAMETER num_ctx 2048
```

### Port Already in Use

```bash
# Check what's using port 11434
lsof -i :11434

# Use different port
OLLAMA_HOST=127.0.0.1:11435 ollama serve
```

### Slow Responses

1. **Use GPU**: Ensure GPU drivers installed
2. **Smaller model**: Switch to 3B or 7B model
3. **Quantization**: Use Q4 quantized models
4. **Reduce context**: Lower num_ctx parameter

## Model Management

### List Downloaded Models

```bash
ollama list
```

### Remove Models

```bash
ollama rm llama3.2:70b
```

### Copy Models

```bash
ollama cp llama3.2 my-llama-backup
```

### Update Models

```bash
ollama pull llama3.2  # Re-pulls latest version
```

## Integration Examples

### Web API with Flask

```python
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    response = client.chat.completions.create(
        model="llama3.2",
        messages=data["messages"]
    )
    return jsonify({"response": response.choices[0].message.content})

if __name__ == "__main__":
    app.run(port=5000)
```

### Streamlit UI

```python
import streamlit as st
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

st.title("Ollama Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3.2",
            messages=st.session_state.messages
        )
        st.write(response.choices[0].message.content)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
```

## Best Practices

1. **Start with smaller models** (3B-7B) for testing
2. **Use quantized models** for better performance
3. **Keep models loaded** with OLLAMA_KEEP_ALIVE
4. **Monitor memory usage** with system tools
5. **Test locally** before deploying to cloud
6. **Secure your server** if exposing to network

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama Models Library](https://ollama.com/library)
- [Ollama Discord](https://discord.gg/ollama)
- [Model Benchmarks](https://ollama.com/blog/model-benchmarks)

## Next Steps

- Check [MODEL-COMPATIBILITY.md](MODEL-COMPATIBILITY.md) for skill-specific model recommendations
- Read [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) to convert your own Claude skills
- See [OPENROUTER-SETUP.md](OPENROUTER-SETUP.md) for cloud-based multi-model access
