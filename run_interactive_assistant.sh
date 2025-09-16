#!/bin/bash

# Interactive Trading Assistant Runner with AI Agent Tools
# Usage: sh run_interactive_assistant.sh <scenario_folder> <openai_api_key> <user_id>

echo "🤖 ADVANCED TRADING ASSISTANT WITH AI AGENT TOOLS"
echo "=================================================="

if [ $# -lt 3 ]; then
    echo "Usage: sh run_interactive_assistant.sh <scenario_folder> <openai_api_key> <user_id>"
    echo ""
    echo "Examples:"
    echo "  sh run_interactive_assistant.sh samples/scenario1 sk-your-api-key john_trader"
    echo "  sh run_interactive_assistant.sh samples/scenario7 sk-your-api-key alice_investor"
    echo ""
    echo "Available scenarios:"
    ls -d samples/scenario* 2>/dev/null | sed 's/^/  /'
    exit 1
fi

scenario_folder="$1"
openai_api_key="$2"
user_id="$3"

# Check if scenario folder exists
if [ ! -d "$scenario_folder" ]; then
    echo "Error: Scenario folder '$scenario_folder' does not exist."
    echo ""
    echo "Available scenarios:"
    ls -d samples/scenario* 2>/dev/null | sed 's/^/  /'
    exit 1
fi

# Check if sample_trades.csv exists in scenario
if [ ! -f "$scenario_folder/sample_trades.csv" ]; then
    echo "Error: No sample_trades.csv found in '$scenario_folder'"
    exit 1
fi

# Run the enhanced interactive assistant
echo "🚀 Starting Enhanced Interactive Trading Assistant..."
echo "📊 Scenario: $scenario_folder"
echo "👤 User ID: $user_id"
echo "🤖 AI Agent Tools: ENABLED"
echo "=================================================="
echo ""

# Use the unified main entry point
python main.py interactive "$scenario_folder" "$openai_api_key" "$user_id"