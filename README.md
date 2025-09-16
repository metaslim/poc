# Professional Trading Assistant AI

An advanced trading psychology and risk management system that detects anti-patterns in trading behavior using AI analysis. Features both basic analysis and interactive learning capabilities with user behavior tracking.

## 🚀 Features

- **25 Anti-Pattern Detection Templates** - Comprehensive behavioral analysis
- **Interactive Learning System** - AI asks follow-up questions and learns from responses
- **User Profile Management** - Tracks behavior patterns and personalizes advice
- **11 Realistic Test Scenarios** - From overtrading to revenge trading patterns
- **Severity-Based Analysis** - Critical, warning, and improvement level categorization
- **Session History Tracking** - Stores past sessions for learning improvement

## 📁 Project Structure

```
├── samples/                           # Trading scenario test data
│   ├── scenario1-11/                  # 11 realistic trading scenarios
│   │   └── sample_trades.csv         # CSV format: date,action,symbol,quantity,price,notes
│   └── sample_trades.csv             # Example CSV format
├── prompts/trading_pattern_templates/ # 25 AI analysis templates
│   ├── overtrading.txt               # Excessive trading detection
│   ├── revenge_trading.txt           # Emotional loss recovery attempts
│   ├── position_sizing_errors.txt    # Risk management failures
│   └── ... (22 more patterns)
├── scripts/                          # Core Python modules
│   ├── pro_trading_assistant.py      # Basic analysis engine
│   ├── interactive_trading_assistant.py  # Interactive learning system
│   ├── pattern_extractor.py          # Pattern detection utilities
│   └── sync_pattern_keywords.py      # Template synchronization
├── user_profiles/                    # User behavior storage
│   └── {user_id}/                    # Individual user data
│       ├── profile.json              # User behavioral profile
│       └── past_sessions/            # Historical session data
├── run_trading_assistant.sh          # Basic analysis launcher
└── run_interactive_assistant.sh      # Interactive mode launcher
```

## 📋 Requirements

- Python 3.8+
- OpenAI Python package (`pip install openai`)
- Valid OpenAI API key

## 🛠️ Installation

```bash
git clone <repository>
cd professional-trading-assistant
pip install openai
```

## 💡 Usage

### Basic Analysis Mode
Analyzes trading data and provides immediate feedback:

```bash
# Using shell script
sh run_trading_assistant.sh samples/scenario1 sk-your-api-key

# Direct Python execution
python scripts/pro_trading_assistant.py samples/scenario1 sk-your-api-key
```

### Interactive Learning Mode
Enhanced experience with follow-up questions and user behavior learning:

```bash
# Using shell script
sh run_interactive_assistant.sh samples/scenario1 sk-your-api-key john_trader

# Direct Python execution
python scripts/interactive_trading_assistant.py samples/scenario1 sk-your-api-key john_trader
```

## 🎯 Anti-Pattern Detection

The system detects 25 trading anti-patterns across three severity levels:

**🔴 CRITICAL** (Account-destroying patterns):
- Revenge trading, No risk management, Martingale strategy

**🟡 WARNING** (Profit-eroding patterns):
- Overtrading, Emotional trading, FOMO, Averaging down

**🔵 IMPROVEMENT** (Performance-limiting patterns):
- Premature profit taking, Timing inconsistency, Liquidity ignorance

## 🧠 Learning System

The interactive assistant:

1. **Analyzes** trading data using 25 behavioral templates
2. **Asks** targeted follow-up questions about trading psychology
3. **Learns** from user responses to build behavioral profiles
4. **Personalizes** advice based on experience level and risk tolerance
5. **Tracks** improvement over multiple sessions

### User Profile Data
- Risk tolerance assessment
- Experience level tracking
- Recurring pattern identification
- Advice style preferences
- Session history and improvement trends

## 📊 Sample Scenarios

11 pre-built scenarios demonstrate different anti-patterns:

- **Scenario 1**: Premature profit-taking and timing inconsistency
- **Scenario 2**: Averaging down addiction and martingale strategy
- **Scenario 3**: FOMO and emotional panic trading with position sizing errors
- **Scenario 4**: Overexposure and lack of position management focus
- **Scenario 5**: No risk management and stop-loss discipline failures
- **Scenario 6**: News-driven emotional trading and social sentiment chasing
- **Scenario 7**: Revenge trading escalation
- **Scenario 8**: Overtrading behavior (16 trades in one day)
- **Scenario 9**: No stop-loss discipline (20%+ losses)
- **Scenario 10**: Trend fighting and strategy confusion
- **Scenario 11**: Averaging down addiction

## 🔧 Customization

### Adding New Anti-Pattern Templates
1. Create new `.txt` file in `prompts/trading_pattern_templates/`
2. Run `python scripts/sync_pattern_keywords.py` to update detection
3. Format: `Prompt: [Detection criteria and behavioral indicators]`

### Creating New Scenarios
1. Add new folder in `samples/` (e.g., `scenario12/`)
2. Create `sample_trades.csv` with columns: `date,action,symbol,quantity,price,notes`
3. Include realistic trading patterns that demonstrate specific anti-patterns

## 📈 Output Examples

**Basic Analysis:**
```
🔴 CRITICAL: Revenge Trading Detected
EVIDENCE: Position sizes tripled after losses on 2025-09-01
PSYCHOLOGY: Loss aversion driving escalating risk-taking
CONSEQUENCES: 15% account loss in single session
SOLUTION: Implement daily loss limits and cooling-off periods
```

**Interactive Follow-up:**
```
FOLLOW-UP QUESTIONS:
1. What emotions were you feeling when you increased position sizes after the TSLA loss?
2. Do you have predetermined daily loss limits in place?
3. How do you typically react when a trade goes against you immediately?
```

## 🔄 Pattern Synchronization

Keep detection keywords synchronized with templates:

```bash
python scripts/sync_pattern_keywords.py
```

This automatically updates the pattern extraction system to match all template files.

## 🏗️ Architecture

- **pro_trading_assistant.py**: Core analysis engine with enhanced prompts
- **interactive_trading_assistant.py**: Learning system with user profiles
- **pattern_extractor.py**: Auto-synced pattern detection from analysis text
- **UserProfile class**: JSON-based behavioral data persistence
- **Template system**: Modular, extensible anti-pattern definitions

---

© 2025 Professional Trading Assistant AI
