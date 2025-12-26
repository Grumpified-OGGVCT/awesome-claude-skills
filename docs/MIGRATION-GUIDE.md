# Migration Guide: Claude Skills to Universal Format

This guide explains how to convert Claude skills to the universal format while maintaining backward compatibility with the original repository.

## Philosophy: Backward Compatibility First

**Key Principle**: The original Claude skills remain unchanged. The universal format is **derived** from them.

### Repository Structure

```
awesome-claude-skills/
├── [skill-folders]/           # ORIGINAL: Never modified, stays in sync with upstream
├── universal/                 # DERIVED: Generated from original skills
│   ├── tier-1-instruction-only/
│   ├── tier-2-tool-enhanced/
│   └── tier-3-claude-only/
└── tools/
    ├── convert.py            # Converts skills to universal format
    └── sync-upstream.sh      # Pulls updates from ComposioHQ
```

### Update Workflow

1. **Sync upstream**: `./tools/sync-upstream.sh` pulls latest from ComposioHQ
2. **Re-convert**: `python tools/convert.py --all` regenerates universal format
3. **Review changes**: Check what changed in universal format
4. **Commit**: Only commit universal format changes

This ensures:
- ✅ Original skills stay pristine and in sync
- ✅ Universal format always reflects latest skills
- ✅ No merge conflicts with upstream
- ✅ Easy to track changes

## Understanding Skill Tiers

### Tier 1: Instruction-Only (90% of skills)
**Characteristics**:
- Pure instructions and workflow guidance
- No tool calling required
- No scripts or external dependencies
- Works with any LLM model

**Examples**: Domain name brainstormer, meeting insights analyzer, brainstorming, content research writer

**Conversion**: Straightforward - extract instructions, remove Claude-specific language

### Tier 2: Tool-Enhanced (10% of skills)
**Characteristics**:
- Has scripts or tool definitions
- Benefits from tool calling but can work without it
- Includes both tool and manual versions

**Examples**: PDF editor, file organizer, image enhancer

**Conversion**: Extract tool capabilities, create OpenAI function schemas, provide manual fallback

### Tier 3: Claude-Only (Reference)
**Characteristics**:
- Requires Claude Artifacts
- Requires Claude MCP Servers
- Requires Claude.ai UI features

**Examples**: Canvas design, artifacts builder, some Claude-specific integrations

**Conversion**: Flagged as Claude-only, kept as reference

## Conversion Process

### Automated Conversion (Recommended)

```bash
# Convert all skills
python tools/convert.py --all

# Convert specific skill
python tools/convert.py --skill domain-name-brainstormer

# Convert specific tier
python tools/convert.py --tier 1

# Dry run (preview changes)
python tools/convert.py --all --dry-run
```

### Manual Conversion (For Custom Skills)

#### Step 1: Determine Tier

Ask yourself:
- Does it use scripts or tools? → Tier 2
- Does it require Claude Artifacts/MCP? → Tier 3
- Just instructions? → Tier 1

#### Step 2: Create Directory Structure

```bash
# For Tier 1
mkdir -p universal/tier-1-instruction-only/your-skill-name

# For Tier 2
mkdir -p universal/tier-2-tool-enhanced/your-skill-name
```

#### Step 3: Convert System Prompt

**Original SKILL.md**:
```markdown
---
name: domain-name-brainstormer
description: Generates creative domain names...
---

# Domain Name Brainstormer

This skill helps Claude find the perfect domain name...

## When to Use This Skill
[instructions]
```

**Converted system-prompt.md**:
```markdown
# Domain Name Brainstormer

Generates creative domain names for projects and checks availability across multiple TLDs.

## Task
Help users find the perfect domain name for their project by generating creative options and checking availability.

## When to Use
- Starting a new project or company
- Launching a product or service
- Creating a personal brand
- Rebranding an existing project

## Instructions

[Core instructions, with Claude-specific language removed]

### Process
1. Understand the project and target audience
2. Generate creative, memorable domain options
3. Suggest across multiple TLDs (.com, .io, .dev, .ai, .app)
4. Provide branding insights

### Domain Quality Criteria
- Short (under 15 characters)
- Memorable and easy to spell
- Pronounceable
- Descriptive of purpose
- Brandable and unique
- No hyphens

[Continue with full instructions...]
```

