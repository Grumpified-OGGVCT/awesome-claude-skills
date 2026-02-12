# 🤖 Daily AI LLM Universal Skills Aggregation Workflow

## Overview

The **Daily Skills Aggregation Workflow** is an intelligent, self-managing system that automatically discovers, validates, tests, fixes, and integrates universal AI skills from across GitHub into this repository.

## 🎯 What It Does

This workflow performs a complete lifecycle automation:

1. **🔍 Discovery** - Searches GitHub for new Claude/AI skills using public APIs (no registration required)
2. **✅ Validation** - Checks each skill for proper YAML format, required fields, and structure
3. **🔒 Security Scan** - Detects hardcoded credentials, dangerous code patterns, and other vulnerabilities
4. **🛠️ Auto-Repair** - Automatically fixes common issues like unquoted YAML descriptions, formatting problems
5. **🧪 Testing** - Validates compatibility and marks skills that need Composio-specific adaptation
6. **📦 Integration** - Creates skill directories, adds attribution, updates indices
7. **📝 Documentation** - Updates README.md with daily discovery section showing new additions
8. **🔍 CoVE QA** - Runs Chain of Verification quality assurance with gap analysis
9. **🚀 PR Creation** - Generates comprehensive pull request with all findings and recommendations

## ⏰ Schedule

- **Daily at 3:00 AM UTC** (1 hour after upstream sync)
- **Manual trigger** available via GitHub Actions UI

## 🔧 Configuration

### Input Parameters (Manual Run)

- `force_run` (boolean): Run even if no new skills are found
- `discovery_limit` (number): Maximum new skills to discover per run (default: 10)

### Environment Variables

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- No additional API keys or services required!

## 📊 Discovery Sources

The workflow searches GitHub using public APIs with these queries:

- `claude skill markdown in:readme`
- `claude prompt template in:file extension:md`
- `claude instructions SKILL.md in:path`
- `AI agent skill claude in:readme`
- `LLM workflow template in:readme language:markdown`

**No API registration required** - Uses free GitHub public search API with rate limiting.

## ✅ Validation Criteria

Skills must meet these requirements to be integrated:

### Format Requirements
- ✅ Valid YAML frontmatter with `---` delimiters
- ✅ Required fields: `name`, `description`
- ✅ Proper YAML syntax (parseable by PyYAML)
- ✅ Consistent line endings and formatting

### Security Requirements
- ✅ No hardcoded API keys or credentials
- ✅ No dangerous code execution patterns (`eval`, `exec`)
- ✅ No suspicious URLs or malware patterns
- ✅ No prompt injection attempts

### Compatibility Requirements
- ✅ Universal format (not Composio-only)
- ✅ No external service dependencies (or clearly documented)
- ✅ Clear, actionable instructions

## 🛠️ Auto-Repair Capabilities

The workflow can automatically fix:

1. **YAML Formatting**
   - Quotes descriptions containing colons
   - Normalizes line endings
   - Fixes common syntax errors

2. **Attribution**
   - Adds source repository links
   - Includes discovery timestamp
   - Credits original authors

3. **Categorization**
   - Auto-detects skill categories
   - Places in appropriate sections
   - Updates indices

## 📦 Integration Process

When a skill passes validation:

1. **Directory Creation**
   ```
   {skill-name}-universal/
   └── SKILL.md
   ```

2. **Content Enhancement**
   - Original skill content preserved
   - Attribution header added
   - Format normalization applied

3. **Index Updates**
   - `SKILL-INDEX.json` regenerated
   - Total skill count updated
   - Category mappings refreshed

4. **README Updates**
   - Daily discovery section added/updated
   - Links to new skills added
   - Source repositories credited with star counts

## 🔍 Chain of Verification (CoVE) QA - Recursive Auto-Fix

After integration, the workflow runs a **recursive CoVE QA process with auto-remediation**:

### Initial Pass
1. **Verification Checks**
   - ✅ Skill count verification (files vs index)
   - ✅ YAML validation (all skills)
   - ✅ Security scan (new skills)
   - ✅ Format consistency

2. **Issue Detection**
   - Identifies all problems
   - Categorizes by severity
   - Determines fixability

### Auto-Fix Phase (if issues found)
1. **Count Mismatch** → Regenerate SKILL-INDEX.json
2. **YAML Issues** → Auto-quote descriptions, fix syntax
3. **Security Issues** → Replace hardcoded keys with env vars, disable dangerous code
4. **Format Issues** → Normalize line endings, fix indentation

### Final Pass
1. **Re-verification**
   - Re-runs all checks
   - Validates fixes were successful
   - Confirms no new issues introduced

2. **Status Determination**
   - ✅ **Passed** → All issues resolved → Auto-merge
   - ⚠️ **Failed** → Unfixable issues → Manual review required

### Gap Analysis
- 🔍 Identifies skills requiring adaptation
- 🔍 Detects missed opportunities
- 🔍 Finds process improvements

### Self-Improvement
- 📈 Applies improvements automatically
- 📊 Tracks quality metrics
- 🎯 Learns from each run

### Reporting
- 📝 Comprehensive QA report (initial + final)
- 📊 Statistics on fixes applied
- ✅ Clear pass/fail status

## 📝 Output Files

### Discovery Tracking
`.github/skill-discovery/discovered-skills.json`
```json
{
  "discovered": [...],      // Newly found, being processed
  "integrated": [...],      // Successfully added
  "rejected": [...]         // Failed validation
}
```

