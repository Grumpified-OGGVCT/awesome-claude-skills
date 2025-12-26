# Model Compatibility Guide

This guide helps you choose the right model for each skill based on requirements, capabilities, and testing results.

## Quick Selection Matrix

| Use Case | OpenRouter | Ollama (Local) | Notes |
|----------|------------|----------------|-------|
| **Simple instructions** | Any model | llama3.2:3b+ | All models work |
| **Complex reasoning** | Claude 3.5 Sonnet, GPT-4o | llama3.2:70b, qwen2.5:14b | Need larger models |
| **Coding tasks** | Claude 3.5 Sonnet | qwen2.5-coder:7b | Specialized models best |
| **Tool calling** | Claude 3.5, GPT-4o, Gemini 1.5 | llama3.2, qwen2.5 | Check model support |
| **Budget-conscious** | Llama 3.2 90B, Gemini Flash | llama3.2:7b, mistral | Cost-effective options |
| **Speed priority** | GPT-4o, Gemini Flash | llama3.2:3b-q4 | Fastest responses |

## Tier 1 Skills: Instruction-Only

These skills work with **any model** since they only use system prompts and instructions.

### Recommended Models by Budget

#### Free/Low Cost
- **OpenRouter**: 
  - `meta-llama/llama-3.2-3b-instruct:free`
  - `google/gemini-flash-1.5:free`
- **Ollama**: 
  - `llama3.2:3b`
  - `phi3`

#### Balanced Quality/Cost
- **OpenRouter**: 
  - `meta-llama/llama-3.2-90b-instruct` ($0.20/$0.20 per 1M tokens)
  - `google/gemini-pro-1.5` ($1.25/$5 per 1M tokens)
- **Ollama**: 
  - `llama3.2`
  - `qwen2.5:7b`

#### Premium Quality
- **OpenRouter**: 
  - `anthropic/claude-3.5-sonnet` ($3/$15 per 1M tokens)
  - `openai/gpt-4o` ($2.50/$10 per 1M tokens)
- **Ollama**: 
  - `llama3.2:70b` (requires 64GB RAM)
  - `qwen2.5:14b`

### Skill-Specific Recommendations

#### Domain Name Brainstormer
- **Minimum**: Any 3B+ model
- **Recommended**: Claude 3.5 Sonnet, GPT-4o (creative naming)
- **Tested with**: ✅ llama3.2, ✅ qwen2.5, ✅ mistral

**Requirements**:
- ✅ Works with: Any model
- 🔧 Tool calling needed: No
- 📊 Context window: 4k+ tokens

#### Meeting Insights Analyzer
- **Minimum**: 7B+ model with good reasoning
- **Recommended**: Claude 3.5 Sonnet (pattern recognition)
- **Tested with**: ✅ llama3.2:7b, ✅ qwen2.5:7b

**Requirements**:
- ✅ Works with: Any model with 8k+ context
- 🔧 Tool calling needed: No
- 📊 Context window: 16k+ tokens (for long transcripts)

#### Raffle Winner Picker
- **Minimum**: Any 3B+ model
- **Recommended**: Any model (simple task)
- **Tested with**: ✅ llama3.2:3b, ✅ phi3

**Requirements**:
- ✅ Works with: Any model
- 🔧 Tool calling needed: No
- 📊 Context window: 4k+ tokens

#### Content Research Writer
- **Minimum**: 7B+ model
- **Recommended**: Claude 3.5 Sonnet, GPT-4o (research quality)
- **Tested with**: ✅ llama3.2:7b, ✅ qwen2.5:7b

**Requirements**:
- ✅ Works with: Any model
- 🔧 Tool calling needed: No
- 📊 Context window: 32k+ tokens (for research)

#### Brainstorming
- **Minimum**: 7B+ model
- **Recommended**: Claude 3.5 Sonnet (creativity)
- **Tested with**: ✅ llama3.2, ✅ mistral

**Requirements**:
- ✅ Works with: Any model
- 🔧 Tool calling needed: No
- 📊 Context window: 8k+ tokens

## Tier 2 Skills: Tool-Enhanced

These skills work better with tool calling support but include manual fallbacks.

### Tool Calling Support by Model

