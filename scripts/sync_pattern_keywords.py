"""Sync Pattern Keywords with Template Files

This script automatically generates pattern keywords dictionary based on
existing template files to keep them in sync.
"""

import os
from pathlib import Path
from typing import Dict, List


def generate_pattern_keywords() -> Dict[str, List[str]]:
    """Generate pattern keywords dictionary from template files."""
    script_dir = Path(__file__).parent
    templates_folder = script_dir.parent / "prompts" / "trading_pattern_templates"

    pattern_keywords = {}

    # Define common keywords that might appear in different patterns
    keyword_mappings = {
        'overtrading': ['overtrading', 'excessive trading', 'too many trades', 'frequent trading'],
        'revenge_trading': ['revenge trading', 'emotional response', 'recover losses', 'impulsive trades'],
        'lack_of_stop_loss': ['no stop loss', 'lack of stop', 'stop-loss', 'risk management'],
        'averaging_down': ['averaging down', 'doubling down', 'adding to losing', 'lower average cost'],
        'fomo': ['fomo', 'fear of missing out', 'market hype', 'missing opportunities'],
        'chasing_losses': ['chasing losses', 'trying to recover', 'recover quickly'],
        'emotional_trading': ['emotional trading', 'panic', 'fear', 'greed', 'emotions'],
        'position_sizing_errors': ['position size', 'risk too much', 'disproportionate', 'account size'],
        'trend_fighting': ['fighting trend', 'against trend', 'counter trend', 'falling knives'],
        'correlation_blindness': ['correlation', 'concentrated risk', 'similar positions', 'correlated'],
        'ignoring_risk_management': ['ignoring risk', 'risk management', 'too much capital'],
        'no_trading_plan': ['no trading plan', 'without strategy', 'clear plan', 'no strategy'],
        'herd_mentality': ['herd mentality', 'following crowd', 'crowd psychology'],
        'overconfidence_bias': ['overconfidence', 'overestimate', 'bias'],
        'holding_losers_too_long': ['holding losers', 'too long', 'unrealized losses'],
        'premature_profit_taking': ['premature profit', 'early exit', 'profit taking'],
        'lack_of_diversification': ['lack of diversification', 'concentrated', 'single position'],
        'ignoring_market_conditions': ['ignoring market', 'market conditions', 'market environment'],
        'trading_on_rumors': ['trading on rumors', 'unverified information', 'speculation'],
        'anchoring_bias': ['anchoring', 'reference point', 'psychological anchor'],
        'martingale_strategy': ['martingale', 'double after loss', 'geometric progression'],
        'confirmation_bias': ['confirmation bias', 'selective information', 'confirming beliefs'],
        'timing_inconsistency': ['timing inconsistency', 'time horizons', 'mixed strategies'],
        'liquidity_ignorance': ['liquidity', 'low volume', 'illiquid', 'bid-ask spread'],
        'news_reaction_trading': ['news reaction', 'news events', 'impulsive news', 'immediate reaction']
    }

    # Get actual template files
    if templates_folder.exists():
        for file_path in templates_folder.glob("*.txt"):
            template_name = file_path.stem

            # Convert filename to pattern key
            pattern_key = template_name.replace('_', '_').lower()

            # Use predefined keywords if available, otherwise create basic ones
            if pattern_key in keyword_mappings:
                pattern_keywords[pattern_key] = keyword_mappings[pattern_key]
            else:
                # Create basic keywords from filename
                words = template_name.replace('_', ' ').split()
                basic_keywords = [
                    template_name.replace('_', ' '),
                    ' '.join(words[:2]) if len(words) > 1 else words[0]
                ]
                pattern_keywords[pattern_key] = basic_keywords

    return pattern_keywords


def update_pattern_extractor():
    """Update the pattern_extractor.py file with synced keywords."""
    script_dir = Path(__file__).parent
    extractor_file = script_dir / "pattern_extractor.py"

    if not extractor_file.exists():
        print(f"Error: {extractor_file} not found")
        return

    # Generate new keywords
    new_keywords = generate_pattern_keywords()

    # Read current file
    content = extractor_file.read_text()

    # Find the pattern_keywords dictionary and replace it
    import re

    # Pattern to match the dictionary definition
    pattern = r'pattern_keywords\s*=\s*{[^}]+}'

    # Create new dictionary string
    new_dict_str = "pattern_keywords = {\n"
    for key, values in sorted(new_keywords.items()):
        values_str = ", ".join([f"'{v}'" for v in values])
        new_dict_str += f"        '{key}': [{values_str}],\n"
    new_dict_str += "    }"

    # Replace in content
    new_content = re.sub(pattern, new_dict_str, content, flags=re.DOTALL)

    # Write back to file
    extractor_file.write_text(new_content)

    print(f"Updated pattern_extractor.py with {len(new_keywords)} patterns")
    print("Synced patterns:")
    for key in sorted(new_keywords.keys()):
        print(f"  - {key}")


if __name__ == "__main__":
    update_pattern_extractor()