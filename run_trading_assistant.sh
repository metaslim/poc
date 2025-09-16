#!/bin/sh
# Usage: sh run_trading_assistant.sh <scenario_folder> <openai_api_key>

SCENARIO_FOLDER="$1"
OPENAI_API_KEY="$2"

python3 scripts/pro_trading_assistant.py "$SCENARIO_FOLDER" "$OPENAI_API_KEY"
