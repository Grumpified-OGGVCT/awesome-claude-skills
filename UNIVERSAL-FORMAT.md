# Universal LLM Skills Format

> **🚀 GrumpiFied Enhancement** - The entire universal format system is a custom addition created by Grumpified-OGGVCT, enabling skills to work with ANY LLM provider beyond just Claude.

## Overview

This repository now includes a universal format that makes all Claude skills compatible with **any OpenAI-compatible LLM provider**. This means you can use the same skills with OpenRouter, Ollama, or any direct API that follows the OpenAI standard.

## 🎯 Key Benefits

### 1. No Vendor Lock-In
- Use skills with Claude, GPT-4, Gemini, Llama, Qwen, Mistral, and more
- Switch providers anytime without rewriting skills
- Future-proof your workflow

### 2. Cost Flexibility
- **Free**: Run models locally with Ollama
- **Budget**: Use cost-effective models on OpenRouter ($0.20/1M tokens)
- **Premium**: Access best models like Claude 3.5 Sonnet when needed

### 3. Privacy Control
- **100% Local**: Use Ollama for complete privacy
- **Cloud**: Use OpenRouter when convenience matters
- Your choice, your data

### 4. Backward Compatible
- Original Claude skills remain untouched
- Universal format is derived, not replacing
- Easy to sync with upstream updates
- Both formats coexist peacefully

## 📁 Structure

```
awesome-claude-skills/
├── [original-skills]/        ← Unchanged! Still works with Claude
│
├── universal/                 ← NEW: Works with any provider
│   ├── tier-1-instruction-only/    # 90% of skills, works with ANY model
│   ├── tier-2-tool-enhanced/       # 10% of skills, works best with tool-calling models
│   └── tier-3-claude-only/         # Reference for Claude-specific features
│
├── docs/                      ← NEW: Setup & compatibility guides
│   ├── OPENROUTER-SETUP.md
│   ├── OLLAMA-SETUP.md
│   ├── MODEL-COMPATIBILITY.md
│   └── MIGRATION-GUIDE.md
│
├── tools/                     ← NEW: Automation tools
│   ├── convert.py            # Convert skills to universal format
│   ├── validate.py           # Validate conversions
│   ├── sync-upstream.sh      # Sync with ComposioHQ/awesome-claude-skills
│   └── model-tester.py       # Test across providers
│
└── examples/                  ← NEW: Working examples
    ├── demo.py               # Multi-provider demo
    └── README.md             # Usage patterns
```

## 🚀 Quick Start

### Option A: OpenRouter (Cloud, 100+ Models)

1. **Get API key** at [openrouter.ai](https://openrouter.ai)

2. **Use a skill:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_KEY"
)

# Load skill
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    prompt = f.read()

# Use it!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or any model!
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Suggest domain names for my AI startup"}
    ]
)
```

### Option B: Ollama (Local, Free, Private)

1. **Install Ollama:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

2. **Use the same skill:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Same skill, different provider!
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    prompt = f.read()

response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": "Suggest domain names for my AI startup"}
    ]
)
```

### Option C: IDE Integration (VS Code, Cursor, etc.)

Skills work seamlessly with AI coding assistants:

**1. Cursor:**
```bash
# Copy skill to Cursor's prompts directory
mkdir -p ~/.cursor/prompts/
cp universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md \
   ~/.cursor/prompts/brainstorm-domains.md
```

Then use Cursor's AI with the skill automatically loaded.

**2. Continue (VS Code):**
```bash
# Add to Continue config
mkdir -p ~/.continue/prompts/
cp universal/tier-1-instruction-only/YOUR_SKILL/system-prompt.md \
   ~/.continue/prompts/
```

**3. Cline (VS Code):**
- Open Cline settings
- Navigate to "Custom Instructions"  
- Paste the content from `system-prompt.md`

**4. Windsurf / Other IDEs:**
- Check your IDE's AI assistant documentation
- Look for "custom prompts" or "custom instructions" settings
- Copy the `system-prompt.md` content there

**Benefits:**
- ✅ Skills available in your coding environment
- ✅ Context-aware: AI can see your code
- ✅ No API calls needed if IDE handles them
- ✅ Works with IDE's choice of model

## 💻 IDE Compatibility

Universal format skills work with these AI coding assistants:

