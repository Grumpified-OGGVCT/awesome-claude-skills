#!/bin/bash
# sync-upstream.sh
#
# Synchronizes this fork with the upstream ComposioHQ/awesome-claude-skills repository
# while preserving the universal/ directory and other GrumpiFied customizations.
#
# This ensures backward compatibility by:
# 1. Keeping original skills in sync with upstream
# 2. Preserving GrumpiFied additions (universal/, tools/, docs/, etc.)
# 3. Allowing easy updates without conflicts

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Syncing with Upstream Repository${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Change to repository root
cd "$REPO_ROOT"

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo -e "${RED}Error: Not in a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}Warning: You have uncommitted changes${NC}"
    echo "Please commit or stash your changes before syncing."
    echo
    git status --short
    echo
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Configure upstream remote if not exists
UPSTREAM_REPO="https://github.com/ComposioHQ/awesome-claude-skills.git"

if ! git remote get-url upstream >/dev/null 2>&1; then
    echo -e "${YELLOW}Adding upstream remote: $UPSTREAM_REPO${NC}"
    git remote add upstream "$UPSTREAM_REPO"
else
    echo -e "${GREEN}Upstream remote already configured${NC}"
fi

# Fetch upstream changes
echo
echo -e "${BLUE}Fetching upstream changes...${NC}"
git fetch upstream

# Get current branch
CURRENT_BRANCH=$(git branch --show-current)
echo -e "Current branch: ${GREEN}$CURRENT_BRANCH${NC}"

# Determine what to merge
# If upstream has a 'main' branch, use that; otherwise use 'master'
if git ls-remote --heads upstream main | grep main >/dev/null; then
    UPSTREAM_BRANCH="main"
elif git ls-remote --heads upstream master | grep master >/dev/null; then
    UPSTREAM_BRANCH="master"
else
    echo -e "${RED}Error: Could not find main or master branch in upstream${NC}"
    exit 1
fi

echo -e "Upstream branch: ${GREEN}$UPSTREAM_BRANCH${NC}"

# Show what will be merged
echo
echo -e "${BLUE}Changes from upstream:${NC}"
git log HEAD..upstream/$UPSTREAM_BRANCH --oneline --max-count=10

# Ask for confirmation
echo
read -p "Do you want to merge these changes? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Sync cancelled"
    exit 0
fi

# Create a backup branch
BACKUP_BRANCH="backup-before-sync-$(date +%Y%m%d-%H%M%S)"
echo
echo -e "${YELLOW}Creating backup branch: $BACKUP_BRANCH${NC}"
git branch "$BACKUP_BRANCH"

# Merge upstream changes
echo
echo -e "${BLUE}Merging upstream/$UPSTREAM_BRANCH into $CURRENT_BRANCH...${NC}"

if git merge upstream/$UPSTREAM_BRANCH --no-edit; then
    echo -e "${GREEN}✓ Merge successful${NC}"
    
    # Check if universal/ directory was affected
    if git diff HEAD~1 HEAD --name-only | grep "^universal/" >/dev/null 2>&1; then
        echo -e "${YELLOW}Warning: universal/ directory was affected by merge${NC}"
        echo "You may need to review and reconvert skills"
    fi
    
else
    echo -e "${RED}✗ Merge conflict detected${NC}"
    echo
    echo "To resolve:"
    echo "  1. Fix conflicts in the affected files"
    echo "  2. Run: git add <resolved-files>"
    echo "  3. Run: git commit"
    echo
    echo "To abort the merge:"
    echo "  git merge --abort"
    echo
    echo "To restore from backup:"
    echo "  git reset --hard $BACKUP_BRANCH"
    echo
    exit 1
fi

# List changed files
echo
echo -e "${BLUE}Files changed from upstream:${NC}"
git diff --name-status HEAD~1 HEAD | grep -v "^universal/" || echo "  (none outside universal/)"

# Suggest next steps
echo
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Sync completed successfully${NC}"
echo -e "${BLUE}========================================${NC}"
echo
echo "Next steps:"
echo "  1. Review changes: git log -1"
echo "  2. Re-convert skills: python tools/convert.py --all"
echo "  3. Test conversions: python tools/validate.py --all"
echo "  4. Commit universal/ changes: git add universal/ && git commit"
echo "  5. Push to your fork: git push origin $CURRENT_BRANCH"
echo
echo "If something went wrong:"
echo "  git reset --hard $BACKUP_BRANCH"
echo

# Offer to run conversion automatically
echo
read -p "Do you want to re-convert all skills now? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Running conversion tool...${NC}"
    python3 "$SCRIPT_DIR/convert.py" --all
    
    echo
    echo -e "${GREEN}Conversion complete!${NC}"
    echo "Review changes with: git status"
fi
