#!/bin/bash

# Professional Trading Assistant with AI Agent Tools
# Usage: sh run_trading_assistant.sh <scenario_folder> <openai_api_key>

echo "🤖 PROFESSIONAL TRADING ASSISTANT WITH AI AGENT TOOLS"
echo "====================================================="

if [ $# -lt 2 ]; then
    echo "Usage: sh run_trading_assistant.sh <scenario_folder> <openai_api_key>"
    echo ""
    echo "Examples:"
    echo "  sh run_trading_assistant.sh samples/scenario1 sk-your-api-key"
    echo "  sh run_trading_assistant.sh samples/scenario7 sk-your-api-key"
    echo ""
    echo "Available scenarios:"
    ls -d samples/scenario* 2>/dev/null | sed 's/^/  /'
    exit 1
fi

SCENARIO_FOLDER="$1"
OPENAI_API_KEY="$2"

# Check if scenario folder exists
if [ ! -d "$SCENARIO_FOLDER" ]; then
    echo "Error: Scenario folder '$SCENARIO_FOLDER' does not exist."
    echo ""
    echo "Available scenarios:"
    ls -d samples/scenario* 2>/dev/null | sed 's/^/  /'
    exit 1
fi

# Check if sample_trades.csv exists
if [ ! -f "$SCENARIO_FOLDER/sample_trades.csv" ]; then
    echo "Error: No sample_trades.csv found in '$SCENARIO_FOLDER'"
    exit 1
fi

echo "🚀 Starting Professional Analysis with AI Agent Tools..."
echo "📊 Scenario: $SCENARIO_FOLDER"
echo "🤖 AI Agent Tools: ENABLED"
echo "====================================================="
echo ""

# Use the unified main entry point
python main.py analyze "$SCENARIO_FOLDER" "$OPENAI_API_KEY"
