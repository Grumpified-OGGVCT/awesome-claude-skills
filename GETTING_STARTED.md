# Getting Started with AI Skills

> **🚀 GrumpiFied Enhancement** - This comprehensive guide is custom documentation created by Grumpified-OGGVCT with extended multi-provider setup instructions.

Welcome! This guide will help you start using AI Skills with **any LLM** (Claude, GPT-4, Gemini, Llama, etc.) and **any IDE or interface** in under 5 minutes.

## 📋 Table of Contents

- [What You'll Learn](#what-youll-learn)
- [Prerequisites](#prerequisites)
- [Choose Your Path](#choose-your-path)
- [Path 0: Finding the Right Skill (Start Here!)](#-path-0-finding-the-right-skill-start-here) ⭐ **NEW**
- [Path 1: Universal Format (Any LLM, Any IDE)](#path-1-universal-format-any-llm-any-ide) ⭐ **RECOMMENDED**
- [Path 2: IDE Integration](#path-2-ide-integration)
- [Path 3: Claude.ai (Web Interface)](#path-3-claudeai-web-interface)
- [Path 4: Claude Code (Terminal)](#path-4-claude-code-terminal)
- [Path 5: Direct API Integration](#path-5-direct-api-integration)
- [Next Steps](#next-steps)
- [Troubleshooting](#troubleshooting)

## What You'll Learn

By the end of this guide, you'll know how to:
- Install and use AI Skills with any LLM provider
- Pick the right skill for your needs
- Integrate skills into your preferred IDE or workflow
- Create your first custom skill
- Use skills across different platforms and providers

## Prerequisites

Choose your path based on what you want to use:

| Path | Requirements | Best For |
|------|-------------|----------|
| **Universal Format** | Any OpenAI-compatible client | Maximum flexibility, any LLM |
| **IDE Integration** | VS Code, Cursor, Cline, etc. | Developers, coding workflows |
| **Claude.ai** | Free Claude account | Quick testing, web interface |
| **Claude Code** | Claude Code installed | Terminal workflows (Claude-specific) |
| **Direct API** | API key for your provider | Programmatic usage, automation |

## Choose Your Path

Not sure which path to choose? Use this decision tree:

```
Want to use ANY AI model (Claude, GPT-4, Gemini, Llama)?
├─ YES → Use Path 1: Universal Format (RECOMMENDED)
└─ NO → Prefer Claude only?
   └─ YES
      └─ Use an IDE for coding?
         ├─ YES → Use Path 2: IDE Integration
         └─ NO
            └─ Web browser?
               ├─ YES → Use Path 3: Claude.ai
               └─ NO → Terminal? → Use Path 4: Claude Code
```

---

## 🔍 Path 0: Finding the Right Skill (Start Here!)

**Time required: 1 minute**

**Problem**: "How do I know what skills exist?"

**Solution**: Use the Skill Discovery Tool!

### Quick Discovery

```bash
# Super simple - just search!
./tools/find-skill pdf
./tools/find-skill domain
./tools/find-skill meeting

# Or use Python for more options
python tools/index-skills.py     # Generate index (one time)
python tools/discover.py          # Interactive mode
python tools/discover.py --search "pdf"
python tools/discover.py --category "Business & Marketing"
```

### Why Use Discovery First?

- 🔍 **Find skills by purpose** - Not by name
- 📂 **Browse categories** - See what's available
- 🏷️ **Filter by tags** - Find by technology
- 📥 **Get install commands** - Copy-paste to use

### Example: Finding a PDF Tool

```bash
# Simple wrapper (easiest)
$ ./tools/find-skill pdf

# Or with Python
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

## Path 1: Universal Format (Any LLM, Any IDE) ⭐ **RECOMMENDED**

**Time required: 3 minutes**

**Why this path?** Works with **any AI model** (Claude, GPT-4, Gemini, Llama, etc.) and **any interface** (web, API, IDE). Maximum flexibility and future-proofing.

### What You'll Need

Choose one of these options:
- **OpenRouter**: Cloud-based, 100+ models, pay-as-you-go ($0.20-$20/1M tokens)
- **Ollama**: 100% local, free, private (requires local GPU/CPU)
- **Direct API**: OpenAI, Anthropic, Google, etc. (various pricing)

### Quick Start Example

Here's how to use a skill with **any** LLM:

```python
from openai import OpenAI

# Configure your provider (examples below)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # or any provider
    api_key="YOUR_API_KEY"
)

# Load ANY skill from universal/ directory
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    skill_prompt = f.read()

# Use it with ANY model!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or any model below
    messages=[
        {"role": "system", "content": skill_prompt},
        {"role": "user", "content": "Suggest domain names for my AI startup"}
    ]
)

print(response.choices[0].message.content)
```

### Supported Models (Examples)

**Claude Models:**
- `anthropic/claude-3.5-sonnet`
- `anthropic/claude-3-opus`
- `anthropic/claude-3-haiku`

**OpenAI Models:**
- `openai/gpt-4o`
- `openai/gpt-4-turbo`
- `openai/o1`

**Google Models:**
- `google/gemini-pro-1.5`
- `google/gemini-flash-1.5`

**Open Source Models:**
- `meta-llama/llama-3.2-90b`
- `mistralai/mistral-large`
- `qwen/qwen-2.5-72b`

**And 100+ more on OpenRouter!**

### Setup Instructions by Provider

#### Option A: OpenRouter (Easiest for Cloud)

1. **Get API key**: Go to [openrouter.ai](https://openrouter.ai) → Sign up → Get API key
2. **Use the code above** with `base_url="https://openrouter.ai/api/v1"`
3. **Pick any model** from their catalog

**Cost**: Pay-as-you-go, starting at $0.20/1M tokens for budget models

#### Option B: Ollama (Best for Local/Private)

1. **Install Ollama**:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

2. **Pull a model**:
   ```bash
   ollama pull llama3.2  # or qwen2.5, mistral, gemma2, etc.
   ```

3. **Use the code above** with `base_url="http://localhost:11434/v1"`

**Cost**: Free! Runs 100% locally

#### Option C: Direct Provider APIs

**Anthropic (Claude):**
```python
from anthropic import Anthropic
client = Anthropic(api_key="YOUR_KEY")
# Load skill and use with Claude API
```

**OpenAI (GPT-4):**
```python
from openai import OpenAI
client = OpenAI(api_key="YOUR_KEY")
# Default base_url works for OpenAI
```

**Google (Gemini):**
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_KEY")
# Use with Gemini models
```

### IDE Integration

Use skills directly in your coding environment:

**VS Code with Continue:**
```bash
mkdir -p ~/.continue/prompts/
cp universal/tier-1-instruction-only/YOUR_SKILL/system-prompt.md ~/.continue/prompts/
```

**Cursor:**
```bash
mkdir -p ~/.cursor/prompts/
cp universal/tier-1-instruction-only/YOUR_SKILL/system-prompt.md ~/.cursor/prompts/
```

**Cline / Windsurf / Other IDEs:**
- Check your IDE's documentation for custom prompts directory
- Copy `system-prompt.md` files there

### Tips for Universal Format

- ✅ **Tier 1 skills** (instruction-only) work with ANY model
- ✅ **Tier 2 skills** (tool-enhanced) work best with tool-calling models
- ✅ Skills are model-agnostic—same file works everywhere
- ✅ No modifications needed when switching providers
- ✅ Future-proof: works with new models as they're released

---

## Path 2: IDE Integration

**Time required: 2 minutes**

Most modern AI coding assistants support custom instructions/prompts. Here's how to integrate skills:

### Supported IDEs

- **VS Code** (with Continue, Cline, or other AI extensions)
- **Cursor** (AI-first code editor)
- **Windsurf** (Codeium IDE)
- **JetBrains IDEs** (with AI Assistant)
- **Any IDE** with AI integration that supports custom prompts

### Generic Integration Steps

1. **Find your IDE's prompts/instructions directory**
2. **Copy skill files** from `universal/tier-1-instruction-only/SKILL_NAME/`
3. **Reference in your IDE settings** (varies by IDE)

### Specific IDE Examples

**Continue (VS Code):**
```bash
# Add to Continue config
mkdir -p ~/.continue/prompts/
cp universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md \
   ~/.continue/prompts/brainstorm-domains.md
```

**Cursor:**
```bash
# Add to Cursor rules
mkdir -p ~/.cursor/rules/
cp universal/tier-1-instruction-only/YOUR_SKILL/system-prompt.md \
   ~/.cursor/rules/your-skill.md
```

**Cline (VS Code):**
1. Open Cline settings
2. Navigate to "Custom Instructions"
3. Paste content from `system-prompt.md`

### Testing Your Integration

1. Open a project in your IDE
2. Invoke the AI assistant (usually Cmd/Ctrl+K or similar)
3. Ask it to perform the skill's task
4. The AI should follow the skill's instructions!

---

## Path 3: Claude.ai (Web Interface)

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

**🎉 Success!** You just used your first AI Skill with Claude.

### Tips for Claude.ai

- Skills persist across conversations
- You can use multiple skills simultaneously
- Skills auto-activate based on context
- View active skills by clicking the skill icon

---

## Path 4: Claude Code (Terminal)

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

## Path 5: Direct API Integration

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

## Next Steps

### Learn More

1. **Explore skills**: Browse the [Skills](README.md#skills) section by category
2. **Create your own**: Follow the [Creating Skills](README.md#creating-skills) guide
3. **Universal format**: Learn about [tier structure and compatibility](UNIVERSAL-FORMAT.md)
4. **IDE setup**: Check [docs/](docs/) for IDE-specific setup guides
5. **Join the community**: [Discord](https://discord.com/invite/composio) | [Twitter](https://x.com/composio)

### Recommended Skills to Try

Based on your role:

**Developers:**
- [MCP Builder](./mcp-builder/) - Create MCP servers (works with any LLM)
- [Changelog Generator](./changelog-generator/) - Auto-generate changelogs (universal)
- [Test-Driven Development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) - External resource

**Business Users:**
- [Domain Name Brainstormer](./domain-name-brainstormer/) - Works with any AI model
- [Lead Research Assistant](./lead-research-assistant/) - Universal format
- [Meeting Insights Analyzer](./meeting-insights-analyzer/) - Any LLM

**Content Creators:**
- [Content Research Writer](./content-research-writer/) - Model-agnostic
- [Brand Guidelines](./brand-guidelines/) - Works everywhere
- [Theme Factory](./theme-factory/) - Universal

**Everyone:**
- [File Organizer](./file-organizer/) - Any AI assistant can use this
- [Invoice Organizer](./invoice-organizer/) - Universal format
- [Brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) - External resource

### Contributing

Found a bug? Have an idea for a skill? Want to add IDE-specific docs? [Open an issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues) or submit a pull request!

**Special interest:**
- Universal format conversions for existing skills
- IDE integration guides (Cursor, Continue, Cline, Windsurf, etc.)
- Multi-provider examples and testing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Troubleshooting

### Common Issues

**Problem: Skill isn't working with my LLM**

Solution:
1. Check skill tier: Tier 1 works with all models, Tier 2 needs tool support
2. Verify you're loading the system prompt correctly
3. Ensure the model has sufficient context window for the skill
4. Try with a different model to isolate the issue

**Problem: Skill not found in IDE**

Solution:
1. Verify skill is in correct directory for your IDE
2. Check IDE's custom prompts/instructions configuration
3. Restart IDE after adding new skills
4. Consult your IDE's documentation for custom prompt support

**Problem: Skill not activating in Claude.ai**

Solution:
1. Check that SKILL.md has valid YAML frontmatter
2. Re-upload the skill if needed
3. Verify your request matches the skill's description
4. Try being more explicit: "Use the domain-name-brainstormer skill to..."

**Problem: Universal format API call failing**

Solution:
1. Verify API key is correct for your provider
2. Check base_url is set correctly (OpenRouter, Ollama, etc.)
3. Ensure model name format matches provider requirements
4. Test with a simple prompt first to verify connection

**Problem: Skill works inconsistently**

Solution:
1. Make the skill description more specific
2. Provide clearer instructions in your prompt
3. Check if you're using the right model tier for the skill
4. Some models perform better with certain types of instructions

### Getting Help

- **Documentation**: Check the [FAQ](README.md#frequently-asked-questions)
- **Universal Format**: [UNIVERSAL-FORMAT.md](UNIVERSAL-FORMAT.md) for multi-provider setup
- **Discord**: [Composio Discord](https://discord.com/invite/composio)
- **Issues**: [GitHub Issues](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues)
- **IDE-Specific**: Check your IDE's documentation for AI assistant configuration

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
