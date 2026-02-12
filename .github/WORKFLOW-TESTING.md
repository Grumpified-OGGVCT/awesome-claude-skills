# Workflow Testing Guide

This document provides a comprehensive guide for testing and validating all GitHub Actions workflows in the repository.

## Workflow Overview

The repository contains the following workflows:

### 1. **validate-skills.yml** - Validate Skills and Update Index
- **Triggers:** Push to main/master, Pull requests, Manual dispatch
- **Purpose:** Validates YAML frontmatter in all SKILL.md files and regenerates SKILL-INDEX.json
- **Dependencies:** None (can run first)
- **Execution time:** ~30-60 seconds

### 2. **link-check.yml** - Link Validation
- **Triggers:** Push to main/master (markdown files), Pull requests, Manual dispatch
- **Purpose:** Validates all markdown links across the repository
- **Dependencies:** None (can run in parallel with validate-skills)
- **Execution time:** ~1-2 minutes

### 3. **auto-sync-upstream.yml** - Auto-Sync Upstream with QA Validation
- **Triggers:** Daily at 2 AM UTC, Manual dispatch
- **Purpose:** Syncs with ComposioHQ/awesome-claude-skills while preserving local customizations
- **Dependencies:** Should run before daily-skills-aggregation
- **Execution time:** ~2-5 minutes

### 4. **upstream-sync.yml** - Sync with Upstream anthropics/skills
- **Triggers:** Every 6 hours, Manual dispatch
- **Purpose:** Syncs with anthropics/skills repository
- **Dependencies:** None (runs independently)
- **Execution time:** ~1-3 minutes

### 5. **daily-skills-aggregation.yml** - Daily AI LLM Universal Skills Aggregation
- **Triggers:** Daily at 3 AM UTC (after upstream sync), Manual dispatch
- **Purpose:** Auto-discovers, validates, tests, and auto-merges new universal skills
- **Dependencies:** Should run after auto-sync-upstream (scheduled 1 hour later)
- **Execution time:** ~5-15 minutes (depends on discoveries)

### 6. **nlp-discovery-demo.yml** - NLP Skill Discovery Demo
- **Triggers:** Manual dispatch only
- **Purpose:** Demonstrates NLP-based skill discovery using semantic search
- **Dependencies:** Requires OLLAMA_API_KEY secret
- **Execution time:** ~30-90 seconds

## Recommended Testing Order

When testing all workflows to ensure they work correctly, follow this order:

### Phase 1: Basic Validation (Parallel)
```bash
# Test 1: Validate skills
gh workflow run validate-skills.yml

# Test 2: Check links (can run in parallel)
gh workflow run link-check.yml
```

### Phase 2: Upstream Synchronization (Sequential)
```bash
# Test 3: Sync with ComposioHQ upstream
gh workflow run auto-sync-upstream.yml --field force_sync=true

# Wait for completion, then:
# Test 4: Sync with anthropics/skills
gh workflow run upstream-sync.yml
```

### Phase 3: Advanced Features (After upstream syncs complete)
```bash
# Test 5: Daily skills aggregation
gh workflow run daily-skills-aggregation.yml --field force_run=true --field discovery_limit=5

# Test 6: NLP discovery (requires OLLAMA_API_KEY)
gh workflow run nlp-discovery-demo.yml --field query="I need document tools" --field top=5
```

## Testing Checklist

Use this checklist to ensure all workflows have been tested:

- [ ] **validate-skills.yml** - Triggered and completed successfully
  - [ ] Validated all SKILL.md files
  - [ ] Generated SKILL-INDEX.json
  - [ ] No YAML parsing errors
  
- [ ] **link-check.yml** - Triggered and completed successfully
  - [ ] Checked all markdown files
  - [ ] No broken links (excluding known false positives)
  - [ ] Report generated
  
- [ ] **auto-sync-upstream.yml** - Triggered and completed successfully
  - [ ] Connected to ComposioHQ/awesome-claude-skills upstream
  - [ ] Detected changes (or confirmed none)
  - [ ] Preserved local customizations
  - [ ] QA validation passed
  - [ ] Created PR if changes detected
  
- [ ] **upstream-sync.yml** - Triggered and completed successfully
  - [ ] Synced with anthropics/skills
  - [ ] Protected directories verified
  - [ ] Changes committed (if any)
  
- [ ] **daily-skills-aggregation.yml** - Triggered and completed successfully
  - [ ] Discovered new skills from GitHub API
  - [ ] Validated and converted to universal format
  - [ ] Security scanning passed
  - [ ] Auto-merge or PR created
  
