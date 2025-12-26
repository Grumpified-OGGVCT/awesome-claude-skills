#!/usr/bin/env python3
"""
Skill Indexer - Generates a searchable index of all skills in the repository.

This tool scans all SKILL.md files and creates a comprehensive index
that can be used for skill discovery and search.
"""

import os
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional

def extract_yaml_frontmatter(content: str) -> Optional[Dict]:
    """Extract YAML frontmatter from markdown file."""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None

def extract_description(content: str, frontmatter: Optional[Dict]) -> str:
    """Extract skill description from frontmatter or content."""
    if frontmatter and 'description' in frontmatter:
        return frontmatter['description']
    
    # Remove frontmatter and look for first paragraph
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Find first paragraph after any headers
    lines = content.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('**'):
            # Get this paragraph
            paragraph = []
            for j in range(i, len(lines)):
                if lines[j].strip():
                    paragraph.append(lines[j].strip())
                else:
                    break
            return ' '.join(paragraph)[:500]
    
    return "No description available"

def extract_tags(content: str, skill_name: str, category: str) -> List[str]:
    """Extract or infer tags from skill content."""
    tags = set()
    
    # Add category as a tag
    tags.add(category.lower())
    
    # Common keywords to look for
    keywords = [
        'api', 'web', 'file', 'document', 'pdf', 'excel', 'word', 'powerpoint',
        'code', 'git', 'test', 'debug', 'automation', 'analysis', 'data',
        'marketing', 'business', 'research', 'writing', 'content', 'design',
        'video', 'image', 'media', 'creative', 'organization', 'productivity',
        'communication', 'meeting', 'email', 'slack', 'security', 'aws'
    ]
    
    content_lower = content.lower()
    for keyword in keywords:
        if keyword in content_lower or keyword in skill_name.lower():
            tags.add(keyword)
    
    return sorted(list(tags))

def determine_category(skill_path: str, readme_content: str) -> str:
    """Determine category from README.md."""
    categories = {
        'Document Processing': ['docx', 'pdf', 'pptx', 'xlsx'],
        'Development & Code Tools': [
            'artifacts-builder', 'changelog-generator', 'mcp-builder', 
            'skill-creator', 'webapp-testing'
        ],
        'Business & Marketing': [
            'brand-guidelines', 'competitive-ads-extractor', 
            'domain-name-brainstormer', 'internal-comms', 'lead-research-assistant'
        ],
        'Communication & Writing': [
            'content-research-writer', 'meeting-insights-analyzer'
        ],
        'Creative & Media': [
            'canvas-design', 'image-enhancer', 'slack-gif-creator', 
            'theme-factory', 'video-downloader'
        ],
        'Productivity & Organization': [
            'file-organizer', 'invoice-organizer', 'raffle-winner-picker'
        ]
    }
    
    skill_name = os.path.basename(skill_path)
    
    for category, skills in categories.items():
        if skill_name in skills:
            return category
    
    # Check if skill is mentioned under a category in README
    if skill_name in readme_content:
        for category in categories.keys():
            # Find section
            section_pattern = rf'### {re.escape(category)}.*?(?=###|\Z)'
            section_match = re.search(section_pattern, readme_content, re.DOTALL)
            if section_match and skill_name in section_match.group(0):
                return category
    
    return 'Other'

def scan_skills(repo_root: str) -> List[Dict]:
    """Scan repository for all skills and build index."""
    skills = []
    repo_path = Path(repo_root)
    
    # Read README for category information
    readme_path = repo_path / 'README.md'
    readme_content = ''
    if readme_path.exists():
        readme_content = readme_path.read_text()
    
    # Find all SKILL.md files
    skill_files = list(repo_path.glob('*/SKILL.md'))
    skill_files.extend(list(repo_path.glob('*/*/SKILL.md')))
    
    for skill_file in skill_files:
        try:
            content = skill_file.read_text()
            frontmatter = extract_yaml_frontmatter(content)
            
            # Get skill directory
            skill_dir = skill_file.parent
            skill_name = frontmatter.get('name') if frontmatter else skill_dir.name
            
            # Build skill entry
            skill_entry = {
                'name': skill_name,
                'path': str(skill_dir.relative_to(repo_path)),
                'skill_file': str(skill_file.relative_to(repo_path)),
                'description': extract_description(content, frontmatter),
                'category': determine_category(str(skill_dir), readme_content),
                'tags': extract_tags(content, skill_name, determine_category(str(skill_dir), readme_content))
            }
            
            # Add optional fields from frontmatter
            if frontmatter:
                if 'author' in frontmatter:
                    skill_entry['author'] = frontmatter['author']
                if 'version' in frontmatter:
                    skill_entry['version'] = frontmatter['version']
            
            skills.append(skill_entry)
            
        except Exception as e:
            print(f"Warning: Failed to process {skill_file}: {e}")
            continue
    
    return sorted(skills, key=lambda x: x['name'].lower())

def generate_index(repo_root: str, output_file: str):
    """Generate skill index file."""
    print("Scanning repository for skills...")
    skills = scan_skills(repo_root)
    
    index = {
        'version': '1.0',
        'total_skills': len(skills),
        'categories': sorted(list(set(s['category'] for s in skills))),
        'skills': skills
    }
    
    print(f"Found {len(skills)} skills across {len(index['categories'])} categories")
    
    # Write index file
    output_path = Path(output_file)
    with open(output_path, 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"✅ Index written to {output_path}")
    
    # Print summary
    print("\nSkills by Category:")
    category_counts = {}
    for skill in skills:
        cat = skill['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    for category in sorted(category_counts.keys()):
        print(f"  {category}: {category_counts[category]}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate searchable index of all skills in the repository'
    )
    parser.add_argument(
        '--output',
        default='SKILL-INDEX.json',
        help='Output file for skill index (default: SKILL-INDEX.json)'
    )
    
    args = parser.parse_args()
    
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    generate_index(str(repo_root), args.output)

if __name__ == '__main__':
    main()
