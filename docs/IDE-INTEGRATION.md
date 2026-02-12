# IDE Integration Guide for AI Skills

> **🚀 GrumpiFied Enhancement** - This guide helps you use universal AI skills in any IDE or coding assistant.

## Overview

Universal AI skills work with **any IDE that supports AI assistants**. This guide shows you how to integrate skills into the most popular coding environments.

## Supported IDEs

| IDE / Tool | AI Integration | Setup Difficulty | Notes |
|------------|----------------|------------------|-------|
| **Cursor** | Built-in | ⭐ Easy | Native AI, supports Claude & GPT-4 |
| **VS Code + Continue** | Extension | ⭐ Easy | Supports 100+ models via OpenRouter |
| **VS Code + Cline** | Extension | ⭐ Easy | Full codebase awareness |
| **Windsurf** | Built-in | ⭐ Easy | Codeium-powered |
| **JetBrains IDEs** | Built-in | ⭐⭐ Medium | AI Assistant in Pro versions |
| **Zed** | Built-in | ⭐⭐ Medium | Emerging AI support |
| **Any IDE** | Manual | ⭐⭐⭐ Advanced | Via custom scripts/prompts |

## Quick Start by IDE

### Cursor

**Setup Time**: 1 minute

1. **Copy skills to Cursor:**
   ```bash
   mkdir -p ~/.cursor/prompts/
   cp universal/tier-1-instruction-only/YOUR_SKILL/system-prompt.md \
      ~/.cursor/prompts/skill-name.md
   ```

2. **Use the skill:**
   - Open Cursor
   - Press `Cmd/Ctrl + K` to open AI chat
   - The skill is automatically loaded
   - Ask: "Help me brainstorm domain names"

**Tips:**
- Skills in `~/.cursor/prompts/` load automatically
- You can have multiple skills active
- Cursor uses Claude or GPT-4 (your choice in settings)

---

### VS Code with Continue

**Setup Time**: 2 minutes

1. **Install Continue:**
   - Open VS Code
   - Install "Continue" extension from marketplace

2. **Configure Continue:**
   ```bash
   mkdir -p ~/.continue/prompts/
   cp universal/tier-1-instruction-only/YOUR_SKILL/system-prompt.md \
      ~/.continue/prompts/skill-name.md
   ```

3. **Set your provider:**
   - Open Continue settings (Cmd/Ctrl + Shift + P → "Continue: Settings")
   - Choose provider: OpenRouter, Ollama, or direct API
   - Add API key if needed

4. **Use the skill:**
   - Press `Cmd/Ctrl + L` to open Continue
   - Skills load automatically
   - Chat with any model you configured

**Tips:**
- Continue supports 100+ models via OpenRouter
- Can use multiple providers simultaneously
- Great for comparing model outputs

**Example Continue config** (`~/.continue/config.json`):
```json
{
  "models": [
    {
      "title": "Claude 3.5 Sonnet",
      "provider": "openrouter",
      "model": "anthropic/claude-3.5-sonnet",
      "apiKey": "YOUR_KEY"
    },
    {
      "title": "Llama 3.2 Local",
      "provider": "ollama",
      "model": "llama3.2"
    }
  ],
  "systemMessage": "~/.continue/prompts/skill-name.md"
}
```

---

### VS Code with Cline

**Setup Time**: 2 minutes

1. **Install Cline:**
   - Open VS Code
   - Install "Cline" extension from marketplace

2. **Add skill to Cline:**
   - Click Cline icon in sidebar
   - Click settings (gear icon)
   - Navigate to "Custom Instructions"
   - Paste content from `system-prompt.md`

3. **Configure API:**
   - Add your preferred provider (OpenRouter, Anthropic, OpenAI)
   - Add API key

4. **Use the skill:**
   - Open Cline panel
   - Start chatting - skill is active
   - Cline has full codebase context

**Tips:**
- Cline sees your entire codebase
- Great for code-aware skills
- Can make file changes directly

---

### Windsurf

**Setup Time**: 1 minute

