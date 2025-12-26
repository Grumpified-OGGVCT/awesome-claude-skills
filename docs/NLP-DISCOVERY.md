# Ollama Cloud Configuration for NLP-Enhanced Skill Discovery

## Setup Instructions

### 1. Get Your Ollama API Key

The repository has `OLLAMA_API_KEY` available as a repository secret.

**For local development:**

1. Go to your GitHub repository settings
2. Navigate to Secrets and variables → Actions
3. Look for `OLLAMA_API_KEY` 
4. Copy the key value

**Note:** This key is already available in GitHub Actions workflows automatically.

### 2. Set the API Key Locally (For Local Testing)

```bash
# Linux/macOS
export OLLAMA_API_KEY='your-key-here'

# Add to your shell profile for persistence
echo 'export OLLAMA_API_KEY="your-key-here"' >> ~/.bashrc
# or ~/.zshrc for zsh users

# Windows (PowerShell)
$env:OLLAMA_API_KEY='your-key-here'

# Windows (Command Prompt)
set OLLAMA_API_KEY=your-key-here
```

The tool automatically detects and uses the key. No configuration needed!

### 3. Install Required Dependencies

```bash
pip install openai
```

### 4. Test the NLP Discovery Tool

```bash
# Basic test
python tools/nlp-discover.py "I need to work with documents"

# With explanations
python tools/nlp-discover.py "help me find domain names" --explain

# More results
python tools/nlp-discover.py "business tools" --top 10
```

## Model Configuration

The tool uses **Gemini 3 Flash Preview** model from Ollama Cloud Service:

- **Model**: `gemini-3-flash-preview`
- **Endpoint**: `https://api.ollama.cloud/v1` (default)
- **API Key**: `OLLAMA_API_KEY` (repository secret - already configured!)
- **Features**:
  - Semantic search (understands intent, not just keywords)
  - Query interpretation (clarifies vague queries)
  - Skill explanations (generates helpful descriptions)
  - Smart recommendations (suggests related skills)

## API Configuration

Default settings in `nlp-discover.py`:

```python
# Endpoint (default for OLLAMA_API_KEY)
endpoint = "https://api.ollama.cloud/v1"

# Model
model = "gemini-3-flash-preview"

# Temperature settings
semantic_search_temp = 0.3    # Low for consistent recommendations
explain_temp = 0.5            # Medium for natural explanations
interpret_temp = 0.4          # Low-medium for accurate interpretation
```

## Environment Variables

| Variable | Description | Status |
|----------|-------------|--------|
| `OLLAMA_API_KEY` | Repository secret | ✅ Already configured! |

**No setup required in GitHub Actions!** The key is automatically available.

## Fallback Behavior

If the API key is not set or the service is unavailable:
- The tool automatically falls back to basic keyword search
- Core functionality remains available
- NLP features are disabled with a warning message

## Usage Examples

### Semantic Search
Understands what you mean, not just what you say:

```bash
# Vague query → Smart interpretation
$ python tools/nlp-discover.py "something for my website"

🔍 Query: "something for my website"
💡 You're looking for tools to test, analyze, or build web applications.

Found 3 relevant skill(s):
1. 📦 webapp-testing
2. 📦 artifacts-builder
3. 📦 domain-name-brainstormer
```

### Query Interpretation
Clarifies what you're actually looking for:

```bash
$ python tools/nlp-discover.py "business stuff"

🔍 Query: "business stuff"
💡 You're looking for business and marketing tools like brand guidelines, 
    lead research, or competitive analysis.

Found 5 relevant skill(s):
[Business & Marketing skills]
```

### Detailed Explanations
Get AI-generated explanations:

```bash
$ python tools/nlp-discover.py "pdf tools" --explain

📦 pdf
📝 Detailed Explanation:
   This skill provides a comprehensive toolkit for working with PDF documents.
   It can extract text and tables, create new PDFs from scratch, merge or split
   existing documents, and handle interactive PDF forms.
   
   Use this when you need to automate PDF processing tasks, extract data from
   PDFs at scale, or programmatically generate PDF reports and documents.
   
   Developers, data analysts, and anyone dealing with batch PDF processing will
   benefit from this skill's automation capabilities.
```

## Comparison: Basic vs NLP Search

### Basic Search (keyword matching)
```bash
$ python tools/discover.py --search "website"
# Returns only skills with "website" in name/description
```

### NLP Search (intent understanding)
```bash
$ python tools/nlp-discover.py "I want to build a website"
# Understands you want web development tools
# Returns: artifacts-builder, webapp-testing, theme-factory, etc.
```

## Troubleshooting

### "OLLAMA_API_KEY not set"

**Solution**: 

For local testing, set the environment variable:
```bash
export OLLAMA_API_KEY='your-key-here'
```

**In GitHub Actions**: The key is automatically available! No action needed.

### "openai library not installed"

**Solution**: Install the dependency:
```bash
pip install openai
```

### "NLP search failed"

The tool automatically falls back to basic search. Check:
1. Is your API key valid?
2. Is the Ollama Cloud service accessible?
3. Check your internet connection

### "No skills found"

Try:
- Being more specific about what you want
- Using different words to describe your need
- Using basic search: `python tools/discover.py --search "keyword"`

## Security Notes

- **Never commit API keys to the repository**
- Use environment variables or GitHub Secrets
- The `.gitignore` file already excludes common secret files
- For CI/CD, use GitHub Actions secrets

## GitHub Actions Integration

To use in workflows, add the secret to your repository:

```yaml
# In .github/workflows/your-workflow.yml
- name: NLP Skill Discovery
  env:
    OLLAMA_API_KEY: ${{ secrets.OLLAMA_API_KEY }}
  run: |
    pip install openai
    python tools/nlp-discover.py "your query"
```

**The repository secret `OLLAMA_API_KEY` is already configured!**  
Just reference it in your workflow as shown above.

## Performance

- **Semantic search**: ~1-2 seconds per query
- **Explanations**: ~1-2 seconds per skill
- **Basic fallback**: <0.1 seconds (instant)

The tool caches results where possible to minimize API calls.

## Limits and Quotas

Check your Ollama Cloud plan for:
- API rate limits
- Token quotas
- Concurrent request limits

The tool is designed to work within reasonable free tier limits.

## Support

For issues with:
- **The tool itself**: Open an issue in this repository
- **Ollama Cloud service**: Contact Ollama support
- **API key access**: Contact your GitHub organization admin
