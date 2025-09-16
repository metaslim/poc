# Advanced Trading Assistant with AI Agent Tools 🤖

This project provides a comprehensive AI-powered trading system with **specialized AI agent tools** that can intelligently analyze trading behavior, market conditions, news sentiment, and risk factors to provide actionable insights for traders.

## 🚀 Key Features

### Enhanced AI Agent System
- **5 Specialized AI Agents**: News, Market Data, Sentiment, Risk Management, and Pattern Analysis
- **Smart Tool Selection**: Automatically chooses appropriate agents based on user queries
- **Parallel Execution**: Run multiple agents simultaneously for comprehensive analysis
- **Function Calling**: OpenAI agent can call AI tools as functions during analysis

### Comprehensive Analysis
- **Anti-Pattern Detection**: Identifies 25+ trading psychology patterns
- **Market Context**: Real-time market conditions and sentiment analysis
- **Risk Assessment**: Portfolio risk metrics, VaR calculations, and position sizing
- **News Integration**: Market-moving news analysis and impact assessment
- **Interactive Learning**: Personalized advice based on user behavior patterns

### Multiple Interface Options
- **Unified Entry Point**: Single main.py script for all functionality
- **Smart Assistant**: Natural language interface with automatic tool selection
- **OpenAI Function Calling**: Direct integration with OpenAI's function calling API
- **Professional Analysis**: In-depth trading behavior analysis
- **Interactive Sessions**: Learning-based system with user profiles

## 📋 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Required packages: `pip install -r requirements.txt`

### Installation

```bash
git clone <repository-url>
cd poc
pip install -r requirements.txt
```

## 🎯 Usage Options

### 1. Unified Main Script (Recommended)

```bash
# Show all available options
python main.py help

# Demo AI agent capabilities
python main.py demo-agents

# Test AI agent system
python main.py test-agents

# Smart assistant with automatic tool selection
python main.py smart-assistant interactive

# OpenAI agent with AI tools (function calling)
python main.py openai-tools sk-your-api-key "Check market conditions for tech stocks"

# Professional analysis with AI tools
python main.py analyze samples/scenario1 sk-your-api-key

# Interactive session with learning
python main.py interactive samples/scenario1 sk-your-api-key trader123
```

### 2. Enhanced Shell Scripts

```bash
# Professional analysis with AI agents
sh run_trading_assistant.sh samples/scenario1 sk-your-api-key

# Interactive session with AI agents
sh run_interactive_assistant.sh samples/scenario1 sk-your-api-key trader123
```

### 3. Direct Script Usage

```bash
# Smart assistant with automatic tool selection
python scripts/smart_trading_assistant.py demo

# OpenAI agent that calls AI tools as functions
python scripts/openai_with_agent_tools.py sk-your-api-key

# Individual AI agents demo
python scripts/demo_agents.py

# Test suite for all agents
python scripts/test_agent_tools.py
```

## 🤖 AI Agent Tools Overview

### Available Agents

1. **📰 News Agent**
   - Latest market news and headlines
   - News impact analysis on sentiment
   - Sector-specific news filtering
   - Trading recommendations based on news

2. **📊 Market Data Agent**
   - Real-time price data (simulated)
   - Technical indicators (RSI, MA, S/R levels)
   - Market overview and conditions
   - Volatility and sector analysis

3. **💭 Sentiment Agent**
   - Social media sentiment analysis
   - Options flow sentiment
   - Institutional positioning
   - Contrarian signal identification

4. **⚠️ Risk Management Agent**
   - Portfolio VaR calculations
   - Position sizing recommendations
   - Correlation analysis
   - Drawdown scenario modeling

5. **🧠 Pattern Analysis Agent**
   - 25+ trading psychology patterns
   - Behavioral bias detection
   - Root cause analysis
   - Correction strategies

### Tool Integration System

The AI agents work as **callable tools** that can be used by:

- **Smart Trading Assistant**: Automatically selects relevant tools
- **OpenAI Function Calling**: OpenAI agent calls tools as functions
- **Direct Tool Access**: Call specific tools programmatically

## 📊 Example Usage Scenarios

### Scenario 1: Market Analysis Request
```bash
python main.py openai-tools sk-your-key "What are current market conditions and should I worry about my tech positions?"
```

**What happens:**
1. OpenAI agent receives query
2. Automatically calls `check_market_conditions` tool
3. Calls `get_market_data` for tech stocks
4. Calls `assess_portfolio_risk` for risk analysis
5. Integrates all results into comprehensive response

### Scenario 2: Trading Behavior Analysis
```bash
python main.py analyze samples/scenario1 sk-your-key
```

**What happens:**
1. Loads trading data from scenario
2. Calls multiple AI agents in parallel:
   - Pattern analysis for psychology patterns
   - Market data for context
   - Sentiment analysis for market conditions
   - Risk assessment for portfolio impact
3. Provides integrated analysis with specific recommendations

### Scenario 3: Interactive Learning Session
```bash
python main.py interactive samples/scenario1 sk-your-key trader123
```

**What happens:**
1. Loads user profile for personalized analysis
2. Uses AI agents for comprehensive market context
3. Analyzes trading data with all available tools
4. Asks personalized follow-up questions
5. Learns from responses to improve future sessions

## 🧪 Testing and Validation

### Run Comprehensive Tests
```bash
# Test all AI agent functionality
python main.py test-agents

# Demo individual agent capabilities
python main.py demo-agents

# Test smart assistant
python main.py smart-assistant demo
```