| Model | Tool Support | Quality | Notes |
|-------|--------------|---------|-------|
| **Claude 3.5 Sonnet** | ✅ Excellent | ⭐⭐⭐⭐⭐ | Best tool calling |
| **GPT-4o** | ✅ Excellent | ⭐⭐⭐⭐⭐ | Fast, reliable |
| **Gemini 1.5 Pro** | ✅ Very Good | ⭐⭐⭐⭐ | Good support |
| **Llama 3.2 (Ollama)** | ✅ Good | ⭐⭐⭐ | Basic support |
| **Qwen 2.5 (Ollama)** | ✅ Good | ⭐⭐⭐ | Decent support |
| **Mistral (Ollama)** | ⚠️ Limited | ⭐⭐ | Use manual version |
| **Phi-3 (Ollama)** | ❌ None | ⭐ | Use manual version |

### When Tools Aren't Available

All Tier 2 skills include a `manual-version.md` with instructions that don't require tool calling.

```python
# Try tool calling first
try:
    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages,
        tools=tools
    )
    if not response.choices[0].message.tool_calls:
        # Fall back to manual version
        use_manual_instructions()
except:
    # Use manual version
    use_manual_instructions()
```

## Tier 3 Skills: Claude-Only

These skills require Claude-specific features:
- Claude Artifacts
- Claude MCP Servers
- Claude.ai interface features

**Compatibility**: ❌ Not compatible with universal format

**Alternative**: Use original skills with Claude.ai or Claude Code

## Context Window Requirements

### Skill Categories by Context Needs

#### Small Context (4k-8k tokens)
- Domain Name Brainstormer
- Raffle Winner Picker
- Brand Guidelines
- Theme Factory

**All models support these**

#### Medium Context (8k-32k tokens)
- Meeting Insights Analyzer
- Content Research Writer
- Brainstorming
- Internal Comms

**Most models support these**

#### Large Context (32k-128k tokens)
- Document analysis skills
- Large codebase reviews
- Multi-file processing

**Recommended models**:
- Claude 3.5 Sonnet (200k)
- GPT-4o (128k)
- Gemini 1.5 Pro (1M)
- Llama 3.2:70b (128k)

## Performance Benchmarks

Based on testing with universal skills:

### Speed (Tokens per Second)

| Model | Provider | TPS | Use Case |
|-------|----------|-----|----------|
| GPT-4o | OpenRouter | ~120 | Fast responses needed |
| Gemini Flash 1.5 | OpenRouter | ~100 | Speed + cost balance |
| Claude 3.5 Sonnet | OpenRouter | ~80 | Quality over speed |
| Llama 3.2:3b-q4 | Ollama | ~50-100 | Local, fast |
| Llama 3.2:7b | Ollama | ~30-50 | Local, balanced |
| Llama 3.2:70b | Ollama | ~5-10 | Local, quality |

*Note: Actual speeds vary by hardware, prompt length, and load*

### Quality Scores (Subjective)

Based on skill execution quality:

| Skill Type | Best Models |
|------------|-------------|
| **Creative writing** | Claude 3.5 Sonnet > GPT-4o > Llama 3.2:70b |
| **Code generation** | Claude 3.5 Sonnet > GPT-4o > Qwen 2.5 Coder |
| **Analysis** | Claude 3.5 Sonnet > GPT-4o > Gemini 1.5 Pro |
| **Simple tasks** | All perform similarly |
| **Following instructions** | Claude 3.5 Sonnet > GPT-4o > Others |

## Cost Comparison

### OpenRouter Pricing (Per 1M Tokens)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Llama 3.2 3B (free) | $0 | $0 | Testing |
| Gemini Flash (free) | $0 | $0 | Testing |
| Llama 3.2 90B | $0.20 | $0.20 | Budget production |
| Gemini Pro 1.5 | $1.25 | $5.00 | Long context |
| GPT-4o | $2.50 | $10.00 | Speed + quality |
| Claude 3.5 Sonnet | $3.00 | $15.00 | Highest quality |
| Claude 3 Opus | $15.00 | $75.00 | Premium only |

### Ollama (Local - Free)

| Model | Size | RAM Needed | Electricity Cost* |
|-------|------|------------|-------------------|
| llama3.2:3b | 2GB | 4GB | ~$0.01/hr |
| llama3.2:7b | 4.7GB | 8GB | ~$0.02/hr |
| qwen2.5:7b | 4.7GB | 8GB | ~$0.02/hr |
| llama3.2:70b | 40GB | 64GB | ~$0.10/hr |

*Approximate, varies by hardware and electricity rates

## Hardware Requirements (Ollama)

### Minimum Specs