| IDE / Tool | Integration Method | Notes |
|------------|-------------------|-------|
| **Cursor** | Copy to `~/.cursor/prompts/` | Native AI integration |
| **VS Code + Continue** | Add to Continue config | Supports multiple providers |
| **VS Code + Cline** | Custom instructions | Full context awareness |
| **Windsurf** | Custom prompts | Codeium-powered |
| **JetBrains + AI Assistant** | Custom prompts | Works with IntelliJ, PyCharm, etc. |
| **Zed** | System prompts | Emerging support |
| **Any IDE** | Manual paste | Copy system-prompt.md content |

## 📊 Skill Tiers

### Tier 1: Instruction-Only (90%)
**What**: Pure instruction-based skills  
**Works with**: ANY model  
**Examples**: domain-name-brainstormer, meeting-insights-analyzer, brainstorming

Files in each skill:
- `system-prompt.md` - Instructions for the AI
- `metadata.yaml` - Skill information
- `api-example.json` - Usage template

### Tier 2: Tool-Enhanced (10%)
**What**: Skills with optional tool calling  
**Works best with**: Claude 3.5, GPT-4o, Gemini 1.5 Pro  
**Fallback**: Manual version for all models  
**Examples**: PDF editor, file organizer

Additional files:
- `tools-schema.json` - Function definitions
- `manual-version.md` - Fallback instructions

### Tier 3: Claude-Only (Reference)
**What**: Requires Claude Artifacts or MCP  
**Purpose**: Reference documentation  
**Examples**: Canvas design, artifacts builder

## 🛠️ Tools

### Convert Skills
```bash
# Convert all skills
python tools/convert.py --all

# Convert specific skill
python tools/convert.py --skill domain-name-brainstormer

# Dry run (preview only)
python tools/convert.py --all --dry-run
```

### Validate Format
```bash
# Validate all conversions
python tools/validate.py --all

# Validate specific skill
python tools/validate.py universal/tier-1-instruction-only/domain-name-brainstormer
```

### Sync Upstream
```bash
# Pull latest from ComposioHQ/awesome-claude-skills and reconvert
./tools/sync-upstream.sh
```

### Test Models
```bash
# Quick test with Ollama
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --quick

# Test with multiple providers
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --providers openrouter ollama
```

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [OpenRouter Setup](docs/OPENROUTER-SETUP.md) | How to use OpenRouter with 100+ models |
| [Ollama Setup](docs/OLLAMA-SETUP.md) | Run models locally (free & private) |
| [Model Compatibility](docs/MODEL-COMPATIBILITY.md) | Which models work best for each skill |
| [Migration Guide](docs/MIGRATION-GUIDE.md) | Convert your own skills |
| [Universal README](universal/README.md) | Detailed format specification |

## 🎓 Examples

See [`examples/`](examples/) directory:
- `demo.py` - Working multi-provider demo
- `README.md` - Usage patterns and recipes

Run the demo:
```bash
python examples/demo.py
```

## 🌐 Real-World Usage Scenarios

### Scenario 1: Developer Using Multiple IDEs

**Challenge**: Work with Cursor for web dev, VS Code for Python, and sometimes use Claude.ai for quick tasks.

**Solution**: Universal format skills work everywhere!

```bash
# One-time setup
# Copy skill to Cursor
cp universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md \
   ~/.cursor/prompts/

# Copy to VS Code Continue
cp universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md \
   ~/.continue/prompts/

# For Claude.ai, just upload the original SKILL.md
```

Now the same skill works in:
- ✅ Cursor with Claude or GPT-4
- ✅ VS Code with any model Continue supports
- ✅ Claude.ai web interface
- ✅ Direct API calls with any provider

### Scenario 2: Cost-Conscious Startup

**Challenge**: Need AI assistance but can't afford premium API costs.

**Solution**: Mix and match based on task complexity!

```python
from openai import OpenAI

# Use cheap model for simple tasks
budget_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_KEY"
)

# Load skill once
with open("universal/tier-1-instruction-only/lead-research-assistant/system-prompt.md") as f:
    skill = f.read()

# Use Llama for bulk work ($0.20/1M tokens)
for lead in leads:
    response = budget_client.chat.completions.create(
        model="meta-llama/llama-3.2-90b",
        messages=[{"role": "system", "content": skill}, 
                  {"role": "user", "content": f"Research {lead}"}]
    )
    
# Switch to Claude for final review ($3/1M tokens, but worth it for quality)
premium_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_KEY"
)
final = premium_client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "system", "content": skill},
              {"role": "user", "content": "Review and refine these leads..."}]
)
```

**Savings**: ~90% cost reduction by using budget models for bulk work!

### Scenario 3: Privacy-Sensitive Company

**Challenge**: Can't send data to external APIs due to compliance requirements.

**Solution**: Use Ollama for 100% local processing!

