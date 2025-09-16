"""News Checking Agent

Agent specialized in fetching and analyzing news that might affect trading decisions.
"""

import random
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent


class NewsAgent(BaseAgent):
    """Agent for checking market-relevant news."""

    def __init__(self):
        super().__init__("NewsBot", "news_analysis")
        self.fake_news_stories = [
            {
                "headline": "Fed Signals Rate Cut by Year-End Amid Economic Cooling",
                "source": "Financial Times",
                "impact": "bullish",
                "confidence": 0.85,
                "timestamp": datetime.now() - timedelta(hours=2),
                "summary": "Federal Reserve officials indicate potential rate cuts as inflation shows signs of cooling."
            },
            {
                "headline": "Tech Giants Report Strong Q3 Earnings Beat Expectations",
                "source": "Reuters",
                "impact": "bullish",
                "confidence": 0.92,
                "timestamp": datetime.now() - timedelta(hours=4),
                "summary": "Major tech companies including Apple, Microsoft, and Google exceed analyst expectations."
            },
            {
                "headline": "Oil Prices Surge on OPEC+ Production Cut Announcement",
                "source": "Bloomberg",
                "impact": "mixed",
                "confidence": 0.78,
                "timestamp": datetime.now() - timedelta(hours=6),
                "summary": "OPEC+ announces unexpected production cuts, sending oil prices higher but raising recession fears."
            },
            {
                "headline": "China Manufacturing PMI Falls Below 50, Signals Contraction",
                "source": "Wall Street Journal",
                "impact": "bearish",
                "confidence": 0.88,
                "timestamp": datetime.now() - timedelta(hours=8),
                "summary": "Chinese manufacturing activity contracts for third consecutive month, raising global growth concerns."
            },
            {
                "headline": "Breakthrough in AI Chips Announced by Major Semiconductor Firm",
                "source": "TechCrunch",
                "impact": "bullish",
                "confidence": 0.72,
                "timestamp": datetime.now() - timedelta(hours=12),
                "summary": "Revolutionary AI processor promises 50% efficiency improvement, sparking sector rally."
            },
            {
                "headline": "European Central Bank Holds Rates Steady, Dovish on Future Policy",
                "source": "Financial Times",
                "impact": "neutral",
                "confidence": 0.65,
                "timestamp": datetime.now() - timedelta(hours=16),
                "summary": "ECB maintains current rate levels but signals openness to cuts if economic data weakens."
            }
        ]

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process news request and return relevant stories."""
        self.simulate_processing_delay(1.0, 3.0)

        # Parse request for specific topics or sectors
        request_lower = request.lower()
        relevant_stories = self._filter_stories_by_request(request_lower)

        # Context can be used for symbol-specific news filtering in future versions
        _ = context  # Acknowledge parameter for future use

        # Generate market impact analysis
        market_sentiment = self._calculate_market_sentiment(relevant_stories)

        response = {
            "agent": self.agent_name,
            "type": "news_analysis",
            "timestamp": datetime.now().isoformat(),
            "stories_found": len(relevant_stories),
            "market_sentiment": market_sentiment,
            "news_stories": relevant_stories,
            "recommendations": self._generate_news_based_recommendations(relevant_stories, market_sentiment)
        }

        self.log_request(request, response)
        return response

    def _filter_stories_by_request(self, request: str) -> List[Dict[str, Any]]:
        """Filter news stories based on request keywords."""
        if "tech" in request or "technology" in request:
            return [story for story in self.fake_news_stories if "tech" in story["headline"].lower() or "ai" in story["headline"].lower()]
        elif "fed" in request or "rate" in request or "interest" in request:
            return [story for story in self.fake_news_stories if "fed" in story["headline"].lower() or "rate" in story["headline"].lower()]
        elif "oil" in request or "energy" in request:
            return [story for story in self.fake_news_stories if "oil" in story["headline"].lower() or "opec" in story["headline"].lower()]
        elif "china" in request or "manufacturing" in request:
            return [story for story in self.fake_news_stories if "china" in story["headline"].lower() or "manufacturing" in story["headline"].lower()]
        else:
            # Return random selection of 3-5 stories
            num_stories = random.randint(3, 5)
            return random.sample(self.fake_news_stories, min(num_stories, len(self.fake_news_stories)))

    def _calculate_market_sentiment(self, stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall market sentiment from news stories."""
        if not stories:
            return {"overall": "neutral", "confidence": 0.5, "bullish_count": 0, "bearish_count": 0, "neutral_count": 0}

        bullish_count = len([s for s in stories if s["impact"] == "bullish"])
        bearish_count = len([s for s in stories if s["impact"] == "bearish"])
        neutral_count = len([s for s in stories if s["impact"] == "neutral" or s["impact"] == "mixed"])

        total_confidence = sum(s["confidence"] for s in stories) / len(stories)

        if bullish_count > bearish_count:
            overall = "bullish"
        elif bearish_count > bullish_count:
            overall = "bearish"
        else:
            overall = "neutral"

        return {
            "overall": overall,
            "confidence": round(total_confidence, 2),
            "bullish_count": bullish_count,
            "bearish_count": bearish_count,
            "neutral_count": neutral_count
        }

    def _generate_news_based_recommendations(self, stories: List[Dict[str, Any]], sentiment: Dict[str, Any]) -> List[str]:
        """Generate trading recommendations based on news analysis."""
        recommendations = []

        if sentiment["overall"] == "bullish" and sentiment["confidence"] > 0.7:
            recommendations.extend([
                "Consider increasing long positions in growth sectors",
                "Monitor for continuation patterns in bullish trending stocks",
                "Be cautious of overbought conditions in momentum plays"
            ])
        elif sentiment["overall"] == "bearish" and sentiment["confidence"] > 0.7:
            recommendations.extend([
                "Consider defensive positions or hedging strategies",
                "Look for short opportunities in weak sectors",
                "Focus on quality dividend stocks for stability"
            ])
        else:
            recommendations.extend([
                "Mixed signals suggest range-bound trading",
                "Focus on individual stock analysis over broad market plays",
                "Wait for clearer directional signals before major position changes"
            ])

        # Add specific recommendations based on stories
        for story in stories:
            if "fed" in story["headline"].lower() and "rate" in story["headline"].lower():
                if story["impact"] == "bullish":
                    recommendations.append("Rate cut expectations favor growth stocks and REITs")
                else:
                    recommendations.append("Rising rate expectations favor financial sector")
            elif "tech" in story["headline"].lower():
                recommendations.append("Monitor semiconductor and AI-related stocks for momentum")

        return recommendations[:5]  # Limit to 5 recommendations

    def get_latest_headlines(self, count: int = 5) -> List[Dict[str, Any]]:
        """Get latest headlines without full analysis."""
        self.simulate_processing_delay(0.3, 0.8)

        sorted_stories = sorted(self.fake_news_stories, key=lambda x: x["timestamp"], reverse=True)
        return sorted_stories[:count]

    def search_news_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Search for news stories by specific topic."""
        self.simulate_processing_delay(0.5, 1.5)

        topic_lower = topic.lower()
        matching_stories = []

        for story in self.fake_news_stories:
            if (topic_lower in story["headline"].lower() or
                topic_lower in story["summary"].lower()):
                matching_stories.append(story)

        return matching_stories