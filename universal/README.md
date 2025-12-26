# Universal LLM Skills Format

This directory contains skills converted to a universal OpenAI-compatible format that works with multiple LLM providers including OpenRouter, Ollama, and direct API access.

## Why Universal Format?

The universal format enables you to:
- 🌍 **Use any model** - Claude, GPT-4, Gemini, Llama, Qwen, Mistral, and more
- 💰 **Choose your cost** - Free local models to premium cloud APIs
- 🔒 **Control privacy** - Run locally with Ollama or use cloud providers
- 🚀 **No vendor lock-in** - Switch providers without rewriting skills

## Directory Structure

```
universal/
├── tier-1-instruction-only/    # Skills that work with ANY model
│   ├── domain-name-brainstormer/
│   ├── meeting-insights-analyzer/
│   ├── raffle-winner-picker/
│   └── ...
│
├── tier-2-tool-enhanced/        # Skills with optional tool calling
│   ├── pdf/
│   └── ...
│
└── tier-3-claude-only/          # Reference-only (requires Claude features)
    └── ...
```

## Skill Tiers Explained

### Tier 1: Instruction-Only (90% of skills)
**What it is**: Pure instruction-based skills with no external tools required.

**Works with**: ANY model that supports system prompts
- ✅ All models on OpenRouter
- ✅ All models on Ollama
- ✅ Any OpenAI-compatible endpoint

**Files in each skill**:
- `system-prompt.md` - The actual instructions for the AI
- `metadata.yaml` - Skill information and requirements
- `api-example.json` - Example API call structure

**Example skills**:
- `domain-name-brainstormer` - Generate creative domain names
- `meeting-insights-analyzer` - Analyze communication patterns
- `raffle-winner-picker` - Randomly select winners

### Tier 2: Tool-Enhanced (10% of skills)
**What it is**: Skills that benefit from tool/function calling but include manual fallbacks.

**Works best with**:
- ✅ Claude 3.5 Sonnet (excellent tool support)
- ✅ GPT-4o (excellent tool support)
- ✅ Gemini 1.5 Pro (very good tool support)
- ⚠️ Llama 3.2, Qwen 2.5 (basic tool support)
- ⚠️ Other models (use manual version)

**Files in each skill**:
- `system-prompt.md` - Core instructions
- `metadata.yaml` - Skill information
- `api-example.json` - Example API call
- `tools-schema.json` - OpenAI function definitions
- `manual-version.md` - Fallback instructions without tools

**Example skills**:
- `pdf` - Extract text, fill forms, manipulate PDFs

### Tier 3: Claude-Only (Reference)
**What it is**: Skills that require Claude-specific features (Artifacts, MCP, UI elements).

**Purpose**: Kept as reference and documentation for Claude users.

**Contains**: README explaining why it's Claude-only and how to use it with Claude.

## Quick Start

### 1. Choose Your Provider

**Option A: OpenRouter (Cloud, Many Models)**
```bash
# Get API key from openrouter.ai
export OPENROUTER_API_KEY="sk-or-v1-..."
```

**Option B: Ollama (Local, Free)**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download a model
ollama pull llama3.2
```

### 2. Use a Skill

```python
from openai import OpenAI

# Connect to your chosen provider
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # or http://localhost:11434/v1 for Ollama
    api_key=os.getenv("OPENROUTER_API_KEY")  # or "ollama" for local
)

# Load a skill
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    system_prompt = f.read()

# Use it!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or "llama3.2" for Ollama
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Suggest domain names for an AI-powered task manager"}
    ]
)

print(response.choices[0].message.content)
```

### 3. With Tool Calling (Tier 2)

```python
import json

# Load skill and tools
with open("universal/tier-2-tool-enhanced/pdf/system-prompt.md") as f:
    system_prompt = f.read()

with open("universal/tier-2-tool-enhanced/pdf/tools-schema.json") as f:
    tools = json.load(f)

# Use with a model that supports tools
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Extract text from document.pdf"}
    ],
    tools=tools
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        print(f"Tool: {tool_call.function.name}")
        print(f"Args: {tool_call.function.arguments}")
        # Execute the tool and send results back...
