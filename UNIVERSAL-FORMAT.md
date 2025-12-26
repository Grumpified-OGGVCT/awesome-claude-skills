# Universal LLM Skills Format

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
│   ├── sync-upstream.sh      # Sync with anthropics/skills
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
# Pull latest from anthropics/skills and reconvert
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

## 🔄 Maintaining Backward Compatibility

The universal format is **derived** from original skills:

1. **Original skills** stay unchanged (in repo root)
2. **Universal format** is generated (in `universal/`)
3. **Sync upstream** with `./tools/sync-upstream.sh`
4. **Regenerate** with `python tools/convert.py --all`

This ensures:
- ✅ No merge conflicts with upstream
- ✅ Both formats stay in sync
- ✅ Easy to pull updates from anthropics/skills
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

- Original skills from [anthropics/skills](https://github.com/anthropics/skills)
- Universal format design inspired by OpenAI's API standard
- Community feedback on provider compatibility

## 📞 Support

- **Questions?** Open an issue
- **Found a bug?** Report it on GitHub  
- **Want to contribute?** PRs welcome!

---

**Made with ❤️ to make AI skills accessible to everyone, regardless of their LLM provider choice.**
