#!/usr/bin/env python3
"""
Script to enhance all trading pattern templates with comprehensive detection criteria.
"""

import os
from pathlib import Path

# Template enhancement patterns
ENHANCEMENTS = {
    'averaging_down': {
        'description': 'Detect averaging down where traders add to losing positions without fundamental justification, often increasing risk exposure.',
        'criteria': [
            '• Multiple purchases of same symbol with decreasing average price',
            '• Position size increases as price moves against initial position',
            '• Adding to positions without stop-loss adjustment or risk reassessment',
            '• Dollar cost averaging into declining fundamentals',
            '• Justifying additions with "cheaper" rather than "better" reasoning',
            '• Ignoring technical breakdown while adding to position'
        ],
        'quantifiable': [
            '• Position size doubles/triples at lower prices without proportional upside increase',
            '• Maximum loss potential increases >50% from original position',
            '• Average cost basis continues declining over multiple entries',
            '• Win rate on averaged-down positions <30%',
            '• Time to breakeven extends significantly with each addition'
        ],
        'psychological': [
            '• Notes contain "getting a better price", "dollar cost averaging", "it can\'t go lower"',
            '• Refusal to admit original entry was mistimed',
            '• Increasing conviction as price falls without new fundamental data',
            '• Treating unrealized losses as "paper" rather than real risk'
        ]
    },

    'correlation_blindness': {
        'description': 'Detect correlation blindness where traders fail to recognize position concentration risk through highly correlated assets.',
        'criteria': [
            '• Multiple positions in same sector without acknowledging correlation',
            '• Holding tech stocks, tech ETFs, and tech options simultaneously',
            '• Geographic concentration (all US, all emerging markets) without hedging',
            '• Similar risk factors across positions (interest rate sensitivity, oil exposure)',
            '• Diversification illusion through different symbols with similar drivers',
            '• Ignoring sector rotation impact on concentrated positions'
        ],
        'quantifiable': [
            '• Portfolio correlation coefficient >0.7 across major positions',
            '• Sector concentration >40% of portfolio in single industry',
            '• Beta-adjusted portfolio exposure >150% due to correlated positions',
            '• Drawdowns affect >80% of positions simultaneously',
            '• Risk-adjusted returns decline due to false diversification'
        ],
        'timing': [
            '• All positions decline together during sector corrections',
            '• Benefits missed from rotation into uncorrelated sectors',
            '• Over-concentration during sector bubbles',
            '• Simultaneous exit pressure during risk-off periods'
        ]
    },

    'herd_mentality': {
        'description': 'Detect herd mentality where trading decisions follow crowd behavior rather than independent analysis.',
        'criteria': [
            '• Trading based on social media sentiment or forums',
            '• Following "guru" recommendations without independent verification',
            '• Buying into popular stocks without understanding business',
            '• Selling during panic periods due to crowd behavior',
            '• FOMO entries during social media hype cycles',
            '• Abandoning profitable strategies due to peer pressure'
        ],
        'social_signals': [
            '• Trading volume and social media mentions strongly correlated',
            '• Position entries coincide with trending hashtags or discussions',
            '• Strategy changes follow popular trading personalities',
            '• Risk tolerance varies with crowd sentiment',
            '• Exit timing influenced by community panic/euphoria'
        ],
        'quantifiable': [
            '• Win rate decreases during high social sentiment periods',
            '• Position size increases with social validation',
            '• Trading frequency correlates with social media activity',
            '• Worst performing trades coincide with peak social interest',
            '• Strategy abandonment follows crowd psychological shifts'
        ]
    },

    'holding_losers_too_long': {
        'description': 'Detect excessive holding of losing positions due to loss aversion and hope rather than objective analysis.',
        'criteria': [
            '• Positions held significantly longer when showing losses vs gains',
            '• Stop-losses repeatedly moved lower rather than executed',
            '• Fundamental deterioration ignored while holding losing positions',
            '• Converting day trades to swing trades, swing trades to investments when losing',
            '• Rationalizing continued holding with "long-term" perspective',
            '• Avoiding realization of losses for tax or psychological reasons'
        ],
        'timing_analysis': [
            '• Average holding period for losers >3x longer than winners',
            '• Time to maximum loss significantly exceeds time to maximum gain',
            '• Position monitoring intensity decreases as losses mount',
            '• Exit delay increases proportionally with loss magnitude'
        ],
        'quantifiable': [
            '• Loss aversion ratio: hold losers 2.5x longer than winners',
            '• Maximum drawdown per position exceeds original risk parameters',
            '• Percentage of portfolio in underwater positions >30%',
            '• Average loss per losing trade significantly exceeds average gain'
        ]
    },

    'ignoring_risk_management': {
        'description': 'Detect systematic violations of risk management principles leading to excessive losses and portfolio instability.',
        'criteria': [
            '• Position sizing exceeds predetermined risk parameters',
            '• No stop-losses set or stop-losses consistently ignored',
            '• Portfolio heat exceeds safe levels (>20% total risk)',
            '• Correlation risk ignored in position sizing',
            '• Leverage used without corresponding position size reduction',
            '• Risk per trade increases after losing streaks'
        ],
        'violations': [
            '• Individual position risk >5% of portfolio without justification',
            '• Total portfolio risk exceeds 25% at any time',
            '• Stop-losses moved against position >3 times',
            '• Position additions increase total risk beyond original plan',
            '• Leverage multiplies position sizes without reducing base allocation'
        ],
        'consequences': [
            '• Maximum drawdown exceeds 20% due to poor risk control',
            '• Single positions cause >10% portfolio impact',
            '• Risk-of-ruin probability exceeds acceptable levels',
            '• Sharpe ratio deteriorates due to excessive volatility'
        ]
    }
}

