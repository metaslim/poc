"""Professional Trading Assistant AI - Anti-Pattern Detector

This module analyzes trading behavior to detect anti-patterns and provides
actionable feedback using OpenAI's GPT models.
"""

import os
import sys
from typing import Dict, Optional
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI package not installed. Run: pip install openai")
    sys.exit(1)


def load_trading_data(scenario_folder: str) -> str:
    """Load trading data from CSV file in the specified scenario folder.

    Args:
        scenario_folder: Path to the scenario folder containing sample_trades.csv

    Returns:
        Content of the CSV file as a string

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
    """
    file_path = Path(scenario_folder) / "sample_trades.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"Trading data file not found: {file_path}")

    return file_path.read_text(encoding='utf-8')


def load_pattern_templates(templates_folder: str) -> Dict[str, str]:
    """Load anti-pattern templates from text files.

    Args:
        templates_folder: Path to folder containing pattern template files

    Returns:
        Dictionary mapping pattern names to their descriptions
    """
    templates = {}
    template_path = Path(templates_folder)

    if not template_path.exists():
        print(f"Warning: Templates folder not found: {template_path}")
        return templates

    for file_path in template_path.glob("*.txt"):
        name = file_path.stem.replace('_', ' ').title()
        content = file_path.read_text(encoding='utf-8')
        # Remove "Prompt: " prefix if present and clean whitespace
        templates[name] = content.replace('Prompt: ', '').strip()

    return templates


def build_system_prompt() -> str:
    """Build the system prompt for the AI assistant."""
    return (
        "You are an elite trading psychology analyst and risk management expert with 20+ years of experience. "
        "Your mission is to identify self-destructive trading patterns that destroy capital and careers.\n\n"
        "ANALYSIS FRAMEWORK:\n"
        "For each anti-pattern you detect, provide:\n"
        "• EVIDENCE: Specific trades/data points that demonstrate the pattern\n"
        "• PSYCHOLOGY: The emotional/cognitive bias driving this behavior\n"
        "• CONSEQUENCES: Quantified impact on performance (losses, missed opportunities)\n"
        "• SOLUTION: Concrete, actionable steps to eliminate this pattern\n\n"
        "SEVERITY LEVELS:\n"
        "🔴 CRITICAL: Patterns that can blow up accounts (revenge trading, no risk management)\n"
        "🟡 WARNING: Patterns that erode profits over time (overtrading, emotional decisions)\n"
        "🔵 IMPROVEMENT: Patterns that limit potential (poor timing, suboptimal execution)\n\n"
        "Be brutally honest but constructive. Focus on the most damaging patterns first. "
        "Use specific numbers and percentages when quantifying impact."
    )


def build_user_prompt(trading_data: str, templates: Dict[str, str]) -> str:
    """Build the user prompt combining trading data and pattern templates.

    Args:
        trading_data: Raw trading data as a string
        templates: Dictionary of anti-pattern templates

    Returns:
        Formatted prompt for analysis
    """
    prompt = "Analyze the following trading data for anti-patterns using these criteria:\n\n"

    for name, rule in sorted(templates.items()):
        prompt += f"• {name}: {rule}\n"

    prompt += f"\n--- Trading Data ---\n{trading_data}\n"
    prompt += "\nProvide your analysis with specific examples from the data."

    return prompt


def detect_anti_patterns(trading_data: str, templates: Dict[str, str], api_key: str) -> str:
    """Detect anti-patterns in trading data using OpenAI API.

    Args:
        trading_data: Raw trading data as a string
        templates: Dictionary of anti-pattern templates
        api_key: OpenAI API key

    Returns:
        Analysis result from the AI model
    """
    try:
        client = OpenAI(api_key=api_key)
        system_prompt = build_system_prompt()
        user_prompt = build_user_prompt(trading_data, templates)

        response = client.chat.completions.create(
            model="gpt-4",  # Changed from gpt-5 to gpt-4 (more reliable)
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=1200,  # Increased for more detailed analysis
            temperature=0.1  # Lower temperature for more consistent analysis
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error analyzing trading data: {str(e)}"


def validate_inputs(scenario_folder: str, api_key: str) -> Optional[str]:
    """Validate input parameters.

    Args:
        scenario_folder: Path to scenario folder
        api_key: OpenAI API key

    Returns:
        Error message if validation fails, None otherwise
    """
    if not os.path.isdir(scenario_folder):
        return f"Error: Scenario folder '{scenario_folder}' does not exist."

    if not api_key or not api_key.startswith('sk-'):
        return "Error: Invalid or missing OpenAI API key."

    return None

def main():
    """Main entry point for the trading assistant."""
    if len(sys.argv) < 3:
        print("Usage: python pro_trading_assistant.py <scenario_folder> <openai_api_key>")
        print("\nExample:")
        print("  python pro_trading_assistant.py data/scenario1 sk-your-api-key")
        sys.exit(1)

    scenario_folder = sys.argv[1]
    api_key = sys.argv[2]

    # Validate inputs
    error = validate_inputs(scenario_folder, api_key)
    if error:
        print(error)
        sys.exit(1)

    # Get templates folder path relative to script location
    script_dir = Path(__file__).parent
    templates_folder = script_dir.parent / "prompts" / "trading_pattern_templates"

    try:
        print(f"Loading trading data from: {scenario_folder}")
        trading_data = load_trading_data(scenario_folder)

        print(f"Loading pattern templates from: {templates_folder}")
        templates = load_pattern_templates(str(templates_folder))

        if not templates:
            print("Warning: No pattern templates found. Analysis may be limited.")

        print(f"Analyzing {len(templates)} anti-patterns...")
        print("-" * 50)

        result = detect_anti_patterns(trading_data, templates, api_key)
        print(result)

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