```python
from openai import OpenAI

# 100% local - data never leaves your machine
local_client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # No real key needed
)

# Same skills, complete privacy
with open("universal/tier-1-instruction-only/meeting-insights-analyzer/system-prompt.md") as f:
    skill = f.read()

# Process sensitive meeting transcripts locally
response = local_client.chat.completions.create(
    model="llama3.2",  # Running on your hardware
    messages=[
        {"role": "system", "content": skill},
        {"role": "user", "content": confidential_meeting_transcript}
    ]
)
```

**Benefits**:
- ✅ No data sent to external servers
- ✅ No API costs
- ✅ Works offline
- ✅ Full compliance with data policies

### Scenario 4: Experimenting with Latest Models

**Challenge**: Want to try new models as they're released without rewriting skills.

**Solution**: Skills work with any new OpenAI-compatible model!

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_KEY"
)

# Load skill once
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    skill = f.read()

# Try different models with ZERO code changes
models_to_test = [
    "anthropic/claude-3.5-sonnet",      # Latest Claude
    "openai/gpt-4o",                    # Latest GPT
    "google/gemini-pro-1.5",            # Latest Gemini
    "meta-llama/llama-3.2-90b",         # Latest Llama
    "mistralai/mistral-large",          # Latest Mistral
    "qwen/qwen-2.5-72b",               # Latest Qwen
]

results = {}
for model in models_to_test:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": skill},
                  {"role": "user", "content": "Suggest domains for my AI startup"}]
    )
    results[model] = response.choices[0].message.content

# Compare outputs to find best model for your use case
```

**Result**: Test 6 different models without changing skill code!

### Scenario 5: Team Using Different Tools

**Challenge**: Team members use different tools - some use Cursor, some use VS Code, some prefer Claude.ai.

**Solution**: Everyone uses the same skills, their own way!

**Team Member A (Cursor user):**
- Skills in `~/.cursor/prompts/`
- Uses Cursor's built-in AI (their choice of model)

**Team Member B (VS Code + Continue):**
- Skills in `~/.continue/prompts/`
- Uses Continue with OpenRouter (access to 100+ models)

**Team Member C (Claude.ai):**
- Uploads SKILL.md files to Claude.ai
- Uses web interface

**Team Member D (API Integration):**
- Integrates skills into internal tools via OpenAI-compatible API
- Uses whatever model the company prefers

**Result**: Same skills, same quality, different preferences - all supported!

## 🔄 Maintaining Backward Compatibility

The universal format is **derived** from original skills:

1. **Original skills** stay unchanged (in repo root)
2. **Universal format** is generated (in `universal/`)
3. **Sync upstream** with `./tools/sync-upstream.sh`
4. **Regenerate** with `python tools/convert.py --all`

This ensures:
- ✅ No merge conflicts with upstream
- ✅ Both formats stay in sync
- ✅ Easy to pull updates from ComposioHQ/awesome-claude-skills
- ✅ Can contribute back to upstream

## 🌟 Model Recommendations

### Best Overall
- **Claude 3.5 Sonnet** (OpenRouter) - Highest quality
- **GPT-4o** (OpenRouter) - Fast and high quality

### Best Budget
- **Llama 3.2 90B** (OpenRouter) - $0.20/1M tokens
- **Llama 3.2 7B** (Ollama) - Free, local

### Best Privacy
- **Llama 3.2** (Ollama) - 100% local
- **Qwen 2.5** (Ollama) - 100% local, good for coding

### Best Speed
- **GPT-4o** (OpenRouter) - ~120 tokens/sec
- **Llama 3.2:3b** (Ollama) - ~50-100 tokens/sec

See [MODEL-COMPATIBILITY.md](docs/MODEL-COMPATIBILITY.md) for details.

## 🤝 Contributing

When contributing universal skills:

1. Test with multiple models
2. Validate with `python tools/validate.py`
3. Document compatibility in `metadata.yaml`
4. Provide examples in `api-example.json`
5. Include manual fallbacks for Tier 2

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

Apache 2.0 - Same as the main repository.

## 🙏 Acknowledgments

- Original automation skills from [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- Additional skills from [Anthropic Skills Repository](https://github.com/anthropics/skills)
- Universal format design inspired by OpenAI's API standard
- Community feedback on provider compatibility

## 📞 Support

- **Questions?** Open an issue
- **Found a bug?** Report it on GitHub  
- **Want to contribute?** PRs welcome!

---

**Made with ❤️ to make AI skills accessible to everyone, regardless of their LLM provider choice.**
