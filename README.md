<h1 align="center">Awesome Claude Skills</h1>

<p align="center">
<a href="https://platform.composio.dev/?utm_source=Github&utm_medium=Youtube&utm_campaign=2025-11&utm_content=AwesomeSkills">
  <img width="1280" height="640" alt="Composio banner" src="https://github.com/user-attachments/assets/adb3f57a-2706-4329-856f-059a32059d48">
</a>


</p>

<p align="center">
  <a href="https://awesome.re">
    <img src="https://awesome.re/badge.svg" alt="Awesome" />
  </a>
  <a href="https://makeapullrequest.com">
    <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square" alt="PRs Welcome" />
  </a>
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square" alt="License: Apache-2.0" />
  </a>
</p>
<div>
<p align="center">
  <a href="https://twitter.com/composio">
    <img src="https://img.shields.io/badge/Follow on X-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" />
  </a>
  <a href="https://www.linkedin.com/company/composiohq/">
    <img src="https://img.shields.io/badge/Follow on LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow on LinkedIn" />
  </a>
  <a href="https://discord.com/invite/composio">
    <img src="https://img.shields.io/badge/Join our Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white" alt="Join our Discord" />
  </a>
  </p>
</div>

<p align="center"><strong>The most comprehensive collection of Claude Skills - reusable AI workflows that supercharge your productivity.</strong></p>

<p align="center">
  <em>Stop repeating instructions. Start using skills.</em>
</p>

---

## 🎯 What Is This Repository?

**Awesome Claude Skills** is a curated collection of **200+ ready-to-use AI workflows** (called "skills") that teach Claude AI how to perform specialized tasks consistently and professionally. Think of skills as expert training modules that transform Claude from a general assistant into a domain specialist.

### What You'll Find Here

- **🎓 Pre-built Skills**: 200+ production-ready skills covering development, business, creative work, and more
- **🌍 Universal Format**: Works with Claude, GPT-4, Llama, Gemini, and any OpenAI-compatible LLM
- **📚 Learning Resources**: Guides for creating your own custom skills
- **🛠️ Tools & Scripts**: Automation for converting, validating, and testing skills
- **💡 Real-World Examples**: Proven workflows from actual users and companies

