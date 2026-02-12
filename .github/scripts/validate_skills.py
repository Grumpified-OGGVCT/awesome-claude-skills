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
    
    # Build headers - only include Authorization if token is available
    headers = {
        'Accept': 'application/vnd.github.v3.raw'
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    else:
        print("⚠️  No GITHUB_TOKEN set - using unauthenticated requests (rate limits apply)")
    
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
            
            # Check for YAML frontmatter (support both LF and CRLF line endings)
            yaml_pattern = r'^---\s*\r?\n(.*?)\r?\n---\s*\r?\n'
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
                
                # Ensure data is a dict
                if not isinstance(data, dict):
                    print("  ❌ YAML frontmatter is not a dictionary")
                    skill['validated'] = False
                    skill['validation_error'] = 'YAML frontmatter must be a dictionary'
                    invalid_count += 1
                    continue
                
                # Check required fields
                if 'name' not in data or 'description' not in data:
                    print("  ❌ Missing required fields (name or description)")
                    skill['validated'] = False
                    skill['validation_error'] = 'Missing required fields'
                    invalid_count += 1
                    continue
                
                # Security check - comprehensive patterns from SECURITY-AUDIT-2026-02-11
                security_issues = []
                
                # Check for hardcoded credentials
                if re.search(r'(api[_-]?key|password|token)\s*[=:]\s*["\'][^"\']{10,}["\']', 
                            content, re.IGNORECASE):
                    # Exclude common placeholders
                    if not re.search(r'(your[_-]|YOUR[_-]|<[^>]*>|placeholder|example|test)', content, re.IGNORECASE):
                        security_issues.append('Potential hardcoded credentials')
                
                # Check for dangerous code execution
                if re.search(r'\beval\s*\(|\bexec\s*\(', content):
                    security_issues.append('Dangerous code execution patterns (eval/exec)')
                
                # Shell / process execution patterns
                if re.search(r'\bsubprocess\.(Popen|call|run|check_call|check_output)\s*\(', content):
                    security_issues.append('Use of subprocess process execution')
                if re.search(r'\bos\.(system|popen)\s*\(', content):
                    security_issues.append('Use of os.system/os.popen for shell execution')
                if re.search(r'shell\s*=\s*True', content):
                    security_issues.append('Use of shell=True in process execution')
                
                # Encoded payloads / base64
                if re.search(r'base64\.b64(?:encode|decode)\s*\(', content):
                    # Check if it's not just legitimate API usage
                    if re.search(r'base64.*eval|base64.*exec|decode.*eval', content, re.IGNORECASE):
                        security_issues.append('Suspicious base64 usage with code execution')
                
                # Prompt-injection phrases
                if re.search(r'(?i)ignore (all )?previous instructions', content):
                    security_issues.append('Prompt-injection phrase: ignore previous instructions')
                if re.search(r'(?i)disregard (the )?(above|earlier) (instructions|rules)', content):
                    security_issues.append('Prompt-injection phrase: disregard earlier instructions')
                
                # Suspicious URLs / potential obfuscation
                if re.search(r'https?://\d{1,3}(?:\.\d{1,3}){3}', content):
                    security_issues.append('URL with literal IP address (suspicious)')
                if re.search(r'https?://(?:bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd)/', content, re.IGNORECASE):
                    security_issues.append('Use of URL shortener (possible obfuscation)')
                
                # Data exfiltration patterns
                if re.search(r'https?://(?:pastebin\.com|hastebin\.com|webhook\.site|requestbin)', content, re.IGNORECASE):
                    security_issues.append('Potential data exfiltration endpoint')
                
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
