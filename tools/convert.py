#!/usr/bin/env python3
"""
Claude Skills to Universal Format Converter

This tool converts Claude-specific skills to universal OpenAI-compatible format
while maintaining backward compatibility with the original repository.

Key principles:
- Original skills are NEVER modified
- Universal format is DERIVED from original skills
- Re-runnable: Can regenerate universal format at any time
- Tracks which original skill each universal skill came from
"""

import os
import re
import json
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Directories
REPO_ROOT = Path(__file__).parent.parent
UNIVERSAL_DIR = REPO_ROOT / "universal"
TIER1_DIR = UNIVERSAL_DIR / "tier-1-instruction-only"
TIER2_DIR = UNIVERSAL_DIR / "tier-2-tool-enhanced"
TIER3_DIR = UNIVERSAL_DIR / "tier-3-claude-only"


class SkillConverter:
    """Converts Claude skills to universal format"""
    
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.stats = {
            "tier1": 0,
            "tier2": 0,
            "tier3": 0,
            "skipped": 0,
            "errors": 0
        }
    
    def find_skills(self) -> List[Path]:
        """Find all SKILL.md files in the repository"""
        skills = []
        for skill_md in REPO_ROOT.glob("*/SKILL.md"):
            # Skip universal directory
            if "universal" not in str(skill_md):
                skills.append(skill_md.parent)
        
        # Also check nested skills (e.g., document-skills/pdf)
        for skill_md in REPO_ROOT.glob("*/*/SKILL.md"):
            if "universal" not in str(skill_md):
                skills.append(skill_md.parent)
        
        return sorted(skills)
    
    def parse_skill_md(self, skill_path: Path) -> Tuple[Dict, str]:
        """Parse SKILL.md and extract frontmatter and content"""
        skill_md = skill_path / "SKILL.md"
        
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML frontmatter
        frontmatter = {}
        body = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    body = parts[2].strip()
                except yaml.YAMLError as e:
                    print(f"Warning: Could not parse YAML frontmatter in {skill_md}: {e}")
        
        return frontmatter, body
    
    def classify_skill(self, skill_path: Path, frontmatter: Dict, content: str) -> int:
        """
        Classify skill into tiers:
        1 = Instruction-only
        2 = Tool-enhanced
        3 = Claude-only
        """
        # Check for scripts directory
        has_scripts = (skill_path / "scripts").exists()
        
        # Check for Claude-specific features
        claude_specific_patterns = [
            r'claude\.ai',
            r'artifacts?',
            r'MCP server',
            r'Model Context Protocol',
            r'canvas',
        ]
        
        is_claude_specific = any(
            re.search(pattern, content, re.IGNORECASE)
            for pattern in claude_specific_patterns
        )
        
        # Classification logic
        if is_claude_specific and not has_scripts:
            # Heavily Claude-specific without alternatives
            return 3
        elif has_scripts:
            # Has tools that can be adapted
            return 2
        else:
            # Pure instructions
            return 1
    
    def remove_claude_language(self, content: str) -> str:
        """Remove Claude-specific language from content"""
        replacements = [
            (r'\bClaude should\b', 'The assistant should'),
            (r'\bClaude can\b', 'The assistant can'),
            (r'\bClaude will\b', 'The assistant will'),
            (r'\bClaude\b', 'The assistant'),
            (r'\bclaude\.ai\b', 'your AI interface'),
            (r'\bClaude Code\b', 'your development environment'),
            (r'\bthis skill\b', 'these instructions'),
        ]
        
        result = content
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def convert_tier1_skill(self, skill_path: Path, frontmatter: Dict, content: str) -> Dict:
        """Convert a Tier 1 (instruction-only) skill"""
        skill_name = skill_path.name
        
        # Clean content
        universal_content = self.remove_claude_language(content)
        
        # Create system prompt
        system_prompt = f"""# {frontmatter.get('name', skill_name).replace('-', ' ').title()}

{frontmatter.get('description', '')}

{universal_content}
"""
        
        # Create metadata
        metadata = {
            "name": frontmatter.get('name', skill_name),
            "description": frontmatter.get('description', ''),
            "tier": 1,
            "version": "1.0",
            "source": {
                "original_path": str(skill_path.relative_to(REPO_ROOT)),
                "last_sync": datetime.now().isoformat()[:10],
                "upstream_repo": "anthropics/skills"
            },
            "requirements": {
                "tool_calling": False,
                "min_context_window": 4096,
                "recommended_context_window": 8192
            },
            "compatibility": {
                "tested_providers": ["openrouter", "ollama"],
                "tested_models": ["llama3.2", "qwen2.5", "mistral"],
                "recommended_models": [
                    "anthropic/claude-3.5-sonnet",
                    "openai/gpt-4o",
                    "meta-llama/llama-3.2-90b-instruct"
                ]
            },
            "tags": []
        }
        
        # Create API example
        api_example = {
            "model": "MODEL_NAME_HERE",
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt[:500] + "..."  # Truncated for example
                },
                {
                    "role": "user",
                    "content": "USER_REQUEST_HERE"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        return {
            "system_prompt": system_prompt,
            "metadata": metadata,
            "api_example": api_example
        }
    
    def convert_tier2_skill(self, skill_path: Path, frontmatter: Dict, content: str) -> Dict:
        """Convert a Tier 2 (tool-enhanced) skill"""
        # Start with Tier 1 conversion
        result = self.convert_tier1_skill(skill_path, frontmatter, content)
        result["metadata"]["tier"] = 2
        result["metadata"]["requirements"]["tool_calling"] = True
        
        # Analyze scripts to create tool schema
        scripts_dir = skill_path / "scripts"
        tools = []
        
        if scripts_dir.exists():
            for script_file in scripts_dir.glob("*.py"):
                # Parse script to extract function info (basic heuristic)
                with open(script_file, 'r', encoding='utf-8') as f:
                    script_content = f.read()
                
                # Look for function definitions
                func_pattern = r'def\s+(\w+)\s*\((.*?)\):'
                matches = re.findall(func_pattern, script_content)
                
                for func_name, params in matches:
                    if not func_name.startswith('_'):  # Skip private functions
                        tools.append({
                            "type": "function",
                            "function": {
                                "name": func_name,
                                "description": f"Function from {script_file.name}",
                                "parameters": {
                                    "type": "object",
                                    "properties": {},
                                    "required": []
                                }
                            }
                        })
        
        result["tools_schema"] = tools
        
        # Create manual fallback version
        manual_version = f"""# {result['metadata']['name']} - Manual Version

For models without tool calling support, follow these manual instructions:

## Overview
{frontmatter.get('description', '')}

## Manual Workflow

{content}

## Note
If your model supports tool calling, use the tools-schema.json file for better integration.
Available tools: {', '.join([t['function']['name'] for t in tools])}
"""
        
        result["manual_version"] = manual_version
        
        return result
    
    def convert_tier3_skill(self, skill_path: Path, frontmatter: Dict, content: str) -> Dict:
        """Convert a Tier 3 (Claude-only) skill - mostly documentation"""
        skill_name = skill_path.name
        
        return {
            "readme": f"""# {frontmatter.get('name', skill_name).replace('-', ' ').title()}

**Tier 3: Claude-Only Skill**

This skill requires Claude-specific features and cannot be fully converted to universal format.

## Original Skill
- **Path**: {skill_path.relative_to(REPO_ROOT)}
- **Description**: {frontmatter.get('description', '')}

## Why Claude-Only?
This skill uses features that are specific to Claude:
- Claude Artifacts
- Claude MCP Servers
- Claude.ai interface features

## Using This Skill
To use this skill, please refer to the original version in the repository root:
- Claude.ai: Upload the skill through the UI
- Claude Code: Place in ~/.config/claude-code/skills/
- Claude API: Use the Claude Skills API

## Alternative Approaches
[Document any potential workarounds or alternative tools]

## Resources
- Original skill: {skill_path.relative_to(REPO_ROOT)}
- Claude Skills Documentation: https://docs.claude.com/en/api/skills-guide
""",
            "metadata": {
                "name": frontmatter.get('name', skill_name),
                "description": frontmatter.get('description', ''),
                "tier": 3,
                "version": "1.0",
                "source": {
                    "original_path": str(skill_path.relative_to(REPO_ROOT)),
                    "last_sync": datetime.now().isoformat()[:10]
                },
                "compatibility": {
                    "claude_only": True,
                    "reason": "Requires Claude-specific features"
                }
            }
        }
    
    def write_converted_skill(self, tier: int, skill_name: str, converted: Dict):
        """Write converted skill to universal directory"""
        # Determine output directory
        if tier == 1:
            output_dir = TIER1_DIR / skill_name
        elif tier == 2:
            output_dir = TIER2_DIR / skill_name
        else:
            output_dir = TIER3_DIR / skill_name
        
        if self.dry_run:
            print(f"[DRY RUN] Would create: {output_dir}")
            return
        
        # Create directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write files based on tier
        if tier in [1, 2]:
            # System prompt
            with open(output_dir / "system-prompt.md", 'w', encoding='utf-8') as f:
                f.write(converted["system_prompt"])
            
            # Metadata
            with open(output_dir / "metadata.yaml", 'w', encoding='utf-8') as f:
                yaml.dump(converted["metadata"], f, default_flow_style=False, sort_keys=False)
            
            # API example
            # Update api_example to use actual system prompt content
            converted["api_example"]["messages"][0]["content"] = f"[Content from system-prompt.md]"
            with open(output_dir / "api-example.json", 'w', encoding='utf-8') as f:
                json.dump(converted["api_example"], f, indent=2)
        
        if tier == 2:
            # Tools schema
            with open(output_dir / "tools-schema.json", 'w', encoding='utf-8') as f:
                json.dump(converted["tools_schema"], f, indent=2)
            
            # Manual version
            with open(output_dir / "manual-version.md", 'w', encoding='utf-8') as f:
                f.write(converted["manual_version"])
        
        if tier == 3:
            # README
            with open(output_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(converted["readme"])
            
            # Metadata
            with open(output_dir / "metadata.yaml", 'w', encoding='utf-8') as f:
                yaml.dump(converted["metadata"], f, default_flow_style=False, sort_keys=False)
    
    def convert_skill(self, skill_path: Path) -> bool:
        """Convert a single skill"""
        try:
            print(f"Converting: {skill_path.name}")
            
            # Parse skill
            frontmatter, content = self.parse_skill_md(skill_path)
            
            # Classify tier
            tier = self.classify_skill(skill_path, frontmatter, content)
            print(f"  Classified as: Tier {tier}")
            
            # Convert based on tier
            if tier == 1:
                converted = self.convert_tier1_skill(skill_path, frontmatter, content)
                self.stats["tier1"] += 1
            elif tier == 2:
                converted = self.convert_tier2_skill(skill_path, frontmatter, content)
                self.stats["tier2"] += 1
            else:
                converted = self.convert_tier3_skill(skill_path, frontmatter, content)
                self.stats["tier3"] += 1
            
            # Write to universal directory
            self.write_converted_skill(tier, skill_path.name, converted)
            
            print(f"  ✓ Converted successfully")
            return True
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            self.stats["errors"] += 1
            return False
    
    def convert_all(self):
        """Convert all skills in the repository"""
        skills = self.find_skills()
        print(f"Found {len(skills)} skills to convert\n")
        
        for skill_path in skills:
            self.convert_skill(skill_path)
            print()
        
        # Print summary
        print("=" * 60)
        print("Conversion Summary:")
        print(f"  Tier 1 (Instruction-only): {self.stats['tier1']}")
        print(f"  Tier 2 (Tool-enhanced):    {self.stats['tier2']}")
        print(f"  Tier 3 (Claude-only):      {self.stats['tier3']}")
        print(f"  Errors:                    {self.stats['errors']}")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Claude skills to universal format"
    )
    parser.add_argument(
        "--skill",
        help="Convert a specific skill by name"
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3],
        help="Convert only skills of a specific tier"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Convert all skills"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview conversion without writing files"
    )
    
    args = parser.parse_args()
    
    converter = SkillConverter(dry_run=args.dry_run)
    
    if args.skill:
        # Convert specific skill
        skill_path = REPO_ROOT / args.skill
        if not skill_path.exists():
            print(f"Error: Skill not found: {args.skill}")
            return 1
        converter.convert_skill(skill_path)
    
    elif args.all:
        # Convert all skills
        converter.convert_all()
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
