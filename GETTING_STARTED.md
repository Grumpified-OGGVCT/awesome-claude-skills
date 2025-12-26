# Getting Started with Claude Skills

Welcome! This guide will help you start using Claude Skills in under 5 minutes.

## 📋 Table of Contents

- [What You'll Learn](#what-youll-learn)
- [Prerequisites](#prerequisites)
- [Choose Your Path](#choose-your-path)
- [Path 0: Finding the Right Skill (Start Here!)](#-path-0-finding-the-right-skill-start-here) ⭐ **NEW**
- [Path 1: Claude.ai (Easiest)](#path-1-claudeai-easiest)
- [Path 2: Claude Code](#path-2-claude-code)
- [Path 3: Claude API](#path-3-claude-api)
- [Path 4: Universal Format (Any LLM)](#path-4-universal-format-any-llm)
- [Next Steps](#next-steps)
- [Troubleshooting](#troubleshooting)

## What You'll Learn

By the end of this guide, you'll know how to:
- Install and use Claude Skills
- Pick the right skill for your needs
- Create your first custom skill
- Use skills with different LLM providers

## Prerequisites

Choose your path based on what you have access to:

| Path | Requirements | Best For |
|------|-------------|----------|
| **Claude.ai** | Free Claude account | Non-technical users, quick testing |
| **Claude Code** | Claude Code installed | Developers, terminal workflows |
| **Claude API** | Claude API key | Programmatic usage, automation |
| **Universal Format** | OpenRouter/Ollama | Multi-model support, local usage |

## Choose Your Path

Not sure which path to choose? Use this decision tree:

```
Do you primarily use Claude in a web browser?
├─ YES → Use Path 1: Claude.ai
└─ NO
   └─ Do you code in a terminal/editor?
      ├─ YES → Use Path 2: Claude Code
      └─ NO
         └─ Do you need programmatic access?
            ├─ YES → Use Path 3: Claude API
            └─ NO → Want to try other AI models?
               └─ YES → Use Path 4: Universal Format
```

---

## 🔍 Path 0: Finding the Right Skill (Start Here!)

**Time required: 1 minute**

**Problem**: "How do I know what skills exist?"

**Solution**: Use the Skill Discovery Tool!

### Quick Discovery

```bash
# Generate skill index (one time only)
python tools/index-skills.py

# Interactive discovery - explore what's available
python tools/discover.py

# Or search for what you need
python tools/discover.py --search "pdf"
python tools/discover.py --search "domain"
python tools/discover.py --category "Business & Marketing"
```

### Why Use Discovery First?

- 🔍 **Find skills by purpose** - Not by name
- 📂 **Browse categories** - See what's available
- 🏷️ **Filter by tags** - Find by technology
- 📥 **Get install commands** - Copy-paste to use

### Example: Finding a PDF Tool

```bash
$ python tools/discover.py --search "pdf"

🔍 Found 10 skill(s) matching 'pdf':

📦 pdf
   Category: Document Processing
   Comprehensive PDF manipulation toolkit...
   
   Installation:
   Claude.ai: Upload 'document-skills/pdf/SKILL.md'
   Claude Code: cp -r document-skills/pdf ~/.config/claude-code/skills/
```

**See the full guide**: [Skill Discovery Documentation](docs/SKILL-DISCOVERY.md)

---

## Path 1: Claude.ai (Easiest)

**Time required: 2 minutes**

### Step 1: Access Claude.ai

1. Go to [claude.ai](https://claude.ai)
2. Sign in or create a free account

### Step 2: Add a Skill

1. **Click the skill icon** (🧩) in the chat interface (bottom left corner)
2. **Choose one of these options:**
   - **Option A**: Browse the marketplace and click "Add" on any skill
   - **Option B**: Click "Add custom skill" and upload a SKILL.md file from this repository

### Step 3: Use the Skill

1. Start a new conversation
2. Type a request that matches the skill's purpose
3. Claude automatically activates the skill!

### Example Walkthrough

Let's try the Domain Name Brainstormer skill:

1. **Download the skill**:
   - Go to [`domain-name-brainstormer/SKILL.md`](./domain-name-brainstormer/SKILL.md)
   - Click "Raw" and save the file

2. **Upload to Claude**:
   - Click the skill icon (🧩)
   - Click "Add custom skill"
   - Upload the SKILL.md file
   - Click "Add"

3. **Test it**:
   ```
   You: "Help me brainstorm domain names for my project management tool"
   
   Claude: "I'll help you find the perfect domain! 
            Tell me about your project management tool:
            - Who is it designed for?
            - What makes it unique?
            - Any preferred keywords or style?"
   ```

**🎉 Success!** You just used your first Claude Skill.

### Tips for Claude.ai

- Skills persist across conversations
- You can use multiple skills simultaneously
- Skills auto-activate based on context
- View active skills by clicking the skill icon

---

## Path 2: Claude Code

**Time required: 3 minutes**

### Prerequisites

- Claude Code installed ([download here](https://claude.ai/download))
- Basic terminal/command-line knowledge

**Note**: Skills in the universal format need to be converted first. Most existing skills in the root directory work directly with Claude Code.

### Step 1: Create Skills Directory

```bash
# Create the skills directory
mkdir -p ~/.config/claude-code/skills/

# Navigate to it
cd ~/.config/claude-code/skills/
```

### Step 2: Install Skills

**Option A: Install All Skills**
```bash
# Clone this entire repository
git clone https://github.com/Grumpified-OGGVCT/awesome-claude-skills.git .

# This gives you access to all 200+ skills
```

**Option B: Install Specific Skills**
```bash
# Clone to a temp directory
cd /tmp
git clone https://github.com/Grumpified-OGGVCT/awesome-claude-skills.git

# Copy just the skills you want
cp -r awesome-claude-skills/domain-name-brainstormer ~/.config/claude-code/skills/
cp -r awesome-claude-skills/file-organizer ~/.config/claude-code/skills/
```

### Step 3: Verify Installation

```bash
# Check that skills are properly installed
ls -la ~/.config/claude-code/skills/

# Verify a skill has proper metadata
head ~/.config/claude-code/skills/domain-name-brainstormer/SKILL.md
```

You should see YAML frontmatter like:
```yaml
---
name: domain-name-brainstormer
description: Generates creative domain name ideas...
---
```

### Step 4: Use Claude Code

```bash
# Start Claude Code
claude

# Skills load automatically!
# Try asking: "Help me organize my Downloads folder"
```

### Example Workflow

1. **Start Claude Code**: `claude`
2. **Check loaded skills**: Claude will mention available skills on startup
3. **Use a skill**:
   ```
   You: "I need to organize my downloads folder"
   Claude: [Activates file-organizer skill]
           "I'll help you organize your downloads! Let me analyze the folder structure..."
   ```

### Tips for Claude Code

- Skills reload when you restart Claude Code
- Place company-specific skills in the same directory
- Skills can reference local scripts and files
- Use `claude --verbose` to see skill loading details

---

## Path 3: Claude API

**Time required: 5 minutes**

### Prerequisites

- Claude API key ([get one here](https://console.anthropic.com/))
- Python 3.8+ or Node.js 16+

### Step 1: Install SDK

**Python:**
```bash
pip install anthropic
```

**JavaScript:**
```bash
npm install @anthropic-ai/sdk
```

### Step 2: Basic Usage

**Python:**
```python
import anthropic

# Initialize client
client = anthropic.Anthropic(api_key="your-api-key")

# Use a skill (skills must first be uploaded to get an ID)
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    skills=["skill-id-from-marketplace"],
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Help me brainstorm domain names"}
    ]
)

print(response.content[0].text)
```

**JavaScript:**
```javascript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

const response = await client.messages.create({
  model: 'claude-3-5-sonnet-20241022',
  skills: ['skill-id-from-marketplace'],
  max_tokens: 1024,
  messages: [
    {role: 'user', content: 'Help me brainstorm domain names'}
  ]
});

console.log(response.content[0].text);
```

### Step 3: Upload Custom Skills

To use custom skills from this repository:

1. **Get the skill content**:
   ```python
   with open('domain-name-brainstormer/SKILL.md', 'r') as f:
       skill_content = f.read()
   ```

2. **Upload to Claude** (via API or dashboard)
3. **Get the skill ID**
4. **Reference it in your code**

See [Skills API documentation](https://docs.claude.com/en/api/skills-guide) for complete upload instructions.

### Tips for API Usage

- Cache skills to reduce latency
- Skills work with all Claude 3 models
- Combine multiple skills in one request
- Monitor usage in the Anthropic console

---

## Path 4: Universal Format (Any LLM)

**Time required: 5-10 minutes**

Use skills with GPT-4, Llama, Gemini, or any OpenAI-compatible model!

### Option A: OpenRouter (Cloud, 100+ Models)

**Step 1: Get API Key**
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up and create an API key

**Step 2: Install SDK**
```bash
pip install openai
```

**Step 3: Use a Skill**

**Note**: Skills must be converted first using `python tools/convert.py --all`. Or use pre-converted skills from the `universal/` directory.

```python
from openai import OpenAI

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_KEY"
)

# Load skill (example assumes skills are converted)
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    skill = f.read()

# Use it with ANY model!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or "openai/gpt-4o", "meta-llama/llama-3.2-90b", etc.
    messages=[
        {"role": "system", "content": skill},
        {"role": "user", "content": "Suggest domain names for my AI startup"}
    ]
)

print(response.choices[0].message.content)
```

**Available Models**: 100+ including Claude, GPT-4, Gemini, Llama, Qwen, Mistral, and more!

### Option B: Ollama (Local, Free, Private)

**Step 1: Install Ollama**
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from ollama.com
```

**Step 2: Download a Model**
```bash
# Fast and capable (3B parameters)
ollama pull llama3.2

# More powerful (8B parameters)
ollama pull llama3.2:8b

# Best quality (70B parameters, requires powerful hardware)
ollama pull llama3.2:70b
```

**Step 3: Use a Skill**

**Note**: Example assumes skill has been converted to universal format. Convert skills with `python tools/convert.py --skill skill-name`.

```python
from openai import OpenAI

# Connect to local Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama doesn't need a real key
)

# Load skill (example path - adjust to your converted skills)
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    skill = f.read()

# Use it - completely local and private!
response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "system", "content": skill},
        {"role": "user", "content": "Suggest domain names for my AI startup"}
    ]
)

print(response.choices[0].message.content)
```

**Benefits**: 100% free, completely private, works offline, no API limits!

### Understanding Skill Tiers

- **Tier 1 (90% of skills)**: Work with ANY model - just system prompts
- **Tier 2 (10% of skills)**: Work best with tool-calling models (Claude 3.5, GPT-4o, Gemini 1.5)
- **Tier 3**: Claude-specific (Artifacts, MCP)

Browse skills by tier:
```bash
ls universal/tier-1-instruction-only/    # Works everywhere
ls universal/tier-2-tool-enhanced/       # Needs tool support
```

### More Resources

- [OpenRouter Setup Guide](docs/OPENROUTER-SETUP.md)
- [Ollama Setup Guide](docs/OLLAMA-SETUP.md)
- [Model Compatibility Guide](docs/MODEL-COMPATIBILITY.md)

---

## Next Steps

### Learn More

1. **Explore skills**: Browse the [Skills](README.md#skills) section by category
2. **Create your own**: Follow the [Creating Skills](README.md#creating-skills) guide
3. **Join the community**: [Discord](https://discord.com/invite/composio) | [Twitter](https://x.com/composio)

### Recommended Skills to Try

Based on your role:

**Developers:**
- [MCP Builder](./mcp-builder/) - Create MCP servers
- [Changelog Generator](./changelog-generator/) - Auto-generate changelogs
- [Test-Driven Development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development)

**Business Users:**
- [Domain Name Brainstormer](./domain-name-brainstormer/)
- [Lead Research Assistant](./lead-research-assistant/)
- [Meeting Insights Analyzer](./meeting-insights-analyzer/)

**Content Creators:**
- [Content Research Writer](./content-research-writer/)
- [Brand Guidelines](./brand-guidelines/)
- [Theme Factory](./theme-factory/)

**Everyone:**
- [File Organizer](./file-organizer/)
- [Invoice Organizer](./invoice-organizer/)
- [Brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming)

### Contributing

Found a bug? Have an idea for a skill? [Open an issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues) or submit a pull request!

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Troubleshooting

### Common Issues

**Problem: Skill isn't activating**

Solution:
1. Check that SKILL.md has valid YAML frontmatter
2. Ensure skill is in correct directory
3. Verify your request matches the skill's description
4. Try being more explicit: "Use the domain-name-brainstormer skill to..."

**Problem: "Skill not found" error**

Solution:
1. Verify file is named `SKILL.md` (uppercase)
2. Check file location:
   - Claude.ai: Re-upload the skill
   - Claude Code: Should be in `~/.config/claude-code/skills/skill-name/`
   - API: Verify skill ID is correct

**Problem: Skill works inconsistently**

Solution:
1. Make the skill description more specific
2. Provide clearer instructions in your prompt
3. Check if you're using the right model (some skills need advanced models)

**Problem: Universal format skill not working**

Solution:
1. Check if you're using a Tier 1 skill (works with all models)
2. For Tier 2 skills, ensure your model supports tool calling
3. Verify the system prompt is being sent correctly
4. Try a different model to isolate the issue

### Getting Help

- **Documentation**: Check the [FAQ](README.md#frequently-asked-questions)
- **Community**: [Claude Community](https://community.anthropic.com)
- **Discord**: [Composio Discord](https://discord.com/invite/composio)
- **Issues**: [GitHub Issues](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues)
- **Official Docs**: [Claude Skills Documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude)

---

## Quick Reference

### File Structure
```
skill-name/
├── SKILL.md          # Required: Instructions and metadata
├── scripts/          # Optional: Helper scripts
├── references/       # Optional: Documentation
└── assets/           # Optional: Templates and resources
```

### SKILL.md Format
```markdown
---
name: skill-name
description: Clear description of what this skill does
---

# Skill Name

Instructions for Claude...
```

### Useful Commands

```bash
# Claude Code: Install all skills
git clone https://github.com/Grumpified-OGGVCT/awesome-claude-skills.git ~/.config/claude-code/skills/

# Universal: Convert a skill
python tools/convert.py --skill skill-name

# Universal: Test a skill
python tools/model-tester.py --skill path/to/skill --quick

# Universal: Validate conversion
python tools/validate.py --skill path/to/skill
```

---

**Ready to supercharge your AI workflow?** Pick your path above and get started! 🚀
