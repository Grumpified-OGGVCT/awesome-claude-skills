# Automated Upstream Sync with QA Validation

This workflow automatically syncs the latest changes from [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) while preserving all local customizations and running comprehensive QA validation.

## Overview

The automation performs these steps daily:

1. **🔍 Check for Updates** - Monitors upstream repository for new commits
2. **📥 Merge Changes** - Intelligently merges new content while preserving customizations
3. **✅ Validate Quality** - Runs YAML validation and regenerates skill index
4. **🛡️ Security Scan** - Checks for hardcoded secrets and dangerous patterns
5. **🔧 Cleanup & Repair** - Automatically fixes common issues if detected
6. **📋 Create PR** - Opens pull request with detailed reports for easy approval

## Workflow Schedule

**Automatic:** Runs daily at 2 AM UTC  
**Manual:** Can be triggered anytime via GitHub Actions UI

## How It Works

### 1. Change Detection

The workflow compares the last synced upstream commit with the current upstream HEAD:
- Stores last sync in `.github/last-upstream-sync`
- Detects new commits since last sync
- Extracts commit messages for PR description

### 2. Intelligent Merge

Uses `rsync --ignore-existing` to merge changes while **never overwriting**:

**Protected Files/Directories (Never Overwritten):**
- ✅ `README.md` - Our enhanced version with comprehensive docs
- ✅ `CONTRIBUTING.md` - Our detailed contribution guidelines
- ✅ `tools/` - Our automation scripts and utilities
- ✅ `docs/` - Our extended documentation
- ✅ `examples/` - Our example implementations
- ✅ `universal/` - Our universal format conversions
- ✅ `.github/` - Our CI/CD workflows
- ✅ `*IMPLEMENTATION*.md` - Implementation documentation
- ✅ `QA-*.md` - Quality assurance reports
- ✅ `ARCHITECTURE.md` - Architecture documentation
- ✅ `UNIVERSAL-FORMAT.md` - Format specifications
- ✅ `CHANGELOG.md` - Change log
- ✅ `GETTING_STARTED.md` - Getting started guide
- ✅ `QUICK-START-NLP.md` - NLP quick start

**What Gets Synced:**
- ✅ New skills from upstream
- ✅ Updates to existing upstream skills
- ✅ Bug fixes and improvements
- ✅ New automation capabilities

### 3. Comprehensive QA Validation

The workflow runs the same rigorous QA process requested:

#### YAML Validation
```bash
python tools/validate-skill-yaml.py
```
- Validates all SKILL.md files have correct YAML frontmatter
- Checks required fields (name, description)
- Validates data types and syntax
- Fails PR if validation errors found

#### Skill Index Regeneration
```bash
python tools/generate-skill-index.py
```
- Auto-generates updated SKILL-INDEX.json
- Includes all skills (old + new from upstream)
- Auto-categorizes new skills
- Validates index integrity

#### Security Scan
- ✅ Checks for hardcoded API keys/secrets
- ✅ Detects dangerous code patterns (eval, exec)
- ✅ Verifies subprocess calls are safe
- ✅ Ensures critical files preserved

#### File Integrity Check
- ✅ Verifies all protected files still exist
- ✅ Checks directory structure intact
- ✅ Counts total skills and compares

### 4. Automatic Cleanup & Repair

If issues are detected, the workflow automatically:
- 🔧 Sets executable permissions on Python scripts
- 🔧 Re-validates YAML after fixes
- 🔧 Regenerates SKILL-INDEX.json if corrupted
- 🔧 Stages all repairs for commit

### 5. Pull Request Creation

Creates a detailed PR with:
- **Status Badge** - ✅ Passed / ⚠️ Warnings / ❌ Critical
- **Summary Stats** - Files changed, skills added, QA status
- **Commit History** - New commits from upstream
- **Merge Report** - What was synced, what was preserved
- **Validation Results** - YAML, index, security checks
- **QA Report** - Comprehensive validation results
- **Cleanup Report** - Any repairs performed
- **Action Required** - Clear next steps

## Using the Automation

### Automatic Daily Sync

The workflow runs automatically every day at 2 AM UTC. No action required!

When changes are detected:
1. You'll receive a notification (if enabled)
2. A new PR is created automatically
3. Review the PR when convenient
4. Click "Merge" if everything looks good

### Manual Trigger

You can trigger a sync anytime:

1. Go to **Actions** tab
2. Select **"Auto-Sync Upstream with QA Validation"**
3. Click **"Run workflow"**
4. Optionally enable "Force sync" to sync even if no changes
5. Click **"Run workflow"** button

### Reviewing PRs

When a sync PR is created:

1. **Check the PR Description**
   - Review the status badge (✅/⚠️/❌)
   - Read the summary stats
   - Review new upstream commits

2. **Check the Files Changed Tab**
   - Verify new skills look correct
   - Ensure no local customizations were overwritten

3. **Review QA Reports**
   - YAML validation status
   - Security scan results
   - File integrity check

4. **Take Action**
   - ✅ **If Passed**: Click "Merge pull request"
   - ⚠️ **If Warnings**: Review warnings, decide if acceptable
   - ❌ **If Critical**: Review issues, may need manual fixes

## PR Labels

The automation automatically adds labels:
- `automated` - Created by automation
- `upstream-sync` - Syncing from upstream
- `ready-to-merge` - All QA checks passed ✅
- `needs-review` - Warnings or issues detected ⚠️

## Configuration

### Customizing Protected Files

Edit the `rsync` command in `.github/workflows/auto-sync-upstream.yml`:

```yaml
rsync -av --ignore-existing /tmp/upstream_repo/ ./ \
  --exclude='README.md' \
  --exclude='YOUR-CUSTOM-FILE.md' \
  --exclude='your-directory/' \
  ...
```

