# AI Research Assistant

A multi-agent system powered by CrewAI that conducts comprehensive research on any topic and generates professional reports.

## 🚀 Live Demo

**[View in AI Portfolio Dashboard](https://unharmable-threadlike-ruth.ngrok-free.dev)** | **[Direct Access](https://unharmable-threadlike-ruth.ngrok-free.dev:8003)**

> Part of **[Nihal's AI Portfolio](https://unharmable-threadlike-ruth.ngrok-free.dev)** - Unified dashboard featuring 5 cutting-edge AI services

## Overview

This project uses three specialized AI agents that collaborate to research topics, analyze findings, and produce well-structured reports:

- **Research Agent**: Gathers information from multiple sources
- **Analyst Agent**: Synthesizes and validates findings
- **Writer Agent**: Creates comprehensive, publication-ready reports

## Features

- Multi-agent collaboration using CrewAI
- Automated web research and information gathering
- Fact-checking and source validation
- Export to Markdown and PDF formats
- Customizable research depth and focus areas

## Installation

### Prerequisites

- Python 3.11 or higher
- OpenAI API key or compatible LLM endpoint

### Setup

1. Clone the repository
```bash
git clone https://github.com/nihal-5/ai-research-assistant.git
cd ai-research-assistant
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Add your API keys to .env
```

## Usage

### Web Dashboard (Recommended)

Start the web interface:
```bash
python app.py
```

Then open https://unharmable-threadlike-ruth.ngrok-free.dev:8000 in your browser.

The dashboard provides:
- Visual interface for research requests
- Real-time progress tracking
- Report history viewer
- Download generated reports

### Command Line Interface

```bash
python research.py "Artificial Intelligence in Healthcare"
```

### Advanced Options

```bash
# Specify output format
python research.py "Climate Change Solutions" --format pdf

# Set research depth
python research.py "Quantum Computing" --depth comprehensive

# Custom focus areas
python research.py "Space Exploration" --focus "recent developments,challenges"
```

## Architecture

```
┌─────────────────┐
│  User Input     │
│  (Topic)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Research Agent  │──► Gathers information
│                 │    from web sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyst Agent   │──► Synthesizes findings
│                 │    validates facts
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Writer Agent    │──► Creates structured
│                 │    report with citations
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Output          │
│ (MD/PDF Report) │
└─────────────────┘
```

## Example Output

Input: "Latest developments in renewable energy"

Output: A comprehensive report including:
- Executive Summary
- Current State Analysis
- Recent Innovations
- Market Trends
- Future Outlook
- Citations and Sources

## Technology Stack

- **CrewAI**: Multi-agent orchestration
- **OpenAI GPT-4**: Language model for agents
- **BeautifulSoup**: Web scraping
- **Markdown/PDF**: Report generation
- **Python 3.11+**: Core runtime

## Configuration

Edit `config.yaml` to customize:

```yaml
research:
  depth: comprehensive  # basic, moderate, comprehensive
  max_sources: 10
  focus_areas: []
  
output:
  format: markdown  # markdown, pdf, both
  include_citations: true
  
agents:
  temperature: 0.7
  max_tokens: 4000
```

## Contributing

This is a portfolio project. Feel free to fork and adapt for your own use!

## License

MIT License - Free to use for personal and educational purposes

## Author

Nihal Veeramalla  
[GitHub](https://github.com/nihal-5) • [LinkedIn](https://linkedin.com/in/nihal-veeramalla)

## Acknowledgments

Built with CrewAI framework and inspired by the need for efficient research automation.

---

*Reducing research time from hours to minutes through intelligent multi-agent collaboration.*
