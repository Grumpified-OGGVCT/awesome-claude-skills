# Skill Discovery Guide

**Problem:** "I have to know what to ask for in order to find it. Most of these I'd never know to even look. This isn't going to be useful at all."

**Solution:** Use the skill discovery tool to find what you need without knowing what exists!

## The Discovery Problem

You're absolutely right - the original setup had a major discoverability issue:

❌ **Before**: You had to:
- Browse through long README files
- Remember skill names exactly
- Know what exists before searching
- Manually read through directories

✅ **Now**: You can:
- Search by what you need (not what it's called)
- Browse by category or technology
- Discover skills interactively
- Get instant installation instructions

## Quick Start (3 Steps)

### 1. Generate the Index (One Time)

```bash
cd /path/to/awesome-claude-skills
python tools/index-skills.py
```

This scans all skills and creates a searchable index.

### 2. Start the Discovery Tool

```bash
python tools/discover.py
```

You'll see an interactive prompt:

```
🔍 Claude Skills Discovery Tool
================================================================================
Welcome! I'll help you find the perfect skill for your needs.
Total skills available: 27

Commands:
  search <keywords>  - Search for skills by keywords
  category <name>    - Show skills in a category
  tag <name>         - Filter by tag
  list               - List all skills
  categories         - Show all categories
  tags               - Show all tags
  help               - Show this help message
  quit               - Exit
================================================================================

> _
```

### 3. Find What You Need

Just describe what you want to do!

```
> search domain
> search pdf editor
> search meeting notes
> category Business
> tag web
```

## Common Use Cases

### "I need to work with documents but don't know what's available"

```bash
# Option 1: Search
$ python tools/discover.py --search "document"

# Option 2: Interactive
$ python tools/discover.py
> search document
> search pdf
> search excel
> category Document Processing
```

**Result**: You'll find:
- PDF manipulation tools
- Word document editors
- Excel spreadsheet tools
- PowerPoint generators
- And more!

### "What can help me with my business/marketing work?"

```bash
# Quick way
$ python tools/discover.py --category "Business & Marketing"

# Interactive way
$ python tools/discover.py
> categories
> category Business & Marketing
```

**Result**: You'll discover:
- Brand guidelines
- Competitive ad analysis
- Domain name brainstorming
- Lead research
- Internal communications

### "I'm a developer - what tools exist for me?"

```bash
$ python tools/discover.py --category "Development & Code Tools"
```

**Result**: Find tools for:
- Changelog generation
- MCP server building
- Web testing
- Artifacts creation
- And more!

### "Show me EVERYTHING"

```bash
# Command line
$ python tools/discover.py --list

# Interactive
$ python tools/discover.py
> list
```

Browse all 27+ skills with full details.

## Interactive Mode Deep Dive

### Searching

Search finds skills in names, descriptions, and tags:

```
> search meeting
🔍 Found 1 skill(s) matching 'meeting':

1. 📦 meeting-insights-analyzer
   Category: Communication & Writing
   Analyzes meeting transcripts to uncover behavioral patterns...

Type a number to see details, or refine your search
```

### Viewing Details

After a search, type the number to see full details:

```
> 1

================================================================================
📦 meeting-insights-analyzer
================================================================================

📁 Location: meeting-insights-analyzer
📂 Category: Communication & Writing

📝 Description:
Analyzes meeting transcripts to uncover behavioral patterns including 
conflict avoidance, speaking ratios, filler words, and leadership style.

🏷️  Tags: analysis, communication, content, meeting, writing

📄 Skill file: meeting-insights-analyzer/SKILL.md

📥 Installation:
   Claude.ai: Upload the file 'meeting-insights-analyzer/SKILL.md'
   Claude Code: cp -r meeting-insights-analyzer ~/.config/claude-code/skills/
   Universal (Any LLM): See universal/tier-1-instruction-only/meeting-insights-analyzer/

================================================================================
```

### Browsing by Category

```
> categories
📂 Available Categories:
  1. Business & Marketing (5 skills)
  2. Communication & Writing (2 skills)
  3. Creative & Media (5 skills)
  4. Development & Code Tools (5 skills)
  5. Document Processing (4 skills)
  6. Other (3 skills)
  7. Productivity & Organization (3 skills)

> category Creative & Media
📂 Skills in 'Creative & Media' (5):

1. 📦 canvas-design
   Category: Creative & Media
   Create beautiful visual art in .png and .pdf documents...
   
[Shows all 5 creative skills]
```

### Filtering by Tag

```
> tags
🏷️  Available Tags:
  analysis (12)  automation (3)  business (5)  code (15)  
  communication (8)  content (10)  creative (8)  data (12)
  design (15)  document (12)  file (18)  git (8)
  [... more tags ...]

> tag git
🏷️  Skills tagged with 'git' (8):

[Shows all git-related skills]
```

## Command-Line Mode (For Scripts)

If you know what you want, skip interactive mode:

```bash
# Quick searches
python tools/discover.py --search "domain name"
python tools/discover.py --search "pdf"

# Category browsing
python tools/discover.py --categories
python tools/discover.py --category "Business & Marketing"

# List everything
python tools/discover.py --list
```

Perfect for:
- Shell scripts
- Documentation
- Quick lookups
- CI/CD pipelines

## Pro Tips

### 1. Start Broad, Then Narrow

```
> categories              # See what's available
> category Business       # Pick one
> 3                       # Check out skill #3
```

### 2. Use Multiple Keywords

```
> search domain web       # Multiple terms
> search meeting analysis # More specific
> search pdf edit         # Technology + action
```

### 3. Explore Tags

```
> tags                    # See all options
> tag automation          # Filter to automation tools
> tag web                 # Filter to web-related
```

### 4. Compare Similar Skills

```
> search document
> 1                       # Check first one
> 2                       # Compare with second
> 3                       # And the third
```

## Installation After Discovery

Once you find a skill you want, the tool shows you exactly how to install it:

### For Claude.ai Users
```
📥 Installation:
   Claude.ai: Upload the file 'domain-name-brainstormer/SKILL.md'
```

1. Go to Claude.ai
2. Click the skill icon (🧩)
3. Upload the SKILL.md file shown
4. Done!

### For Claude Code Users
```
📥 Installation:
   Claude Code: cp -r domain-name-brainstormer ~/.config/claude-code/skills/
```

Just copy-paste that command in your terminal.

### For Other LLM Users
```
📥 Installation:
   Universal (Any LLM): See universal/tier-1-instruction-only/domain-name-brainstormer/
```

Check the universal format directory for OpenAI-compatible versions.

## Troubleshooting

### "Index not found"

Run the indexer first:
```bash
python tools/index-skills.py
```

### "No skills found"

Try:
- Broader keywords: "document" instead of "docx"
- Check available tags: `> tags`
- Browse categories: `> categories`
- List everything: `> list`

### "Tool won't start"

Check you have Python 3.8+:
```bash
python --version
python tools/index-skills.py  # Rebuild index
python tools/discover.py      # Try again
```

## What Makes This Better?

### Before: Manual Browsing ❌
1. Open README.md (100+ lines)
2. Scroll to find skills section
3. Read through every skill
4. Hope you find what you need
5. Remember the path
6. Look up installation instructions

### After: Smart Discovery ✅
1. `python tools/discover.py`
2. `> search pdf`
3. `> 1` (see details)
4. Copy the installation command
5. Done!

## Examples of What You Can Find

**Real searches that work:**

- "domain" → Find domain name brainstorming
- "pdf" → Find PDF editing and creation tools
- "meeting" → Find meeting analysis tools  
- "git" → Find version control helpers
- "video" → Find video downloading tools
- "invoice" → Find invoice organization
- "brand" → Find brand guideline tools
- "test" → Find testing frameworks
- "lead" → Find lead research tools
- "slack" → Find Slack integration tools

**Can't think of keywords? Use categories:**

- "Business & Marketing" → All business tools
- "Development" → All coding tools
- "Creative" → All creative/design tools
- "Document" → All document processors

## Keep It Updated

The index is automatically updated, but you can manually refresh:

```bash
# After adding new skills
python tools/index-skills.py

# Verify the update
python tools/discover.py --search "new skill name"
```

## Summary

**You said**: "I have to know what to ask for in order to find it."

**We built**: A discovery tool where you describe what you need, and it finds matching skills.

**No more**:
- ❌ Guessing skill names
- ❌ Reading long READMEs  
- ❌ Manual directory browsing
- ❌ Missing useful skills

**Instead**:
- ✅ Search by purpose
- ✅ Browse by category
- ✅ Filter by technology
- ✅ Discover interactively

**Try it now**:
```bash
python tools/index-skills.py
python tools/discover.py
```

**This should actually be useful!** 🎉
