# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Attribution Documentation** (Feb 12, 2026): Comprehensive documentation clarifying original vs GrumpiFied content
  - Created ATTRIBUTIONS.md with complete breakdown of upstream vs fork contributions
  - Added attribution headers to all GrumpiFied documentation files
  - Updated README.md with prominent attribution section and footer
  - Enhanced ARCHITECTURE.md, CONTRIBUTING.md with fork overview
  - Clarified that all automation skills (943) are from ComposioHQ upstream
  - Documented all GrumpiFied enhancements (universal format, tools, docs, CI/CD)
- **Massive Skills Expansion**: Synced 832 new automation skills from ComposioHQ/awesome-claude-skills (Feb 11, 2026)
  - Total skills: 943 (from 111)
  - All 874 Composio toolkit integrations
  - 71 popular app skills upgraded with real tool data from RUBE_SEARCH_TOOLS
  - Comprehensive API integration skills across 20+ categories
- **Security Review Completed**: Audited all new skills for OpenClaw-style vulnerabilities
  - No hardcoded API keys or secrets found
  - No malicious shell commands or base64 encoded malware
  - No prompt injection or social engineering patterns
  - All YAML frontmatter properly formatted
- **Universal LLM Skills Format**: All 27 skills now available in OpenAI-compatible format
  - Tier 1 (Instruction-only): 16 skills - works with ANY model
  - Tier 2 (Tool-enhanced): 7 skills - works with tool-calling models
  - Tier 3 (Claude-only): 4 skills - reference for Claude-specific features
- **Automated Conversion**: `tools/convert.py` for converting Claude skills to universal format
- **Validation Tool**: `tools/validate.py` for ensuring universal format compliance
- **Skill Discovery**: Three tiers of discovery tools
  - `tools/find-skill` - Zero-config wrapper for quick lookups
  - `tools/discover.py` - Interactive keyword search and category browsing
  - `tools/nlp-discover.py` - AI-powered semantic search with Gemini 3 Flash Preview
- **Automated Upstream Sync**: GitHub Actions workflow syncing with anthropics/skills every 6 hours
- **Enhanced Documentation**:
  - OpenRouter setup guide for accessing 100+ models
  - Ollama setup guide for local/private usage
  - Model compatibility guide
  - Migration guide for converting custom skills
  - Comprehensive skill discovery documentation
- **Automation Tools**:
  - `tools/sync-upstream.sh` - Manual upstream sync with safety checks
  - `tools/index-skills.py` - Generate searchable skill index
  - `tools/model-tester.py` - Test skills across different models
- **Examples**: Working code examples for multi-provider usage
- **Requirements file**: `requirements.txt` for easy dependency installation

### Changed
- Repository structure now includes `universal/` directory alongside original skills
- All skills validated and converted to universal format
- README updated with universal format documentation
- SKILL-INDEX.json updated with all 27 skills across 7 categories

### Fixed
- Claude-specific language cleaned up in universal format conversions
- Validation warnings addressed in system prompts
- Metadata consistency across all converted skills

## [1.0.0] - 2025-12-26

### Added
- Initial fork from anthropics/skills
- 27 curated Claude Skills across 7 categories:
  - Business & Marketing (5 skills)
  - Communication & Writing (2 skills)
  - Creative & Media (5 skills)
  - Development & Code Tools (5 skills)
  - Document Processing (4 skills)
  - Other (3 skills)
  - Productivity & Organization (3 skills)
- Comprehensive README with skill descriptions
- Contributing guidelines
- Getting started guide
- License information (Apache 2.0)

[Unreleased]: https://github.com/Grumpified-OGGVCT/awesome-claude-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Grumpified-OGGVCT/awesome-claude-skills/releases/tag/v1.0.0
