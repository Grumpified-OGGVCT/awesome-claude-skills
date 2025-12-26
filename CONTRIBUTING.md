# Contributing to Awesome Claude Skills

Thank you for your interest in contributing to the premier collection of Claude Skills! This guide will help you add new skills that benefit the entire Claude community.

## 🎯 What We're Looking For

We welcome contributions including:
- **New skills** based on real-world use cases
- **Improvements** to existing skills
- **Documentation** enhancements
- **Bug reports** and fixes
- **Examples** and tutorials

## 📋 Quick Contribution Checklist

Before submitting, ensure your contribution:

- [ ] Solves a **real problem** (not hypothetical)
- [ ] Is **not a duplicate** of existing skills
- [ ] Includes **clear documentation**
- [ ] Has been **tested** across relevant platforms
- [ ] Follows the **skill structure** template
- [ ] Includes proper **attribution** (if based on someone else's workflow)

## Before You Start

### 1. Search for Duplicates

Search existing skills to avoid duplicates:
```bash
# Search by keyword
grep -r "domain name" */SKILL.md

# List all skills
ls -d */
```

Browse the [Skills](README.md#skills) section organized by category.

### 2. Ensure Real Use Case

All skills must be based on **real usage**, not theoretical applications. Ask yourself:
- Have I (or someone else) actually used this workflow?
- Does this solve a problem that occurs repeatedly?
- Would others benefit from this?

**Good examples:**
- ✅ "I brainstorm domain names weekly for clients"
- ✅ "Our team analyzes meeting transcripts every sprint"
- ✅ "I organize invoice PDFs for tax season"

**Poor examples:**
- ❌ "Someone might want to..."
- ❌ "Theoretically, Claude could..."
- ❌ "I thought it would be cool if..."

## Skill Requirements

All skills must meet these requirements:

### Core Requirements

1. **Real Problem** ✅
   - Based on actual usage, not theoretical
   - Solves a recurring need
   - Documented use case or attribution

2. **Well-Documented** 📚
   - Clear YAML frontmatter (name, description)
   - Step-by-step instructions
   - Real-world examples
   - When to use this skill

3. **Accessible** 🌐
   - Written for both technical and non-technical users
   - Clear language, no unexplained jargon
   - Includes context and rationale

4. **Includes Examples** 💡
   - Show practical, real-world usage
   - Include expected input and output
   - Cover common edge cases

5. **Tested** ✅
   - Works across platforms (Claude.ai, Claude Code, or API)
   - Instructions are accurate and complete
   - No broken references or dependencies

6. **Safe** 🛡️
   - Confirms before destructive operations
   - Includes error handling guidance
   - Documents potential risks

7. **Portable** 🚀
   - Works across Claude platforms when applicable
   - Minimal external dependencies
   - Clear setup instructions for any dependencies

### Optional Enhancements

- **Universal format** conversion (we can help with this)
- **Helper scripts** for complex operations
- **Reference materials** for domain knowledge
- **Assets/templates** for consistent output

## Skill Structure

Create a new folder with your skill name (use lowercase and hyphens):

```
skill-name/
└── SKILL.md
```

## SKILL.md Template

Use this template for your skill:

```markdown
---
name: skill-name
description: One-sentence description of what this skill does and when to use it.
---

# Skill Name

Detailed description of the skill and what it helps users accomplish.

## When to Use This Skill

- Bullet point use case 1
- Bullet point use case 2
- Bullet point use case 3

## What This Skill Does

1. **Capability 1**: Description
2. **Capability 2**: Description
3. **Capability 3**: Description

## How to Use

### Basic Usage

```
Simple example prompt
```

### Advanced Usage

```
More complex example prompt with options
```

## Example

**User**: "Example prompt"

**Output**:
```
Show what the skill produces
```

**Inspired by:** [Attribution to original source, if applicable]

## Tips

- Tip 1
- Tip 2
- Tip 3

## Common Use Cases

- Use case 1
- Use case 2
- Use case 3
```

### Review Process

After you submit a PR:

1. **Automated checks** run (if any)
2. **Maintainers review** your contribution
3. **Feedback provided** (if changes needed)
4. **Merged** once approved!

**Average review time**: 2-5 days

## 🎨 Skill Naming Guidelines

Choose clear, descriptive names that indicate what the skill does:

**Good names:**
- ✅ `domain-name-brainstormer` - Clear what it does
- ✅ `invoice-organizer` - Specific and descriptive
- ✅ `meeting-insights-analyzer` - Indicates analysis function

**Poor names:**
- ❌ `helper` - Too vague
- ❌ `cool-ai-thing` - Not descriptive
- ❌ `tool1` - Meaningless

**Naming conventions:**
- Use `lowercase-with-hyphens`
- Be specific: `pdf-editor` not `editor`
- Include the domain: `slack-gif-creator` not `gif-creator`
- Avoid generic terms: `lead-research-assistant` not `assistant`

## Adding Your Skill to README

1. Choose the appropriate category:
   - Business & Marketing
   - Communication & Writing
   - Creative & Media
   - Development
   - Productivity & Organization

2. Add your skill in alphabetical order within the category:

```markdown
- [Skill Name](./skill-name/) - One-sentence description. Inspired by [Person/Source].
```

3. Follow the existing format exactly - no emojis, consistent punctuation.

## Pull Request Process

### Step-by-Step Guide

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/awesome-claude-skills.git
   cd awesome-claude-skills
   ```

2. **Create a branch**
   ```bash
   git checkout -b add-skill-name
   ```

3. **Add your skill folder**
   ```
   awesome-claude-skills/
   └── your-skill-name/
       ├── SKILL.md          # Required
       ├── scripts/          # Optional
       ├── references/       # Optional
       └── assets/           # Optional
   ```

4. **Update README.md**
   - Find the appropriate category
   - Add your skill in alphabetical order
   - Follow the existing format exactly

   ```markdown
   - [Your Skill Name](./your-skill-name/) - One-sentence description of what it does and when to use it.
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add [Skill Name] skill"
   ```

6. **Push to your fork**
   ```bash
   git push origin add-skill-name
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "Pull Requests" → "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

### Pull Request Guidelines

Your PR should include:

**Title Format:**
```
Add [Skill Name] skill
```

**Description Should Include:**
- **Problem it solves**: What real-world problem does this address?
- **Use case**: Who uses this workflow and when?
- **Attribution**: If based on someone's workflow, give credit
- **Example**: Show how it's used in practice
- **Testing**: Confirm which platforms you tested on

**Example PR Description:**
```markdown
## Summary
Adds a skill for automatically organizing invoice files for tax preparation.

## Problem
Freelancers and small business owners spend hours manually organizing 
receipts and invoices before tax season.

## Use Case
Based on my workflow as a freelancer organizing 200+ invoices annually. 
The skill:
- Reads invoice PDFs and images
- Extracts vendor, date, and amount
- Renames files consistently
- Organizes into folders by category

## Attribution
Inspired by my own workflow, refined over 3 tax seasons.

## Testing
- ✅ Tested on Claude.ai
- ✅ Tested on Claude Code
- ✅ Works with 50+ real invoices

## Example Usage
Input: "Organize my Downloads/invoices folder"
Output: Files renamed and sorted into Business/Travel/Equipment folders
```

## Code of Conduct

- Be respectful and constructive
- Credit original sources and inspirations
- Focus on practical, helpful skills
- Write clear, accessible documentation
- Test your skills before submitting

## Questions?

Open an issue if you have questions about contributing or need help structuring your skill.

## Attribution

When adding a skill based on someone's workflow or use case, include proper attribution:

```markdown
**Inspired by:** [Person Name]'s workflow
```

or

```markdown
**Credit:** Based on [Company/Team]'s process
```

Examples:
- **Inspired by:** Dan Shipper's meeting analysis workflow
- **Inspired by:** Teresa Torres's content research process
- **Credit:** Based on Notion's documentation workflow

## Skill Categories

### Business & Marketing
Skills for lead generation, competitive research, branding, and business development.

### Communication & Writing
Skills for improving communication, analyzing conversations, and creating content.

### Creative & Media
Skills for working with images, videos, audio, and creative content.

### Development
Skills for software development, documentation, and technical workflows.

### Productivity & Organization
Skills for organizing files, managing tasks, and personal productivity.

---

Thank you for contributing to Awesome Claude Skills!

## 📞 Need Help?

### Before Contributing

- **Not sure if your idea is a good fit?** [Open an issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues/new) to discuss it first
- **New to Claude Skills?** Read our [Getting Started Guide](GETTING_STARTED.md)
- **Need skill creation help?** Check out the [Skill Creator](./skill-creator/) skill

### During Development

- **Questions about structure?** See existing skills as examples
- **Need review?** Tag maintainers in your PR
- **Stuck on something?** Ask in [Discussions](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/discussions)

### Community

- [Discord](https://discord.com/invite/composio) - Real-time help
- [Twitter](https://x.com/composio) - Updates and announcements
- [Claude Community](https://community.anthropic.com) - Official Claude discussions

## 🎉 Recognition

Contributors are recognized in several ways:

- **Attribution** in the skill's README entry
- **GitHub contribution graph** shows your impact
- **Community appreciation** from users who benefit from your work
- **Potential features** on social media and newsletters

## 📊 Contribution Ideas

Not sure where to start? Here are some ideas:

### High-Impact Contributions

1. **Popular workflows**: Skills that solve common problems
2. **Industry-specific**: Accounting, legal, medical, education workflows
3. **Integration skills**: Tools that work with popular software (Notion, Slack, etc.)
4. **Localization**: Non-English skills or multi-language support

### Documentation Improvements

1. Add more examples to existing skills
2. Improve setup instructions
3. Create tutorial videos or blog posts
4. Translate documentation

### Code Improvements

1. Convert more skills to universal format
2. Add helper scripts to existing skills
3. Improve error handling
4. Add tests for validation tools

## 🔄 Syncing with Upstream

This repository automatically syncs with [anthropics/skills](https://github.com/anthropics/skills) every 6 hours. Your contributions stay protected while we pull in upstream updates.

See [Automated Upstream Sync](README.md#automated-upstream-sync) for details.

## ⚖️ Legal

By contributing, you agree that:

- Your contributions are your original work or properly attributed
- You grant permission for your contributions to be licensed under Apache 2.0
- You have the right to contribute the code/content
- Your contributions don't violate any copyrights or licenses

---

**Thank you for making Claude Skills better for everyone!** 🙏