Each entry includes:
- Repository URL and name
- Star count
- Discovery query used
- Validation status
- Integration status
- Fixes applied

### Reports Generated
- `/tmp/cove-report.md` - CoVE QA findings
- `/tmp/yaml-validation.txt` - YAML check results
- Pull request description - Complete summary

## 🚀 Automatic Merge Behavior

### When Auto-Merge Happens
The workflow **automatically merges** the PR when:
- ✅ All skills validated successfully
- ✅ Security scan passed
- ✅ YAML validation passed
- ✅ CoVE QA final pass: All issues resolved
- ✅ No merge conflicts detected

**No user action required!** The changes are applied directly to main branch.

### When Manual Review is Required
The workflow creates a PR requiring manual review when:
- ⚠️ **Merge Conflicts**: Changes conflict with recent commits
- ⚠️ **Unfixable CoVE Issues**: Auto-fix couldn't resolve all problems
- ⚠️ **Security Concerns**: Complex security issues needing human judgment

**User notified via PR** with clear explanation of what needs attention.

## 📝 Pull Request Details

Each successful run creates a PR with:

### Summary Section
- Skills discovered, validated, fixed, integrated
- Total skill count after integration
- Pass/fail status of all checks

### CoVE QA Report
- Verification results
- Security findings
- Gap analysis
- Self-improvement recommendations

### Files Changed
- List of new skill directories
- Updated index and README
- Discovery log updates

### Action Required
- Clear merge recommendation
- Pre-flight check results
- Link to workflow run

## 🏷️ PR Labels

Automatic labels applied:

**Auto-merge path**:
- `automated` - Created by workflow
- `daily-aggregation` - From this specific workflow
- `universal-skills` - Contains universal format skills
- `auto-merge` - Will be automatically merged

**Manual review path**:
- `automated` - Created by workflow
- `daily-aggregation` - From this specific workflow
- `needs-review` - Requires human attention
- `merge-conflict` - Has merge conflicts (if applicable)
- `cove-qa-failed` - CoVE QA issues remain (if applicable)

## 🔒 Security Features

### Pre-Integration Security Checks
- Hardcoded credential detection
- Code injection pattern scanning
- Malicious URL detection
- Social engineering attempt detection

### Post-Integration Security
- All changes reviewed in PR
- Security findings highlighted
- Manual review opportunity before merge

## 🎓 Skill Categorization

Skills are automatically categorized into:

- **Development** - Code generation, debugging, testing
- **Business** - Lead research, competitive analysis
- **Creative** - Content generation, design
- **Automation** - Workflow automation, integration
- **General** - Multi-purpose skills

## 📈 Metrics Tracked

The workflow tracks:
- Skills discovered per run
- Validation pass rate
- Common rejection reasons
- Integration success rate
- Repository growth over time
- Popular source repositories

## 🔄 Integration with Other Workflows

### Upstream Sync (2 AM UTC)
- Runs **before** daily aggregation
- Syncs ComposioHQ skills
- Preserves local customizations

### Daily Aggregation (3 AM UTC)
- Runs **after** upstream sync
- Discovers new universal skills
- Complements upstream content

### Link Checker
- Validates all skill links
- Runs independently
- Ensures quality

## 📚 Manual Override

You can manually trigger the workflow:

1. Go to **Actions** tab
2. Select **Daily AI LLM Universal Skills Aggregation**
3. Click **Run workflow**
4. Set parameters:
   - `force_run`: true/false
   - `discovery_limit`: 1-50

## 🐛 Troubleshooting

### No Skills Discovered
- ✅ Normal - may not find new skills every day
- ✅ Discovery queries may need expansion
- ✅ Check GitHub API rate limits

### Validation Failures
- ✅ Check `/tmp/cove-report.md` in workflow logs
- ✅ Review security findings
- ✅ Skills logged in `rejected` array

### Integration Skipped
- ✅ Check for `requires_adaptation` flag
- ✅ Composio-specific skills need manual review
- ✅ Duplicate directory names are skipped

## 🎯 Future Enhancements

Planned improvements:

1. **Expanded Discovery**
   - More search queries
   - Additional platforms (GitLab, Bitbucket)
   - Community submissions

2. **Quality Scoring**
   - Documentation completeness
   - Example quality
   - Community ratings

3. **Functional Testing**
   - Actual skill execution tests
   - Integration testing
   - Performance benchmarks

4. **AI-Powered Adaptation**
   - Automatic Composio migration
   - Format conversion
   - Enhancement suggestions

## 📖 Related Documentation

- [Auto-Sync Upstream](.github/workflows/AUTO-SYNC-README.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Universal Format](../../UNIVERSAL-FORMAT.md)
- [Testing Guide](../../TESTING-GUIDE.md)

## 🤝 Contributing

Found a skill that should be included? 

1. **Automatic**: Just wait - the workflow will discover it if it's public
2. **Manual**: Submit a PR with the skill
3. **Suggest**: Open an issue with the repository URL

## 📜 License

All discovered skills maintain their original licenses. Attribution is automatically added to each integrated skill.

---

🤖 **Created by**: Grumpified-OGGVCT  
📅 **Last Updated**: 2026-02-12  
🔗 **Workflow File**: [daily-skills-aggregation.yml](./daily-skills-aggregation.yml)