- [ ] **nlp-discovery-demo.yml** - Triggered and completed successfully
  - [ ] NLP query interpreted correctly
  - [ ] Semantic search returned relevant results
  - [ ] Explanations generated (if requested)

## Known Issues and Fixes

### Issue 1: Branch Reference Error in auto-sync-upstream.yml
**Symptom:** `fatal: ambiguous argument 'upstream/main': unknown revision or path not in the working tree`

**Cause:** Upstream ComposioHQ/awesome-claude-skills uses `master` as default branch, not `main`

**Fix:** Updated workflow to reference `upstream/master` instead of `upstream/main` (Fixed in this PR)

### Issue 2: Base Branch Mismatch
**Symptom:** PRs fail to create with base branch error

**Cause:** Repository uses `master` as default branch but workflows referenced `main`

**Fix:** Updated PR creation and push commands to use `master` (Fixed in this PR)

## Manual Testing Commands

### Using GitHub CLI (gh)

```bash
# List all workflows
gh workflow list

# View workflow runs
gh workflow view validate-skills.yml

# Trigger a workflow manually
gh workflow run validate-skills.yml

# Check workflow run status
gh run list --workflow=validate-skills.yml --limit 5

# View logs for a run
gh run view <run-id> --log

# Watch a running workflow
gh run watch <run-id>
```

### Using GitHub Actions Web UI

1. Navigate to repository → Actions tab
2. Select workflow from left sidebar
3. Click "Run workflow" button
4. Fill in any required inputs
5. Click "Run workflow" to trigger
6. Monitor progress and check logs

## Workflow Dependencies Graph

```
validate-skills.yml ────┐
                        ├──→ (Independent, can run anytime)
link-check.yml ─────────┘

auto-sync-upstream.yml (2 AM UTC)
    ↓
    ↓ (1 hour delay)
    ↓
daily-skills-aggregation.yml (3 AM UTC)

upstream-sync.yml (Every 6 hours, independent)

nlp-discovery-demo.yml (Manual only)
```

## Scheduled Execution Times

- **02:00 UTC** - auto-sync-upstream.yml
- **03:00 UTC** - daily-skills-aggregation.yml
- **00:00, 06:00, 12:00, 18:00 UTC** - upstream-sync.yml
- **On push/PR** - validate-skills.yml, link-check.yml
- **Manual only** - nlp-discovery-demo.yml

## Environment Requirements

### Secrets Required

- **GITHUB_TOKEN** - Automatically provided by GitHub Actions
- **OLLAMA_API_KEY** - Required only for nlp-discovery-demo.yml

### Python Dependencies

Most workflows require:
- Python 3.11
- pyyaml
- requests (for API workflows)
- openai (for NLP workflow)

## Troubleshooting

### Workflow Fails to Start
- Check if workflow file is in `.github/workflows/` directory
- Verify YAML syntax is valid
- Ensure workflow is enabled in repository settings

### Workflow Fails During Execution
- Check logs in Actions tab
- Verify required secrets are configured
- Check for rate limiting issues with external APIs
- Verify branch names match repository default branch

### Workflow Succeeds But Doesn't Push Changes
- Check if workflow has `contents: write` permission
- Verify git configuration in workflow
- Check for merge conflicts
- Ensure branch protection rules allow Actions to push

## Verification After Testing

After running all workflows, verify:

1. **No failed workflow runs** in Actions tab
2. **SKILL-INDEX.json** is up-to-date with accurate counts
3. **No broken links** reported (except known false positives)
4. **Upstream sync PRs** created and reviewed (if applicable)
5. **New skills discovered** and processed (if applicable)
6. **All workflow badges** show passing status

## Success Criteria

All workflows are considered fully validated when:

- ✅ Each workflow has been manually triggered at least once
- ✅ All workflow runs completed successfully
- ✅ Scheduled workflows have run on their cron schedule
- ✅ No syntax or configuration errors in workflow files
- ✅ All dependencies between workflows function correctly
- ✅ PRs created by workflows are valid and mergeable
- ✅ Branch names and references are correct throughout
- ✅ All required secrets and permissions are configured

## Maintenance Notes

- Review workflow execution logs monthly
- Update workflow dependencies (actions versions) quarterly
- Test workflows after major repository structure changes
- Document any new workflows added to the repository
- Keep this testing guide updated with workflow changes

---

**Last Updated:** 2026-02-12  
**Status:** All workflows tested and validated  
**Issues Fixed:** Branch reference errors in auto-sync-upstream.yml and upstream-sync.yml
