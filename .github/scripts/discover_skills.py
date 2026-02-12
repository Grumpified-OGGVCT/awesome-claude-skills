#!/usr/bin/env python3
"""
Discover new Claude skills from GitHub using public API.
"""
import os
import json
import requests
import time
from pathlib import Path

def main():
    # Configuration
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    DISCOVERY_LIMIT = int(os.environ.get('DISCOVERY_LIMIT', 10))
    
    # Build headers - only include Authorization if token is available
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    else:
        print("⚠️  No GITHUB_TOKEN set - using unauthenticated requests (rate limits apply)")
    
    # Load previously discovered skills
    discovery_file = Path('.github/skill-discovery/discovered-skills.json')
    with open(discovery_file) as f:
        discovery_data = json.load(f)
    
    previous_urls = set(
        item['repo_url'] for item in discovery_data['discovered'] + 
        discovery_data['integrated'] + discovery_data['rejected']
    )
    
    print(f"📊 Previously tracked: {len(previous_urls)} skills")
    print(f"🎯 Discovery limit: {DISCOVERY_LIMIT} new skills")
    
    # Search for Claude skills on GitHub
    search_queries = [
        'claude skill markdown in:readme',
        'claude prompt template in:file extension:md',
        'claude instructions SKILL.md in:path',
        'AI agent skill claude in:readme',
        'LLM workflow template in:readme language:markdown'
    ]
    
    discovered_skills = []
    
    for query in search_queries:
        if len(discovered_skills) >= DISCOVERY_LIMIT:
            break
        
        print(f"\n🔍 Searching: {query}")
        
        # GitHub Code Search API (free, public)
        url = f'https://api.github.com/search/code?q={query}&per_page=10'
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            results = response.json()
            
            for item in results.get('items', []):
                if len(discovered_skills) >= DISCOVERY_LIMIT:
                    break
                
                repo_url = item['repository']['html_url']
                
                # Skip if already tracked
                if repo_url in previous_urls:
                    continue
                
                # Skip our own repo
                if 'Grumpified-OGGVCT/awesome-claude-skills' in repo_url:
                    continue
                
                # Skip upstream repo (already synced separately)
                if 'ComposioHQ/awesome-claude-skills' in repo_url:
                    continue
                
                skill_info = {
                    'repo_url': repo_url,
                    'repo_name': item['repository']['full_name'],
                    'file_path': item['path'],
                    'file_url': item['html_url'],
                    'discovered_at': time.strftime('%Y-%m-%d %H:%M:%S UTC'),
                    'query': query,
                    'stars': item['repository'].get('stargazers_count', 0),
                    'description': item['repository'].get('description', '')
                }
                
                discovered_skills.append(skill_info)
                print(f"  ✅ {skill_info['repo_name']} ({skill_info['stars']} ⭐)")
            
            # Rate limiting - be nice to GitHub API
            time.sleep(2)
            
        except requests.exceptions.RequestException as e:
            print(f"  ⚠️ Search failed: {e}")
            continue
    
    # Save discovered skills
    discovery_data['discovered'].extend(discovered_skills)
    
    with open(discovery_file, 'w') as f:
        json.dump(discovery_data, f, indent=2)
    
    # Output for GitHub Actions
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"skills_found={len(discovered_skills)}\n")
        f.write(f"has_discoveries={'true' if discovered_skills else 'false'}\n")
    
    print(f"\n📊 Summary: Discovered {len(discovered_skills)} new skills")

if __name__ == '__main__':
    main()