**Key Changes**:
- Remove YAML frontmatter (moved to metadata.yaml)
- Change "Claude should" to "The AI should" or imperative form
- Remove references to "claude.ai" → "your AI interface"
- Remove MCP-specific instructions
- Keep core logic and examples

#### Step 4: Create API Example

**api-example.json**:
```json
{
  "model": "MODEL_NAME_HERE",
  "messages": [
    {
      "role": "system",
      "content": "[Content from system-prompt.md]"
    },
    {
      "role": "user",
      "content": "I'm building a project management tool for remote teams. Suggest domain names."
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Note**: This is a template. Users will replace `MODEL_NAME_HERE` with their chosen model.

#### Step 5: Create Metadata

**metadata.yaml**:
```yaml
name: domain-name-brainstormer
description: Generates creative domain names for your project and checks availability across multiple TLDs (.com, .io, .dev, .ai, etc.).
tier: 1
version: "1.0"

# Source information
source:
  original_path: domain-name-brainstormer/SKILL.md
  last_sync: 2025-12-26
  upstream_repo: anthropics/skills

# Requirements
requirements:
  tool_calling: false
  min_context_window: 4096
  recommended_context_window: 8192

# Model compatibility
compatibility:
  tested_providers:
    - openrouter
    - ollama
  tested_models:
    - llama3.2
    - qwen2.5
    - mistral
  recommended_models:
    - anthropic/claude-3.5-sonnet
    - openai/gpt-4o
    - meta-llama/llama-3.2-90b-instruct

# Features
features:
  - creative_naming
  - availability_checking
  - multi_tld_support
  - branding_insights

# Tags for discovery
tags:
  - business
  - branding
  - naming
  - domains
```

### Tier 2 Conversion: Adding Tools

#### Step 6: Extract Tool Capabilities

For skills with scripts (e.g., PDF editor):

**Original structure**:
```
pdf-editor/
├── SKILL.md
└── scripts/
    ├── fill_form.py
    └── extract_text.py
