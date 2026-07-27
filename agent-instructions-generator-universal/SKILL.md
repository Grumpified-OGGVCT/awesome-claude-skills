---
name: agent-instructions-generator
description: Generate baseline CLAUDE.md and AGENTS.md instruction files for a project. Use when a repo is missing instruction files or needs standardized agent guidance.
---

<!--
  Source: https://github.com/CurryTang/Amadeus
  Original: https://github.com/CurryTang/Amadeus/blob/092e0c9b85782723dbb472d107f5b2d073f8b8e0/.claude/skills/agent-instructions-generator/SKILL.md
  Discovered: 2026-03-17 04:53:35 UTC
  Integrated via: Daily AI LLM Universal Skills Aggregation
-->

# Agent Instructions Generator

## What this skill does

- Creates `CLAUDE.md` and `AGENTS.md` from templates.
- Enforces a reference-first rule pointing agents to `resource/`.

## How to run

From repo root:

```bash
./scripts/generate-agent-instructions.sh
```

For a different project and name:

```bash
./scripts/generate-agent-instructions.sh /path/to/project ProjectName
```

Overwrite existing files:

```bash
./scripts/generate-agent-instructions.sh /path/to/project ProjectName --force
```