def enhance_template(file_path: Path, enhancement_data: dict):
    """Enhance a single template with comprehensive criteria."""

    # Read existing content
    if file_path.exists():
        with open(file_path, 'r') as f:
            original = f.read().strip()
    else:
        original = f"Prompt: Detect {file_path.stem.replace('_', ' ')} patterns."

    # Create enhanced content
    enhanced = f"Prompt: {enhancement_data['description']}\n\n"

    enhanced += "SPECIFIC DETECTION CRITERIA:\n"
    for criterion in enhancement_data['criteria']:
        enhanced += f"{criterion}\n"

    enhanced += "\nQUANTIFIABLE SIGNALS:\n"
    for signal in enhancement_data['quantifiable']:
        enhanced += f"{signal}\n"

    if 'psychological' in enhancement_data:
        enhanced += "\nPSYCHOLOGICAL MARKERS:\n"
        for marker in enhancement_data['psychological']:
            enhanced += f"{marker}\n"

    if 'social_signals' in enhancement_data:
        enhanced += "\nSOCIAL BEHAVIOR INDICATORS:\n"
        for signal in enhancement_data['social_signals']:
            enhanced += f"{signal}\n"

    if 'timing_analysis' in enhancement_data:
        enhanced += "\nTIMING ANALYSIS:\n"
        for timing in enhancement_data['timing_analysis']:
            enhanced += f"{timing}\n"

    if 'violations' in enhancement_data:
        enhanced += "\nRISK VIOLATIONS:\n"
        for violation in enhancement_data['violations']:
            enhanced += f"{violation}\n"

    if 'consequences' in enhancement_data:
        enhanced += "\nPERFORMANCE CONSEQUENCES:\n"
        for consequence in enhancement_data['consequences']:
            enhanced += f"{consequence}\n"

    enhanced += "\nCALCULATE IMPACT: Measure performance, risk metrics, and behavioral consistency across different periods"

    # Write enhanced content
    with open(file_path, 'w') as f:
        f.write(enhanced)

    print(f"✅ Enhanced: {file_path.name}")

def main():
    """Enhance all templates in the directory."""
    templates_dir = Path(__file__).parent / "prompts" / "trading_pattern_templates"

    if not templates_dir.exists():
        print(f"❌ Directory not found: {templates_dir}")
        return

    # Process templates we have enhancements for
    for template_name, enhancement in ENHANCEMENTS.items():
        template_file = templates_dir / f"{template_name}.txt"
        enhance_template(template_file, enhancement)

    print(f"\n🎉 Enhanced {len(ENHANCEMENTS)} templates!")
    print("Note: Some templates were already enhanced manually and are not included in this batch.")

if __name__ == "__main__":
    main()