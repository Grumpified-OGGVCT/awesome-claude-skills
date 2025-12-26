# Tools

Automation tools for working with Claude Skills and the universal format.

## 🛠️ Available Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| [find-skill](#find-skill) 🌟 | Simple skill search wrapper | `./tools/find-skill pdf` |
| [discover.py](#discoverpy) ⭐ | Find skills by search/browse | `python tools/discover.py` |
| [index-skills.py](#index-skillspy) | Generate skill search index | `python tools/index-skills.py` |
| [convert.py](#convertpy) | Convert skills to universal format | `python tools/convert.py --all` |
| [validate.py](#validatepy) | Validate universal skill format | `python tools/validate.py --all` |
| [sync-upstream.sh](#sync-upstreamsh) | Sync with anthropics/skills | `./tools/sync-upstream.sh` |
| [model-tester.py](#model-testerpy) | Test skills across models | `python tools/model-tester.py --skill path` |

## 📋 Prerequisites

Most tools require Python 3.8+:

```bash
# Install required packages
pip install pyyaml
```

## Tool Documentation

### find-skill

🌟 **The simplest way to find skills!**

#### Why Use This?

This is a convenience wrapper around discover.py that:
- Automatically generates the index if needed (first run)
- Simplifies the command syntax
- Perfect for quick searches

#### Usage

```bash
# Search for anything
./tools/find-skill pdf
./tools/find-skill domain name
./tools/find-skill meeting notes

# Interactive mode (no arguments)
./tools/find-skill
```

#### Examples

**Quick search:**
```bash
$ ./tools/find-skill pdf

🔍 Found 10 skill(s) matching 'pdf':
[Shows all PDF-related skills with details]
```

**Multi-word search:**
```bash
$ ./tools/find-skill domain name

🔍 Found 1 skill(s) matching 'domain name':
[Shows domain name brainstormer]
```

**First time:**
```bash
$ ./tools/find-skill pdf
📦 First time setup - generating skill index...
[Generates index, then shows results]
```

### discover.py

⭐ **Start here!** Interactive tool to discover and search for skills.

#### Why Use This?

Can't remember what skills are available? Don't know what to search for? This tool solves the discoverability problem by letting you:
- **Search** by keywords without knowing exact skill names
- **Browse** by category or tags
- **Explore** interactively to see what's available
- **Get installation instructions** for any skill

#### Features

- 🔍 **Keyword search** - Find skills by what they do, not what they're called
- 📂 **Category filtering** - Browse skills by type (Business, Development, Creative, etc.)
- 🏷️ **Tag-based discovery** - Filter by technology or use case
- 📋 **Interactive mode** - Explore with a friendly CLI interface
- ⚡ **Quick search** - One-line command for fast lookups
- 📥 **Installation help** - Get exact commands to install any skill

#### Quick Start

```bash
# Interactive mode (recommended for first-time users)
python tools/discover.py

# Quick search for specific needs
python tools/discover.py --search "domain name"
python tools/discover.py --search "pdf"
python tools/discover.py --search "meeting"

# Browse by category
python tools/discover.py --categories
python tools/discover.py --category "Business & Marketing"

# List everything
python tools/discover.py --list
```

#### Interactive Mode Commands

When you run `python tools/discover.py` without arguments, you enter interactive mode:

```
> search pdf              # Find skills related to PDFs
> search domain name      # Find domain-related skills
> category Business       # Show business & marketing skills
> tag web                 # Show all web-related skills
> list                    # List all skills
> categories              # Show all categories
> tags                    # Show all available tags
> 1                       # View details of skill #1 from last results
> help                    # Show available commands
> quit                    # Exit
```

#### Real-World Examples

**Example 1: "I need to work with PDFs but don't know what's available"**
```bash
$ python tools/discover.py --search "pdf"

🔍 Found 10 skill(s) matching 'pdf':

📦 pdf
   Category: Document Processing
   Comprehensive PDF manipulation toolkit for extracting text...
   
   Installation:
   Claude.ai: Upload the file 'document-skills/pdf/SKILL.md'
   Claude Code: cp -r document-skills/pdf ~/.config/claude-code/skills/
```

**Example 2: "What business tools are available?"**
```bash
$ python tools/discover.py --category "Business & Marketing"

📂 Skills in 'Business & Marketing' (5):

📦 brand-guidelines
   Applies Anthropic's official brand colors...
   
📦 competitive-ads-extractor
   Extracts and analyzes competitors' ads...
   
📦 domain-name-brainstormer
   Generates creative domain name ideas...
```

**Example 3: "Show me everything with 'git'"**
```bash
$ python tools/discover.py --search "git"

🔍 Found 3 skill(s) matching 'git':
[Lists all git-related skills with details]
```

#### Prerequisites

First, generate the skill index:
```bash
python tools/index-skills.py
```

This creates `SKILL-INDEX.json` which the discovery tool uses. The index is automatically updated when you add new skills.

#### Tips

- **Use broad keywords**: Search for "document" instead of specific file types
- **Try tags**: Use `tags` command to see all filterable tags
- **Browse categories**: Start with `categories` to understand what's available
- **Interactive is best**: Use interactive mode for exploration, command-line for quick lookups

### index-skills.py

Generates a searchable index of all skills in the repository.

#### Purpose

This tool scans all SKILL.md files and creates `SKILL-INDEX.json`, which powers the discovery tool. Run this whenever:
- You add new skills
- You update skill descriptions
- The index is missing or outdated

#### Usage

```bash
# Generate index (creates SKILL-INDEX.json)
python tools/index-skills.py

# Generate index to custom location
python tools/index-skills.py --output my-index.json
```

#### What It Does

1. Scans repository for all `SKILL.md` files
2. Extracts metadata (name, description, category)
3. Generates searchable tags from content
4. Categorizes skills automatically
5. Creates `SKILL-INDEX.json` with all information

#### Output

```
Scanning repository for skills...
Found 27 skills across 7 categories
✅ Index written to SKILL-INDEX.json

Skills by Category:
  Business & Marketing: 5
  Development & Code Tools: 5
  ...
```

#### Automation

The index is automatically regenerated by:
- The discovery tool (if index is missing)
- CI/CD on skill additions
- Manual runs when needed

### convert.py

Converts Claude-specific skills to universal OpenAI-compatible format.

#### Features

- Converts skills to Tier 1 (instruction-only), Tier 2 (tool-enhanced), or Tier 3 (Claude-only)
- Preserves original skills (never modifies them)
- Re-runnable (safe to run multiple times)
- Tracks conversion metadata

#### Basic Usage

```bash
# Convert all skills
python tools/convert.py --all

# Convert specific skill
python tools/convert.py --skill domain-name-brainstormer

# Dry run (preview without making changes)
python tools/convert.py --all --dry-run

# Show help
python tools/convert.py --help
```

#### How It Works

1. Finds all SKILL.md files in the repository
2. Analyzes each skill to determine tier:
   - **Tier 1**: Instruction-only (works with any model)
   - **Tier 2**: Uses tool calling (works best with advanced models)
   - **Tier 3**: Requires Claude Artifacts or MCP
3. Creates universal format files:
   - `system-prompt.md` - Instructions for the AI
   - `metadata.yaml` - Skill information
   - `api-example.json` - Usage template
   - `tools-schema.json` - Tool definitions (Tier 2 only)
4. Preserves bundled resources (scripts, references, assets)

#### Output Structure

```
universal/
├── tier-1-instruction-only/
│   └── skill-name/
│       ├── system-prompt.md
│       ├── metadata.yaml
│       ├── api-example.json
│       └── [original bundled resources]
├── tier-2-tool-enhanced/
│   └── skill-name/
│       ├── system-prompt.md
│       ├── metadata.yaml
│       ├── api-example.json
│       ├── tools-schema.json
│       ├── manual-version.md
│       └── [original bundled resources]
└── tier-3-claude-only/
    └── [reference documentation]
```

### validate.py

Validates that converted skills meet universal format requirements.

#### Features

- Checks required files exist
- Validates YAML frontmatter
- Detects Claude-specific language
- Verifies JSON schema
- Provides actionable error messages

#### Basic Usage

```bash
# Validate all converted skills
python tools/validate.py --all

# Validate specific skill
python tools/validate.py universal/tier-1-instruction-only/domain-name-brainstormer

# Detailed output
python tools/validate.py --all --verbose

# Show help
python tools/validate.py --help
```

#### What It Checks

**Tier 1 Skills:**
- ✅ Has `system-prompt.md`, `metadata.yaml`, `api-example.json`
- ✅ System prompt is provider-neutral (no "Claude" references)
- ✅ Metadata includes name, description, tier
- ✅ API example is valid JSON

**Tier 2 Skills:**
- ✅ All Tier 1 checks
- ✅ Has `tools-schema.json` with valid OpenAI tool format
- ✅ Has `manual-version.md` for fallback
- ✅ Tool descriptions are clear and complete

#### Example Output

```
✅ domain-name-brainstormer: All checks passed
⚠️  meeting-analyzer: Warning - Contains 'Claude should'
❌ invalid-skill: Missing required file: metadata.yaml

Summary:
  Passed: 45
  Warnings: 3
  Errors: 2
```

### sync-upstream.sh

Syncs this repository with the official anthropics/skills repository while protecting custom work.

#### Features

- Interactive mode with safety checks
- Creates backup before syncing
- Shows what will be merged
- Protects custom directories
- Offers to re-convert after sync

#### Basic Usage

```bash
# Interactive sync with safety checks
./tools/sync-upstream.sh

# The script will:
# 1. Check current branch
# 2. Create backup branch
# 3. Show what will be merged
# 4. Ask for confirmation
# 5. Merge upstream changes
# 6. Offer to re-convert skills
```

#### Protected Directories

These are NEVER overwritten by upstream:
- `universal/` - Universal format conversions
- `tools/` - Custom tools
- `docs/` - Enhanced documentation
- Custom skills not in upstream

#### What Gets Synced

✅ New skills from anthropics/skills  
✅ Updates to existing upstream skills  
✅ Bug fixes from official repository  

❌ Custom enhancements (these are protected)

#### Troubleshooting

If sync fails with conflicts:
1. The script creates a backup branch
2. Review conflicts manually
3. Resolve and commit
4. Re-run conversion if needed

### model-tester.py

Tests skills across different LLM providers and models.

#### Features

- Test with multiple providers (OpenRouter, Ollama)
- Compare model performance
- Validate compatibility
- Generate test reports

#### Basic Usage

```bash
# Quick test with Ollama
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --quick

# Test with multiple providers
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --providers openrouter ollama

# Test with specific models
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/domain-name-brainstormer \
  --models "llama3.2" "qwen2.5"

# Show help
python tools/model-tester.py --help
```

#### Prerequisites

For OpenRouter testing:
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

For Ollama testing:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download models
ollama pull llama3.2
```

#### Example Output

```
Testing: domain-name-brainstormer
Provider: Ollama

Model: llama3.2
✅ Response generated successfully
⏱️  Time: 2.3s
📊 Quality: Good (generates creative domain names)

Model: qwen2.5
✅ Response generated successfully
⏱️  Time: 1.8s
📊 Quality: Excellent (includes availability checks)

Summary: 2/2 models passed
```

## 🔄 Common Workflows

### Adding New Skills

```bash
# 1. Add skill to repository
cp -r my-new-skill ./

# 2. Convert to universal format
python tools/convert.py --skill my-new-skill

# 3. Validate conversion
python tools/validate.py universal/tier-1-instruction-only/my-new-skill

# 4. Test with different models
python tools/model-tester.py \
  --skill universal/tier-1-instruction-only/my-new-skill \
  --quick
```

### Updating from Upstream

```bash
# 1. Sync with anthropics/skills
./tools/sync-upstream.sh

# 2. Re-convert affected skills
python tools/convert.py --all

# 3. Validate conversions
python tools/validate.py --all
```

### Quality Checking

```bash
# Full quality check pipeline
python tools/convert.py --all && \
python tools/validate.py --all && \
python tools/model-tester.py --all --quick
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'yaml'"

Install PyYAML:
```bash
pip install PyYAML
```

### "Permission denied" when running sync-upstream.sh

Make script executable:
```bash
chmod +x tools/sync-upstream.sh
```

### Conversion creates wrong tier

Check skill content:
- Tier 1: Instructions only
- Tier 2: Includes tool/function calls
- Tier 3: Requires Claude Artifacts or MCP

Manually specify tier:
```bash
python tools/convert.py --skill my-skill --tier 1
```

### Validation fails with Claude references

Edit `system-prompt.md` to use provider-neutral language:
- ❌ "Claude should..."
- ✅ "The assistant should..."
- ❌ "In Claude.ai..."
- ✅ "In your AI interface..."

## 📚 Additional Resources

- [Universal Format Specification](../UNIVERSAL-FORMAT.md)
- [Model Compatibility Guide](../docs/MODEL-COMPATIBILITY.md)
- [Contributing Guidelines](../CONTRIBUTING.md)

## 🆘 Getting Help

- **Tool not working?** [Open an issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues)
- **Feature request?** [Start a discussion](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/discussions)
- **Questions?** [Join Discord](https://discord.com/invite/composio)

## 🤝 Contributing

Want to improve these tools?

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Happy automating!** 🚀
