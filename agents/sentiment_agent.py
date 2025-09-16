"""Sentiment Analysis Agent

Agent specialized in analyzing market sentiment from various sources including
social media, options flow, and institutional positioning.
"""

import random
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent


class SentimentAgent(BaseAgent):
    """Agent for market sentiment analysis."""

    def __init__(self):
        super().__init__("SentimentBot", "sentiment_analysis")
        self.sentiment_sources = [
            "Twitter/X", "Reddit", "StockTwits", "Discord", "Telegram",
            "Options Flow", "Dark Pool Activity", "Institutional Flow"
        ]

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process sentiment analysis request."""
        self.simulate_processing_delay(1.0, 2.5)

        request_lower = request.lower()
        symbols = self.extract_symbols_from_request(request)

        # Context can be used for additional sentiment sources in future versions
        _ = context  # Acknowledge parameter for future use

        if "options" in request_lower or "flow" in request_lower:
            response_data = self._analyze_options_sentiment(symbols)
        elif "social" in request_lower or "reddit" in request_lower or "twitter" in request_lower:
            response_data = self._analyze_social_sentiment(symbols)
        elif "institutional" in request_lower or "smart money" in request_lower:
            response_data = self._analyze_institutional_sentiment(symbols)
        else:
            response_data = self._analyze_overall_sentiment(symbols)

        response_data.update({
            "agent": self.agent_name,
            "type": "sentiment_analysis",
            "timestamp": datetime.now().isoformat(),
            "symbols_analyzed": symbols
        })

        self.log_request(request, response_data)
        return response_data


    def _analyze_options_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze options flow sentiment."""
        options_data = {}

        for symbol in symbols:
            put_call_ratio = round(random.uniform(0.5, 1.8), 2)
            gamma_exposure = random.randint(-500000000, 500000000)

            # Determine sentiment based on put/call ratio
            if put_call_ratio > 1.2:
                sentiment = "bearish"
                confidence = 0.75
            elif put_call_ratio < 0.8:
                sentiment = "bullish"
                confidence = 0.75
            else:
                sentiment = "neutral"
                confidence = 0.6

            options_data[symbol] = {
                "put_call_ratio": put_call_ratio,
                "sentiment": sentiment,
                "confidence": confidence,
                "gamma_exposure": gamma_exposure,
                "dark_pool_sentiment": random.choice(["bullish", "bearish", "neutral"]),
                "unusual_activity": random.choice([True, False]),
                "volume_vs_oi": round(random.uniform(0.1, 3.0), 2),
                "skew": round(random.uniform(-0.3, 0.3), 3)
            }

        return {
            "analysis_type": "options_sentiment",
            "options_data": options_data,
            "market_wide_metrics": {
                "vix_put_call": round(random.uniform(0.8, 1.4), 2),
                "skew_index": round(random.uniform(120, 140), 2),
                "term_structure": random.choice(["backwardation", "contango", "flat"])
            },
            "key_insights": self._generate_options_insights(options_data)
        }

    def _analyze_social_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze social media sentiment."""
        social_data = {}

        for symbol in symbols:
            # Generate fake social metrics
            mentions = random.randint(500, 15000)
            sentiment_score = round(random.uniform(-1.0, 1.0), 2)
            engagement_rate = round(random.uniform(0.02, 0.12), 3)

            social_data[symbol] = {
                "total_mentions": mentions,
                "sentiment_score": sentiment_score,
                "engagement_rate": engagement_rate,
                "trending_rank": random.randint(1, 50) if random.random() > 0.7 else None,
                "influencer_mentions": random.randint(0, 5),
                "reddit_wsb_mentions": random.randint(0, 100),
                "twitter_volume": random.randint(100, 5000),
                "sentiment_change_24h": round(random.uniform(-0.5, 0.5), 2)
            }

        return {
            "analysis_type": "social_sentiment",
            "social_data": social_data,
            "trending_topics": [
                "Fed Rate Cuts", "AI Revolution", "Meme Stock Revival",
                "Crypto Correlation", "Earnings Season"
            ][:random.randint(2, 4)],
            "sentiment_drivers": self._generate_sentiment_drivers(),
            "key_insights": self._generate_social_insights(social_data)
        }

    def _analyze_institutional_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        """Analyze institutional sentiment indicators."""
        institutional_data = {}

        for symbol in symbols:
            institutional_data[symbol] = {
                "13f_flow": random.choice(["buying", "selling", "neutral"]),
                "insider_activity": random.choice(["buying", "selling", "neutral"]),
                "hedge_fund_positioning": round(random.uniform(-2.0, 2.0), 2),
                "etf_flows": random.randint(-1000000, 1000000),
                "short_interest": round(random.uniform(2.0, 25.0), 1),
                "institutional_ownership": round(random.uniform(40.0, 85.0), 1),
                "smart_money_confidence": round(random.uniform(0.3, 0.9), 2)
            }

        return {
            "analysis_type": "institutional_sentiment",
            "institutional_data": institutional_data,
            "market_positioning": {
                "risk_parity_funds": random.choice(["risk-on", "risk-off", "neutral"]),
                "cta_positioning": round(random.uniform(-1.5, 1.5), 2),
                "pension_fund_allocation": "increasing equity exposure" if random.random() > 0.5 else "reducing equity exposure"
            },
            "key_insights": self._generate_institutional_insights(institutional_data)
        }

    def _analyze_overall_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        """Comprehensive sentiment analysis combining all sources."""
        overall_data = {}

        for symbol in symbols:
            # Combine multiple sentiment indicators
            social_score = round(random.uniform(-1.0, 1.0), 2)
            options_score = round(random.uniform(-1.0, 1.0), 2)
            institutional_score = round(random.uniform(-1.0, 1.0), 2)

            # Weighted average
            composite_score = round((social_score * 0.3 + options_score * 0.4 + institutional_score * 0.3), 2)

            overall_data[symbol] = {
                "composite_sentiment": composite_score,
                "social_sentiment": social_score,
                "options_sentiment": options_score,
                "institutional_sentiment": institutional_score,
                "sentiment_label": self._score_to_label(composite_score),
                "conviction_level": self._calculate_conviction(social_score, options_score, institutional_score),
                "momentum": random.choice(["accelerating", "decelerating", "stable"]),
                "contrarian_signal": abs(composite_score) > 0.7  # Extreme sentiment as contrarian
            }

        return {
            "analysis_type": "comprehensive_sentiment",
            "sentiment_data": overall_data,
            "market_regime": self._determine_market_regime(),
            "sentiment_extremes": self._identify_sentiment_extremes(overall_data),
            "actionable_insights": self._generate_actionable_insights(overall_data)
        }

    def _score_to_label(self, score: float) -> str:
        """Convert numeric sentiment score to label."""
        if score >= 0.3:
            return "bullish"
        elif score <= -0.3:
            return "bearish"
        else:
            return "neutral"

    def _calculate_conviction(self, social: float, options: float, institutional: float) -> str:
        """Calculate conviction level based on alignment of sentiment sources."""
        scores = [social, options, institutional]
        alignment = len([s for s in scores if s > 0.2]) == 3 or len([s for s in scores if s < -0.2]) == 3

        if alignment:
            return "high"
        elif abs(max(scores) - min(scores)) < 0.5:
            return "moderate"
        else:
            return "low"

    def _generate_options_insights(self, options_data: Dict[str, Any]) -> List[str]:
        """Generate insights from options data."""
        insights = []

        for symbol, data in options_data.items():
            if data["put_call_ratio"] > 1.5:
                insights.append(f"{symbol}: Extremely high put/call ratio indicates fear or hedging activity")
            elif data["put_call_ratio"] < 0.6:
                insights.append(f"{symbol}: Low put/call ratio suggests excessive bullishness - potential reversal signal")

            if data["unusual_activity"]:
                insights.append(f"{symbol}: Unusual options activity detected - smart money potentially positioning")

            if abs(data["gamma_exposure"]) > 300000000:
                insights.append(f"{symbol}: High gamma exposure may cause increased volatility around key levels")

        return insights

    def _generate_social_insights(self, social_data: Dict[str, Any]) -> List[str]:
        """Generate insights from social sentiment data."""
        insights = []

        for symbol, data in social_data.items():
            if data["sentiment_score"] > 0.7:
                insights.append(f"{symbol}: Extremely positive social sentiment - watch for potential exhaustion")
            elif data["sentiment_score"] < -0.7:
                insights.append(f"{symbol}: Very negative social sentiment - potential contrarian opportunity")

            if data["total_mentions"] > 10000:
                insights.append(f"{symbol}: High social media buzz - increased retail interest")

            if data["trending_rank"] and data["trending_rank"] <= 10:
                insights.append(f"{symbol}: Trending in top 10 - momentum play potential")

        return insights

    def _generate_institutional_insights(self, institutional_data: Dict[str, Any]) -> List[str]:
        """Generate insights from institutional data."""
        insights = []

        for symbol, data in institutional_data.items():
            if data["smart_money_confidence"] > 0.8:
                insights.append(f"{symbol}: High institutional confidence - strong fundamental support")
            elif data["smart_money_confidence"] < 0.4:
                insights.append(f"{symbol}: Low institutional confidence - potential headwinds")

            if data["short_interest"] > 20:
                insights.append(f"{symbol}: High short interest ({data['short_interest']}%) - squeeze potential")

            if data["13f_flow"] == "buying" and data["insider_activity"] == "buying":
                insights.append(f"{symbol}: Both institutions and insiders buying - strong bullish signal")

        return insights

    def _generate_sentiment_drivers(self) -> List[str]:
        """Generate current sentiment drivers."""
        return random.sample([
            "Fed policy expectations",
            "AI/Technology hype",
            "Earnings season results",
            "Geopolitical tensions",
            "Inflation concerns",
            "Consumer spending data",
            "Energy price volatility",
            "China reopening optimism",
            "Banking sector stress",
            "Cryptocurrency correlation"
        ], random.randint(3, 6))

    def _determine_market_regime(self) -> Dict[str, Any]:
        """Determine current market sentiment regime."""
        regimes = ["Risk-On", "Risk-Off", "Rotation", "Uncertainty", "Euphoria", "Panic"]
        current_regime = random.choice(regimes)

        return {
            "regime": current_regime,
            "confidence": round(random.uniform(0.6, 0.9), 2),
            "duration": f"{random.randint(5, 30)} days",
            "characteristics": self._get_regime_characteristics(current_regime)
        }

    def _get_regime_characteristics(self, regime: str) -> List[str]:
        """Get characteristics of sentiment regime."""
        characteristics_map = {
            "Risk-On": ["Growth outperforming", "High beta names leading", "Low VIX"],
            "Risk-Off": ["Defensive sectors leading", "High VIX", "Flight to quality"],
            "Rotation": ["Sector rotation active", "Mixed signals", "Stock picking environment"],
            "Uncertainty": ["High volatility", "News-driven moves", "Range-bound action"],
            "Euphoria": ["FOMO driving", "Speculative excess", "Complacency indicators high"],
            "Panic": ["Indiscriminate selling", "Margin calls", "Oversold conditions"]
        }
        return characteristics_map.get(regime, ["Mixed characteristics"])

    def _identify_sentiment_extremes(self, sentiment_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Identify sentiment extremes that might signal reversals."""
        extremely_bullish = []
        extremely_bearish = []

        for symbol, data in sentiment_data.items():
            if data["composite_sentiment"] >= 0.7:
                extremely_bullish.append(symbol)
            elif data["composite_sentiment"] <= -0.7:
                extremely_bearish.append(symbol)

        return {
            "extremely_bullish": extremely_bullish,
            "extremely_bearish": extremely_bearish,
            "contrarian_candidates": extremely_bullish + extremely_bearish
        }

    def _generate_actionable_insights(self, sentiment_data: Dict[str, Any]) -> List[str]:
        """Generate actionable trading insights from sentiment analysis."""
        insights = []

        for symbol, data in sentiment_data.items():
            if data["contrarian_signal"]:
                insights.append(f"{symbol}: Extreme sentiment detected - consider contrarian positioning")

            if data["conviction_level"] == "high":
                if data["composite_sentiment"] > 0:
                    insights.append(f"{symbol}: High conviction bullish sentiment - momentum play candidate")
                else:
                    insights.append(f"{symbol}: High conviction bearish sentiment - avoid or short candidate")

            if data["momentum"] == "accelerating" and abs(data["composite_sentiment"]) > 0.3:
                insights.append(f"{symbol}: Sentiment momentum accelerating - trend likely to continue")

        # Add general market insights
        bullish_count = sum(1 for data in sentiment_data.values() if data["composite_sentiment"] > 0.2)
        bearish_count = sum(1 for data in sentiment_data.values() if data["composite_sentiment"] < -0.2)

        if bullish_count > bearish_count * 2:
            insights.append("Market sentiment broadly bullish - potential for momentum continuation")
        elif bearish_count > bullish_count * 2:
            insights.append("Market sentiment broadly bearish - defensive positioning warranted")

        return insights