```

**Analyze scripts** to understand:
- What functions do they provide?
- What parameters do they need?
- What do they return?

#### Step 7: Create OpenAI Function Schema

**tools-schema.json**:
```json
[
  {
    "type": "function",
    "function": {
      "name": "extract_pdf_text",
      "description": "Extracts text content from a PDF file",
      "parameters": {
        "type": "object",
        "properties": {
          "file_path": {
            "type": "string",
            "description": "Path to the PDF file"
          },
          "page_numbers": {
            "type": "array",
            "items": {"type": "integer"},
            "description": "Optional: Specific pages to extract (defaults to all)"
          }
        },
        "required": ["file_path"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fill_pdf_form",
      "description": "Fills form fields in a PDF",
      "parameters": {
        "type": "object",
        "properties": {
          "file_path": {"type": "string"},
          "field_values": {
            "type": "object",
            "description": "Dictionary of field names to values"
          },
          "output_path": {"type": "string"}
        },
        "required": ["file_path", "field_values", "output_path"]
      }
    }
  }
]
```

#### Step 8: Create Manual Fallback

**manual-version.md**:
```markdown
# PDF Editor - Manual Version

For models without tool calling support, follow these instructions:

## When User Wants to Extract PDF Text

Instead of calling a tool, guide them:

```
To extract text from your PDF:

1. Use a Python script:
   ```python
   import PyPDF2
   
   with open('document.pdf', 'rb') as file:
       reader = PyPDF2.PdfReader(file)
       for page in reader.pages:
           print(page.extract_text())
   ```

2. Or use command line:
   ```bash
   pdftotext document.pdf output.txt
   ```

3. Or upload to [tool website] and download text
```

[Continue with manual alternatives for each tool...]
```

## Common Patterns to Convert

### Pattern 1: Remove Claude Branding

| Original | Universal |
|----------|-----------|
| "Claude should" | "The assistant should" or imperative |
| "this skill" | "these instructions" |
| "claude.ai" | "your AI interface" |
| "Claude Code" | "your development environment" |

### Pattern 2: Generalize Tool Instructions

| Original | Universal |
|----------|-----------|
| "Use the MCP server to..." | "Use the available tools to..." |
| "Claude can access..." | "The assistant can use..." |
| "Ask Claude to run..." | "Execute the function..." |

### Pattern 3: Model-Agnostic Examples

**Original**:
```
Upload your meeting transcripts to Claude Code and ask Claude to analyze them.
```

**Universal**:
```
Provide your meeting transcripts and request analysis of communication patterns.

Example API call:
{
  "messages": [
    {"role": "system", "content": "[skill instructions]"},
    {"role": "user", "content": "Analyze these meeting transcripts: [content]"}
  ]
}
```

## Testing Your Conversion

### 1. Validate Structure

```bash
python tools/validate.py universal/tier-1-instruction-only/your-skill-name
```

Checks:
- ✓ system-prompt.md exists
- ✓ metadata.yaml is valid
- ✓ api-example.json is valid JSON
- ✓ No Claude-specific language remains
- ✓ All required fields present

### 2. Test with Models

```bash
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/your-skill-name \
  --providers openrouter ollama \
  --models llama3.2 qwen2.5
```

### 3. Compare with Original

Ensure the universal version:
- Preserves all core functionality
- Maintains the same workflow
- Produces similar quality output
- Works across multiple models

## Advanced Topics

### Handling MCP Servers

MCP servers are Claude-specific. For universal format:

1. **Document the capability** in the description
2. **Provide manual alternatives** in Tier 2
3. **Flag as Claude-only** if no alternative exists (Tier 3)

Example:
```markdown
## Tool Capabilities

This skill can use MCP servers when available (Claude only), or fall back to manual execution.

### With MCP (Claude)
[Instructions for Claude users]

### Without MCP (Universal)
[Alternative instructions using standard tools/APIs]
```

### Handling Artifacts

Claude Artifacts (interactive UI components) have no universal equivalent:

1. **Classify as Tier 3** (Claude-only)
2. **Reference in docs** but don't convert
3. **Suggest alternatives** where possible

### Custom Models and Fine-tuning

The universal format works with custom models:

```yaml
# In metadata.yaml
compatibility:
  custom_models: true
  notes: "Works with any OpenAI-compatible endpoint"
```

## Automation: Keeping Skills Updated

### Daily Sync Workflow

```bash
#!/bin/bash
# daily-sync.sh

# 1. Pull upstream changes
./tools/sync-upstream.sh

# 2. Check if any original skills changed
if git diff --name-only | grep -v "^universal/"; then
    echo "Original skills updated, reconverting..."
    
    # 3. Re-convert changed skills
    python tools/convert.py --changed-only
    
    # 4. Validate conversions
    python tools/validate.py --all
    
    # 5. Run tests
    python tools/model-tester.py --quick
    
    # 6. Commit changes
    git add universal/
    git commit -m "Update universal skills from upstream"
    git push
fi
```

### CI/CD Integration

```yaml
# .github/workflows/sync-upstream.yml
name: Sync Upstream Skills

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Sync upstream
        run: ./tools/sync-upstream.sh
      
      - name: Convert skills
        run: python tools/convert.py --changed-only
      
      - name: Validate
        run: python tools/validate.py --all
      
      - name: Create PR
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Update universal skills from upstream"
          body: "Automated sync from anthropics/skills"
```

## Contributing Converted Skills

When contributing your converted skills:

1. **Test thoroughly** with multiple models
2. **Document model compatibility** in metadata.yaml
3. **Provide examples** in api-example.json
4. **Include manual fallbacks** for Tier 2
5. **Update MODEL-COMPATIBILITY.md** with findings

## FAQ

### Q: Can I modify the original skills?
**A**: No. Keep them pristine for upstream sync. Make changes in the universal version only.

### Q: What if a skill can't be converted?
**A**: Classify it as Tier 3 (Claude-only) and document why.

### Q: How do I handle breaking changes from upstream?
**A**: Re-run conversion tools. They'll regenerate the universal format.

### Q: Can I add new fields to metadata.yaml?
**A**: Yes! The format is extensible. Document new fields in this guide.

### Q: What about localization?
**A**: Create separate universal versions per language, e.g., `universal/tier-1-instruction-only/skill-name-es/`

## Resources

- [OpenRouter API Docs](https://openrouter.ai/docs)
- [Ollama OpenAI Compatibility](https://github.com/ollama/ollama/blob/main/docs/openai.md)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)

## Next Steps

1. Read [OPENROUTER-SETUP.md](OPENROUTER-SETUP.md) for OpenRouter setup
2. Read [OLLAMA-SETUP.md](OLLAMA-SETUP.md) for Ollama setup
3. Check [MODEL-COMPATIBILITY.md](MODEL-COMPATIBILITY.md) for model selection
4. Start converting your first skill!
5. Test with multiple models
6. Share your results with the community
