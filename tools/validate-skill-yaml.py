#!/usr/bin/env python3
"""
Validate YAML frontmatter in all SKILL.md files.
Checks for syntax errors and required fields.

Usage:
    python validate-skill-yaml.py [--file FILE] [--fix] [--verbose]
    
Options:
    --file FILE      Validate specific file instead of all
    --fix            Auto-fix common issues (quotes, formatting)
    --verbose, -v    Show detailed validation info
    --help, -h       Show this help message
    
Examples:
    python validate-skill-yaml.py
    python validate-skill-yaml.py --file domain-name-brainstormer/SKILL.md
    python validate-skill-yaml.py --verbose
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


def extract_yaml_frontmatter(content: str, filepath: str) -> Tuple[Optional[Dict], Optional[str]]:
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return None, f"No YAML frontmatter found (missing --- delimiters)"
    
    yaml_content = match.group(1)
    try:
        data = yaml.safe_load(yaml_content)
        return data, None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def validate_skill_frontmatter(data: Dict, filepath: str) -> List[str]:
    """Validate required fields and data types in skill frontmatter."""
    errors = []
    
    # Required fields
    if 'name' not in data:
        errors.append("Missing required field: 'name'")
    elif not isinstance(data['name'], str):
        errors.append("Field 'name' must be a string")
    
    if 'description' not in data:
        errors.append("Missing required field: 'description'")
    elif not isinstance(data['description'], str):
        errors.append("Field 'description' must be a string")
    
    # Optional fields validation
    if 'tags' in data:
        if not isinstance(data['tags'], list):
            errors.append("Field 'tags' must be a list")
        else:
            for tag in data['tags']:
                if not isinstance(tag, str):
                    errors.append(f"Tag must be a string, found: {type(tag).__name__}")
    
    if 'requires' in data:
        if not isinstance(data['requires'], dict):
            errors.append("Field 'requires' must be a dictionary")
    
    if 'category' in data:
        if not isinstance(data['category'], str):
            errors.append("Field 'category' must be a string")
    
    return errors


def validate_skill_file(skill_file: Path) -> Tuple[bool, List[str]]:
    """Validate a single SKILL.md file."""
    try:
        content = skill_file.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Error reading file: {e}"]
    
    # Extract and parse YAML
    data, error = extract_yaml_frontmatter(content, str(skill_file))
    
    if error:
        return False, [error]
    
    if data is None:
        return False, ["No valid YAML frontmatter found"]
    
    # Validate fields
    errors = validate_skill_frontmatter(data, str(skill_file))
    
    if errors:
        return False, errors
    
    return True, []


def find_skill_files(root_dir: Path) -> List[Path]:
    """Find all SKILL.md files in the repository."""
    skill_files = []
    for skill_file in root_dir.glob("*/SKILL.md"):
        # Skip hidden directories
        if not any(part.startswith('.') for part in skill_file.parts):
            skill_files.append(skill_file)
    return sorted(skill_files)


def main():
    """Main function to validate all SKILL.md files."""
    parser = argparse.ArgumentParser(
        description='Validate YAML frontmatter in SKILL.md files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate-skill-yaml.py
  python validate-skill-yaml.py --file domain-name-brainstormer/SKILL.md
  python validate-skill-yaml.py --verbose
        """
    )
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Validate specific file instead of all'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed validation info'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-fix common issues (not implemented yet)'
    )
    
    args = parser.parse_args()
    
    root_dir = Path(__file__).parent.parent
    
    if args.file:
        # Validate single file
        skill_file = Path(args.file)
        if not skill_file.is_absolute():
            skill_file = root_dir / skill_file
        
        if not skill_file.exists():
            print(f"❌ File not found: {skill_file}")
            return 1
        
        skill_files = [skill_file]
        print(f"Validating {skill_file}...\n")
    else:
        # Validate all files
        skill_files = find_skill_files(root_dir)
        print(f"Validating {len(skill_files)} SKILL.md files...\n")
    
    errors_found = 0
    files_with_errors = []
    
    for skill_file in skill_files:
        valid, errors = validate_skill_file(skill_file)
        
        if not valid:
            errors_found += len(errors)
            files_with_errors.append(skill_file)
            
            rel_path = skill_file.relative_to(root_dir) if skill_file.is_relative_to(root_dir) else skill_file
            print(f"❌ {rel_path}")
            for error in errors:
                print(f"   - {error}")
            print()
        elif args.verbose:
            rel_path = skill_file.relative_to(root_dir) if skill_file.is_relative_to(root_dir) else skill_file
            print(f"✅ {rel_path}")
    
    # Summary
    print("=" * 70)
    if errors_found == 0:
        print(f"✅ All {len(skill_files)} SKILL.md files are valid!")
        return 0
    else:
        print(f"❌ Found {errors_found} errors in {len(files_with_errors)} files")
        print(f"   Valid files: {len(skill_files) - len(files_with_errors)}/{len(skill_files)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
