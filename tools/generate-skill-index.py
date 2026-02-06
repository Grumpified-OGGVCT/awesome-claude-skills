#!/usr/bin/env python3
"""
Generate SKILL-INDEX.json from all SKILL.md files in the repository.
Parses YAML frontmatter and auto-categorizes skills.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
import yaml


def extract_yaml_frontmatter(content: str) -> Optional[Dict]:
    """Extract YAML frontmatter from markdown content."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            print(f"YAML parse error: {e}")
            return None
    return None


def categorize_skill(skill_name: str, description: str, tags: List[str]) -> str:
    """Auto-categorize a skill based on its name, description, and tags."""
    name_lower = skill_name.lower()
    desc_lower = description.lower()
    tags_lower = [t.lower() for t in tags]
    
    # Automation skills
    if 'automation' in name_lower:
        return "App Automation"
    
    # Document processing
    if any(x in name_lower or x in desc_lower for x in ['pdf', 'docx', 'pptx', 'document', 'word', 'excel']):
        return "Document Processing"
    
    # Development & Code
    if any(x in name_lower or x in desc_lower for x in ['code', 'github', 'git', 'mcp', 'builder', 'sdk', 'api']):
        return "Development & Code Tools"
    
    # Creative & Media
    if any(x in name_lower or x in desc_lower for x in ['design', 'canvas', 'image', 'video', 'art', 'creative']):
        return "Creative & Media"
    
    # Business & Marketing
    if any(x in name_lower or x in desc_lower for x in ['brand', 'marketing', 'ads', 'competitive', 'business']):
        return "Business & Marketing"
    
    # Communication & Writing
    if any(x in name_lower or x in desc_lower for x in ['slack', 'communication', 'writing', 'content', 'changelog']):
        return "Communication & Writing"
    
    # Productivity & Organization
    if any(x in name_lower or x in desc_lower for x in ['organizer', 'productivity', 'meeting', 'invoice', 'file-organizer']):
        return "Productivity & Organization"
    
    # Check tags
    for tag in tags_lower:
        if 'development' in tag or 'code' in tag:
            return "Development & Code Tools"
        if 'business' in tag or 'marketing' in tag:
            return "Business & Marketing"
        if 'creative' in tag or 'media' in tag:
            return "Creative & Media"
        if 'communication' in tag or 'writing' in tag:
            return "Communication & Writing"
        if 'productivity' in tag or 'organization' in tag:
            return "Productivity & Organization"
        if 'document' in tag:
            return "Document Processing"
    
    return "Other"


def find_skill_files(root_dir: Path) -> List[Path]:
    """Find all SKILL.md files in the repository."""
    skill_files = []
    for skill_file in root_dir.glob("*/SKILL.md"):
        # Skip hidden directories and specific paths
        if not any(part.startswith('.') for part in skill_file.parts):
            skill_files.append(skill_file)
    return sorted(skill_files)


def parse_skill_file(skill_file: Path, root_dir: Path) -> Optional[Dict]:
    """Parse a SKILL.md file and extract metadata."""
    try:
        content = skill_file.read_text(encoding='utf-8')
        frontmatter = extract_yaml_frontmatter(content)
        
        if not frontmatter:
            print(f"Warning: No YAML frontmatter in {skill_file}")
            return None
        
        skill_dir = skill_file.parent
        skill_name = frontmatter.get('name', skill_dir.name)
        description = frontmatter.get('description', '')
        tags = frontmatter.get('tags', [])
        
        # Ensure tags is a list
        if isinstance(tags, str):
            tags = [tags]
        elif not isinstance(tags, list):
            tags = []
        
        # Get category
        category = categorize_skill(skill_name, description, tags)
        
        # Relative path from root
        rel_path = skill_dir.relative_to(root_dir)
        
        skill_data = {
            "name": skill_name,
            "path": str(rel_path),
            "skill_file": str(skill_file.relative_to(root_dir)),
            "description": description,
            "category": category,
            "tags": tags if tags else []
        }
        
        # Add requires if present
        if 'requires' in frontmatter:
            skill_data['requires'] = frontmatter['requires']
        
        return skill_data
        
    except Exception as e:
        print(f"Error parsing {skill_file}: {e}")
        return None


def generate_skill_index(root_dir: Path) -> Dict:
    """Generate the complete skill index."""
    skill_files = find_skill_files(root_dir)
    print(f"Found {len(skill_files)} SKILL.md files")
    
    skills = []
    categories_set = set()
    
    for skill_file in skill_files:
        skill_data = parse_skill_file(skill_file, root_dir)
        if skill_data:
            skills.append(skill_data)
            categories_set.add(skill_data['category'])
        else:
            print(f"Skipped: {skill_file}")
    
    # Sort skills by name
    skills.sort(key=lambda x: x['name'])
    
    # Sort categories
    categories = sorted(categories_set)
    
    index = {
        "version": "2.0",
        "generated_date": "2026-02-06",
        "total_skills": len(skills),
        "categories": categories,
        "skills": skills
    }
    
    return index


def main():
    """Main function to generate SKILL-INDEX.json."""
    root_dir = Path(__file__).parent.parent
    output_file = root_dir / "SKILL-INDEX.json"
    
    print("Generating SKILL-INDEX.json...")
    print(f"Root directory: {root_dir}")
    
    index = generate_skill_index(root_dir)
    
    # Write to file with pretty formatting
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Generated {output_file}")
    print(f"   Total skills: {index['total_skills']}")
    print(f"   Categories: {len(index['categories'])}")
    print(f"   Categories: {', '.join(index['categories'])}")


if __name__ == "__main__":
    main()