```

## File Formats

### system-prompt.md
The core instructions that guide the AI's behavior. Written in clear markdown with:
- Task description
- When to use the skill
- Step-by-step instructions
- Examples and edge cases
- Best practices

### metadata.yaml
Skill metadata including:
```yaml
name: skill-name
description: What this skill does
tier: 1  # or 2, or 3
version: "1.0"
source:
  original_path: path/to/original/skill
  last_sync: 2025-12-26
requirements:
  tool_calling: false
  min_context_window: 4096
compatibility:
  tested_providers: [openrouter, ollama]
  tested_models: [llama3.2, qwen2.5]
  recommended_models: [anthropic/claude-3.5-sonnet]
```

### api-example.json
Example API call structure:
```json
{
  "model": "MODEL_NAME_HERE",
  "messages": [
    {"role": "system", "content": "[Content from system-prompt.md]"},
    {"role": "user", "content": "USER_REQUEST_HERE"}
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

### tools-schema.json (Tier 2 only)
OpenAI-compatible function definitions:
```json
[
  {
    "type": "function",
    "function": {
      "name": "function_name",
      "description": "What this function does",
      "parameters": {
        "type": "object",
        "properties": {
          "param_name": {
            "type": "string",
            "description": "Parameter description"
          }
        },
        "required": ["param_name"]
      }
    }
  }
]
```

## Model Recommendations

### Best Overall Quality
- **Claude 3.5 Sonnet** (OpenRouter) - Best instruction following, reasoning
- **GPT-4o** (OpenRouter) - Fast, high quality, good tool support

### Best for Budget
- **Llama 3.2 90B** (OpenRouter) - $0.20/$0.20 per 1M tokens
- **Gemini Pro 1.5** (OpenRouter) - $1.25/$5 per 1M tokens
- **Llama 3.2 7B** (Ollama) - Free, local

### Best for Privacy
- **Llama 3.2** (Ollama) - 100% local, no data sent
- **Qwen 2.5** (Ollama) - 100% local, good for coding
- **Mistral** (Ollama) - 100% local, efficient

### Best for Speed
- **GPT-4o** (OpenRouter) - ~120 tokens/sec
- **Gemini Flash 1.5** (OpenRouter) - ~100 tokens/sec
- **Llama 3.2:3b** (Ollama) - ~50-100 tokens/sec on good hardware

See [docs/MODEL-COMPATIBILITY.md](../docs/MODEL-COMPATIBILITY.md) for detailed comparisons.

## Testing Skills

### Test a Skill Locally
```bash
# Quick test with Ollama
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --quick

# Test with multiple models
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --providers openrouter ollama \
  --models "openrouter:claude-3.5,ollama:llama3.2"
```

### Validate Skill Format
```bash
# Validate single skill
python tools/validate.py universal/tier-1-instruction-only/domain-name-brainstormer

# Validate all skills
python tools/validate.py --all
```

## Converting Your Own Skills

### From Claude Skills
```bash
# Convert a single skill
python tools/convert.py --skill your-skill-name

# Convert all skills
python tools/convert.py --all
```

See [docs/MIGRATION-GUIDE.md](../docs/MIGRATION-GUIDE.md) for detailed instructions.

## Staying Updated

The universal format is derived from the original skills and can be regenerated at any time:

```bash
# Sync with upstream repository
./tools/sync-upstream.sh

# Regenerate universal format
python tools/convert.py --all
```

This ensures backward compatibility while staying current with the latest skills from the upstream repository.

## Documentation

- **[OpenRouter Setup](../docs/OPENROUTER-SETUP.md)** - Configure OpenRouter for multi-model access
- **[Ollama Setup](../docs/OLLAMA-SETUP.md)** - Install and run models locally
- **[Model Compatibility](../docs/MODEL-COMPATIBILITY.md)** - Which models work best
- **[Migration Guide](../docs/MIGRATION-GUIDE.md)** - Convert your own skills

## Contributing

When contributing converted skills:

1. **Test thoroughly** with multiple models
2. **Document compatibility** in metadata.yaml
3. **Provide clear examples** in api-example.json
4. **Include manual fallbacks** for Tier 2 skills
5. **Validate** with `python tools/validate.py`

## Support

- Issues? Check the [Model Compatibility Guide](../docs/MODEL-COMPATIBILITY.md)
- Questions? Open an issue on GitHub
- Want to contribute? See [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

Same as the main repository - Apache 2.0. Individual skills may have their own licenses.