**✨ NEW: Universal Format** - All skills now available in OpenAI-compatible format for use with OpenRouter, Ollama, and other LLM providers! See [Universal Skills](#universal-llm-skills-format) below.

> If you want your skills to take actions across 500+ apps, wire them up with [Composio](https://platform.composio.dev/?utm_source=Github&utm_medium=Youtube&utm_campaign=2025-11&utm_content=AwesomeSkills)

---

## 👥 Who Is This For?

This repository is perfect for:

- **Developers** building applications with Claude API, Claude Code, or other LLMs
- **Product Teams** automating workflows like changelogs, documentation, or competitive research
- **Content Creators** generating consistent, high-quality content with AI assistance
- **Business Users** leveraging AI for lead research, domain brainstorming, or meeting analysis
- **AI Enthusiasts** learning how to build effective AI workflows and prompts
- **Anyone** who uses Claude regularly and wants to save time with reusable workflows

---

## 🚀 Quick Start

### Option 1: Use Skills with Claude.ai (Easiest)

1. Browse the [Skills](#skills) section below
2. Pick a skill that matches your needs (e.g., [Domain Name Brainstormer](./domain-name-brainstormer/))
3. Click the skill icon (🧩) in Claude.ai chat
4. Add the skill or upload the SKILL.md file
5. Claude will automatically use it when relevant!

**Example**: "Help me brainstorm domain names for my startup" → Claude uses the Domain Name Brainstormer skill

### Option 2: Use Skills with Claude Code

```bash
# Install a skill
mkdir -p ~/.config/claude-code/skills/
cp -r domain-name-brainstormer ~/.config/claude-code/skills/

# Start Claude Code - skills load automatically
claude
```

### Option 3: Use Skills with Any LLM (Universal Format)

**Note**: Skills must be converted to universal format first. See [Universal Skills Format](#universal-llm-skills-format) for details.

```python
from openai import OpenAI

# Works with OpenRouter, Ollama, or any OpenAI-compatible API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # or http://localhost:11434/v1 for Ollama
    api_key="YOUR_API_KEY"
)

# Load any skill (example assumes skills are already converted)
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    skill = f.read()

# Use it with any model!
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or "gpt-4o", "llama3.2", etc.
    messages=[
        {"role": "system", "content": skill},
        {"role": "user", "content": "Suggest domain names for my AI startup"}
    ]
)
```

See [Universal Skills Format](#universal-llm-skills-format) for more details.

---


## Contents

- [🎯 What Is This Repository?](#-what-is-this-repository)
- [👥 Who Is This For?](#-who-is-this-for)
- [🚀 Quick Start](#-quick-start)
- [💡 What Are Claude Skills?](#-what-are-claude-skills)
- [Universal LLM Skills Format](#universal-llm-skills-format) ✨ **NEW**
- [Automated Upstream Sync](#automated-upstream-sync)
- [Skills](#skills)
  - [Document Processing](#document-processing)
  - [Development & Code Tools](#development--code-tools)
  - [Data & Analysis](#data--analysis)
  - [Business & Marketing](#business--marketing)
  - [Communication & Writing](#communication--writing)
  - [Creative & Media](#creative--media)
  - [Productivity & Organization](#productivity--organization)
  - [Collaboration & Project Management](#collaboration--project-management)
  - [Security & Systems](#security--systems)
- [Getting Started](#getting-started)
- [Creating Skills](#creating-skills)
- [Contributing](#contributing)
- [Resources](#resources)
- [📚 Frequently Asked Questions](#-frequently-asked-questions)
- [License](#license)

**👉 New to Claude Skills?** Start with our comprehensive [Getting Started Guide](GETTING_STARTED.md)!

## 💡 What Are Claude Skills?

**Claude Skills** are structured instruction sets that teach AI models how to perform specialized tasks consistently and professionally. They're like training manuals for AI - reusable workflows that transform a general-purpose assistant into a domain expert.

### Real-World Examples

**Without a skill:**
> "Help me come up with a domain name"
> 
> Claude: "How about mycompany.com or projectname.io?"

**With the Domain Name Brainstormer skill:**
> "Help me come up with a domain name"
>
> Claude: "I'll help you brainstorm domain names! First, tell me about your project:
> - What does it do?
> - Who is it for?
> - Any preferred keywords or style?"
>
> [Then generates 15+ creative options, checks availability across multiple TLDs, explains naming rationale, and provides branding insights]

### Why Use Skills?

- **🎯 Consistency**: Get the same high-quality output every time
- **⚡ Speed**: No need to explain requirements repeatedly
- **🧠 Expertise**: Leverage proven workflows from experts
- **🔄 Reusability**: Write once, use across all Claude platforms
- **📦 Portability**: Works with Claude.ai, Claude Code, and API
- **🌐 Universal**: Now compatible with any OpenAI-compatible LLM

### How Skills Work

1. **Instructions**: Detailed step-by-step workflows in SKILL.md
2. **Scripts** (optional): Helper tools for complex operations
3. **References** (optional): Domain knowledge and documentation
4. **Assets** (optional): Templates, examples, or resources

Skills automatically activate when Claude detects a relevant task, ensuring expertise is applied at the right time.

## Universal LLM Skills Format

🎯 **Skills now work with any OpenAI-compatible LLM!**

All skills in this repository are available in a universal format that works with:
- ✅ **OpenRouter** - Access 100+ models (GPT-4, Claude, Gemini, Llama, etc.) through one API
- ✅ **Ollama** - Run models locally on your machine (completely free and private)
- ✅ **Direct APIs** - OpenAI, Anthropic, and other compatible providers

### Why Universal Format?

Instead of being locked into Claude-specific features, the universal format uses standard **system prompts + tool calling** that work everywhere. This means:

- 🌍 **One skill, many models** - Use the same skill across different LLM providers
- 💰 **Cost flexibility** - Choose from free, budget, or premium models
- 🔒 **Privacy options** - Run locally with Ollama or use cloud APIs
- 🚀 **Easy migration** - Switch providers without rewriting skills

### Quick Start

```python
# Example: Using a skill with OpenRouter
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="YOUR_OPENROUTER_KEY"
)

# Load any universal skill
with open("universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md") as f:
    system_prompt = f.read()

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",  # or any model!
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Suggest domain names for a project management tool"}
    ]
)
```

### Three Skill Tiers

**Tier 1: Instruction-Only (90% of skills)** 📝
- Pure instructions and workflows
- Works with ANY model
- Examples: domain-name-brainstormer, meeting-insights-analyzer, brainstorming

**Tier 2: Tool-Enhanced (10% of skills)** 🔧
- Includes tool/function calling
- Works best with Claude 3.5, GPT-4o, Gemini 1.5 Pro
- Includes manual fallback for models without tool support
- Examples: pdf editor, file organizer

**Tier 3: Claude-Only (Reference)** 🎨
- Requires Claude Artifacts or MCP
- Kept as reference for Claude users
- Examples: canvas design, artifacts builder

### Documentation

- **[OpenRouter Setup Guide](docs/OPENROUTER-SETUP.md)** - Use 100+ models through one API
- **[Ollama Setup Guide](docs/OLLAMA-SETUP.md)** - Run models locally (free & private)
- **[Model Compatibility Guide](docs/MODEL-COMPATIBILITY.md)** - Which models work best for each skill
- **[Migration Guide](docs/MIGRATION-GUIDE.md)** - Convert your own skills to universal format

### Tools

```bash
# Convert skills to universal format
python tools/convert.py --all

# Validate converted skills
python tools/validate.py --all

# Sync with upstream repository
./tools/sync-upstream.sh
```

### Backward Compatibility

✅ **Original skills remain unchanged** - The universal format is derived from originals
✅ **Stays in sync with upstream** - Easy to pull updates from anthropics/skills
✅ **No breaking changes** - Both formats coexist peacefully

## Automated Upstream Sync

This repository automatically stays synchronized with the official [anthropics/skills](https://github.com/anthropics/skills) repository while protecting all custom enhancements.

### How It Works

🤖 **Automated Synchronization**
- Runs every 6 hours (4 times daily) to check for upstream updates
- Can also be triggered manually from the Actions tab
- Uses fast-forward-only merge strategy for safety

🛡️ **Safety First**
- **Never overwrites custom work** - All custom directories are protected:
  - `universal/` - Universal LLM Skills Format and conversions
  - `tools/` - Custom tools (convert.py, validate.py, sync-upstream.sh)
  - `docs/` - Enhanced documentation and guides
  - Custom skill folders not in upstream
- **Automatic PR on conflicts** - If changes can't be merged cleanly, a pull request is automatically created for manual review
- **No force pushes** - Human review required for any conflicts

### What Gets Synced

✅ **New skills** from anthropics/skills main branch  
✅ **Updates to existing skills** from upstream  
✅ **Bug fixes and improvements** from the official repository  

❌ **Never synced** (protected):
- Universal format conversions in `universal/`
- Custom tools and scripts in `tools/`
- Enhanced documentation in `docs/`
- Custom skills not in upstream (changelog-generator, domain-name-brainstormer, etc.)

### Manual Sync (Fallback)

You can always sync manually using the provided script:

```bash
# Interactive manual sync with safety checks
./tools/sync-upstream.sh
```

This script:
- Creates a backup branch before syncing
- Shows you what will be merged before proceeding
- Prompts for confirmation at each step
- Offers to re-convert skills after sync

### When Human Review Is Needed

The automation creates a pull request when:
- 🔄 **Merge conflicts** occur between upstream and custom changes
- 🚫 **Non-fast-forward** merge is required
- ⚠️ **Protected files** would be modified by upstream

Simply review the auto-generated PR, resolve any conflicts, and merge when ready.

### Monitoring

Check the [Actions tab](../../actions) to:
- View sync history and results
- Manually trigger a sync
- Check for any auto-generated PRs needing review

## Skills

### Document Processing

- [docx](https://github.com/anthropics/skills/tree/main/skills/docx) - Create, edit, analyze Word docs with tracked changes, comments, formatting.
- [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) - Extract text, tables, metadata, merge & annotate PDFs.
- [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) - Read, generate, and adjust slides, layouts, templates.
- [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) - Spreadsheet manipulation: formulas, charts, data transformations.
- [Markdown to EPUB Converter](https://github.com/smerchek/claude-epub-skill) - Converts markdown documents and chat summaries into professional EPUB ebook files. *By [@smerchek](https://github.com/smerchek)*

### Development & Code Tools

- [artifacts-builder](https://github.com/anthropics/skills/tree/main/web-artifacts-builder) - Suite of tools for creating elaborate, multi-component claude.ai HTML artifacts using modern frontend web technologies (React, Tailwind CSS, shadcn/ui).
- [aws-skills](https://github.com/zxkane/aws-skills) - AWS development with CDK best practices, cost optimization MCP servers, and serverless/event-driven architecture patterns.
- [Changelog Generator](./changelog-generator/) - Automatically creates user-facing changelogs from git commits by analyzing history and transforming technical commits into customer-friendly release notes.
- [Claude Code Terminal Title](https://github.com/bluzername/claude-code-terminal-title) - Gives each Claud-Code terminal window a dynamic title that describes the work being done so you don't lose track of what window is doing what.
- [D3.js Visualization](https://github.com/chrisvoncsefalvay/claude-d3js-skill) - Teaches Claude to produce D3 charts and interactive data visualizations. *By [@chrisvoncsefalvay](https://github.com/chrisvoncsefalvay)*
- [FFUF Web Fuzzing](https://github.com/jthack/ffuf_claude_skill) - Integrates the ffuf web fuzzer so Claude can run fuzzing tasks and analyze results for vulnerabilities. *By [@jthack](https://github.com/jthack)*
- [finishing-a-development-branch](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) - Guides completion of development work by presenting clear options and handling chosen workflow.
- [iOS Simulator](https://github.com/conorluddy/ios-simulator-skill) - Enables Claude to interact with iOS Simulator for testing and debugging iOS applications. *By [@conorluddy](https://github.com/conorluddy)*
- [MCP Builder](./mcp-builder/) - Guides creation of high-quality MCP (Model Context Protocol) servers for integrating external APIs and services with LLMs using Python or TypeScript.
- [move-code-quality-skill](https://github.com/1NickPappas/move-code-quality-skill) - Analyzes Move language packages against the official Move Book Code Quality Checklist for Move 2024 Edition compliance and best practices.
- [Playwright Browser Automation](https://github.com/lackeyjb/playwright-skill) - Model-invoked Playwright automation for testing and validating web applications. *By [@lackeyjb](https://github.com/lackeyjb)*
- [prompt-engineering](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/customaize-agent/skills/prompt-engineering) - Teaches well-known prompt engineering techniques and patterns, including Anthropic best practices and agent persuasion principles.
- [pypict-claude-skill](https://github.com/omkamal/pypict-claude-skill) - Design comprehensive test cases using PICT (Pairwise Independent Combinatorial Testing) for requirements or code, generating optimized test suites with pairwise coverage.
- [Skill Creator](./skill-creator/) - Provides guidance for creating effective Claude Skills that extend capabilities with specialized knowledge, workflows, and tool integrations.
- [Skill Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) - Automatically converts any documentation website into a Claude AI skill in minutes. *By [@yusufkaraaslan](https://github.com/yusufkaraaslan)*
- [software-architecture](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/ddd/skills/software-architecture) - Implements design patterns including Clean Architecture, SOLID principles, and comprehensive software design best practices.
- [subagent-driven-development](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/sadd/skills/subagent-driven-development) - Dispatches independent subagents for individual tasks with code review checkpoints between iterations for rapid, controlled development.
- [test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) - Use when implementing any feature or bugfix, before writing implementation code.
- [using-git-worktrees](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/) - Creates isolated git worktrees with smart directory selection and safety verification.
- [Webapp Testing](./webapp-testing/) - Tests local web applications using Playwright for verifying frontend functionality, debugging UI behavior, and capturing screenshots.

### Data & Analysis

- [CSV Data Summarizer](https://github.com/coffeefuelbump/csv-data-summarizer-claude-skill) - Automatically analyzes CSV files and generates comprehensive insights with visualizations without requiring user prompts. *By [@coffeefuelbump](https://github.com/coffeefuelbump)*
- [root-cause-tracing](https://github.com/obra/superpowers/tree/main/skills/root-cause-tracing) - Use when errors occur deep in execution and you need to trace back to find the original trigger.

### Business & Marketing

- [Brand Guidelines](./brand-guidelines/) - Applies Anthropic's official brand colors and typography to artifacts for consistent visual identity and professional design standards.
- [Competitive Ads Extractor](./competitive-ads-extractor/) - Extracts and analyzes competitors' ads from ad libraries to understand messaging and creative approaches that resonate.
- [Domain Name Brainstormer](./domain-name-brainstormer/) - Generates creative domain name ideas and checks availability across multiple TLDs including .com, .io, .dev, and .ai extensions.
- [Internal Comms](./internal-comms/) - Helps write internal communications including 3P updates, company newsletters, FAQs, status reports, and project updates using company-specific formats.
- [Lead Research Assistant](./lead-research-assistant/) - Identifies and qualifies high-quality leads by analyzing your product, searching for target companies, and providing actionable outreach strategies.

### Communication & Writing

- [article-extractor](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/article-extractor) - Extract full article text and metadata from web pages.
- [brainstorming](https://github.com/obra/superpowers/tree/main/skills/brainstorming) - Transform rough ideas into fully-formed designs through structured questioning and alternative exploration.
- [Content Research Writer](./content-research-writer/) - Assists in writing high-quality content by conducting research, adding citations, improving hooks, and providing section-by-section feedback.
- [family-history-research](https://github.com/emaynard/claude-family-history-research-skill) - Provides assistance with planning family history and genealogy research projects.
- [Meeting Insights Analyzer](./meeting-insights-analyzer/) - Analyzes meeting transcripts to uncover behavioral patterns including conflict avoidance, speaking ratios, filler words, and leadership style.
- [NotebookLM Integration](https://github.com/PleasePrompto/notebooklm-skill) - Lets Claude Code chat directly with NotebookLM for source-grounded answers based exclusively on uploaded documents. *By [@PleasePrompto](https://github.com/PleasePrompto)*

### Creative & Media

- [Canvas Design](./canvas-design/) - Creates beautiful visual art in PNG and PDF documents using design philosophy and aesthetic principles for posters, designs, and static pieces.
- [Image Enhancer](./image-enhancer/) - Improves image and screenshot quality by enhancing resolution, sharpness, and clarity for professional presentations and documentation.
- [Slack GIF Creator](./slack-gif-creator/) - Creates animated GIFs optimized for Slack with validators for size constraints and composable animation primitives.
- [Theme Factory](./theme-factory/) - Applies professional font and color themes to artifacts including slides, docs, reports, and HTML landing pages with 10 pre-set themes.
- [Video Downloader](./video-downloader/) - Downloads videos from YouTube and other platforms for offline viewing, editing, or archival with support for various formats and quality options.
- [youtube-transcript](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/youtube-transcript) - Fetch transcripts from YouTube videos and prepare summaries.

### Productivity & Organization

- [File Organizer](./file-organizer/) - Intelligently organizes files and folders by understanding context, finding duplicates, and suggesting better organizational structures.
- [Invoice Organizer](./invoice-organizer/) - Automatically organizes invoices and receipts for tax preparation by reading files, extracting information, and renaming consistently.
- [kaizen](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/kaizen/skills/kaizen) - Applies continuous improvement methodology with multiple analytical approaches, based on Japanese Kaizen philosophy and Lean methodology.
- [n8n-skills](https://github.com/haunchen/n8n-skills) - Enables AI assistants to directly understand and operate n8n workflows.
- [Raffle Winner Picker](./raffle-winner-picker/) - Randomly selects winners from lists, spreadsheets, or Google Sheets for giveaways and contests with cryptographically secure randomness.
- [ship-learn-next](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/ship-learn-next) - Skill to help iterate on what to build or learn next, based on feedback loops.
- [tapestry](https://github.com/michalparkola/tapestry-skills-for-claude-code/tree/main/tapestry) - Interlink and summarize related documents into knowledge networks.

### Collaboration & Project Management

- [git-pushing](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/git-pushing) - Automate git operations and repository interactions.
- [review-implementing](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/review-implementing) - Evaluate code implementation plans and align with specs.
- [test-fixing](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/engineering-workflow-plugin/skills/test-fixing) - Detect failing tests and propose patches or fixes.

### Security & Systems

- [computer-forensics](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/computer-forensics) - Digital forensics analysis and investigation techniques.
- [file-deletion](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/file-deletion) - Secure file deletion and data sanitization methods.
- [metadata-extraction](https://github.com/mhattingpete/claude-skills-marketplace/tree/main/computer-forensics-skills/skills/metadata-extraction) - Extract and analyze file metadata for forensic purposes.
- [threat-hunting-with-sigma-rules](https://github.com/jthack/threat-hunting-with-sigma-rules-skill) - Use Sigma detection rules to hunt for threats and analyze security events.

## Getting Started

### Step-by-Step Guides

#### Using Skills in Claude.ai

1. **Open Claude.ai** and start a new conversation
2. **Click the skill icon** (🧩) in the chat interface
3. **Browse the marketplace** or click "Add custom skill"
4. **Upload a SKILL.md file** from this repository (or select from marketplace)
5. **Start chatting** - Claude automatically activates relevant skills based on your task

**Example workflow:**
```
You: "Help me brainstorm domain names for my startup"
Claude: [Automatically uses Domain Name Brainstormer skill]
         "I'll help you find the perfect domain! Tell me about your startup..."
```

#### Using Skills in Claude Code

**Installation:**
```bash
# Create skills directory
mkdir -p ~/.config/claude-code/skills/

# Copy a skill (example: domain-name-brainstormer)
cp -r domain-name-brainstormer ~/.config/claude-code/skills/

# Or clone the entire repository for all skills
cd ~/.config/claude-code/skills/
git clone https://github.com/Grumpified-OGGVCT/awesome-claude-skills.git .
```

**Verify installation:**
```bash
# Check the skill metadata
head ~/.config/claude-code/skills/domain-name-brainstormer/SKILL.md

# You should see YAML frontmatter with name and description
```

**Usage:**
```bash
# Start Claude Code (skills load automatically)
claude

# Skills activate when relevant
# Example: Working on a new project triggers domain-name-brainstormer
```

#### Using Skills via API

**Basic example:**
```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    skills=["skill-id-here"],  # Skill IDs from marketplace
    messages=[{"role": "user", "content": "Your prompt"}]
)

print(response.content)
```

**With custom skills:**
```python
# First, upload your skill to get a skill_id
# Then reference it in the skills parameter
response = client.messages.create(
    model="claude-3-5-sonnet-20241022", 
    skills=["your-custom-skill-id"],
    messages=[{"role": "user", "content": "Task that uses your skill"}]
)
```

See the [Skills API documentation](https://docs.claude.com/en/api/skills-guide) for complete details including skill upload, management, and advanced usage.

## Creating Skills

### Skill Structure

Each skill is a folder containing a `SKILL.md` file with YAML frontmatter:

```
skill-name/
├── SKILL.md          # Required: Skill instructions and metadata
├── scripts/          # Optional: Helper scripts
├── templates/        # Optional: Document templates
└── resources/        # Optional: Reference files
```

### Basic Skill Template

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it.
---

# My Skill Name

Detailed description of the skill's purpose and capabilities.

## When to Use This Skill

- Use case 1
- Use case 2
- Use case 3

## Instructions

[Detailed instructions for Claude on how to execute this skill]

## Examples

[Real-world examples showing the skill in action]
```

### Skill Best Practices

- Focus on specific, repeatable tasks
- Include clear examples and edge cases
- Write instructions for Claude, not end users
- Test across Claude.ai, Claude Code, and API
- Document prerequisites and dependencies
- Include error handling guidance

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- How to submit new skills
- Skill quality standards
- Pull request process
- Code of conduct

### Quick Contribution Steps

1. Ensure your skill is based on a real use case
2. Check for duplicates in existing skills
3. Follow the skill structure template
4. Test your skill across platforms
5. Submit a pull request with clear documentation

## Resources

### Official Documentation

- [Claude Skills Overview](https://www.anthropic.com/news/skills) - Official announcement and features
- [Skills User Guide](https://support.claude.com/en/articles/12512180-using-skills-in-claude) - How to use skills in Claude
- [Creating Custom Skills](https://support.claude.com/en/articles/12512198-creating-custom-skills) - Skill development guide
- [Skills API Documentation](https://docs.claude.com/en/api/skills-guide) - API integration guide
- [Agent Skills Blog Post](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Engineering deep dive

### Community Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills) - Official example skills
- [Claude Community](https://community.anthropic.com) - Discuss skills with other users
- [Skills Marketplace](https://claude.ai/marketplace) - Discover and share skills

### Inspiration & Use Cases

- [Lenny's Newsletter](https://www.lennysnewsletter.com/p/everyone-should-be-using-claude-code) - 50 ways people use Claude Code
- [Notion Skills](https://www.notion.so/notiondevs/Notion-Skills-for-Claude-28da4445d27180c7af1df7d8615723d0) - Notion integration skills


## Join the Community

- Have questions about integrating Composio with your auth setup? [Hop on a quick call with us](https://calendly.com/thomas-composio/composio-enterprise-setup)
- [Follow us on Twitter](https://x.com/composio)
- [Join our Discord](https://discord.com/invite/composio)

---

## 📚 Frequently Asked Questions

### General Questions

**Q: What exactly are Claude Skills?**  
A: Skills are structured instruction sets (like training manuals) that teach AI models how to perform specialized tasks consistently. They contain workflows, best practices, and sometimes helper scripts to ensure high-quality, repeatable results.

**Q: Do I need to be technical to use skills?**  
A: No! Most users can simply upload a SKILL.md file to Claude.ai and start using it. Technical users can leverage advanced features like API integration and custom skill development.

**Q: Are skills only for Claude?**  
A: Originally yes, but this repository now includes a **Universal Format** that works with any OpenAI-compatible LLM including GPT-4, Llama, Gemini, and others via OpenRouter or Ollama.

**Q: How is this different from just writing a good prompt?**  
A: Skills are more comprehensive than prompts. They include:
- Multi-step workflows and decision trees
- Domain-specific knowledge and best practices
- Helper scripts for complex operations
- Templates and examples
- Automatic activation when relevant
- Reusability across platforms

### Using Skills

**Q: How do I know which skill to use?**  
A: Browse the [Skills](#skills) section organized by category (Development, Business, Creative, etc.). Each skill includes a clear description of what it does and when to use it.

**Q: Can I use multiple skills at once?**  
A: Yes! Claude can use multiple skills in a single conversation. Each skill activates when relevant to the current task.

**Q: Do skills work offline?**  
A: Skills for Claude.ai and Claude API require internet. However, with the Universal Format and Ollama, you can run skills completely locally and offline.

**Q: How much do skills cost?**  
A: Skills themselves are **free and open source**. You only pay for the LLM service you use:
- Claude.ai: Free tier or paid subscription
- Claude Code: Requires Claude API access
- Universal Format: Free with Ollama (local) or paid with cloud providers (OpenRouter, OpenAI, etc.)

### Creating Skills

**Q: Can I create my own skills?**  
A: Absolutely! See [Creating Skills](#creating-skills) and check out the [Skill Creator](./skill-creator/) skill for guidance.

**Q: How do I share my skill with others?**  
A: Submit a pull request to this repository! See [Contributing](#contributing) for guidelines. You can also share the SKILL.md file directly.

**Q: What makes a good skill?**  
A: Good skills:
- Solve specific, real-world problems
- Include clear, step-by-step instructions
- Provide examples and use cases
- Work consistently across platforms
- Are well-documented

### Technical Questions

**Q: What's the difference between the skill tiers?**  
A: 
- **Tier 1 (90% of skills)**: Instruction-only, works with ANY model
- **Tier 2 (10% of skills)**: Includes tool/function calling, works best with advanced models
- **Tier 3**: Claude-specific features (Artifacts, MCP)

**Q: How do I convert a Claude skill to universal format?**  
A: Use the conversion tool:
```bash
python tools/convert.py --skill skill-name
```
See [UNIVERSAL-FORMAT.md](UNIVERSAL-FORMAT.md) for details.

**Q: Can I use skills with my company's private data?**  
A: Yes! Skills are just instruction sets. When using Ollama locally, everything stays on your machine. With cloud APIs, follow your organization's data policies.

**Q: How do I test if a skill works with different models?**  
A: Use the model tester:
```bash
python tools/model-tester.py --skill path/to/skill --providers openrouter ollama
```

### Troubleshooting

**Q: My skill isn't activating. What's wrong?**  
A: Common issues:
1. **Check metadata**: Ensure YAML frontmatter has clear `name` and `description`
2. **File location**: Verify skill is in correct directory (`~/.config/claude-code/skills/`)
3. **File name**: Must be `SKILL.md` (uppercase)
4. **Relevance**: Make sure your task matches the skill's description

**Q: Can I modify existing skills?**  
A: Yes! Skills are open source. Fork the skill, modify it for your needs, and use it. Consider contributing improvements back to the community.

**Q: Where can I get help?**  
A: 
- Open an [issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues) on GitHub
- Check [Claude Community](https://community.anthropic.com)
- Join the [Composio Discord](https://discord.com/invite/composio)
- Read the official [Claude Skills documentation](https://support.claude.com/en/articles/12512180-using-skills-in-claude)

### Contributing

**Q: How can I contribute?**  
A: Several ways:
- Submit new skills via pull request
- Improve existing skills
- Add documentation or examples
- Report bugs or suggest features
- Share your use cases and workflows

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

This repository is licensed under the Apache License 2.0.

Individual skills may have different licenses - please check each skill's folder for specific licensing information.

---

**Note**: Claude Skills work across Claude.ai, Claude Code, and the Claude API. Once you create a skill, it's portable across all platforms, making your workflows consistent everywhere you use Claude.

- [AgentsKB](https://agentskb.com) - Upgrade your AI with researched answers. We did the research so your AI gets it right the first time.
