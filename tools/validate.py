#!/usr/bin/env python3
"""
Universal Skills Validator

Validates that converted skills meet the universal format requirements.
"""

import os
import json
import yaml
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

REPO_ROOT = Path(__file__).parent.parent
UNIVERSAL_DIR = REPO_ROOT / "universal"


class SkillValidator:
    """Validates universal skill format"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
    
    def validate_tier1_skill(self, skill_dir: Path, skip_tier_check: bool = False) -> bool:
        """Validate a Tier 1 skill directory"""
        skill_name = skill_dir.name
        all_valid = True
        
        # Check required files
        required_files = [
            "system-prompt.md",
            "metadata.yaml",
            "api-example.json"
        ]
        
        for filename in required_files:
            filepath = skill_dir / filename
            if not filepath.exists():
                self.errors.append(f"{skill_name}: Missing required file: {filename}")
                all_valid = False
        
        # Validate system-prompt.md
        if (skill_dir / "system-prompt.md").exists():
            with open(skill_dir / "system-prompt.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for Claude-specific language
            claude_patterns = [
                ("Claude should", "Use 'The assistant should' instead"),
                ("claude.ai", "Use 'your AI interface' instead"),
                ("Claude Code", "Use 'your development environment' instead"),
            ]
            
            for pattern, suggestion in claude_patterns:
                if pattern.lower() in content.lower():
                    self.warnings.append(
                        f"{skill_name}/system-prompt.md: Contains '{pattern}'. {suggestion}"
                    )
            
            # Check minimum length
            if len(content) < 200:
                self.warnings.append(
                    f"{skill_name}/system-prompt.md: Very short content ({len(content)} chars)"
                )
        
        # Validate metadata.yaml
        if (skill_dir / "metadata.yaml").exists():
            try:
                with open(skill_dir / "metadata.yaml", 'r', encoding='utf-8') as f:
                    metadata = yaml.safe_load(f)
                
                # Check required fields
                required_fields = ["name", "description", "tier"]
                for field in required_fields:
                    if field not in metadata:
                        self.errors.append(
                            f"{skill_name}/metadata.yaml: Missing required field: {field}"
                        )
                        all_valid = False
                
                # Validate tier (only if not skipping tier check)
                if not skip_tier_check and "tier" in metadata and metadata["tier"] != 1:
                    self.errors.append(
                        f"{skill_name}/metadata.yaml: Tier should be 1, got {metadata['tier']}"
                    )
                    all_valid = False
                
            except yaml.YAMLError as e:
                self.errors.append(f"{skill_name}/metadata.yaml: Invalid YAML: {e}")
                all_valid = False
        
        # Validate api-example.json
        if (skill_dir / "api-example.json").exists():
            try:
                with open(skill_dir / "api-example.json", 'r', encoding='utf-8') as f:
                    api_example = json.load(f)
                
                # Check required fields
                if "model" not in api_example:
                    self.errors.append(
                        f"{skill_name}/api-example.json: Missing 'model' field"
                    )
                    all_valid = False
                
                if "messages" not in api_example:
                    self.errors.append(
                        f"{skill_name}/api-example.json: Missing 'messages' field"
                    )
                    all_valid = False
                elif len(api_example["messages"]) < 2:
                    self.errors.append(
                        f"{skill_name}/api-example.json: Should have at least system and user messages"
                    )
                    all_valid = False
                
            except json.JSONDecodeError as e:
                self.errors.append(f"{skill_name}/api-example.json: Invalid JSON: {e}")
                all_valid = False
        
        if all_valid:
            self.passed.append(f"{skill_name} (Tier 1)")
        
        return all_valid
    
    def validate_tier2_skill(self, skill_dir: Path) -> bool:
        """Validate a Tier 2 skill directory"""
        skill_name = skill_dir.name
        
        # First validate as Tier 1, but skip tier check
        all_valid = self.validate_tier1_skill(skill_dir, skip_tier_check=True)
        
        # Check additional Tier 2 files
        required_files = [
            "tools-schema.json",
            "manual-version.md"
        ]
        
        for filename in required_files:
            filepath = skill_dir / filename
            if not filepath.exists():
                self.errors.append(f"{skill_name}: Missing required file: {filename}")
                all_valid = False
        
        # Validate tools-schema.json
        if (skill_dir / "tools-schema.json").exists():
            try:
                with open(skill_dir / "tools-schema.json", 'r', encoding='utf-8') as f:
                    tools = json.load(f)
                
                if not isinstance(tools, list):
                    self.errors.append(
                        f"{skill_name}/tools-schema.json: Should be an array of tool definitions"
                    )
                    all_valid = False
                else:
                    for i, tool in enumerate(tools):
                        if "type" not in tool or tool["type"] != "function":
                            self.errors.append(
                                f"{skill_name}/tools-schema.json: Tool {i} missing 'type': 'function'"
                            )
                            all_valid = False
                        
                        if "function" not in tool:
                            self.errors.append(
                                f"{skill_name}/tools-schema.json: Tool {i} missing 'function' field"
                            )
                            all_valid = False
                
            except json.JSONDecodeError as e:
                self.errors.append(f"{skill_name}/tools-schema.json: Invalid JSON: {e}")
                all_valid = False
        
        # Validate metadata tier
        if (skill_dir / "metadata.yaml").exists():
            try:
                with open(skill_dir / "metadata.yaml", 'r', encoding='utf-8') as f:
                    metadata = yaml.safe_load(f)
                
                if "tier" in metadata and metadata["tier"] != 2:
                    self.errors.append(
                        f"{skill_name}/metadata.yaml: Tier should be 2, got {metadata['tier']}"
                    )
                    all_valid = False
                
                if "requirements" in metadata:
                    if not metadata["requirements"].get("tool_calling"):
                        self.warnings.append(
                            f"{skill_name}/metadata.yaml: tool_calling should be true for Tier 2"
                        )
            except yaml.YAMLError:
                pass  # Already reported in tier1 validation
        
        if all_valid:
            # Update passed list
            self.passed = [p for p in self.passed if not p.startswith(skill_name)]
            self.passed.append(f"{skill_name} (Tier 2)")
        
        return all_valid
    
    def validate_tier3_skill(self, skill_dir: Path) -> bool:
        """Validate a Tier 3 skill directory"""
        skill_name = skill_dir.name
        all_valid = True
        
        # Check required files
        required_files = [
            "README.md",
            "metadata.yaml"
        ]
        
        for filename in required_files:
            filepath = skill_dir / filename
            if not filepath.exists():
                self.errors.append(f"{skill_name}: Missing required file: {filename}")
                all_valid = False
        
        # Validate metadata
        if (skill_dir / "metadata.yaml").exists():
            try:
                with open(skill_dir / "metadata.yaml", 'r', encoding='utf-8') as f:
                    metadata = yaml.safe_load(f)
                
                if "tier" in metadata and metadata["tier"] != 3:
                    self.errors.append(
                        f"{skill_name}/metadata.yaml: Tier should be 3, got {metadata['tier']}"
                    )
                    all_valid = False
                
                if "compatibility" in metadata:
                    if not metadata["compatibility"].get("claude_only"):
                        self.warnings.append(
                            f"{skill_name}/metadata.yaml: Should mark claude_only as true"
                        )
            
            except yaml.YAMLError as e:
                self.errors.append(f"{skill_name}/metadata.yaml: Invalid YAML: {e}")
                all_valid = False
        
        if all_valid:
            self.passed.append(f"{skill_name} (Tier 3)")
        
        return all_valid
    
    def validate_skill_dir(self, skill_dir: Path) -> bool:
        """Validate a skill directory based on its tier"""
        # Determine tier from parent directory
        parent = skill_dir.parent.name
        
        if parent == "tier-1-instruction-only":
            return self.validate_tier1_skill(skill_dir)
        elif parent == "tier-2-tool-enhanced":
            return self.validate_tier2_skill(skill_dir)
        elif parent == "tier-3-claude-only":
            return self.validate_tier3_skill(skill_dir)
        else:
            self.errors.append(f"{skill_dir}: Unknown tier directory: {parent}")
            return False
    
    def validate_all(self):
        """Validate all skills in the universal directory"""
        if not UNIVERSAL_DIR.exists():
            print("Error: universal/ directory does not exist")
            return False
        
        # Find all skill directories
        skill_dirs = []
        for tier_dir in ["tier-1-instruction-only", "tier-2-tool-enhanced", "tier-3-claude-only"]:
            tier_path = UNIVERSAL_DIR / tier_dir
            if tier_path.exists():
                skill_dirs.extend([d for d in tier_path.iterdir() if d.is_dir()])
        
        if not skill_dirs:
            print("No skills found in universal/ directory")
            return True
        
        print(f"Validating {len(skill_dirs)} skills...\n")
        
        for skill_dir in sorted(skill_dirs):
            self.validate_skill_dir(skill_dir)
        
        # Print results
        print("=" * 60)
        print(f"Validation Results:")
        print("=" * 60)
        
        if self.passed:
            print(f"\n✓ Passed ({len(self.passed)}):")
            for item in self.passed:
                print(f"  ✓ {item}")
        
        if self.warnings:
            print(f"\n⚠ Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        if self.errors:
            print(f"\n✗ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        print("\n" + "=" * 60)
        print(f"Total: {len(self.passed)} passed, {len(self.warnings)} warnings, {len(self.errors)} errors")
        print("=" * 60)
        
        return len(self.errors) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Validate universal skills format"
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        help="Validate a specific skill directory"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all skills"
    )
    
    args = parser.parse_args()
    
    validator = SkillValidator()
    
    if args.skill_dir:
        # Validate specific skill
        skill_path = Path(args.skill_dir)
        if not skill_path.exists():
            print(f"Error: Skill directory not found: {args.skill_dir}")
            return 1
        
        success = validator.validate_skill_dir(skill_path)
        
        # Print results
        if validator.passed:
            print(f"✓ {validator.passed[0]}")
        for warning in validator.warnings:
            print(f"⚠ {warning}")
        for error in validator.errors:
            print(f"✗ {error}")
        
        return 0 if success else 1
    
    elif args.all:
        # Validate all skills
        success = validator.validate_all()
        return 0 if success else 1
    
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    exit(main())
