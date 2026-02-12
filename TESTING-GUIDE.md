# Testing Guide for Claude Skills

This guide helps you test and validate Claude skills from this repository.

## Quick Start Testing

### 1. Test Skill Loading (Manual)

Pick any skill and verify it loads correctly:

```bash
# View a skill's frontmatter
head -20 github-automation/SKILL.md

# Expected: Valid YAML between --- markers
---
name: github-automation
description: "..."
requires:
  mcp: [rube]
---
```

### 2. YAML Frontmatter Validation (Automated)

Validate all skills have proper YAML:

```bash
python3 << 'EOF'
import yaml
import glob

for skill_file in glob.glob('*/SKILL.md') + glob.glob('*/*/SKILL.md'):
    with open(skill_file, 'r') as f:
        content = f.read()
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1])
                    assert 'name' in fm and 'description' in fm
                    print(f"✓ {skill_file}")
                except:
                    print(f"✗ {skill_file}")
EOF
```

### 3. Security Scan (Automated)

Scan for common security issues:

```bash
# Check for hardcoded credentials
grep -r "api[_-]key.*=.*['\"][A-Za-z0-9]\{20,\}" */SKILL.md || echo "✓ No hardcoded keys"

# Check for shell injection
grep -r "eval\|exec\|system.*(" */SKILL.md | grep -v "Execute Tools" || echo "✓ No shell injection"

# Check for suspicious base64
grep -r "base64.*decode.*|" */SKILL.md || echo "✓ No suspicious base64"
```

## Testing Automation Skills

### Prerequisites

To test automation skills, you need:

1. **Rube MCP Server**: Add `https://rube.app/mcp` to your MCP client
2. **Composio Account**: Sign up at https://composio.dev (optional for testing)
3. **Claude Client**: Claude Desktop, Claude CLI, or API access

### Test Workflow

1. **Load the Skill**
   ```
   # In Claude
   "Load the GitHub automation skill"
   ```

2. **Verify Prerequisites**
   ```
   "Check if RUBE_SEARCH_TOOLS is available"
   ```

3. **Test Connection**
   ```
   "Connect to GitHub via RUBE_MANAGE_CONNECTIONS"
   ```

4. **Execute a Simple Action**
   ```
   "List my GitHub repositories using RUBE_MULTI_EXECUTE_TOOL"
   ```

### Example: Testing GitHub Automation

```
User: "I want to test the GitHub automation skill. First, search for available GitHub tools."

Claude: [Calls RUBE_SEARCH_TOOLS with useCase: "list github repositories"]

User: "Now connect to GitHub."

Claude: [Calls RUBE_MANAGE_CONNECTIONS with toolkit: "github"]

User: "List my repositories."

Claude: [Calls RUBE_MULTI_EXECUTE_TOOL with appropriate GitHub tool]
```

## Testing Non-Automation Skills

For skills like `raffle-winner-picker`, `domain-name-brainstormer`, etc.:

1. **Review the Skill Instructions**
   ```bash
   cat raffle-winner-picker/SKILL.md
   ```

2. **Test with Sample Data**
   ```
   User: "Pick 3 winners from this list: Alice, Bob, Carol, Dave, Eve"
   
   Claude: [Follows skill instructions to randomly select 3 winners]
   ```

3. **Verify Output**
   - Check winners are from the provided list
   - Verify no duplicates
   - Confirm randomness (different results on repeated runs)

## Validation Checklist

### For All Skills
- [ ] YAML frontmatter parses correctly
- [ ] Required fields present (name, description)
- [ ] No obvious security issues (credentials, shell commands)
- [ ] Skill instructions are clear and actionable
- [ ] Examples are present and make sense

### For Automation Skills
- [ ] Composio toolkit link is present
- [ ] Prerequisites are documented
- [ ] RUBE_SEARCH_TOOLS pattern is mentioned
- [ ] Connection setup is explained
- [ ] Tool execution examples are provided

### For Security
- [ ] No hardcoded API keys or secrets
- [ ] No shell command injection patterns
- [ ] No prompt injection attempts
- [ ] External links use HTTPS
- [ ] Links point to official domains only

## Continuous Validation

Run these checks regularly:

```bash
# Count skills
find . -name "SKILL.md" | wc -l

# Validate YAML (all skills)
python3 -c "import yaml, glob; [yaml.safe_load(open(f).read().split('---')[1]) for f in glob.glob('*/SKILL.md')]"

# Security scan
grep -r "password.*=\|secret.*=" */SKILL.md | wc -l  # Should be 0
```

## Reporting Issues

If you find issues during testing:

1. **Security Issues**: Report immediately to repository maintainers
2. **Skill Errors**: Open an issue with:
   - Skill name
   - Error message
   - Steps to reproduce
   - Expected vs actual behavior

3. **Documentation Issues**: Submit a PR with corrections

## Testing Statistics

As of February 11, 2026:
- **Total Skills**: 943
- **Automation Skills**: ~910
- **Security Scans Passed**: 100%
- **YAML Validation**: 943/943 passed
- **Known Issues**: 0

## Additional Resources

- [Composio Documentation](https://docs.composio.dev)
- [Rube MCP Server](https://rube.app)
- [Claude Skills Format](./UNIVERSAL-FORMAT.md)
- [Security Audit Report](./SECURITY-AUDIT-2026-02-11.md)
