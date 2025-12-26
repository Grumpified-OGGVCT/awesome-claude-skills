#!/usr/bin/env python3
"""
Example: Using Universal Skills with Different Providers

This script demonstrates how to use the same skill with multiple LLM providers.
"""

import os
from pathlib import Path

# Check if openai is installed
try:
    from openai import OpenAI
except ImportError:
    print("Please install the openai package: pip install openai")
    exit(1)

# Path to repository
REPO_ROOT = Path(__file__).parent.parent
SKILL_PATH = REPO_ROOT / "universal/tier-1-instruction-only/domain-name-brainstormer/system-prompt.md"


def load_skill(skill_path: Path) -> str:
    """Load a skill's system prompt"""
    with open(skill_path, 'r', encoding='utf-8') as f:
        return f.read()


def test_with_openrouter(system_prompt: str, user_message: str):
    """Test with OpenRouter (cloud, multiple models)"""
    print("\n" + "=" * 60)
    print("Testing with OpenRouter (Claude 3.5 Sonnet)")
    print("=" * 60)
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("⚠️  OPENROUTER_API_KEY not set. Skipping OpenRouter test.")
        print("   Get a key at https://openrouter.ai")
        return
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500
        )
        
        print("\n✅ Success!")
        print("\nResponse:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_with_ollama(system_prompt: str, user_message: str):
    """Test with Ollama (local, free)"""
    print("\n" + "=" * 60)
    print("Testing with Ollama (Llama 3.2)")
    print("=" * 60)
    
    try:
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Dummy key for local
        )
        
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500
        )
        
        print("\n✅ Success!")
        print("\nResponse:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTo use Ollama:")
        print("1. Install: curl -fsSL https://ollama.com/install.sh | sh")
        print("2. Pull model: ollama pull llama3.2")
        print("3. Run this script again")


def main():
    print("=" * 60)
    print("Universal Skills Demo")
    print("=" * 60)
    print("\nThis demo shows the same skill working with multiple providers:")
    print("- OpenRouter (cloud, many models)")
    print("- Ollama (local, free)")
    
    # Load the skill
    print(f"\nLoading skill from: {SKILL_PATH.relative_to(REPO_ROOT)}")
    system_prompt = load_skill(SKILL_PATH)
    print(f"✓ Loaded {len(system_prompt)} characters")
    
    # Test message
    user_message = "I'm building an AI-powered task manager. Suggest 3 creative domain names."
    print(f"\nTest query: \"{user_message}\"")
    
    # Test with both providers
    test_with_openrouter(system_prompt, user_message)
    test_with_ollama(system_prompt, user_message)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
The same skill worked with both providers! This demonstrates:
✓ No vendor lock-in - switch providers anytime
✓ Cost flexibility - free local or paid cloud
✓ Privacy control - keep data local or use APIs
✓ Model variety - choose the best model for your needs

Next steps:
1. Explore more skills in universal/tier-1-instruction-only/
2. Read the documentation in docs/
3. Convert your own skills with tools/convert.py
""")


if __name__ == "__main__":
    main()
