#!/usr/bin/env python3
"""
Model Tester for Universal Skills

Tests a skill across different models and providers to verify compatibility.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Dict, List

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai package not installed. Install with: pip install openai")

REPO_ROOT = Path(__file__).parent.parent


def test_skill_with_model(skill_path: Path, provider: str, model: str, api_key: str = None) -> Dict:
    """Test a single skill with a specific model"""
    
    if not OPENAI_AVAILABLE:
        return {"error": "openai package not installed"}
    
    # Load system prompt
    system_prompt_path = skill_path / "system-prompt.md"
    if not system_prompt_path.exists():
        return {"error": "system-prompt.md not found"}
    
    with open(system_prompt_path, 'r', encoding='utf-8') as f:
        system_prompt = f.read()
    
    # Configure client based on provider
    if provider == "openrouter":
        base_url = "https://openrouter.ai/api/v1"
        api_key = api_key or os.getenv("OPENROUTER_API_KEY")
    elif provider == "ollama":
        base_url = "http://localhost:11434/v1"
        api_key = "ollama"  # Dummy key for local Ollama
    else:
        return {"error": f"Unknown provider: {provider}"}
    
    if not api_key:
        return {"error": f"No API key provided for {provider}"}
    
    # Create client
    client = OpenAI(base_url=base_url, api_key=api_key)
    
    # Simple test message
    test_message = "Hello! Please provide a brief example of what you can do based on your instructions."
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt[:2000]},  # Truncate for speed
                {"role": "user", "content": test_message}
            ],
            max_tokens=200,
            timeout=30
        )
        
        result = {
            "success": True,
            "model": model,
            "provider": provider,
            "response_preview": response.choices[0].message.content[:200] + "...",
            "tokens_used": {
                "prompt": response.usage.prompt_tokens if hasattr(response.usage, 'prompt_tokens') else 0,
                "completion": response.usage.completion_tokens if hasattr(response.usage, 'completion_tokens') else 0,
            }
        }
        return result
        
    except Exception as e:
        return {
            "success": False,
            "model": model,
            "provider": provider,
            "error": str(e)
        }


def test_skill(skill_path: Path, providers: List[str], models: Dict[str, List[str]], api_keys: Dict[str, str]) -> Dict:
    """Test a skill across multiple providers and models"""
    
    results = {
        "skill": skill_path.name,
        "tests": []
    }
    
    for provider in providers:
        provider_models = models.get(provider, [])
        api_key = api_keys.get(provider)
        
        for model in provider_models:
            print(f"Testing {provider}/{model}...", end=" ")
            
            result = test_skill_with_model(skill_path, provider, model, api_key)
            results["tests"].append(result)
            
            if result.get("success"):
                print("✓")
            else:
                print(f"✗ ({result.get('error', 'unknown error')})")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Test universal skills across different models"
    )
    parser.add_argument(
        "--skill",
        required=True,
        help="Path to skill directory (e.g., universal/tier-1-instruction-only/domain-name-brainstormer)"
    )
    parser.add_argument(
        "--providers",
        nargs="+",
        default=["ollama"],
        choices=["openrouter", "ollama"],
        help="Providers to test with"
    )
    parser.add_argument(
        "--models",
        help="Comma-separated models per provider (e.g., 'openrouter:claude-3.5,ollama:llama3.2')"
    )
    parser.add_argument(
        "--openrouter-key",
        help="OpenRouter API key (or set OPENROUTER_API_KEY env var)"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick test with default free models only"
    )
    
    args = parser.parse_args()
    
    if not OPENAI_AVAILABLE:
        print("Error: openai package required. Install with: pip install openai")
        return 1
    
    # Parse skill path
    skill_path = Path(args.skill)
    if not skill_path.exists():
        print(f"Error: Skill path not found: {args.skill}")
        return 1
    
    # Configure models to test
    if args.quick:
        models = {
            "ollama": ["llama3.2:3b"],
            "openrouter": []  # Skip OpenRouter in quick mode
        }
        providers = ["ollama"]
    elif args.models:
        # Parse models from command line
        models = {}
        for item in args.models.split(","):
            provider, model = item.split(":")
            if provider not in models:
                models[provider] = []
            models[provider].append(model)
        providers = args.providers
    else:
        # Default models
        models = {
            "ollama": ["llama3.2", "qwen2.5", "mistral"],
            "openrouter": [
                "anthropic/claude-3.5-sonnet",
                "openai/gpt-4o",
                "meta-llama/llama-3.2-3b-instruct:free"
            ]
        }
        providers = args.providers
    
    # Configure API keys
    api_keys = {
        "openrouter": args.openrouter_key or os.getenv("OPENROUTER_API_KEY"),
        "ollama": "ollama"
    }
    
    # Run tests
    print(f"\nTesting skill: {skill_path.name}")
    print("=" * 60)
    
    results = test_skill(skill_path, providers, models, api_keys)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    total = len(results["tests"])
    passed = sum(1 for t in results["tests"] if t.get("success"))
    failed = total - passed
    
    print(f"Total tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed > 0:
        print("\nFailed tests:")
        for test in results["tests"]:
            if not test.get("success"):
                print(f"  ✗ {test['provider']}/{test['model']}: {test.get('error')}")
    
    # Save results to JSON
    output_file = skill_path / "test-results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: {output_file}")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
