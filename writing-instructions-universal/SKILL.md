---
name: writing-instructions
description: |
  Create custom instruction files (.instructions.md) for GitHub Copilot. Use when asked to create, write, or generate instruction files, coding guidelines, or auto-applied rules for specific file types. Covers frontmatter format, glob patterns, and best practices.
---

<!--
  Source: https://github.com/J03Fr0st/maestro
  Original: https://github.com/J03Fr0st/maestro/blob/1da344a0b76be113d6dd69254a4ec8d56966dd02/.claude/skills/writing-instructions/SKILL.md
  Discovered: 2026-02-25 04:54:42 UTC
  Integrated via: Daily AI LLM Universal Skills Aggregation
-->

# Writing Instruction Files

Create `.instructions.md` files in `.github/instructions/` that automatically apply guidelines when matching files are edited.

## File Types

| Type | Location | Scope |
|------|----------|-------|
| `copilot-instructions.md` | `.github/` root | All chat requests |
| `*.instructions.md` | `.github/instructions/` | Files matching `applyTo` glob |
| `AGENTS.md` | Workspace root | Multi-agent workflows |

## File Format

```markdown
---
applyTo: "**/*.ts"
description: TypeScript coding standards
name: TypeScript Guidelines
---

# Your Instructions Here

Write clear, actionable guidelines in Markdown.
```

## Frontmatter Fields

| Field | Purpose |
|-------|---------|
| `applyTo` | Glob pattern for automatic application |
| `description` | Short description shown in UI |
| `name` | Display name (defaults to filename) |

## Common Glob Patterns

| Pattern | Matches |
|---------|---------|
| `**` | All files |
| `**/*.ts` | All TypeScript files |
| `**/*.component.ts` | Angular components |
| `src/**` | All files in src/ |
| `**/*.{js,ts}` | JS and TS files |
| `**/tests/**` | All test files |

## Body Content

- Write in natural language using Markdown
- Keep instructions short, concise, and actionable
- Use bullet points, not lengthy paragraphs
- Reference files: `[config](../path/to/file.json)`
- Reference tools: `#tool:<tool-name>`

## Rules

- One instruction file per topic or language
- Use specific glob patterns, avoid overly broad `applyTo`
- Don't duplicate instructions across files
- Don't include secrets or credentials
- Store project-specific instructions in workspace (version controlled)
- Reference other instruction files in prompts to avoid duplication
