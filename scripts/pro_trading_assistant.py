"""Professional Trading Assistant AI - Anti-Pattern Detector

This module analyzes trading behavior to detect anti-patterns and provides
actionable feedback using OpenAI's GPT models.
"""

import os
import sys
from typing import Dict, Optional
from pathlib import Path

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI package not installed. Run: pip install openai")
    sys.exit(1)

# Import configuration
try:
    from config import config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# Import AI agent tools
try:
    from scripts.openai_with_agent_tools import OpenAIWithAgentTools
    AI_TOOLS_AVAILABLE = True
except ImportError:
    try:
        # Try direct import if running from scripts directory
        from openai_with_agent_tools import OpenAIWithAgentTools
        AI_TOOLS_AVAILABLE = True
    except ImportError:
        print("Warning: AI agent tools not available, falling back to basic OpenAI analysis")
        AI_TOOLS_AVAILABLE = False


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
    """Detect anti-patterns in trading data using OpenAI API with AI agent tools.

    Args:
        trading_data: Raw trading data as a string
        templates: Dictionary of anti-pattern templates
        api_key: OpenAI API key

    Returns:
        Analysis result from the AI model
    """
    try:
        if AI_TOOLS_AVAILABLE:
            return detect_anti_patterns_with_tools(trading_data, templates, api_key)
        else:
            return detect_anti_patterns_basic(trading_data, templates, api_key)

    except Exception as e:
        print(f"⚠️ AI tools failed, falling back to basic analysis: {e}")
        return detect_anti_patterns_basic(trading_data, templates, api_key)


def detect_anti_patterns_with_tools(trading_data: str, templates: Dict[str, str], api_key: str) -> str:
    """Enhanced analysis using OpenAI with AI agent tools."""
    openai_with_tools = OpenAIWithAgentTools(api_key)

    # Build comprehensive analysis query
    analysis_query = "Perform comprehensive trading psychology analysis with the following data:\n\n"

    # Add pattern templates
    analysis_query += "Anti-pattern criteria to check:\n"
    for name, rule in sorted(templates.items()):
        analysis_query += f"• {name}: {rule}\n"

    analysis_query += f"\n--- Trading Data ---\n{trading_data}\n"
    analysis_query += "\nPlease use your available tools to:\n"
    analysis_query += "1. Check current market conditions for context\n"
    analysis_query += "2. Analyze market sentiment that might affect this trading behavior\n"
    analysis_query += "3. Assess risk factors in the trades\n"
    analysis_query += "4. Detect specific trading psychology patterns\n"
    analysis_query += "5. Provide detailed analysis with specific examples from the data\n"
    analysis_query += "6. Rate the severity of each detected anti-pattern\n"
    analysis_query += "7. Provide concrete actionable recommendations\n"

    print("🤖 Enhanced analysis using AI agent tools...")
    return openai_with_tools.analyze_with_tools(analysis_query, trading_data)


def detect_anti_patterns_basic(trading_data: str, templates: Dict[str, str], api_key: str) -> str:
    """Basic analysis using standard OpenAI API."""
    client = OpenAI(api_key=api_key)
    system_prompt = build_system_prompt()
    user_prompt = build_user_prompt(trading_data, templates)

    # Use config if available, otherwise use defaults
    if CONFIG_AVAILABLE:
        openai_config = config.get_openai_config()
        openai_config["stream"] = True
        stream = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            **openai_config
        )
    else:
        stream = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_completion_tokens=1500,
            temperature=1.0,
            stream=True
        )

    # Collect streamed response
    response_text = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            response_text += content
            print(content, end='', flush=True)

    print()  # Add newline at end
    return response_text


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
