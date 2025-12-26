# Documentation

This directory contains detailed guides for using Claude Skills with various LLM providers and understanding compatibility.

## 📚 Available Guides

### Getting Started with Providers

| Guide | Description | Best For |
|-------|-------------|----------|
| [OpenRouter Setup](OPENROUTER-SETUP.md) | Use 100+ models through one API | Cloud usage, multi-model access |
| [Ollama Setup](OLLAMA-SETUP.md) | Run models locally on your machine | Privacy, offline usage, free |

### Understanding Skills

| Guide | Description | Helps You |
|-------|-------------|-----------|
| [Model Compatibility](MODEL-COMPATIBILITY.md) | Which models work best for each skill | Choose the right model |
| [Migration Guide](MIGRATION-GUIDE.md) | Convert your own skills to universal format | Create compatible skills |

## 🚀 Quick Navigation

### New to Skills?

Start here:
1. Read the main [README](../README.md) for overview
2. Follow the [Getting Started Guide](../GETTING_STARTED.md)
3. Choose your provider setup guide above

### Want to Use Different Models?

1. Check [Model Compatibility Guide](MODEL-COMPATIBILITY.md) for recommendations
2. Follow setup guide for your chosen provider:
   - [OpenRouter](OPENROUTER-SETUP.md) for cloud access to 100+ models
   - [Ollama](OLLAMA-SETUP.md) for local/private usage

### Creating Your Own Skills?

1. Read [Creating Skills](../README.md#creating-skills) in the main README
2. Use the [Skill Creator](../skill-creator/) skill for guidance
3. Check [Migration Guide](MIGRATION-GUIDE.md) to make it universal
4. See [Contributing Guidelines](../CONTRIBUTING.md) to share it

## 📖 What Each Guide Covers

### OpenRouter Setup Guide

Learn how to:
- Create an OpenRouter account and get API keys
- Use skills with 100+ different models
- Switch between models (Claude, GPT-4, Llama, etc.)
- Handle streaming responses
- Manage costs across providers

**Perfect for**: Users who want flexibility to try different models without managing multiple API keys.

### Ollama Setup Guide

Learn how to:
- Install Ollama on your machine
- Download and manage local models
- Use skills completely offline
- Optimize performance for your hardware
- Run multiple models simultaneously

**Perfect for**: Users who value privacy, need offline access, or want to avoid API costs.

### Model Compatibility Guide

Find out:
- Which models work with which skills
- Performance differences between models
- Cost comparisons
- Hardware requirements for local models
- Recommendations by use case

**Perfect for**: Users choosing between models or troubleshooting compatibility issues.

### Migration Guide

Learn to:
- Convert Claude-specific skills to universal format
- Understand the three skill tiers
- Handle tool-calling in universal format
- Test skills across different models
- Contribute universal skills back

**Perfect for**: Developers creating or converting skills to work across LLM providers.

## 🆘 Getting Help

### Common Questions

**Q: Which provider should I choose?**

A: Depends on your needs:
- **Need flexibility?** → OpenRouter (switch between 100+ models)
- **Value privacy?** → Ollama (100% local)
- **Just want Claude?** → Use Claude.ai directly
- **Building an app?** → Claude API or OpenRouter

**Q: Do skills work the same across all providers?**

A: Mostly yes for Tier 1 skills (90% of skills). Tier 2 skills work best with models that support tool calling. See [Model Compatibility Guide](MODEL-COMPATIBILITY.md).

**Q: Can I use multiple providers?**

A: Yes! The universal format works with any OpenAI-compatible API. Use different providers for different use cases.

### Need More Help?

- **Technical issues**: Check the specific setup guide above
- **Skill questions**: See main [FAQ](../README.md#frequently-asked-questions)
- **Community support**: Join [Discord](https://discord.com/invite/composio)
- **Report bugs**: Open an [issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues)

## 🔗 Related Resources

- [Main README](../README.md) - Project overview and skill list
- [Getting Started Guide](../GETTING_STARTED.md) - Step-by-step setup
- [Contributing Guidelines](../CONTRIBUTING.md) - How to contribute
- [Universal Format Spec](../UNIVERSAL-FORMAT.md) - Technical details
- [Examples](../examples/) - Working code examples

## 📝 Contributing to Docs

Found a mistake? Want to improve these guides?

1. Fork the repository
2. Edit the relevant markdown file
3. Submit a pull request

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Questions?** [Open an issue](https://github.com/Grumpified-OGGVCT/awesome-claude-skills/issues) or ask in [Discord](https://discord.com/invite/composio)!
