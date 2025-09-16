# AI Trading Assistant 🤖

**Single Script. Complete Solution.**

Professional AI-powered trading assistant with anti-pattern detection, interactive learning, parallel AI tool execution, and personalized coaching - all in one unified script.

## 🚀 Quick Start

### Installation
```bash
git clone <repository-url>
cd poc
pip install -r requirements.txt

# Configure your API key
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Basic Usage
```bash
# Interactive mode (recommended)
python main.py interactive sk-your-api-key-here

# Analyze trading data
python main.py analyze samples/scenario1 sk-your-api-key-here

# Quick market query
python main.py openai-tools sk-your-api-key-here "Check AAPL market conditions"

# Demo system (no API key needed)
python main.py demo-agents
```

💡 **Tip:** Set `DEFAULT_USER_ID=your-username` in `.env` to avoid typing it every time!

## 🎯 Unified Features

### ⭐ All-in-One Script: `scripts/trading_assistant.py`

This single file contains everything:

**🔍 Professional Analysis**
- Detects 25+ trading psychology anti-patterns
- Shows exact trade evidence with dollar amounts
- Quantified consequences and solutions

**🎓 Interactive Learning**
- Personalized user profiles with learning history
- Adaptive coaching based on trading behavior
- Smart follow-up questions and insights
- Session-based improvement tracking

**🤖 AI Tool Integration**
- 7 specialized AI agents (news, sentiment, risk, patterns)
- Intelligent tool selection based on queries
- Real-time performance statistics

**🧠 Self-Learning System**
- Tracks user preferences and query patterns
- Builds personalized trading profiles
- Stores session history and improvements
- Adapts recommendations over time

## 📊 Usage Examples

### Interactive Mode (Best Experience)
```bash
# Start interactive session
python main.py interactive sk-your-api-key-here

# Inside interactive session:
scenarios                    # List all available scenarios
analyze 1                    # Load scenario1
analyze scenario5            # Load scenario5 by name
analyze FOMO                 # Find scenario by description (scenario3)
Check current market sentiment for AAPL
What are the biggest risks in tech stocks?
help
```

### Professional Analysis
```bash
# Analyze trading data
python main.py analyze samples/scenario1 sk-your-api-key-here
```

### Quick Queries
```bash
python main.py openai-tools sk-your-api-key-here "Analyze TSLA market conditions"
python main.py openai-tools sk-your-api-key-here "What are current market risks?"
```

## 🔧 Configuration

Edit `.env` file:
```bash
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4.1
OPENAI_MAX_COMPLETION_TOKENS=1500
OPENAI_TEMPERATURE=1.0

# Optional: Set default username (avoids typing it every time)
DEFAULT_USER_ID=your-username-here
```

## 🤖 AI Agent Tools

The system uses 8 specialized AI agents organized in clean, modular architecture:

### Core Trading Agents
- **📰 News Agent** - Market headlines and impact analysis
- **📊 Market Data Agent** - Prices, technicals, indicators
- **💭 Sentiment Agent** - Social and institutional sentiment
- **⚠️ Risk Agent** - Portfolio risk and VaR calculations
- **🧠 Pattern Agent** - Trading psychology analysis

### Orchestration Agents
- **🔍 Comprehensive Agent** - Coordinates multiple agents for complete analysis
- **🌍 Market Conditions Agent** - Overall market environment assessment
- **📁 Scenario Loader Agent** - Loads trading scenarios from samples folder

## 🧪 Testing & Demo

```bash
# Demo system without API key (recommended)
python main.py demo-agents

# Test with API key via main.py
python main.py openai-tools sk-your-api-key-here "Test query"

# Direct script access (still works)
python scripts/demo_agents.py
python scripts/trading_assistant.py query sk-your-api-key-here "Test query"
```

## 💡 Interactive Commands

Inside interactive mode:
```
analyze <scenario>     - Smart scenario analysis
  • analyze 1          - Load scenario1
  • analyze scenario5  - Load scenario5 by name
  • analyze FOMO       - Find scenario by description
scenarios / list      - List all available scenarios
help                  - Show available commands
quit/exit             - End session and save data
```

## 📁 Project Structure

```
📦 poc/
├── 🤖 agents/                     # AI Agent System (8 agents)
│   ├── base_agent.py             # Agent base class
│   ├── news_agent.py             # Market news analysis
│   ├── market_data_agent.py      # Technical analysis
│   ├── sentiment_agent.py        # Market sentiment
│   ├── risk_management_agent.py  # Risk assessment
│   ├── pattern_analysis_agent.py # Trading psychology
│   ├── scenario_loader_agent.py  # Scenario loading
│   ├── comprehensive_analysis_agent.py # Multi-agent coordination
│   ├── market_conditions_agent.py # Market environment
│   ├── agent_manager.py          # Agent orchestration
│   └── tool_integration.py       # Tool registry (refactored)
├── 📜 scripts/
│   ├── trading_assistant.py      # Main trading assistant
│   └── demo_agents.py           # System demonstrations
├── 📋 prompts/                   # Psychology patterns
├── 📊 samples/                   # Trading scenarios
│   ├── scenario1/               # Premature profit-taking
│   ├── scenario2/               # Averaging down
│   ├── scenario3/               # FOMO patterns
│   └── ... scenario11/          # 11 total scenarios
├── 🚀 main.py                   # Entry point wrapper
└── 📚 README.md                 # This file
```

## ⚠️ Important Notes

- **Educational use only** - Not financial advice
- **Simulated data** - AI agents provide realistic fake responses
- **API required** - Needs OpenAI API key for analysis
- **Privacy** - User profiles stored locally only

## 🆘 Support

Issues? Try these:
1. `python main.py demo-agents` - Demo system (no API key needed)
2. Check your API key starts with `sk-`

**Usage:**
```bash
python main.py interactive sk-your-api-key-here
python main.py analyze samples/scenario1 sk-your-api-key-here
```

---

**AI-Powered Trading Psychology Analysis.** 🎯