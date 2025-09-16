"""Pattern Extraction Utilities

This module provides utilities to extract detected patterns from AI analysis results.
"""

import re
from typing import List, Dict


def extract_detected_patterns(analysis_text: str) -> List[str]:
    """Extract detected anti-patterns from analysis text.

    Args:
        analysis_text: The AI analysis result text

    Returns:
        List of detected pattern names
    """
    patterns = []

    # Common pattern keywords to look for
    pattern_keywords = {
        'anchoring_bias': ['anchoring', 'reference point', 'psychological anchor'],
        'averaging_down': ['averaging down', 'doubling down', 'adding to losing', 'lower average cost'],
        'chasing_losses': ['chasing losses', 'trying to recover', 'recover quickly'],
        'confirmation_bias': ['confirmation bias', 'selective information', 'confirming beliefs'],
        'correlation_blindness': ['correlation', 'concentrated risk', 'similar positions', 'correlated'],
        'emotional_trading': ['emotional trading', 'panic', 'fear', 'greed', 'emotions'],
        'fomo': ['fomo', 'fear of missing out', 'market hype', 'missing opportunities'],
        'herd_mentality': ['herd mentality', 'following crowd', 'crowd psychology'],
        'holding_losers_too_long': ['holding losers', 'too long', 'unrealized losses'],
        'ignoring_market_conditions': ['ignoring market', 'market conditions', 'market environment'],
        'ignoring_risk_management': ['ignoring risk', 'risk management', 'too much capital'],
        'lack_of_diversification': ['lack of diversification', 'concentrated', 'single position'],
        'lack_of_stop_loss': ['no stop loss', 'lack of stop', 'stop-loss', 'risk management'],
        'liquidity_ignorance': ['liquidity', 'low volume', 'illiquid', 'bid-ask spread'],
        'martingale_strategy': ['martingale', 'double after loss', 'geometric progression'],
        'news_reaction_trading': ['news reaction', 'news events', 'impulsive news', 'immediate reaction'],
        'no_trading_plan': ['no trading plan', 'without strategy', 'clear plan', 'no strategy'],
        'overconfidence_bias': ['overconfidence', 'overestimate', 'bias'],
        'overtrading': ['overtrading', 'excessive trading', 'too many trades', 'frequent trading'],
        'position_sizing_errors': ['position size', 'risk too much', 'disproportionate', 'account size'],
        'premature_profit_taking': ['premature profit', 'early exit', 'profit taking'],
        'revenge_trading': ['revenge trading', 'emotional response', 'recover losses', 'impulsive trades'],
        'timing_inconsistency': ['timing inconsistency', 'time horizons', 'mixed strategies'],
        'trading_on_rumors': ['trading on rumors', 'unverified information', 'speculation'],
        'trend_fighting': ['fighting trend', 'against trend', 'counter trend', 'falling knives'],
    }

    analysis_lower = analysis_text.lower()

    for pattern_name, keywords in pattern_keywords.items():
        for keyword in keywords:
            if keyword in analysis_lower:
                if pattern_name not in patterns:
                    patterns.append(pattern_name)
                break

    return patterns


def extract_severity_levels(analysis_text: str) -> Dict[str, List[str]]:
    """Extract patterns grouped by severity level from analysis text.

    Args:
        analysis_text: The AI analysis result text

    Returns:
        Dictionary with severity levels as keys and pattern lists as values
    """
    severity_patterns = {
        'critical': [],
        'warning': [],
        'improvement': []
    }

    # Look for severity indicators
    lines = analysis_text.split('\n')

    for line in lines:
        line_lower = line.lower()
        if '🔴' in line or 'critical' in line_lower:
            # Extract pattern from this line
            pattern = extract_pattern_from_line(line)
            if pattern:
                severity_patterns['critical'].append(pattern)
        elif '🟡' in line or 'warning' in line_lower:
            pattern = extract_pattern_from_line(line)
            if pattern:
                severity_patterns['warning'].append(pattern)
        elif '🔵' in line or 'improvement' in line_lower:
            pattern = extract_pattern_from_line(line)
            if pattern:
                severity_patterns['improvement'].append(pattern)

    return severity_patterns


def extract_pattern_from_line(line: str) -> str:
    """Extract pattern name from a single line of text.

    Args:
        line: Single line of text

    Returns:
        Extracted pattern name or empty string
    """
    # Remove emojis and common prefixes
    clean_line = re.sub(r'[🔴🟡🔵]', '', line).strip()
    clean_line = re.sub(r'^(CRITICAL|WARNING|IMPROVEMENT):', '', clean_line, flags=re.IGNORECASE).strip()

    # Look for pattern names (usually capitalized or in quotes)
    pattern_match = re.search(r'([A-Z][A-Z\s]+)|"([^"]+)"|\'([^\']+)\'', clean_line)
    if pattern_match:
        return pattern_match.group(1) or pattern_match.group(2) or pattern_match.group(3)

    return ""


def extract_follow_up_questions(analysis_text: str) -> List[str]:
    """Extract follow-up questions from analysis text.

    Args:
        analysis_text: The AI analysis result text

    Returns:
        List of follow-up questions
    """
    questions = []

    if "FOLLOW-UP QUESTIONS:" in analysis_text:
        questions_section = analysis_text.split("FOLLOW-UP QUESTIONS:")[-1].strip()

        # Split by lines and extract questions
        lines = questions_section.split('\n')
        for line in lines:
            line = line.strip()
            # Look for numbered or bulleted questions
            if line and (re.match(r'^\d+\.', line) or line.startswith('•') or line.startswith('-')):
                # Clean up formatting
                question = re.sub(r'^\d+\.\s*|^[•\-]\s*', '', line).strip()
                if question.endswith('?'):
                    questions.append(question)

    return questions


def extract_recommendations(analysis_text: str) -> List[str]:
    """Extract recommendations from analysis text.

    Args:
        analysis_text: The AI analysis result text

    Returns:
        List of recommendations
    """
    recommendations = []

    # Look for sections with recommendations
    sections = ['SOLUTION:', 'RECOMMENDATIONS:', 'ADVICE:', 'ACTION STEPS:']

    for section in sections:
        if section in analysis_text.upper():
            # Find all instances of this section
            parts = analysis_text.upper().split(section)
            for i in range(1, len(parts)):
                # Get text until next major section or end
                text = parts[i].split('\n\n')[0] if '\n\n' in parts[i] else parts[i]

                # Extract bulleted or numbered recommendations
                lines = text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and (re.match(r'^\d+\.', line) or line.startswith('•') or line.startswith('-')):
                        rec = re.sub(r'^\d+\.\s*|^[•\-]\s*', '', line).strip()
                        if rec and rec not in recommendations:
                            recommendations.append(rec)

    return recommendations