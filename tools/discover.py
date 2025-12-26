#!/usr/bin/env python3
"""
Skill Discovery Tool - Find the perfect Claude skill for your needs.

This interactive tool helps you search, filter, and discover skills in the repository
without needing to know what exists beforehand.
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

def load_index(index_path: str) -> Dict:
    """Load skill index from file."""
    try:
        with open(index_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Skill index not found at {index_path}")
        print("Run 'python tools/index-skills.py' to generate the index first.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid skill index file at {index_path}")
        sys.exit(1)

def search_skills(skills: List[Dict], query: str) -> List[Dict]:
    """Search skills by keywords in name, description, and tags."""
    query_lower = query.lower()
    results = []
    
    for skill in skills:
        # Search in name
        if query_lower in skill['name'].lower():
            results.append({'skill': skill, 'score': 10})
            continue
        
        # Search in description
        if query_lower in skill['description'].lower():
            results.append({'skill': skill, 'score': 5})
            continue
        
        # Search in tags
        if any(query_lower in tag for tag in skill['tags']):
            results.append({'skill': skill, 'score': 3})
            continue
    
    # Sort by score and return skills
    results.sort(key=lambda x: x['score'], reverse=True)
    return [r['skill'] for r in results]

def filter_by_category(skills: List[Dict], category: str) -> List[Dict]:
    """Filter skills by category."""
    return [s for s in skills if s['category'].lower() == category.lower()]

def filter_by_tag(skills: List[Dict], tag: str) -> List[Dict]:
    """Filter skills by tag."""
    return [s for s in skills if tag.lower() in [t.lower() for t in s['tags']]]

def display_skill_summary(skill: Dict, index: Optional[int] = None):
    """Display a brief summary of a skill."""
    prefix = f"{index}. " if index is not None else "• "
    print(f"\n{prefix}📦 {skill['name']}")
    print(f"   Category: {skill['category']}")
    desc = skill['description'][:100] + "..." if len(skill['description']) > 100 else skill['description']
    print(f"   {desc}")

def display_skill_details(skill: Dict, repo_root: str):
    """Display detailed information about a skill."""
    print(f"\n{'='*80}")
    print(f"📦 {skill['name']}")
    print(f"{'='*80}")
    print(f"\n📁 Location: {skill['path']}")
    print(f"📂 Category: {skill['category']}")
    print(f"\n📝 Description:\n{skill['description']}")
    
    if skill['tags']:
        print(f"\n🏷️  Tags: {', '.join(skill['tags'])}")
    
    if 'author' in skill:
        print(f"\n👤 Author: {skill['author']}")
    
    if 'version' in skill:
        print(f"🔢 Version: {skill['version']}")
    
    print(f"\n📄 Skill file: {skill['skill_file']}")
    
    # Installation instructions
    print(f"\n📥 Installation:")
    print(f"   Claude.ai: Upload the file '{skill['skill_file']}'")
    print(f"   Claude Code: cp -r {skill['path']} ~/.config/claude-code/skills/")
    
    # Check for universal format
    universal_tiers = ['tier-1-instruction-only', 'tier-2-tool-enhanced', 'tier-3-claude-only']
    for tier in universal_tiers:
        universal_path = Path(repo_root) / 'universal' / tier / skill['name']
        if universal_path.exists():
            print(f"   Universal (Any LLM): See universal/{tier}/{skill['name']}/")
            break
    
    print(f"\n{'='*80}\n")

def interactive_mode(index: Dict, repo_root: str):
    """Interactive skill discovery interface."""
    print("\n" + "="*80)
    print("🔍 Claude Skills Discovery Tool")
    print("="*80)
    print(f"\nWelcome! I'll help you find the perfect skill for your needs.")
    print(f"Total skills available: {index['total_skills']}")
    print(f"\nCommands:")
    print("  search <keywords>  - Search for skills by keywords")
    print("  category <name>    - Show skills in a category")
    print("  tag <name>         - Filter by tag")
    print("  list               - List all skills")
    print("  categories         - Show all categories")
    print("  tags               - Show all tags")
    print("  <number>           - View details of skill by number")
    print("  help               - Show this help message")
    print("  quit               - Exit")
    print("\n" + "="*80)
    
    current_results = []
    
    while True:
        try:
            command = input("\n> ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['quit', 'exit', 'q']:
                print("👋 Thanks for using Claude Skills Discovery!")
                break
            
            if command.lower() == 'help':
                print("\nCommands:")
                print("  search <keywords>  - Search for skills by keywords")
                print("  category <name>    - Show skills in a category")
                print("  tag <name>         - Filter by tag")
                print("  list               - List all skills")
                print("  categories         - Show all categories")
                print("  tags               - Show all tags")
                print("  <number>           - View details of skill by number")
                print("  help               - Show this help message")
                print("  quit               - Exit")
                continue
            
            if command.lower() == 'list':
                current_results = index['skills']
                print(f"\n📋 All Skills ({len(current_results)}):")
                for i, skill in enumerate(current_results, 1):
                    display_skill_summary(skill, i)
                continue
            
            if command.lower() == 'categories':
                print("\n📂 Available Categories:")
                for i, cat in enumerate(index['categories'], 1):
                    count = len([s for s in index['skills'] if s['category'] == cat])
                    print(f"  {i}. {cat} ({count} skills)")
                print("\nUse 'category <name>' to see skills in a category")
                continue
            
            if command.lower() == 'tags':
                all_tags = set()
                for skill in index['skills']:
                    all_tags.update(skill['tags'])
                print("\n🏷️  Available Tags:")
                for i, tag in enumerate(sorted(all_tags), 1):
                    count = len([s for s in index['skills'] if tag in s['tags']])
                    print(f"  {tag} ({count})", end='  ')
                    if i % 5 == 0:
                        print()
                print("\n\nUse 'tag <name>' to filter by tag")
                continue
            
            if command.lower().startswith('search '):
                query = command[7:].strip()
                if not query:
                    print("❌ Please provide search keywords")
                    continue
                
                results = search_skills(index['skills'], query)
                current_results = results
                
                if results:
                    print(f"\n🔍 Found {len(results)} skill(s) matching '{query}':")
                    for i, skill in enumerate(results, 1):
                        display_skill_summary(skill, i)
                    print(f"\nType a number to see details, or refine your search")
                else:
                    print(f"❌ No skills found matching '{query}'")
                    print("Try different keywords or use 'tags' to see available options")
                continue
            
            if command.lower().startswith('category '):
                category = command[9:].strip()
                if not category:
                    print("❌ Please provide a category name")
                    continue
                
                results = filter_by_category(index['skills'], category)
                current_results = results
                
                if results:
                    print(f"\n📂 Skills in '{category}' ({len(results)}):")
                    for i, skill in enumerate(results, 1):
                        display_skill_summary(skill, i)
                    print(f"\nType a number to see details")
                else:
                    print(f"❌ Category '{category}' not found")
                    print("Use 'categories' to see available categories")
                continue
            
            if command.lower().startswith('tag '):
                tag = command[4:].strip()
                if not tag:
                    print("❌ Please provide a tag name")
                    continue
                
                results = filter_by_tag(index['skills'], tag)
                current_results = results
                
                if results:
                    print(f"\n🏷️  Skills tagged with '{tag}' ({len(results)}):")
                    for i, skill in enumerate(results, 1):
                        display_skill_summary(skill, i)
                    print(f"\nType a number to see details")
                else:
                    print(f"❌ No skills found with tag '{tag}'")
                    print("Use 'tags' to see available tags")
                continue
            
            # Try to parse as number
            try:
                num = int(command)
                if current_results and 1 <= num <= len(current_results):
                    display_skill_details(current_results[num - 1], repo_root)
                else:
                    print(f"❌ Invalid number. Please choose 1-{len(current_results)}")
            except ValueError:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands")
        
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for using Claude Skills Discovery!")
            break
        except EOFError:
            break

def quick_search(index: Dict, query: str, repo_root: str):
    """Quick non-interactive search."""
    results = search_skills(index['skills'], query)
    
    if results:
        print(f"\n🔍 Found {len(results)} skill(s) matching '{query}':\n")
        for skill in results:
            display_skill_details(skill, repo_root)
    else:
        print(f"❌ No skills found matching '{query}'")
        print("\nTry:")
        print(f"  - Different keywords")
        print(f"  - Run 'python tools/discover.py' for interactive mode")
        print(f"  - Browse categories with '--categories'")

def list_categories(index: Dict):
    """List all categories."""
    print("\n📂 Available Categories:\n")
    for cat in index['categories']:
        count = len([s for s in index['skills'] if s['category'] == cat])
        print(f"  • {cat} ({count} skills)")
    print(f"\nUse '--category <name>' to see skills in a category")

def list_category_skills(index: Dict, category: str, repo_root: str):
    """List skills in a category."""
    results = filter_by_category(index['skills'], category)
    
    if results:
        print(f"\n📂 Skills in '{category}' ({len(results)}):\n")
        for skill in results:
            display_skill_details(skill, repo_root)
    else:
        print(f"❌ Category '{category}' not found")
        print("\nAvailable categories:")
        for cat in index['categories']:
            print(f"  • {cat}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Discover Claude skills - Find the perfect skill for your needs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended for exploration)
  python tools/discover.py
  
  # Quick search
  python tools/discover.py --search "domain name"
  python tools/discover.py --search "pdf"
  
  # Browse by category
  python tools/discover.py --categories
  python tools/discover.py --category "Business & Marketing"
  
  # List all skills
  python tools/discover.py --list
        """
    )
    
    parser.add_argument(
        '--index',
        default='SKILL-INDEX.json',
        help='Path to skill index file (default: SKILL-INDEX.json)'
    )
    parser.add_argument(
        '--search',
        metavar='QUERY',
        help='Search for skills by keywords'
    )
    parser.add_argument(
        '--categories',
        action='store_true',
        help='List all categories'
    )
    parser.add_argument(
        '--category',
        metavar='NAME',
        help='Show skills in a specific category'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all skills'
    )
    
    args = parser.parse_args()
    
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = str(script_dir.parent)
    
    # Load index
    index_path = args.index if os.path.isabs(args.index) else os.path.join(repo_root, args.index)
    index = load_index(index_path)
    
    # Handle command-line arguments
    if args.search:
        quick_search(index, args.search, repo_root)
    elif args.categories:
        list_categories(index)
    elif args.category:
        list_category_skills(index, args.category, repo_root)
    elif args.list:
        print(f"\n📋 All Skills ({index['total_skills']}):\n")
        for skill in index['skills']:
            display_skill_details(skill, repo_root)
    else:
        # Interactive mode
        interactive_mode(index, repo_root)

if __name__ == '__main__':
    main()
