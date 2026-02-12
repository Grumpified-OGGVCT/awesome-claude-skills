#!/usr/bin/env python3
"""
Test the daily skills aggregation workflow components.
"""
import json
import os
import sys
from pathlib import Path

def test_discovery_tracking():
    """Test that discovery tracking file is properly initialized."""
    print("🧪 Testing discovery tracking initialization...")
    
    discovery_file = Path('.github/skill-discovery/discovered-skills.json')
    
    if not discovery_file.exists():
        print("  ❌ Discovery file doesn't exist")
        return False
    
    try:
        with open(discovery_file) as f:
            data = json.load(f)
        
        required_keys = ['discovered', 'integrated', 'rejected']
        for key in required_keys:
            if key not in data:
                print(f"  ❌ Missing key: {key}")
                return False
            if not isinstance(data[key], list):
                print(f"  ❌ Key {key} is not a list")
                return False
        
        print("  ✅ Discovery tracking file is valid")
        return True
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON: {e}")
        return False

def test_scripts_exist():
    """Test that required scripts exist and are executable."""
    print("\n🧪 Testing script files...")
    
    scripts = [
        '.github/scripts/discover_skills.py',
        '.github/scripts/validate_skills.py'
    ]
    
    all_exist = True
    for script in scripts:
        script_path = Path(script)
        if not script_path.exists():
            print(f"  ❌ Script not found: {script}")
            all_exist = False
        elif not os.access(script_path, os.X_OK):
            print(f"  ⚠️  Script not executable: {script}")
        else:
            print(f"  ✅ Script exists and is executable: {script}")
    
    return all_exist

def test_workflow_yaml():
    """Test that workflow YAML is valid."""
    print("\n🧪 Testing workflow YAML...")
    
    try:
        import yaml
        with open('.github/workflows/daily-skills-aggregation.yml') as f:
            workflow = yaml.safe_load(f)
        
        # Check required keys
        if 'name' not in workflow:
            print("  ❌ Missing 'name' in workflow")
            return False
        
        # 'on' gets parsed as True (boolean) in YAML
        if True not in workflow and 'on' not in workflow:
            print("  ❌ Missing trigger in workflow")
            return False
        
        if 'jobs' not in workflow:
            print("  ❌ Missing 'jobs' in workflow")
            return False
        
        print(f"  ✅ Workflow YAML is valid: {workflow['name']}")
        print(f"  ✅ Has {len(workflow['jobs'])} job(s)")
        
        return True
    except Exception as e:
        print(f"  ❌ Workflow YAML validation failed: {e}")
        return False

def test_documentation():
    """Test that documentation exists."""
    print("\n🧪 Testing documentation...")
    
    docs = [
        '.github/workflows/DAILY-AGGREGATION-README.md',
        'README.md'
    ]
    
    all_exist = True
    for doc in docs:
        if not Path(doc).exists():
            print(f"  ❌ Documentation missing: {doc}")
            all_exist = False
        else:
            print(f"  ✅ Documentation exists: {doc}")
    
    return all_exist

def test_readme_mentions_workflow():
    """Test that README mentions the new workflow."""
    print("\n🧪 Testing README content...")
    
    with open('README.md') as f:
        content = f.read()
    
    required_phrases = [
        'Daily AI Skills Discovery',
        'Universal Skills Discovery',
        'DAILY-AGGREGATION-README'
    ]
    
    all_found = True
    for phrase in required_phrases:
        if phrase in content:
            print(f"  ✅ README mentions: {phrase}")
        else:
            print(f"  ❌ README missing mention of: {phrase}")
            all_found = False
    
    return all_found

def main():
    """Run all tests."""
    print("=" * 70)
    print("Testing Daily AI LLM Universal Skills Aggregation Workflow")
    print("=" * 70)
    
    tests = [
        ("Discovery Tracking", test_discovery_tracking),
        ("Script Files", test_scripts_exist),
        ("Workflow YAML", test_workflow_yaml),
        ("Documentation", test_documentation),
        ("README Content", test_readme_mentions_workflow)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 70)
    print(f"Results: {passed_count}/{total_count} tests passed")
    print("=" * 70)
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Workflow is ready to use.")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed. Please review.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
