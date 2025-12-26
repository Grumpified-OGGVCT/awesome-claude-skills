#!/usr/bin/env python3
"""
NLP-Enhanced Skill Discovery Tool

Uses Ollama Cloud Service with Gemini 3 Flash Preview model for:
- Semantic search (understand intent, not just keywords)
- Intelligent query interpretation
- Skill explanations and recommendations
- Natural language interactions
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Try to import OpenAI library for Ollama cloud
try:
    from openai import OpenAI
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Warning: openai library not installed. NLP features disabled.")
    print("   Install with: pip install openai")

class NLPSkillDiscovery:
    """NLP-powered skill discovery using Ollama Cloud + Gemini 3 Flash Preview"""
    
    def __init__(self, index_path: str, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        """Initialize NLP discovery tool."""
        self.index = self.load_index(index_path)
        
        # Try multiple API key options in order of preference
        self.api_key = (
            api_key or 
            os.getenv('OLLAMA_TURBO_CLOUD_API_KEY') or  # Fastest option
            os.getenv('OLLAMA_PROXY_API_KEY') or 
            os.getenv('OLLAMA_API_KEY') or
            os.getenv('OLLAMA_CLOUD_API_KEY')  # Legacy fallback
        )
        
        # Determine endpoint
        if endpoint:
            self.endpoint = endpoint
        elif os.getenv('OLLAMA_TURBO_CLOUD_API_KEY'):
            self.endpoint = "https://turbo.ollama.cloud/v1"
        elif os.getenv('OLLAMA_PROXY_API_KEY'):
            self.endpoint = "https://proxy.ollama.cloud/v1"
        else:
            self.endpoint = "https://cloud.ollama.ai/v1"
        
        self.client = None
        
        if OLLAMA_AVAILABLE and self.api_key:
            try:
                # Initialize Ollama Cloud client
                self.client = OpenAI(
                    base_url=self.endpoint,
                    api_key=self.api_key
                )
                endpoint_name = self.endpoint.split('//')[1].split('/')[0]
                print(f"✅ NLP-enhanced search enabled via {endpoint_name}")
                print(f"   Model: Gemini 3 Flash Preview")
            except Exception as e:
                print(f"⚠️  Could not initialize Ollama Cloud: {e}")
                self.client = None
        elif not self.api_key:
            print("⚠️  No Ollama API key found. Using basic search.")
            print("   Available keys: OLLAMA_TURBO_CLOUD_API_KEY, OLLAMA_PROXY_API_KEY, OLLAMA_API_KEY")
            print("   Set with: export OLLAMA_TURBO_CLOUD_API_KEY='your-key'")
    
    def load_index(self, index_path: str) -> Dict:
        """Load skill index from file."""
        try:
            with open(index_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Skill index not found at {index_path}")
            print("Run 'python tools/index-skills.py' to generate the index first.")
            sys.exit(1)
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Use Gemini 3 Flash Preview to understand query intent and find relevant skills.
        
        This goes beyond keyword matching to understand what the user actually wants.
        """
        if not self.client:
            # Fallback to basic keyword search
            return self._basic_search(query)[:top_k]
        
        try:
            # Create context with all skills
            skills_context = self._build_skills_context()
            
            # Ask Gemini to analyze the query and recommend skills
            prompt = f"""You are an expert skill recommender. A user is searching for: "{query}"

Available skills:
{skills_context}

Based on the user's query, recommend the TOP {top_k} most relevant skills.
Consider:
1. Direct matches (explicit mentions)
2. Implicit needs (what they're trying to accomplish)
3. Related capabilities (complementary skills)
4. Use case alignment

Respond ONLY with a JSON array of skill names, ranked by relevance:
["skill-name-1", "skill-name-2", ...]

Example: ["pdf", "domain-name-brainstormer"]
"""
            
            response = self.client.chat.completions.create(
                model="gemini-3-flash-preview",  # Gemini 3 Flash Preview model
                messages=[
                    {"role": "system", "content": "You are a helpful skill recommendation system. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent results
                max_tokens=500
            )
            
            # Parse recommended skills
            content = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            recommended_names = json.loads(content)
            
            # Return full skill objects in recommended order
            result = []
            for name in recommended_names:
                for skill in self.index['skills']:
                    if skill['name'].lower() == name.lower() or skill['path'].lower() == name.lower():
                        result.append(skill)
                        break
            
            return result[:top_k]
            
        except Exception as e:
            print(f"⚠️  NLP search failed: {e}")
            print("   Falling back to basic keyword search...")
            return self._basic_search(query)[:top_k]
    
    def explain_skill(self, skill: Dict) -> str:
        """
        Use Gemini to generate a clear, helpful explanation of what the skill does
        and when to use it.
        """
        if not self.client:
            return skill['description']
        
        try:
            prompt = f"""Explain this skill in simple, helpful terms:

Skill Name: {skill['name']}
Description: {skill['description']}
Category: {skill['category']}
Tags: {', '.join(skill['tags'])}

Provide:
1. A clear explanation of what it does (2-3 sentences)
2. When to use it (1-2 specific scenarios)
3. Who would benefit from it

Keep it concise and practical."""
            
            response = self.client.chat.completions.create(
                model="gemini-3-flash-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant explaining software tools clearly and concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️  Could not generate explanation: {e}")
            return skill['description']
    
    def interpret_query(self, query: str) -> str:
        """
        Use Gemini to interpret what the user is really looking for,
        even if they describe it vaguely.
        """
        if not self.client:
            return f"Searching for: {query}"
        
        try:
            prompt = f"""A user is searching for skills with this query: "{query}"

Interpret what they're looking for and rephrase it more clearly.
Consider:
- What task are they trying to accomplish?
- What tools or capabilities might help?
- Are there common use cases that match?

Respond in one sentence starting with "You're looking for..."

Example queries:
- "something for documents" → "You're looking for tools to create, edit, or analyze documents like PDFs, Word files, or spreadsheets."
- "help with my website" → "You're looking for tools to test, analyze, or build web applications."
- "business stuff" → "You're looking for business and marketing tools like brand guidelines, lead research, or competitive analysis."
"""
            
            response = self.client.chat.completions.create(
                model="gemini-3-flash-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful search assistant that clarifies user intentions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Searching for: {query}"
    
    def _build_skills_context(self) -> str:
        """Build a concise context string with all skills."""
        lines = []
        for skill in self.index['skills']:
            desc = skill['description'][:150] + "..." if len(skill['description']) > 150 else skill['description']
            lines.append(f"- {skill['name']}: {desc} (Category: {skill['category']})")
        return "\n".join(lines)
    
    def _basic_search(self, query: str) -> List[Dict]:
        """Fallback basic keyword search."""
        query_lower = query.lower()
        results = []
        
        for skill in self.index['skills']:
            score = 0
            if query_lower in skill['name'].lower():
                score += 10
            if query_lower in skill['description'].lower():
                score += 5
            if any(query_lower in tag for tag in skill['tags']):
                score += 3
            
            if score > 0:
                results.append({'skill': skill, 'score': score})
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return [r['skill'] for r in results]

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='NLP-Enhanced Skill Discovery - Find skills using natural language',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Semantic search (understands intent)
  python tools/nlp-discover.py "I need to work with documents"
  python tools/nlp-discover.py "help me find domain names"
  python tools/nlp-discover.py "tools for my startup"
  
  # Get detailed explanation
  python tools/nlp-discover.py "pdf tools" --explain
  
  # Show more results
  python tools/nlp-discover.py "business tools" --top 10

Requirements:
  - Set one of: OLLAMA_TURBO_CLOUD_API_KEY, OLLAMA_PROXY_API_KEY, or OLLAMA_API_KEY
  - Install: pip install openai
  
Environment Variables (in order of preference):
  OLLAMA_TURBO_CLOUD_API_KEY    - Fastest endpoint (recommended)
  OLLAMA_PROXY_API_KEY          - Proxy endpoint
  OLLAMA_API_KEY                - Standard endpoint
        """
    )
    
    parser.add_argument(
        'query',
        help='Natural language search query'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=5,
        help='Number of results to show (default: 5)'
    )
    parser.add_argument(
        '--explain',
        action='store_true',
        help='Generate detailed explanations for each skill'
    )
    parser.add_argument(
        '--index',
        default='SKILL-INDEX.json',
        help='Path to skill index file'
    )
    parser.add_argument(
        '--api-key',
        help='Ollama Cloud API key (or use OLLAMA_TURBO_CLOUD_API_KEY env var)'
    )
    parser.add_argument(
        '--endpoint',
        help='Ollama Cloud endpoint URL (auto-detected from API key type)'
    )
    
    args = parser.parse_args()
    
    # Find repository root
    script_dir = Path(__file__).parent
    repo_root = str(script_dir.parent)
    index_path = args.index if os.path.isabs(args.index) else os.path.join(repo_root, args.index)
    
    # Initialize NLP discovery
    nlp = NLPSkillDiscovery(index_path, api_key=args.api_key, endpoint=args.endpoint)
    
    # Interpret the query
    print(f"\n🔍 Query: \"{args.query}\"")
    interpretation = nlp.interpret_query(args.query)
    print(f"💡 {interpretation}\n")
    
    # Perform semantic search
    results = nlp.semantic_search(args.query, top_k=args.top)
    
    if not results:
        print("❌ No skills found matching your query.")
        print("\nTry:")
        print("  - Being more specific about what you want to accomplish")
        print("  - Using different words to describe your need")
        print("  - Browsing categories with: python tools/discover.py --categories")
        return
    
    # Display results
    print(f"Found {len(results)} relevant skill(s):\n")
    print("="*80)
    
    for i, skill in enumerate(results, 1):
        print(f"\n{i}. 📦 {skill['name']}")
        print(f"   📂 Category: {skill['category']}")
        print(f"   📁 Path: {skill['path']}")
        
        if args.explain:
            print(f"\n   📝 Detailed Explanation:")
            explanation = nlp.explain_skill(skill)
            for line in explanation.split('\n'):
                print(f"      {line}")
        else:
            desc = skill['description'][:200] + "..." if len(skill['description']) > 200 else skill['description']
            print(f"   📝 {desc}")
        
        print(f"\n   📥 Installation:")
        print(f"      Claude.ai: Upload '{skill['skill_file']}'")
        print(f"      Claude Code: cp -r {skill['path']} ~/.config/claude-code/skills/")
        
        print("\n" + "-"*80)
    
    print(f"\n💡 Tip: Use --explain flag for detailed explanations")
    print(f"💡 Tip: Use --top N to see more results")

if __name__ == '__main__':
    main()