### Validate Integration
```bash
# Test OpenAI function calling
python main.py openai-tools sk-your-key "Analyze AAPL sentiment"

# Test professional analysis
python main.py analyze samples/scenario1 sk-your-key
```

## 📁 Project Structure

```
📦 poc/
├── 🤖 agents/                    # AI Agent System
│   ├── __init__.py
│   ├── base_agent.py            # Base agent class
│   ├── news_agent.py            # News analysis
│   ├── market_data_agent.py     # Market data & technicals
│   ├── sentiment_agent.py       # Sentiment analysis
│   ├── risk_management_agent.py # Risk & portfolio analysis
│   ├── pattern_analysis_agent.py # Psychology patterns
│   ├── agent_manager.py         # Agent coordinator
│   └── tool_integration.py      # Tool system integration
├── 📜 scripts/                  # Main Scripts
│   ├── pro_trading_assistant.py # Professional analysis
│   ├── interactive_trading_assistant.py # Interactive sessions
│   ├── smart_trading_assistant.py # Smart tool selection
│   ├── openai_with_agent_tools.py # OpenAI function calling
│   ├── demo_agents.py          # Agent demonstration
│   └── test_agent_tools.py     # Test suite
├── 📋 prompts/                  # Pattern Templates
│   └── trading_pattern_templates/ # 25+ psychology patterns
├── 📊 samples/                  # Trading Scenarios
│   └── scenario1-11/           # Sample trading data
├── 👥 user_profiles/           # User Learning Data
├── 🚀 main.py                  # Unified Entry Point
├── 🔧 run_trading_assistant.sh # Enhanced shell script
├── 🔧 run_interactive_assistant.sh # Enhanced shell script
└── 📚 README.md               # This file
```

## 🎨 Customization

### Adding New AI Agents

1. Create new agent class inheriting from `BaseAgent`
2. Implement `process_request()` method
3. Add to `AgentManager` in `agent_manager.py`
4. Register as tool in `tool_integration.py`

### Adding New Trading Patterns

Add `.txt` files to `prompts/trading_pattern_templates/`:
```
Prompt: Detect your_pattern. Description of pattern detection criteria.
```

### Customizing Analysis

- Modify system prompts in individual scripts
- Adjust agent response parameters
- Add new tool functions in `tool_integration.py`

## 🔧 Configuration Options

### Environment Variables
```bash
export OPENAI_API_KEY=sk-your-key
```

### Configuration Files
- Pattern templates in `prompts/trading_pattern_templates/`
- User profiles in `user_profiles/`
- Sample scenarios in `samples/`

## 📈 Performance

- **Individual Agent**: ~0.5-2.0 seconds
- **Parallel Execution**: ~2-3 seconds for 4+ agents
- **Function Calling**: ~3-5 seconds with multiple tools
- **Full Analysis**: ~5-10 seconds comprehensive

## 🚨 Important Notes

### Fake Data Notice
**All AI agents currently provide simulated responses for testing purposes.** This includes:
- Market news and headlines
- Price data and technical indicators
- Sentiment scores and social media data
- Risk calculations and metrics

The system demonstrates capabilities with realistic-looking fake data.

### OpenAI API Usage
The system uses OpenAI's GPT-4 for:
- Main trading analysis and psychology assessment
- Function calling to AI agent tools
- Natural language query processing
- Personalized advice generation

## 🎯 Anti-Pattern Detection

The system detects 25+ trading anti-patterns across three severity levels:

**🔴 CRITICAL** (Account-destroying patterns):
- Revenge trading, No risk management, Martingale strategy

**🟡 WARNING** (Profit-eroding patterns):
- Overtrading, Emotional trading, FOMO, Averaging down

**🔵 IMPROVEMENT** (Performance-limiting patterns):
- Premature profit taking, Timing inconsistency, Liquidity ignorance

## 📊 Sample Scenarios

11 pre-built scenarios demonstrate different anti-patterns:

- **Scenario 1**: Premature profit-taking and timing inconsistency
- **Scenario 2**: Averaging down addiction and martingale strategy
- **Scenarios 3-11**: FOMO, overtrading, revenge trading, and more

Each scenario includes `sample_trades.csv` with realistic trading data.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're in the project root directory
2. **API Key Issues**: Verify your OpenAI API key format (starts with `sk-`)
3. **Missing Scenarios**: Use `python main.py list-scenarios` to see available data
4. **Tool Failures**: AI agents have fallback mechanisms to basic OpenAI analysis

### Debug Mode
```bash
# Test individual components
python scripts/test_agent_tools.py

# Check available scenarios
python main.py list-scenarios

# Validate AI agent system
python scripts/demo_agents.py
```

## 🚀 Future Enhancements

- Real market data integration (APIs)
- Advanced machine learning pattern recognition
- Web-based dashboard interface
- Real-time streaming data processing
- Custom agent creation tools
- Advanced risk models and backtesting

## 📞 Support

For questions and issues:
1. Run the test suite: `python main.py test-agents`
2. Check available options: `python main.py help`
3. Validate your setup with demo mode: `python main.py demo-agents`

## 📄 License

MIT License - see LICENSE file for details.

## ⚠️ Disclaimer

This tool is for educational and analytical purposes. All AI agent responses are simulated for demonstration. Trading decisions should be based on comprehensive analysis and proper risk management. Not financial advice.

---

© 2025 Advanced Trading Assistant with AI Agent Tools