1. **Add skill:**
   - Open Windsurf
   - Go to Settings → AI → Custom Prompts
   - Create new prompt
   - Paste content from `system-prompt.md`

2. **Use the skill:**
   - Open AI panel (Cmd/Ctrl + I)
   - Select your custom prompt
   - Start chatting

**Tips:**
- Windsurf is Codeium's AI-first IDE
- Built-in AI is fast and free tier available
- Good for quick iterations

---

### JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)

**Setup Time**: 3 minutes

**Requirements**: JetBrains AI Assistant (available in Pro versions)

1. **Enable AI Assistant:**
   - Settings → Plugins → Install "AI Assistant"
   - Restart IDE

2. **Add custom prompt:**
   - Settings → Tools → AI Assistant → Custom Prompts
   - Create new prompt
   - Paste content from `system-prompt.md`

3. **Use the skill:**
   - Open AI Assistant panel
   - Select your custom prompt
   - Chat with AI

**Tips:**
- AI Assistant uses JetBrains' models by default
- Can configure to use OpenAI or other providers
- Great integration with IntelliJ features

---

### Zed

**Setup Time**: 2 minutes

**Note**: Zed's AI support is evolving rapidly.

1. **Add skill:**
   - Open Zed
   - Access AI settings (Cmd/Ctrl + ,)
   - Add system prompt from `system-prompt.md`

2. **Use the skill:**
   - Open assistant panel
   - Start chatting

**Tips:**
- Zed is a fast, modern editor
- AI features are actively being developed
- Check Zed docs for latest AI capabilities

---

## Generic Integration (Any IDE)

If your IDE isn't listed, you can still use skills:

### Method 1: Copy-Paste
1. Open the `system-prompt.md` file
2. Copy its contents
3. Paste into your IDE's AI chat as context
4. Continue your conversation

### Method 2: Custom Script
Create a helper script that loads skills:

```python
# load_skill.py
import sys
from openai import OpenAI

def load_skill(skill_name, model="gpt-4o"):
    # Load skill
    with open(f"universal/tier-1-instruction-only/{skill_name}/system-prompt.md") as f:
        skill = f.read()
    
    # Setup client (configure for your provider)
    client = OpenAI(api_key="YOUR_KEY")
    
    # Interactive chat
    messages = [{"role": "system", "content": skill}]
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        assistant_msg = response.choices[0].message.content
        print(f"\nAssistant: {assistant_msg}\n")
        messages.append({"role": "assistant", "content": assistant_msg})

if __name__ == "__main__":
    skill = sys.argv[1] if len(sys.argv) > 1 else "domain-name-brainstormer"
    load_skill(skill)
```

Usage:
```bash
python load_skill.py domain-name-brainstormer
```

---

## Troubleshooting

### Skill Not Loading

**Problem**: IDE doesn't recognize the skill.

**Solutions**:
1. Check file location matches IDE's expected path
2. Verify file format (should be plain text/markdown)
3. Restart IDE after adding skills
4. Check IDE's documentation for custom prompts location

### Skill Not Working as Expected

**Problem**: AI doesn't follow skill instructions properly.

**Solutions**:
1. Ensure you're using a capable model (GPT-4, Claude 3.5, Gemini Pro, etc.)
2. Check if it's a Tier 2 skill requiring tool support
3. Try being more explicit: "Using the domain-brainstormer skill, suggest names for..."
4. Verify the system prompt is loaded correctly

### IDE-Specific Issues

**Problem**: Can't find where to add custom prompts.

**Solutions**:
1. Check IDE's official documentation for AI features
2. Look for settings under: AI, Assistant, Copilot, or Extensions
3. Search IDE settings for "prompt", "system", or "instruction"
4. Join IDE's Discord/community for help

---

## Best Practices

### 1. Organize Your Skills

Create a clear folder structure:
```
~/.ai-skills/
├── document-processing/
│   ├── pdf-editor.md
│   └── invoice-organizer.md
├── development/
│   ├── changelog-generator.md
│   └── code-reviewer.md
└── business/
    ├── domain-brainstormer.md
    └── lead-researcher.md
```

