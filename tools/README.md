# Tools

> **🚀 GrumpiFied Enhancement** - All tools in this directory are custom additions created by Grumpified-OGGVCT. These automation tools are NOT part of the upstream ComposioHQ/awesome-claude-skills repository.

Automation tools for working with Claude Skills and the universal format.

## 🎯 Attribution

**All tools here are GrumpiFied original creations:**
- NLP-powered discovery (`nlp-discover.py`)
- Universal format conversion (`convert.py`)
- YAML validation (`validate-skill-yaml.py`, `validate.py`)
- Skill index generation (`generate-skill-index.py`, `index-skills.py`)
- Upstream sync automation (`sync-upstream.sh`)
- Multi-model testing (`model-tester.py`)
- Interactive discovery (`discover.py`, `find-skill`)

These tools enable the enhanced functionality that makes this fork special.

📋 **[See Full Attribution Guide](../ATTRIBUTIONS.md)** for complete details.

## 🛠️ Available Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| [generate-skill-index.py](#generate-skill-indexpy) 🆕 | Auto-generate SKILL-INDEX.json | `python tools/generate-skill-index.py` |
| [validate-skill-yaml.py](#validate-skill-yamlpy) 🆕 | Validate YAML frontmatter | `python tools/validate-skill-yaml.py` |
| [nlp-discover.py](#nlp-discoverpy) 🤖 | NLP-powered semantic search | `python tools/nlp-discover.py "query"` |
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

### generate-skill-index.py

🆕 **Auto-Generate SKILL-INDEX.json**

#### Purpose

Automatically generates the complete `SKILL-INDEX.json` file from all `SKILL.md` files in the repository. This is the **authoritative** skill index used throughout the project.

#### Features

- 🔍 **Auto-discovery** - Scans all `*/SKILL.md` files automatically
- 🏷️ **Smart categorization** - Auto-assigns categories based on name/description/tags
- 📊 **Complete metadata** - Extracts name, description, tags, requires from YAML
- 🔄 **Idempotent** - Safe to run multiple times
- ✅ **Validation** - Ensures all YAML frontmatter is valid before generation

#### Usage

```bash
# Generate SKILL-INDEX.json at repository root
python tools/generate-skill-index.py
```

#### Output

```
Generating SKILL-INDEX.json...
Root directory: /home/user/awesome-claude-skills
Found 107 SKILL.md files

✅ Generated /home/user/awesome-claude-skills/SKILL-INDEX.json
   Total skills: 107
   Categories: 8
   Categories: App Automation, Business & Marketing, Communication & Writing, ...
```

#### Auto-Categorization Rules

Skills are categorized based on:
1. **Directory name patterns** - e.g., `*-automation` → App Automation
2. **Description keywords** - e.g., "code", "github" → Development & Code Tools
3. **Tags** - e.g., `[document, pdf]` → Document Processing
4. **Default fallback** - "Other" category if no match

**Categories:**
- App Automation (78 skills)
- Business & Marketing
- Communication & Writing
- Creative & Media
- Development & Code Tools
- Document Processing
- Other
- Productivity & Organization

#### When to Run

Run this tool when:
- ✅ Adding new skills to the repository
- ✅ Updating skill descriptions or metadata
- ✅ SKILL-INDEX.json is missing or outdated
- ✅ After merging upstream changes

**Note:** This tool is automatically run by CI/CD on push to main/master.

### validate-skill-yaml.py

🆕 **Validate YAML Frontmatter in All Skills**

#### Purpose

Validates YAML frontmatter syntax and required fields in all `SKILL.md` files. Ensures consistency and catches errors before they reach production.

#### Features

- ✅ **Syntax validation** - Detects YAML parse errors
- ✅ **Required fields** - Checks for `name` and `description`
- ✅ **Type checking** - Validates data types (strings, lists, dicts)
- ✅ **Clear errors** - Shows exactly which files have issues
- ✅ **CI/CD ready** - Exit codes for automation

#### Usage

```bash
# Validate all SKILL.md files
python tools/validate-skill-yaml.py

# Use in CI/CD (exits with code 1 on errors)
python tools/validate-skill-yaml.py || exit 1
```

#### Example Output

**Success:**
```
Validating 107 SKILL.md files...

======================================================================
✅ All 107 SKILL.md files are valid!
```

**With Errors:**
```
Validating 107 SKILL.md files...

❌ my-skill/SKILL.md
   - Missing required field: 'description'
   - Field 'tags' must be a list

❌ another-skill/SKILL.md
   - YAML parse error: found unexpected ':'

======================================================================
❌ Found 3 errors in 2 files
   Valid files: 105/107
```

#### Validation Rules

**Required Fields:**
- `name` (string) - Skill identifier
- `description` (string) - Brief description of what skill does

**Optional Fields:**
- `tags` (list of strings) - Searchable keywords
- `requires` (dict) - External dependencies (e.g., MCP servers)
- `category` (string) - Manual category override

**YAML Syntax:**
- Must start and end with `---` delimiters
- Proper indentation (2 spaces)
- Quote strings with colons: `description: "This: works"`

#### Common Errors & Fixes

**Error: "No YAML frontmatter found"**
```yaml
# ❌ Missing delimiters
name: my-skill

# ✅ Correct format
---
name: my-skill
description: Brief description
---
```

**Error: "YAML parse error: found unexpected ':'"**
```yaml
# ❌ Unquoted colon
description: This does: something

# ✅ Quote the string
description: "This does: something"
```

**Error: "Field 'tags' must be a list"**
```yaml
# ❌ Wrong type
tags: web

# ✅ Use list format
tags: [web]
# or
tags:
  - web
  - code
```

#### Integration

This tool is automatically run by:
- 🔄 **CI/CD** - On every PR and push (`.github/workflows/validate-skills.yml`)
- 🪝 **Pre-commit hooks** - Optional local validation before commit
- 📦 **generate-skill-index.py** - Validates before generating index

### nlp-discover.py

🤖 **AI-Powered Semantic Search using Gemini 3 Flash Preview**

#### Why Use This?

The most advanced skill discovery method! Uses LLM-powered natural language understanding to:
- **Understand intent** - "I need help with documents" → finds PDF, Word, Excel tools
- **Interpret queries** - Clarifies vague searches automatically
- **Generate explanations** - AI-written descriptions of each skill
- **Smart recommendations** - Suggests related skills you might not know about

This solves the original problem: "I have to know what to ask for in order to find it."  
Now you just describe what you need in plain English!

#### Features

- 🧠 **Semantic search** - Understands meaning, not just keywords
- 💡 **Query interpretation** - "business stuff" → "business and marketing tools"
- 📝 **AI explanations** - Detailed, helpful skill descriptions
- ⚡ **Powered by Gemini 3 Flash Preview** - Fast and accurate
- 🔄 **Auto-fallback** - Uses basic search if API unavailable

#### Prerequisites

1. **API Key** - Set one of (in order of preference):
   ```bash
   export OLLAMA_TURBO_CLOUD_API_KEY='your-key'   # Fastest (recommended)
   export OLLAMA_PROXY_API_KEY='your-key'         # Alternative
   export OLLAMA_API_KEY='your-key'               # Alternative
   ```

2. **Install dependencies**:
   ```bash
   pip install openai
   ```

#### Usage

```bash
# Natural language search
python tools/nlp-discover.py "I need to work with documents"
python tools/nlp-discover.py "help me with my business"
python tools/nlp-discover.py "tools for my website"

# Get AI-generated explanations
python tools/nlp-discover.py "pdf tools" --explain

# More results
python tools/nlp-discover.py "business tools" --top 10

# Specify custom API key
python tools/nlp-discover.py "query" --api-key "your-key"

# Specify custom endpoint
python tools/nlp-discover.py "query" --endpoint "https://custom.endpoint/v1"
```

#### Real Examples

**Example 1: Vague query gets interpreted**
```bash
$ python tools/nlp-discover.py "something for my website"

🔍 Query: "something for my website"
💡 You're looking for tools to test, analyze, or build web applications.

Found 3 relevant skill(s):

1. 📦 webapp-testing
   Testing and validation for web applications
   
2. 📦 artifacts-builder
   Build complex web artifacts with React and Tailwind
   
3. 📦 domain-name-brainstormer
   Find the perfect domain name for your project
```

**Example 2: Business query with explanation**
```bash
$ python tools/nlp-discover.py "I need help with my business" --explain

🔍 Query: "I need help with my business"
💡 You're looking for business and marketing tools like lead research,
    competitive analysis, and brand guidelines.

Found 5 relevant skill(s):

1. 📦 lead-research-assistant
   📝 Detailed Explanation:
      This skill helps you identify and qualify high-quality leads by
      analyzing your product, searching for target companies, and
      providing actionable outreach strategies.
      
      Use this when you're prospecting new clients, building a sales
      pipeline, or need to research potential customers at scale.
      
      Sales teams, business development professionals, and startups
      looking to grow their customer base will find this invaluable.
```

#### How It Works

1. **Query Interpretation**: Gemini analyzes your query and clarifies the intent
2. **Context Building**: Creates a summary of all available skills
3. **Semantic Matching**: LLM ranks skills by relevance to your need
4. **Result Generation**: Returns top matches with installation instructions
5. **Explanation (Optional)**: Generates AI-written skill descriptions

#### Comparison: NLP vs Basic Search

| Feature | NLP Search | Basic Search |
|---------|-----------|--------------|
| Understands intent | ✅ Yes | ❌ No (keywords only) |
| Vague queries | ✅ Interprets | ❌ May fail |
| Explanations | ✅ AI-generated | ❌ Static description |
| Related skills | ✅ Smart suggestions | ❌ Exact matches only |
| Setup | API key required | None needed |
| Speed | ~1-2 seconds | Instant |

**When to use NLP:** Exploring, vague needs, want recommendations  
**When to use basic:** Know exact keyword, offline, API unavailable

#### Configuration

**Available Endpoints** (auto-detected from API key):

| API Key | Endpoint | Speed |
|---------|----------|-------|
| `OLLAMA_TURBO_CLOUD_API_KEY` | `turbo.ollama.cloud` | Fastest ⚡ |
| `OLLAMA_PROXY_API_KEY` | `proxy.ollama.cloud` | Fast |
| `OLLAMA_API_KEY` | `cloud.ollama.ai` | Standard |

**Model Parameters:**

```python
semantic_search_temp = 0.3    # Consistent recommendations
explain_temp = 0.5            # Natural explanations  
interpret_temp = 0.4          # Accurate interpretation
max_tokens = 500              # Sufficient for JSON response
```

#### Troubleshooting

**"No API key found"**
```bash
export OLLAMA_TURBO_CLOUD_API_KEY='your-key-here'
```

**"openai library not installed"**
```bash
pip install openai
```

**"NLP search failed"**
- Tool automatically falls back to basic keyword search
- Check API key validity
- Verify internet connection

#### See Also

- [NLP Discovery Guide](../docs/NLP-DISCOVERY.md) - Full documentation
- [GitHub Workflow](../.github/workflows/nlp-discovery-demo.yml) - CI/CD example
- [discover.py](#discoverpy) - Basic search alternative

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

Syncs this repository with [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) while protecting GrumpiFied customizations.

#### Features

- Interactive mode with safety checks
- Creates backup before syncing
- Shows what will be merged
- Protects GrumpiFied directories
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
- `universal/` - Universal format conversions (GrumpiFied)
- `tools/` - Custom automation tools (GrumpiFied)
- `docs/` - Enhanced documentation (GrumpiFied)
- `.github/` - CI/CD workflows (GrumpiFied)
- Custom skills not in upstream

#### What Gets Synced

✅ New automation skills from ComposioHQ/awesome-claude-skills  
✅ Updates to existing Composio skills  
✅ Bug fixes from official repository  

❌ GrumpiFied enhancements (these are protected)

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
