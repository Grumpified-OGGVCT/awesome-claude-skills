# Quick Start: Testing NLP-Enhanced Skill Discovery

## ✅ What's Ready

- **API Key**: `OLLAMA_API_KEY` configured in repository secrets
- **Tool**: `tools/nlp-discover.py` ready to use
- **Model**: Gemini 3 Flash Preview
- **Endpoint**: https://api.ollama.cloud/v1

## 🚀 Test It Now (3 Ways)

### Option 1: GitHub Actions Workflow (Easiest - No Setup!)

1. Go to **Actions** tab in GitHub
2. Select **"NLP Skill Discovery Demo"** workflow
3. Click **"Run workflow"**
4. Enter a search query, e.g.:
   - "I need to work with documents"
   - "help me with my business"
   - "tools for my website"
   - Or type "test" to run all examples
5. Click **"Run workflow"** green button
6. Watch the results in the workflow run!

**The API key is automatically available - no configuration needed!**

### Option 2: Local Development

```bash
# 1. Get the API key from repository secrets
# (Go to Settings → Secrets → Actions → OLLAMA_API_KEY)

# 2. Set it locally
export OLLAMA_API_KEY='your-key-here'

# 3. Install dependencies
pip install openai

# 4. Generate skill index (one time)
python tools/index-skills.py

# 5. Use natural language!
python tools/nlp-discover.py "I need to work with documents"
python tools/nlp-discover.py "help me find domain names"
python tools/nlp-discover.py "tools for my startup"

# 6. Get detailed explanations
python tools/nlp-discover.py "pdf tools" --explain

# 7. More results
python tools/nlp-discover.py "business tools" --top 10
```

### Option 3: Simple Fallback (No API Key)

If you don't want to use NLP, the basic discovery still works:

```bash
# Simple wrapper
./tools/find-skill pdf
./tools/find-skill domain

# Interactive mode
python tools/discover.py

# Direct search
python tools/discover.py --search "pdf"
python tools/discover.py --category "Business & Marketing"
```

## 📊 Expected Output

### NLP Discovery Example

```
$ python tools/nlp-discover.py "I need something for documents"

✅ NLP-enhanced search enabled via api.ollama.cloud
   Model: Gemini 3 Flash Preview

🔍 Query: "I need something for documents"
💡 You're looking for tools to create, edit, or analyze documents like 
    PDFs, Word files, Excel spreadsheets, or PowerPoint presentations.

Found 5 relevant skill(s):

================================================================================

1. 📦 pdf
   📂 Category: Document Processing
   📁 Path: document-skills/pdf
   📝 Comprehensive PDF manipulation toolkit for extracting text and tables...
   
   📥 Installation:
      Claude.ai: Upload 'document-skills/pdf/SKILL.md'
      Claude Code: cp -r document-skills/pdf ~/.config/claude-code/skills/

--------------------------------------------------------------------------------

2. 📦 docx
   📂 Category: Document Processing
   📁 Path: document-skills/docx
   📝 Create, edit, and analyze Word documents...
   
   📥 Installation:
      Claude.ai: Upload 'document-skills/docx/SKILL.md'
      Claude Code: cp -r document-skills/docx ~/.config/claude-code/skills/

[... more results ...]
```

### With Explanations

```
$ python tools/nlp-discover.py "pdf tools" --explain

🔍 Query: "pdf tools"
💡 You're looking for PDF processing and manipulation tools.

Found 1 relevant skill(s):

1. 📦 pdf
   
   📝 Detailed Explanation:
      This skill provides a comprehensive toolkit for working with PDF documents 
      programmatically. It can extract text and tables from existing PDFs, create 
      new PDF files from scratch with custom layouts, merge multiple PDFs into one, 
      split large PDFs into smaller files, and even fill out interactive PDF forms 
      automatically.
      
      Use this when you need to automate PDF processing at scale, extract structured 
      data from PDF reports, generate PDF invoices or reports programmatically, or 
      batch process large numbers of PDF files.
      
      Software developers building document automation systems, data analysts 
      extracting information from PDF reports, and businesses that need to process 
      invoices or forms will find this skill invaluable for saving hours of manual work.
   
   📥 Installation:
      Claude.ai: Upload 'document-skills/pdf/SKILL.md'
      Claude Code: cp -r document-skills/pdf ~/.config/claude-code/skills/
```

## 🎯 Example Queries to Try

### Business
- "I need help with my business"
- "tools for marketing"
- "help me find customers"
- "competitive analysis tools"

### Development
- "something for my website"
- "I need testing tools"
- "help with git and code"
- "changelog automation"

### Documents
- "I need to work with documents"
- "pdf tools"
- "help with presentations"
- "spreadsheet automation"

### Creative
- "I need design tools"
- "help me make graphics"
- "video downloader"
- "create themes"

### Vague (Tests NLP Intelligence)
- "business stuff"
- "something for documents"
- "I need tools"
- "help me"

## 🐛 Troubleshooting

### In GitHub Actions

**If workflow fails:**
1. Check the workflow run logs
2. Verify `OLLAMA_API_KEY` secret exists in Settings → Secrets
3. Check if the secret name is exactly `OLLAMA_API_KEY`

**If "No API key found":**
- The secret might not be exposed to the workflow
- Check the workflow YAML has: `env: OLLAMA_API_KEY: ${{ secrets.OLLAMA_API_KEY }}`

### Local Development

**If "OLLAMA_API_KEY not set":**
```bash
echo $OLLAMA_API_KEY  # Check if set
export OLLAMA_API_KEY='your-key'  # Set it
```

**If "openai library not installed":**
```bash
pip install openai
```

**If "NLP search failed":**
- Tool automatically falls back to basic keyword search
- Check if API key is valid
- Check internet connection
- Try basic search: `python tools/discover.py --search "keyword"`

### Fallback Behavior

If NLP fails for any reason, the tool automatically uses basic keyword search:

```
⚠️  NLP search failed: [error details]
   Falling back to basic keyword search...

🔍 Found 5 skill(s) matching 'pdf':
[Basic keyword results]
```

## ✅ Success Indicators

You'll know it's working when you see:

1. ✅ `NLP-enhanced search enabled via api.ollama.cloud`
2. 💡 Query interpretation message
3. 📦 Ranked skills based on semantic relevance
4. 📝 AI-generated explanations (with --explain flag)

## 📚 Documentation

- **[README.md](../README.md)** - Quick start
- **[SKILL-DISCOVERY.md](../docs/SKILL-DISCOVERY.md)** - Basic discovery guide
- **[NLP-DISCOVERY.md](../docs/NLP-DISCOVERY.md)** - NLP features and setup
- **[tools/README.md](../tools/README.md)** - Complete tool documentation
- **[IMPLEMENTATION-SUMMARY.md](../IMPLEMENTATION-SUMMARY.md)** - Full technical overview

## 🎉 That's It!

The NLP-enhanced discovery is ready to use. Just run the GitHub Actions workflow or set the API key locally and start searching in natural language!

**No more "I have to know what to ask for in order to find it" - just describe what you need!**