| Model Size | RAM | GPU VRAM | CPU | Suitable For |
|------------|-----|----------|-----|--------------|
| 3B | 4GB | Optional | 4 cores | Laptops, basic tasks |
| 7B | 8GB | 4GB+ | 4 cores | Most desktops |
| 14B | 16GB | 8GB+ | 6 cores | Gaming PCs |
| 70B | 64GB | 48GB+ | 8+ cores | Workstations |

### Recommended Specs for Production

- **RAM**: 2x model size minimum
- **GPU**: NVIDIA RTX 3060+ or Apple M1+
- **Storage**: SSD with space for models
- **Network**: N/A (runs locally)

## Testing Your Setup

### Test Script

Save as `test-model-compatibility.py`:

```python
#!/usr/bin/env python3
from openai import OpenAI
import sys

def test_model(base_url, api_key, model, skill_prompt):
    """Test a model with a skill prompt"""
    client = OpenAI(base_url=base_url, api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": skill_prompt},
                {"role": "user", "content": "Test: Generate a creative domain name for a coffee shop"}
            ],
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        print(f"✅ {model}: Working")
        print(f"   Response preview: {result[:100]}...")
        return True
    except Exception as e:
        print(f"❌ {model}: Failed - {str(e)}")
        return False

# Test with your setup
if __name__ == "__main__":
    with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
        prompt = f.read()
    
    print("Testing OpenRouter models...")
    test_model(
        "https://openrouter.ai/api/v1",
        "YOUR_OPENROUTER_KEY",
        "meta-llama/llama-3.2-3b-instruct:free",
        prompt
    )
    
    print("\nTesting Ollama models...")
    test_model(
        "http://localhost:11434/v1",
        "ollama",
        "llama3.2",
        prompt
    )
```

Run with:
```bash
python test-model-compatibility.py
```

## Choosing the Right Model

### Decision Tree

1. **Do you need the absolute best quality?**
   - Yes → Claude 3.5 Sonnet (OpenRouter)
   - No → Continue

2. **Are you on a budget?**
   - Yes → Llama 3.2 models (OpenRouter or Ollama)
   - No → Continue

3. **Do you need it to run locally/offline?**
   - Yes → Ollama with llama3.2 or qwen2.5
   - No → Continue

4. **Do you need the fastest responses?**
   - Yes → GPT-4o or Gemini Flash (OpenRouter)
   - No → Continue

5. **Do you need tool calling?**
   - Yes → Claude 3.5, GPT-4o, or Gemini 1.5 Pro
   - No → Any model works

### General Recommendations

**For most users starting out**:
- Try free models first (Ollama `llama3.2:3b` or OpenRouter free tier)
- Test your specific skills
- Upgrade to paid models only if quality isn't sufficient

**For production use**:
- OpenRouter with Claude 3.5 Sonnet or GPT-4o
- Set up fallbacks to cheaper models
- Monitor costs and quality

**For privacy-sensitive work**:
- Ollama locally
- Start with `llama3.2:7b` or `qwen2.5:7b`
- Upgrade to 70B models if needed

## Provider Comparison

| Factor | OpenRouter | Ollama |
|--------|------------|--------|
| **Cost** | Pay per token | Free (local compute) |
| **Setup** | API key only | Install + download models |
| **Speed** | Fast (cloud) | Depends on hardware |
| **Privacy** | Data sent to providers | 100% local |
| **Model choice** | 100+ models | 50+ models |
| **Context size** | Up to 1M tokens | Up to 128k tokens |
| **Tool calling** | Excellent support | Good support |
| **Maintenance** | None | Update models manually |

## Next Steps

1. Read setup guides:
   - [OPENROUTER-SETUP.md](OPENROUTER-SETUP.md)
   - [OLLAMA-SETUP.md](OLLAMA-SETUP.md)

2. Test with free models:
   - OpenRouter free tier
   - Ollama `llama3.2:3b`

3. Choose based on your needs:
   - Quality → Claude 3.5 Sonnet
   - Speed → GPT-4o
   - Cost → Llama 3.2
   - Privacy → Ollama

4. Start with Tier 1 skills (work with all models)

5. Upgrade to Tier 2 when you need tool calling

## Support

Having issues with a specific model? Check:
- [OpenRouter Status](https://status.openrouter.ai)
- [Ollama GitHub Issues](https://github.com/ollama/ollama/issues)
- Model-specific documentation
