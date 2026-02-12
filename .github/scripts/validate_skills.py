#!/usr/bin/env python3
"""
Validate discovered skills for proper format and security.
"""
import os
import json
import requests
import re
import yaml
from pathlib import Path

def main():
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3.raw'
    }
    
    # Load discovered skills
    discovery_file = Path('.github/skill-discovery/discovered-skills.json')
    with open(discovery_file) as f:
        discovery_data = json.load(f)
    
    # Only process newly discovered (not yet validated)
    unprocessed = [s for s in discovery_data['discovered'] 
                  if 'validated' not in s or not s['validated']]
    
    valid_count = 0
    invalid_count = 0
    
    print(f"🔍 Validating {len(unprocessed)} skills...")
    
    for skill in unprocessed:
        print(f"\n📄 {skill['repo_name']} - {skill['file_path']}")
        
        # Download the skill file
        api_url = f"https://api.github.com/repos/{skill['repo_name']}/contents/{skill['file_path']}"
        
        try:
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            content = response.text
            
            # Check for YAML frontmatter
            yaml_pattern = r'^---\s*\n(.*?)\n---\s*\n'
            match = re.match(yaml_pattern, content, re.DOTALL)
            
            if not match:
                print("  ❌ No YAML frontmatter found")
                skill['validated'] = False
                skill['validation_error'] = 'Missing YAML frontmatter'
                invalid_count += 1
                continue
            
            # Parse YAML
            yaml_content = match.group(1)
            try:
                data = yaml.safe_load(yaml_content)
                
                # Check required fields
                if 'name' not in data or 'description' not in data:
                    print("  ❌ Missing required fields (name or description)")
                    skill['validated'] = False
                    skill['validation_error'] = 'Missing required fields'
                    invalid_count += 1
                    continue
                
                # Security check - basic patterns
                security_issues = []
                
                # Check for hardcoded credentials
                if re.search(r'(api[_-]?key|password|token)\s*[=:]\s*["\'][^"\']{10,}["\']', 
                            content, re.IGNORECASE):
                    security_issues.append('Potential hardcoded credentials')
                
                # Check for dangerous code execution
                if re.search(r'\beval\s*\(|\bexec\s*\(', content):
                    security_issues.append('Dangerous code execution patterns')
                
                if security_issues:
                    print(f"  ⚠️ Security issues: {', '.join(security_issues)}")
                    skill['validated'] = False
                    skill['validation_error'] = 'Security concerns: ' + ', '.join(security_issues)
                    invalid_count += 1
                    continue
                
                # Skill is valid!
                skill['validated'] = True
                skill['skill_name'] = data['name']
                skill['skill_description'] = data['description']
                skill['skill_category'] = data.get('category', 'general')
                skill['raw_content'] = content
                valid_count += 1
                
                print(f"  ✅ Valid: {data['name']}")
                
            except yaml.YAMLError as e:
                print(f"  ❌ YAML parse error: {e}")
                skill['validated'] = False
                skill['validation_error'] = f'YAML parse error: {str(e)}'
                invalid_count += 1
                continue
            
        except requests.exceptions.RequestException as e:
            print(f"  ⚠️ Download failed: {e}")
            skill['validated'] = False
            skill['validation_error'] = f'Download error: {str(e)}'
            invalid_count += 1
            continue
    
    # Save updated discovery data
    with open(discovery_file, 'w') as f:
        json.dump(discovery_data, f, indent=2)
    
    # Output for GitHub Actions
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"valid_skills={valid_count}\n")
        f.write(f"invalid_skills={invalid_count}\n")
        f.write(f"has_valid={'true' if valid_count > 0 else 'false'}\n")
    
    print(f"\n📊 Validation Summary:")
    print(f"  ✅ Valid: {valid_count}")
    print(f"  ❌ Invalid: {invalid_count}")

if __name__ == '__main__':
    main()
