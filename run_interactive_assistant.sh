#!/bin/bash

# Interactive Trading Assistant Runner
# Usage: sh run_interactive_assistant.sh <scenario_folder> <openai_api_key> <user_id>

if [ $# -lt 3 ]; then
    echo "Usage: sh run_interactive_assistant.sh <scenario_folder> <openai_api_key> <user_id>"
    echo ""
    echo "Examples:"
    echo "  sh run_interactive_assistant.sh data/scenario1 sk-your-api-key john_trader"
    echo "  sh run_interactive_assistant.sh data/scenario7 sk-your-api-key alice_investor"
    echo ""
    echo "Available scenarios:"
    ls -d data/scenario* 2>/dev/null | sed 's/^/  /'
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
    ls -d data/scenario* 2>/dev/null | sed 's/^/  /'
    exit 1
fi

# Check if sample_trades.csv exists in scenario
if [ ! -f "$scenario_folder/sample_trades.csv" ]; then
    echo "Error: No sample_trades.csv found in '$scenario_folder'"
    exit 1
fi

# Run the interactive assistant
echo "Starting Interactive Trading Assistant..."
echo "Scenario: $scenario_folder"
echo "User ID: $user_id"
echo "=========================================="
echo ""

cd scripts
python interactive_trading_assistant.py "../$scenario_folder" "$openai_api_key" "$user_id"