### Adjusting Schedule

Change the cron expression:

```yaml
schedule:
  # Daily at 2 AM UTC
  - cron: '0 2 * * *'
  
  # Options:
  # - cron: '0 */6 * * *'  # Every 6 hours
  # - cron: '0 0 * * 0'    # Weekly (Sunday midnight)
  # - cron: '0 8 * * 1-5'  # Weekdays at 8 AM
```

### Customizing QA Checks

Add your own validation in the "Run comprehensive QA validation" step:

```yaml
- name: Run comprehensive QA validation
  run: |
    # Your custom checks here
    python your-custom-validator.py
    
    # Add results to QA report
    echo "### Your Custom Check" >> /tmp/qa-report.md
    echo "✅ Check passed" >> /tmp/qa-report.md
```

## Troubleshooting

### No PR Created

**Issue:** Workflow runs but no PR appears

**Possible causes:**
1. No new commits in upstream
2. Changes resulted in no file differences
3. GitHub token permissions issue

**Check:**
- View workflow logs in Actions tab
- Check "Summary" output at end of workflow
- Verify `.github/last-upstream-sync` is updated

### Merge Conflicts

**Issue:** PR shows merge conflicts

**This shouldn't happen** because we use `rsync --ignore-existing`. If it does:

1. Checkout the sync branch locally
2. Resolve conflicts manually
3. Push the resolution
4. PR will update automatically

### QA Validation Fails

**Issue:** PR marked with ❌ or ⚠️

**Steps:**
1. Review the QA Report section in PR
2. Check which validation failed
3. Decide if acceptable or needs fix
4. If needs fix:
   - Close the PR
   - Fix issues in main branch
   - Re-run workflow manually

### YAML Validation Issues

**Issue:** YAML validation fails on new upstream skills

**Likely causes:**
- Upstream added skill with invalid YAML
- Upstream used unquoted colons in description

**Solution:**
1. View the validation errors in PR
2. Edit the problematic SKILL.md files
3. Fix YAML syntax (quote strings with colons)
4. Commit fixes to the sync branch
5. QA will re-run automatically

## Monitoring

### Workflow Status

Check workflow status:
- **Actions Tab** → **Auto-Sync Upstream with QA Validation**
- Green ✅ = Successful (PR created or no changes)
- Red ❌ = Failed (check logs)

### Notifications

Enable notifications for:
- New pull requests created
- Workflow failures
- PR ready for review

**Settings** → **Notifications** → Enable:
- "Pull requests"
- "Actions"

## Security

The automation is designed with security in mind:

✅ **Read-only access** to upstream repository  
✅ **Never overwrites** protected customizations  
✅ **Scans for secrets** before creating PR  
✅ **Validates all code** with QA checks  
✅ **Creates PR** (not auto-merge) for human review  
✅ **Uses GitHub token** with minimal permissions  

## Benefits

### Time Savings
- ⏱️ **No manual checks** - Automation monitors for you
- ⏱️ **No manual merging** - Intelligent merge preserves customizations
- ⏱️ **No manual validation** - Comprehensive QA runs automatically
- ⏱️ **No manual PR creation** - Everything documented in PR

### Quality Assurance
- ✅ **Consistent validation** - Same QA every time
- ✅ **Early detection** - Catches issues before merge
- ✅ **Automatic repair** - Fixes common problems
- ✅ **Full traceability** - Complete logs and reports

### Risk Reduction
- 🛡️ **Protected customizations** - Never lose your work
- 🛡️ **Security scans** - Catches potential vulnerabilities
- 🛡️ **Review required** - Human approval before merge
- 🛡️ **Rollback capable** - Easy to revert if needed

## Example PR

When the automation runs successfully, you'll see a PR like:

```markdown
# 🔄 Automated Upstream Sync

✅ **QA Status:** PASSED

This PR automatically merges the latest changes from ComposioHQ/awesome-claude-skills 
while preserving all local customizations.

## Summary
- **Upstream Commit:** `e762a98`
- **New Files:** 5
- **Modified Files:** 2
- **Total Skills:** 112

## New Commits from Upstream
- Add new langchain integration skill (a1b2c3d)
- Fix YAML frontmatter in docker skill (d4e5f6g)
- Update README with new examples (h7i8j9k)

## Merge Strategy
Using rsync with --ignore-existing to preserve local customizations

### Files Changed
- New files: 5
- Modified files: 2

## YAML Validation Results
✅ All YAML frontmatter valid

## Skill Index Regeneration
✅ Regenerated SKILL-INDEX.json: 112 skills

## Comprehensive QA Validation

### Security Scan
✅ No hardcoded secrets detected
✅ No dangerous code execution patterns

### File Integrity
✅ ARCHITECTURE.md preserved
✅ UNIVERSAL-FORMAT.md preserved
✅ tools/README.md preserved

### Repository Stats
- Total SKILL.md files: 112

**Status:** ✅ All checks passed

## Local Customizations Preserved
[... list of protected files ...]

## Action Required
✅ **Ready to Merge** - All QA checks passed. Click "Merge" to apply these updates.
```

## Support

**Issues?** [Open an issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues)  
**Questions?** [Start a discussion](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/discussions)  
**Workflow not running?** Check Actions tab for error logs

## See Also

- [Validate Skills Workflow](.github/workflows/validate-skills.yml) - YAML validation on PR
- [Upstream Sync Workflow](.github/workflows/upstream-sync.yml) - Alternative manual sync
- [Tools Documentation](../../tools/README.md) - Automation scripts used by this workflow

---

🤖 **Automated by GitHub Actions** | 🔄 **Daily at 2 AM UTC** | ✅ **QA Validated**
