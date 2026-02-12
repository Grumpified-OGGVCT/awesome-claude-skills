# GitHub Actions Workflows Documentation

This directory contains GitHub Actions workflows and their comprehensive documentation.

## 📚 Documentation Files

### Quick Start
- **[WORKFLOW-SUMMARY.md](WORKFLOW-SUMMARY.md)** - Start here! Executive summary of all workflows, their status, and fixes applied.

### Detailed Documentation
- **[WORKFLOW-TESTING.md](WORKFLOW-TESTING.md)** - Complete testing guide with execution order, troubleshooting, and commands.
- **[WORKFLOW-TEST-RESULTS.md](WORKFLOW-TEST-RESULTS.md)** - Detailed test results and status for each workflow.

## 🔄 Workflows

Located in [`workflows/`](workflows/) directory:

1. **validate-skills.yml** - Validates YAML frontmatter and updates SKILL-INDEX.json
2. **link-check.yml** - Validates markdown links across the repository
3. **auto-sync-upstream.yml** - Syncs with ComposioHQ/awesome-claude-skills (daily 2 AM UTC)
4. **upstream-sync.yml** - Syncs with anthropics/skills (every 6 hours)
5. **daily-skills-aggregation.yml** - Discovers and aggregates new skills (daily 3 AM UTC)
6. **nlp-discovery-demo.yml** - NLP-based skill discovery demo (manual trigger only)

## ✅ Current Status

**Working:** 3 workflows confirmed functional  
**Fixed:** 2 workflows repaired and ready  
**Manual:** 1 workflow requires manual trigger  

See [WORKFLOW-SUMMARY.md](WORKFLOW-SUMMARY.md) for complete status.

## 🔧 Recent Fixes (2026-02-12)

- Fixed branch references (main → master) in auto-sync-upstream.yml
- Fixed upstream references (upstream/main → upstream/master)
- Fixed push targets in upstream-sync.yml
- Created comprehensive testing documentation

## 🚀 Testing Workflows

To test workflows manually:

```bash
# View workflow status
gh workflow list

# Trigger a workflow
gh workflow run validate-skills.yml

# Check recent runs
gh run list --workflow=validate-skills.yml
```

See [WORKFLOW-TESTING.md](WORKFLOW-TESTING.md) for complete testing procedures.

## 📂 Other Directories

- **scripts/** - Python scripts used by workflows
- **skill-discovery/** - Tracks discovered skills
- **last-upstream-sync** - Marker file for upstream sync tracking

## 🔍 Need Help?

1. Start with [WORKFLOW-SUMMARY.md](WORKFLOW-SUMMARY.md) for an overview
2. Check [WORKFLOW-TESTING.md](WORKFLOW-TESTING.md) for testing procedures
3. See [WORKFLOW-TEST-RESULTS.md](WORKFLOW-TEST-RESULTS.md) for detailed status
4. Review workflow files in [`workflows/`](workflows/) directory

## 📅 Last Updated

**Date:** 2026-02-12  
**Status:** All workflows documented and ready for production  
**Next Review:** After 48 hours of monitoring scheduled runs
