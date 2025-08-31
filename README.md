# avrtt.blog-agents

Web agent integrations for my website that simplify scientific research, SMM, content creation & editing.

## Overview

This repository contains 4 AI agents designed to automate various aspects of blog management:

- **Research Agent**: Automates research and draft generation using Tavily search and LLM
- **Content Agent**: Handles post creation, editing, and SEO optimization
- **Dev Agent**: Manages GitHub issues, PRs, and code quality
- **SMM Agent**: Automates social media announcements across platforms

## Project Structure

```
avrtt.blog-agents/
├─ agents/
│  ├─ research_agent/     # Research and draft generation
│  ├─ content_agent/      # Content creation and editing
│  ├─ dev_agent/         # GitHub integration
│  └─ smm_agent/         # Social media automation
├─ .github/workflows/     # GitHub Actions
├─ out/                  # Generated outputs (gitignored)
├─ logs/                 # Log files (gitignored)
├─ requirements.txt      # Python dependencies
├─ Makefile             # Build commands
└─ README.md            # This file
```

## Quick Start

### Local Development

1. **Setup environment**:
   ```bash
   make venv
   source .venv/bin/activate
   make install
   ```

2. **Create `.env` file** (optional, for local testing):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Test research agent**:
   ```bash
   make run-research TOPIC="AI automation trends"
   ```

### GitHub Actions Setup

Configure these secrets in your repository:

#### Required Secrets
- `OPENAI_API_KEY`: OpenAI API key for LLM operations
- `TAVILY_API_KEY`: Tavily search API key
- `BLOG_PAT`: Personal access token for blog repository access
- `BLOG_REPO`: Blog repository name (e.g., "username/blog-repo")

#### Optional Secrets (for SMM)
- `TELEGRAM_BOT_TOKEN`: Telegram bot token
- `TELEGRAM_CHAT_ID`: Telegram chat/channel ID
- `FB_PAGE_TOKEN`: Facebook page access token
- `X_API_TOKEN`: Twitter/X API token

## Usage

### Research Agent

Generates research drafts from topics:

```bash
# Local run
python -m agents.research_agent.main "AI in healthcare"

# Via Makefile
make run-research TOPIC="AI in healthcare"
```

**Outputs**:
- `out/draft-YYYYMMDD-HHMM.md` - Generated draft
- `out/sources-YYYYMMDD-HHMM.json` - Source references

### Content Agent

Creates and edits blog posts:

```bash
# Create outline from topic
python -m agents.content_agent.main "My Topic"

# Edit existing outline
python -m agents.content_agent.main "outline.md"
```

**Outputs**:
- `out/draft-*.md` - Expanded draft
- `out/critique-*.md` - Self-critique
- `out/seo-*.md` - SEO checklist

### Dev Agent

Manages GitHub issues and PRs:

```bash
python -m agents.dev_agent.main
```

**Features**:
- Issue analysis and labeling
- PR review suggestions
- Code quality checks

### SMM Agent

Automates social media posts:

```bash
python -m agents.smm_agent.main "post.md"
```

**Platforms**:
- Telegram
- Facebook Pages
- Twitter/X

## GitHub Actions

### Research → Blog PR
- **Trigger**: Manual (`workflow_dispatch`) or weekly schedule
- **Action**: Runs research agent, creates PR in blog repo
- **Schedule**: Every Monday at 8 AM UTC

### SMM on Post Merge
- **Trigger**: PR merge or direct push to `content/posts/`
- **Action**: Generates and posts social media announcements

### Dev Agent Listener
- **Trigger**: Issue/PR events
- **Action**: Analyzes and provides suggestions

## Development

### Adding New Agents

1. Create agent directory: `agents/new_agent/`
2. Implement `main.py` with dry-run capability
3. Add to `Makefile` commands
4. Create GitHub Action if needed

### Testing

```bash
# Test all agents in dry-run mode
make run-research TOPIC="test"
make run-content OUTLINE="test"
make run-dev
make run-smm POST="test.md"
```

### Logging

All LLM calls are logged to `logs/` directory (gitignored). Check logs for debugging:

```bash
tail -f logs/agent-*.log
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required secrets are set in GitHub
2. **Import Errors**: Run `make install` to install dependencies
3. **Permission Errors**: Check GitHub token permissions
4. **Rate Limits**: Agents include built-in rate limiting

### Dry-Run Mode

All agents work without API keys in dry-run mode, generating placeholder outputs for testing.

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with dry-run capability
4. Test locally and via GitHub Actions
5. Submit pull request

## License

MIT License - see LICENSE file for details.