Then symlink to your IDE:
```bash
ln -s ~/.ai-skills/document-processing/pdf-editor.md ~/.cursor/prompts/
ln -s ~/.ai-skills/development/changelog-generator.md ~/.continue/prompts/
```

### 2. Name Skills Clearly

Good names:
- ✅ `domain-brainstormer.md`
- ✅ `pdf-invoice-organizer.md`
- ✅ `meeting-insights-analyzer.md`

Poor names:
- ❌ `skill1.md`
- ❌ `temp.md`
- ❌ `untitled.md`

### 3. Test Before Committing

Before adding a skill to your IDE config:
1. Test it in a simple Python script first
2. Try with 2-3 different models
3. Verify it produces expected results
4. Then add to IDE

### 4. Version Control

Keep your skill configs in git:
```bash
# Create a dotfiles repo
mkdir ~/.dotfiles
cd ~/.dotfiles
git init

# Add IDE configs
mkdir -p ide-configs/cursor
mkdir -p ide-configs/continue
cp -r ~/.cursor/prompts/ ide-configs/cursor/
cp -r ~/.continue/prompts/ ide-configs/continue/

git add .
git commit -m "Add AI skills configs"
```

---

## Advanced Tips

### Multiple Skills at Once

Most IDEs support loading multiple skills. Create a "combined" skill:

```markdown
# Combined Skills: Development Assistant

You are a development assistant with expertise in:

## Skill 1: Code Review
[paste code-review skill content]

## Skill 2: Documentation
[paste documentation skill content]

## Skill 3: Testing
[paste testing skill content]

When asked to perform a task, identify which skill applies and use it.
```

### Dynamic Skill Loading

For advanced users, create a script that dynamically loads skills:

```python
# skill_loader.py
import os
from openai import OpenAI

class SkillLoader:
    def __init__(self, skills_dir="universal/tier-1-instruction-only"):
        self.skills_dir = skills_dir
        self.loaded_skills = {}
    
    def load(self, skill_name):
        path = f"{self.skills_dir}/{skill_name}/system-prompt.md"
        with open(path) as f:
            self.loaded_skills[skill_name] = f.read()
    
    def combine(self):
        return "\n\n---\n\n".join(self.loaded_skills.values())
    
    def chat(self, model="gpt-4o"):
        combined = self.combine()
        client = OpenAI()
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": combined},
                {"role": "user", "content": input("You: ")}
            ]
        )
        print(response.choices[0].message.content)

# Usage
loader = SkillLoader()
loader.load("domain-name-brainstormer")
loader.load("meeting-insights-analyzer")
loader.chat()
```

---

## IDE-Specific Resources

### Cursor
- [Official Docs](https://docs.cursor.com/)
- [Custom Rules](https://docs.cursor.com/context/rules-for-ai)

### Continue
- [Official Docs](https://continue.dev/docs)
- [Model Providers](https://continue.dev/docs/model-providers)
- [GitHub](https://github.com/continuedev/continue)

### Cline
- [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- [GitHub](https://github.com/cline/cline)

### Windsurf
- [Official Site](https://codeium.com/windsurf)
- [Docs](https://docs.codeium.com/)

### JetBrains AI Assistant
- [Official Docs](https://www.jetbrains.com/help/idea/ai-assistant.html)
- [Setup Guide](https://www.jetbrains.com/help/idea/ai-assistant-setup.html)

---

## Getting Help

- **GitHub Issues**: [Report IDE-specific issues](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues)
- **Discord**: [Join Composio Discord](https://discord.com/invite/composio)
- **Docs**: Check your IDE's official documentation
- **Community**: Ask in your IDE's community forums

---

## Contributing

Have setup instructions for an IDE we didn't cover? 

1. Test the integration thoroughly
2. Document the steps clearly
3. Submit a PR to add it to this guide
4. Include screenshots if helpful

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Bottom Line**: Universal AI skills work in **any IDE** with AI support. Choose your favorite tool, follow the setup for that IDE, and you're ready to go!
