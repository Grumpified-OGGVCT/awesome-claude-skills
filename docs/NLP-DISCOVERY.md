# Ollama Cloud Configuration for NLP-Enhanced Skill Discovery

## Setup Instructions

### 1. Get Your Ollama Cloud API Keys

The organization has multiple Ollama API keys available as GitHub Secrets:

- **OLLAMA_TURBO_CLOUD_API_KEY** - Fastest endpoint (recommended)
- **OLLAMA_PROXY_API_KEY** - Proxy endpoint
- **OLLAMA_API_KEY** - Standard endpoint

To access them:

1. Go to your GitHub organization settings
2. Navigate to Secrets and variables → Actions
3. Look for the OLLAMA keys listed above
4. Copy the key value you want to use

### 2. Set the API Key Locally

**Recommended (Turbo for best performance):**

```bash
# Linux/macOS
export OLLAMA_TURBO_CLOUD_API_KEY='your-key-here'

# Add to your shell profile for persistence
echo 'export OLLAMA_TURBO_CLOUD_API_KEY="your-key-here"' >> ~/.bashrc
# or ~/.zshrc for zsh users

# Windows (PowerShell)
$env:OLLAMA_TURBO_CLOUD_API_KEY='your-key-here'

# Windows (Command Prompt)
set OLLAMA_TURBO_CLOUD_API_KEY=your-key-here
```

**Alternative options:**

```bash
# Proxy endpoint
export OLLAMA_PROXY_API_KEY='your-key-here'

# Standard endpoint
export OLLAMA_API_KEY='your-key-here'
```

The tool automatically selects the best available key in this order:
1. OLLAMA_TURBO_CLOUD_API_KEY (fastest)
2. OLLAMA_PROXY_API_KEY
3. OLLAMA_API_KEY
4. OLLAMA_CLOUD_API_KEY (legacy fallback)

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
- **Endpoints**:
  - Turbo: `https://turbo.ollama.cloud/v1` (recommended - fastest)
  - Proxy: `https://proxy.ollama.cloud/v1`
  - Standard: `https://cloud.ollama.ai/v1`
- **Features**:
  - Semantic search (understands intent, not just keywords)
  - Query interpretation (clarifies vague queries)
  - Skill explanations (generates helpful descriptions)
  - Smart recommendations (suggests related skills)

## API Configuration

Default settings in `nlp-discover.py`:

```python
# Endpoints (auto-selected based on API key)
turbo_endpoint = "https://turbo.ollama.cloud/v1"     # Fastest
proxy_endpoint = "https://proxy.ollama.cloud/v1"    # Proxy
standard_endpoint = "https://cloud.ollama.ai/v1"    # Standard

# Model
model = "gemini-3-flash-preview"

# Temperature settings
semantic_search_temp = 0.3    # Low for consistent recommendations
explain_temp = 0.5            # Medium for natural explanations
interpret_temp = 0.4          # Low-medium for accurate interpretation
```

## Environment Variables

| Variable | Description | Endpoint | Priority |
|----------|-------------|----------|----------|
| `OLLAMA_TURBO_CLOUD_API_KEY` | Turbo cloud service | turbo.ollama.cloud | 1st (fastest) |
| `OLLAMA_PROXY_API_KEY` | Proxy service | proxy.ollama.cloud | 2nd |
| `OLLAMA_API_KEY` | Standard service | cloud.ollama.ai | 3rd |
| `OLLAMA_CLOUD_API_KEY` | Legacy fallback | cloud.ollama.ai | 4th |

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

### "OLLAMA_TURBO_CLOUD_API_KEY not set"

**Solution**: Set the environment variable (use turbo for best performance):
```bash
export OLLAMA_TURBO_CLOUD_API_KEY='your-key-here'
```

Or use one of the alternative keys:
```bash
export OLLAMA_PROXY_API_KEY='your-key-here'
export OLLAMA_API_KEY='your-key-here'
```

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
    OLLAMA_TURBO_CLOUD_API_KEY: ${{ secrets.OLLAMA_TURBO_CLOUD_API_KEY }}
  run: |
    pip install openai
    python tools/nlp-discover.py "your query"
```

**Available secrets in this organization:**
- `OLLAMA_TURBO_CLOUD_API_KEY` - Recommended for CI/CD
- `OLLAMA_PROXY_API_KEY` - Alternative
- `OLLAMA_API_KEY` - Alternative

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
