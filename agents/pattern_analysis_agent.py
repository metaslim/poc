"""Trading Psychology Pattern Analysis Agent

Agent specialized in analyzing trading data for psychological anti-patterns
using the trading pattern templates from the prompts directory.
"""

import os
import random
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent


class PatternAnalysisAgent(BaseAgent):
    """Agent for analyzing trading psychology patterns and anti-patterns."""

    def __init__(self):
        super().__init__("PatternBot", "pattern_analysis")
        self.pattern_templates = self._load_pattern_templates()

    def _load_pattern_templates(self) -> Dict[str, str]:
        """Load trading pattern templates from prompts directory."""
        templates = {}
        templates_dir = Path(__file__).parent.parent / "prompts" / "trading_pattern_templates"

        if not templates_dir.exists():
            return {}

        for template_file in templates_dir.glob("*.txt"):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    # Extract the prompt part after "Prompt: "
                    if content.startswith("Prompt: "):
                        content = content[8:]  # Remove "Prompt: " prefix
                    templates[template_file.stem] = content
            except Exception as e:
                print(f"Warning: Could not load template {template_file}: {e}")

        return templates

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process pattern analysis request."""
        self.simulate_processing_delay(2.0, 4.0)

        trading_data = context.get("trading_data") if context else None
        user_profile = context.get("user_profile") if context else None

        if "specific" in request.lower() and "pattern" in request.lower():
            # Analyze for specific patterns mentioned in request
            response_data = self._analyze_specific_patterns(request, trading_data, user_profile)
        elif "all" in request.lower() or "comprehensive" in request.lower():
            # Comprehensive analysis using all patterns
            response_data = self._comprehensive_pattern_analysis(trading_data, user_profile)
        elif "behavioral" in request.lower() or "psychology" in request.lower():
            # Focus on behavioral patterns
            response_data = self._behavioral_pattern_analysis(trading_data, user_profile)
        else:
            # Default pattern screening
            response_data = self._pattern_screening(trading_data, user_profile)

        response_data.update({
            "agent": self.agent_name,
            "type": "pattern_analysis",
            "timestamp": datetime.now().isoformat(),
            "templates_used": len(self.pattern_templates)
        })

        self.log_request(request, response_data)
        return response_data

    def _analyze_specific_patterns(self, request: str, trading_data: Optional[str], user_profile: Optional[Dict]) -> Dict[str, Any]:
        """Analyze for specific patterns mentioned in the request."""
        request_lower = request.lower()
        relevant_patterns = {}

        # Match request to available patterns
        for pattern_name, pattern_desc in self.pattern_templates.items():
            if pattern_name.replace('_', ' ') in request_lower or any(keyword in request_lower for keyword in pattern_name.split('_')):
                relevant_patterns[pattern_name] = pattern_desc

        if not relevant_patterns:
            # Fallback to general patterns
            sample_patterns = dict(random.sample(list(self.pattern_templates.items()), min(5, len(self.pattern_templates))))
            relevant_patterns = sample_patterns

        detected_patterns = self._simulate_pattern_detection(relevant_patterns, trading_data, user_profile)

        return {
            "analysis_type": "specific_pattern_analysis",
            "patterns_searched": list(relevant_patterns.keys()),
            "detected_patterns": detected_patterns,
            "pattern_summary": self._generate_pattern_summary(detected_patterns),
            "recommendations": self._generate_pattern_recommendations(detected_patterns)
        }

    def _comprehensive_pattern_analysis(self, trading_data: Optional[str], user_profile: Optional[Dict]) -> Dict[str, Any]:
        """Comprehensive analysis using all available patterns."""
        detected_patterns = self._simulate_pattern_detection(self.pattern_templates, trading_data, user_profile)

        # Group patterns by severity
        severity_groups = {
            "critical": [],
            "warning": [],
            "minor": []
        }

        for pattern in detected_patterns:
            severity = pattern.get("severity", "minor")
            severity_groups[severity].append(pattern)

        return {
            "analysis_type": "comprehensive_analysis",
            "total_patterns_analyzed": len(self.pattern_templates),
            "patterns_detected": len(detected_patterns),
            "severity_breakdown": {k: len(v) for k, v in severity_groups.items()},
            "detected_patterns": detected_patterns,
            "pattern_clusters": self._identify_pattern_clusters(detected_patterns),
            "risk_score": self._calculate_behavioral_risk_score(detected_patterns),
            "improvement_priorities": self._prioritize_improvements(detected_patterns),
            "detailed_recommendations": self._generate_detailed_recommendations(detected_patterns)
        }

    def _behavioral_pattern_analysis(self, trading_data: Optional[str], user_profile: Optional[Dict]) -> Dict[str, Any]:
        """Focus on behavioral and psychological patterns."""
        behavioral_patterns = {
            k: v for k, v in self.pattern_templates.items()
            if any(keyword in k for keyword in ['bias', 'emotional', 'fomo', 'revenge', 'overconfidence', 'herd'])
        }

        detected_patterns = self._simulate_pattern_detection(behavioral_patterns, trading_data, user_profile)

        return {
            "analysis_type": "behavioral_analysis",
            "psychological_profile": self._generate_psychological_profile(detected_patterns),
            "emotional_triggers": self._identify_emotional_triggers(detected_patterns),
            "cognitive_biases": self._identify_cognitive_biases(detected_patterns),
            "behavioral_recommendations": self._generate_behavioral_recommendations(detected_patterns),
            "mindfulness_suggestions": self._generate_mindfulness_suggestions(detected_patterns)
        }

    def _pattern_screening(self, trading_data: Optional[str], user_profile: Optional[Dict]) -> Dict[str, Any]:
        """Quick screening for common patterns."""
        # Focus on most common and impactful patterns
        common_patterns = {
            k: v for k, v in self.pattern_templates.items()
            if k in ['fomo', 'emotional_trading', 'averaging_down', 'chasing_losses', 'ignoring_risk_management']
        }

        detected_patterns = self._simulate_pattern_detection(common_patterns, trading_data, user_profile)

        return {
            "analysis_type": "pattern_screening",
            "screening_focus": "common_high_impact_patterns",
            "detected_patterns": detected_patterns,
            "quick_alerts": self._generate_quick_alerts(detected_patterns),
            "immediate_actions": self._suggest_immediate_actions(detected_patterns)
        }

    def _simulate_pattern_detection(self, patterns: Dict[str, str], trading_data: Optional[str], user_profile: Optional[Dict]) -> List[Dict[str, Any]]:
        """Simulate pattern detection with realistic fake results."""
        detected = []

        for pattern_name, pattern_desc in patterns.items():
            # Simulate pattern detection probability based on pattern type
            detection_prob = self._get_detection_probability(pattern_name)

            if random.random() < detection_prob:
                pattern_result = {
                    "pattern_name": pattern_name,
                    "pattern_description": pattern_desc,
                    "detected": True,
                    "confidence": round(random.uniform(0.6, 0.95), 2),
                    "severity": random.choice(["critical", "warning", "minor"]),
                    "frequency": random.choice(["rare", "occasional", "frequent", "very_frequent"]),
                    "evidence": self._generate_pattern_evidence(pattern_name),
                    "impact_metrics": self._generate_impact_metrics(pattern_name),
                    "root_causes": self._identify_root_causes(pattern_name),
                    "correction_strategies": self._suggest_correction_strategies(pattern_name)
                }
                detected.append(pattern_result)

        return detected

    def _get_detection_probability(self, pattern_name: str) -> float:
        """Get detection probability based on pattern commonality."""
        common_patterns = {
            'fomo': 0.7,
            'emotional_trading': 0.8,
            'confirmation_bias': 0.6,
            'averaging_down': 0.5,
            'chasing_losses': 0.4,
            'ignoring_risk_management': 0.6,
            'anchoring_bias': 0.3,
            'overtrading': 0.5,
            'revenge_trading': 0.3
        }
        return common_patterns.get(pattern_name, 0.2)

    def _generate_pattern_evidence(self, pattern_name: str) -> List[str]:
        """Generate realistic evidence for detected patterns."""
        evidence_map = {
            'fomo': [
                "Multiple trades executed during high volatility periods",
                "Position sizes increased during market rallies",
                "Trades clustered around earnings announcements",
                "Social media mentions correlation with trade timing"
            ],
            'emotional_trading': [
                "Large position adjustments after minor price moves",
                "Inconsistent position sizing patterns",
                "Trading activity spikes during market stress",
                "Deviation from planned entry/exit points"
            ],
            'averaging_down': [
                "Multiple purchases of same security at declining prices",
                "Position size increases correlated with losses",
                "Cost basis deterioration over time",
                "Lack of stop-loss execution"
            ],
            'chasing_losses': [
                "Increased trading frequency after losing streaks",
                "Position sizes grow following losses",
                "Sector rotation after poor performance",
                "Shortened holding periods during drawdowns"
            ],
            'confirmation_bias': [
                "Selective news consumption during positions",
                "Ignored negative analyst reports",
                "Echo chamber social media engagement",
                "Dismissed contrary technical signals"
            ]
        }

        base_evidence = evidence_map.get(pattern_name, [
            "Pattern detected through behavioral analysis",
            "Statistical deviation from optimal trading patterns",
            "Correlation with known psychological biases"
        ])

        # Return 2-4 evidence points
        return random.sample(base_evidence, min(random.randint(2, 4), len(base_evidence)))

    def _generate_impact_metrics(self, pattern_name: str) -> Dict[str, Any]:
        """Generate impact metrics for detected patterns."""
        impact_metrics = {
            "performance_impact": f"{random.uniform(-15, -5):.1f}%",
            "frequency_impact": f"{random.randint(5, 25)} trades affected",
            "risk_increase": f"{random.uniform(10, 40):.0f}%",
            "opportunity_cost": f"${random.randint(500, 5000)}",
            "drawdown_contribution": f"{random.uniform(2, 8):.1f}%"
        }

        return impact_metrics

    def _identify_root_causes(self, pattern_name: str) -> List[str]:
        """Identify root causes for specific patterns."""
        root_causes_map = {
            'fomo': ["Fear of missing profits", "Social media influence", "Market FOMO psychology", "Lack of patience"],
            'emotional_trading': ["Stress response to losses", "Lack of trading plan", "Overattachment to positions", "Market anxiety"],
            'averaging_down': ["Denial of being wrong", "Hope for reversal", "Insufficient risk management", "Anchoring to entry price"],
            'chasing_losses': ["Loss aversion bias", "Revenge psychology", "Impatience with recovery", "Ego preservation"],
            'confirmation_bias': ["Selective attention", "Need to be right", "Information filtering", "Cognitive dissonance"]
        }

        return root_causes_map.get(pattern_name, ["Psychological bias", "Lack of systematic approach", "Emotional decision making"])

    def _suggest_correction_strategies(self, pattern_name: str) -> List[str]:
        """Suggest correction strategies for specific patterns."""
        strategies_map = {
            'fomo': [
                "Implement cooling-off period before trades",
                "Set specific entry criteria and stick to them",
                "Limit social media consumption during trading hours",
                "Practice mindfulness before executing trades"
            ],
            'emotional_trading': [
                "Develop and follow a written trading plan",
                "Use position sizing rules to limit emotional impact",
                "Implement stop-losses before entering positions",
                "Take breaks during high-stress trading periods"
            ],
            'averaging_down': [
                "Set maximum number of averaging attempts",
                "Use stop-losses to limit downside",
                "Require new fundamental analysis before averaging",
                "Implement position size limits for single securities"
            ],
            'chasing_losses': [
                "Set daily/weekly loss limits",
                "Take mandatory breaks after losing streaks",
                "Focus on risk management over profit recovery",
                "Practice acceptance of losses as part of trading"
            ],
            'confirmation_bias': [
                "Actively seek contrarian viewpoints",
                "Use devil's advocate approach in analysis",
                "Set up news feeds from diverse sources",
                "Regularly review and challenge assumptions"
            ]
        }

        return strategies_map.get(pattern_name, [
            "Implement systematic rules to override emotions",
            "Use pre-defined criteria for decisions",
            "Practice self-awareness and mindfulness",
            "Seek objective third-party perspectives"
        ])

    def _generate_pattern_summary(self, detected_patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of detected patterns."""
        if not detected_patterns:
            return {"message": "No significant patterns detected"}

        critical_patterns = [p for p in detected_patterns if p["severity"] == "critical"]
        warning_patterns = [p for p in detected_patterns if p["severity"] == "warning"]

        return {
            "total_detected": len(detected_patterns),
            "critical_issues": len(critical_patterns),
            "warning_issues": len(warning_patterns),
            "most_severe": critical_patterns[0]["pattern_name"] if critical_patterns else None,
            "average_confidence": round(sum(p["confidence"] for p in detected_patterns) / len(detected_patterns), 2),
            "dominant_theme": self._identify_dominant_theme(detected_patterns)
        }

    def _identify_dominant_theme(self, patterns: List[Dict[str, Any]]) -> str:
        """Identify the dominant psychological theme."""
        themes = {
            "emotional_control": ["emotional_trading", "revenge_trading", "panic_selling"],
            "risk_management": ["ignoring_risk_management", "overleveraging", "liquidity_ignorance"],
            "cognitive_bias": ["confirmation_bias", "anchoring_bias", "overconfidence"],
            "discipline": ["fomo", "chasing_losses", "averaging_down", "overtrading"]
        }

        theme_scores = {}
        for theme, theme_patterns in themes.items():
            score = sum(1 for p in patterns if p["pattern_name"] in theme_patterns)
            theme_scores[theme] = score

        return max(theme_scores, key=theme_scores.get) if theme_scores else "mixed"

    def _generate_pattern_recommendations(self, detected_patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on detected patterns."""
        if not detected_patterns:
            return ["Continue current trading approach", "Monitor for pattern development"]

        recommendations = []

        # Priority recommendations for critical patterns
        critical_patterns = [p for p in detected_patterns if p["severity"] == "critical"]
        for pattern in critical_patterns:
            recommendations.append(f"URGENT: Address {pattern['pattern_name'].replace('_', ' ')} immediately")

        # General recommendations
        recommendations.extend([
            "Implement systematic rules to reduce emotional decision making",
            "Regular review of trading journal to identify pattern triggers",
            "Consider position sizing adjustments to manage risk",
            "Develop mindfulness practices for trading psychology"
        ])

        return recommendations[:6]

    def _identify_pattern_clusters(self, patterns: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Identify clusters of related patterns."""
        clusters = {
            "emotional_cluster": [],
            "risk_cluster": [],
            "bias_cluster": [],
            "discipline_cluster": []
        }

        for pattern in patterns:
            name = pattern["pattern_name"]
            if any(keyword in name for keyword in ["emotional", "revenge", "panic"]):
                clusters["emotional_cluster"].append(name)
            elif any(keyword in name for keyword in ["risk", "leverage", "liquidity"]):
                clusters["risk_cluster"].append(name)
            elif any(keyword in name for keyword in ["bias", "anchoring", "confirmation"]):
                clusters["bias_cluster"].append(name)
            else:
                clusters["discipline_cluster"].append(name)

        # Remove empty clusters
        return {k: v for k, v in clusters.items() if v}

    def _calculate_behavioral_risk_score(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall behavioral risk score."""
        if not patterns:
            return {"score": 2, "level": "low", "max_score": 10}

        # Weight patterns by severity
        severity_weights = {"critical": 3, "warning": 2, "minor": 1}
        weighted_score = sum(severity_weights.get(p["severity"], 1) for p in patterns)

        # Normalize to 1-10 scale
        max_possible = len(patterns) * 3
        normalized_score = min(10, (weighted_score / max_possible) * 10)

        level = "low" if normalized_score < 4 else "moderate" if normalized_score < 7 else "high"

        return {
            "score": round(normalized_score, 1),
            "level": level,
            "max_score": 10,
            "contributing_patterns": len(patterns)
        }

    def _prioritize_improvements(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize improvement areas based on pattern analysis."""
        if not patterns:
            return []

        # Sort by severity and confidence
        sorted_patterns = sorted(patterns, key=lambda x: (
            {"critical": 3, "warning": 2, "minor": 1}.get(x["severity"], 1),
            x["confidence"]
        ), reverse=True)

        priorities = []
        for i, pattern in enumerate(sorted_patterns[:5]):
            priorities.append({
                "rank": i + 1,
                "pattern": pattern["pattern_name"],
                "priority_level": pattern["severity"],
                "expected_impact": "high" if pattern["severity"] == "critical" else "medium",
                "time_to_fix": random.choice(["1-2 weeks", "2-4 weeks", "1-2 months"]),
                "difficulty": random.choice(["easy", "moderate", "challenging"])
            })

        return priorities

    def _generate_detailed_recommendations(self, patterns: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Generate detailed recommendations by category."""
        recommendations = {
            "immediate_actions": [],
            "systematic_changes": [],
            "long_term_development": [],
            "monitoring_suggestions": []
        }

        if not patterns:
            return recommendations

        # Immediate actions for critical patterns
        critical_patterns = [p for p in patterns if p["severity"] == "critical"]
        for pattern in critical_patterns:
            recommendations["immediate_actions"].extend([
                f"Stop {pattern['pattern_name'].replace('_', ' ')} behavior immediately",
                f"Review recent trades for {pattern['pattern_name']} instances"
            ])

        # Systematic changes
        recommendations["systematic_changes"].extend([
            "Implement pre-trade checklist to verify decision criteria",
            "Set up automated alerts for position size limits",
            "Create trading rules document and review monthly",
            "Establish cooling-off periods for emotional decisions"
        ])

        # Long-term development
        recommendations["long_term_development"].extend([
            "Develop trading psychology education program",
            "Practice mindfulness and emotional regulation techniques",
            "Regular consultation with trading psychology coach",
            "Build systematic backtesting for strategy validation"
        ])

        # Monitoring suggestions
        recommendations["monitoring_suggestions"].extend([
            "Daily trading journal with emotional state tracking",
            "Weekly pattern analysis review",
            "Monthly performance attribution analysis",
            "Quarterly psychology assessment"
        ])

        return recommendations

    def _generate_psychological_profile(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate psychological trading profile."""
        if not patterns:
            return {"profile": "balanced", "strengths": [], "weaknesses": []}

        profile_types = ["analytical", "emotional", "impulsive", "conservative", "aggressive"]
        profile = random.choice(profile_types)

        strengths = random.sample([
            "Disciplined risk management",
            "Systematic approach to analysis",
            "Emotional control under pressure",
            "Patience with position development",
            "Objective decision making"
        ], 2)

        weaknesses = [p["pattern_name"].replace("_", " ") for p in patterns[:3]]

        return {
            "profile_type": profile,
            "dominant_traits": [pattern["pattern_name"] for pattern in patterns[:2]],
            "strengths": strengths,
            "weaknesses": weaknesses,
            "stress_response": random.choice(["flight", "fight", "freeze"]),
            "decision_style": random.choice(["intuitive", "analytical", "mixed"])
        }

    def _identify_emotional_triggers(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify emotional triggers from patterns."""
        triggers = [
            {"trigger": "Market volatility", "response": "Increased trading activity", "pattern": "emotional_trading"},
            {"trigger": "Losing positions", "response": "Averaging down behavior", "pattern": "averaging_down"},
            {"trigger": "Social media hype", "response": "FOMO trading", "pattern": "fomo"},
            {"trigger": "Market gaps", "response": "Panic decisions", "pattern": "panic_selling"},
            {"trigger": "Earnings announcements", "response": "Impulsive positioning", "pattern": "news_reaction_trading"}
        ]

        detected_triggers = []
        for pattern in patterns:
            for trigger in triggers:
                if pattern["pattern_name"] == trigger["pattern"]:
                    detected_triggers.append(trigger)

        return detected_triggers

    def _identify_cognitive_biases(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Identify cognitive biases from detected patterns."""
        bias_map = {
            "confirmation_bias": "Confirmation Bias",
            "anchoring_bias": "Anchoring Bias",
            "fomo": "Fear of Missing Out",
            "chasing_losses": "Loss Aversion",
            "averaging_down": "Sunk Cost Fallacy",
            "overconfidence": "Overconfidence Bias",
            "herd_mentality": "Herd Behavior"
        }

        detected_biases = []
        for pattern in patterns:
            bias = bias_map.get(pattern["pattern_name"])
            if bias and bias not in detected_biases:
                detected_biases.append(bias)

        return detected_biases

    def _generate_behavioral_recommendations(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate behavioral psychology recommendations."""
        return [
            "Implement pre-trade meditation or mindfulness practice",
            "Use systematic checklists to override emotional responses",
            "Set up accountability partner for trading decisions",
            "Practice scenario planning for various market conditions",
            "Develop personal trading rules and review them regularly"
        ]

    def _generate_mindfulness_suggestions(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate mindfulness and mental training suggestions."""
        return [
            "5-minute breathing exercise before trading sessions",
            "Body scan meditation to recognize stress signals",
            "Journaling thoughts and emotions during trades",
            "Progressive muscle relaxation for high-stress periods",
            "Visualization exercises for successful trading outcomes"
        ]

    def _generate_quick_alerts(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Generate quick alerts for screening results."""
        alerts = []
        for pattern in patterns:
            if pattern["severity"] == "critical":
                alerts.append(f"🚨 CRITICAL: {pattern['pattern_name'].replace('_', ' ').title()} detected")
            elif pattern["severity"] == "warning":
                alerts.append(f"⚠️ WARNING: {pattern['pattern_name'].replace('_', ' ').title()} behavior identified")

        return alerts

    def _suggest_immediate_actions(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Suggest immediate actions for detected patterns."""
        if not patterns:
            return ["Continue current approach"]

        actions = []
        for pattern in patterns[:3]:  # Top 3 patterns
            if pattern["severity"] == "critical":
                actions.append(f"Immediately stop {pattern['pattern_name'].replace('_', ' ')} behavior")
            else:
                actions.append(f"Monitor and reduce {pattern['pattern_name'].replace('_', ' ')} instances")

        actions.append("Review and update trading rules")
        return actions

    def get_available_patterns(self) -> Dict[str, str]:
        """Get all available pattern templates."""
        return self.pattern_templates.copy()

    def analyze_single_pattern(self, pattern_name: str, trading_data: Optional[str] = None) -> Dict[str, Any]:
        """Analyze for a single specific pattern."""
        if pattern_name not in self.pattern_templates:
            return {
                "error": f"Pattern '{pattern_name}' not found",
                "available_patterns": list(self.pattern_templates.keys())
            }

        self.simulate_processing_delay(1.0, 2.0)

        pattern_desc = self.pattern_templates[pattern_name]
        detected = random.random() < self._get_detection_probability(pattern_name)

        if detected:
            result = {
                "pattern_name": pattern_name,
                "pattern_description": pattern_desc,
                "detected": True,
                "confidence": round(random.uniform(0.7, 0.95), 2),
                "severity": random.choice(["critical", "warning", "minor"]),
                "evidence": self._generate_pattern_evidence(pattern_name),
                "impact_metrics": self._generate_impact_metrics(pattern_name),
                "correction_strategies": self._suggest_correction_strategies(pattern_name)
            }
        else:
            result = {
                "pattern_name": pattern_name,
                "pattern_description": pattern_desc,
                "detected": False,
                "message": "No significant instances of this pattern detected"
            }

        return {
            "analysis_type": "single_pattern",
            "pattern_analyzed": pattern_name,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }