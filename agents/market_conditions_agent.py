"""Market Conditions Agent

WHEN TO USE THIS AGENT:
- User asks about "market conditions", "market environment", "trading conditions"
- User wants to know "how's the market today?", "what's the market like now?"
- Need overall market assessment before making trading decisions
- User asks about volatility levels, market trends, or trading environment
- Questions about market sentiment, liquidity, or general market health
- User wants to understand if it's a good time to trade

WHAT THIS AGENT DOES:
- Assesses overall market conditions using major indices (SPY, QQQ, IWM, DIA)
- Analyzes market volatility levels (low/medium/high)
- Determines trend direction (bullish/bearish/sideways)
- Evaluates trading environment (liquidity, volatility, trend strength)
- Synthesizes news sentiment and market data into overall assessment
- Provides trading recommendations based on current conditions

MARKET METRICS ANALYZED:
- Major index movements and trends
- Volatility regime (VIX-like analysis)
- Market sentiment from news and social media
- Liquidity conditions
- Trend strength and direction
- Key market factors and catalysts

OUTPUT INCLUDES:
- Overall market condition (bullish/bearish/neutral)
- Volatility level assessment
- Trend direction and strength
- Key market factors driving conditions
- Trading environment characteristics
- Specific trading recommendations

EXAMPLE USE CASES:
- "How are market conditions today?" → full market assessment
- "Is it a good time to trade?" → trading environment analysis
- "What's the market volatility like?" → volatility regime analysis
- "Should I be cautious in this market?" → risk assessment of conditions
- "Market overview before I start trading" → comprehensive conditions check

WHEN NOT TO USE:
- User asks about specific stocks (use market_data agent)
- User wants news only (use news agent)
- User wants technical analysis of particular symbols (use market_data agent)

Specialized agent for assessing overall market conditions and trading environment.
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from .agent_manager import AgentManager


class MarketConditionsAgent(BaseAgent):
    """Agent specialized in assessing overall market conditions."""

    def __init__(self):
        super().__init__("MarketConditions", "market_conditions")
        self.agent_manager = AgentManager()

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process market conditions assessment requests."""
        self.simulate_processing_delay(0.8, 2.0)

        result = self.assess_market_conditions()

        self.log_request(request, result)
        return result

    def assess_market_conditions(self) -> Dict[str, Any]:
        """Assess current market conditions using multiple data sources.

        This method provides a comprehensive assessment of market conditions by analyzing
        major indices, volatility, sentiment, and news to determine the overall trading environment.

        Returns:
            Dict containing:
                - success: bool indicating if assessment was successful
                - overall_condition: str ("bullish", "bearish", "neutral")
                - volatility_level: str ("low", "medium", "high")
                - trend_direction: str ("bullish", "bearish", "sideways")
                - market_sentiment: str ("positive", "negative", "neutral")
                - key_factors: List[str] major factors affecting the market
                - trading_environment: Dict with liquidity, volatility, trend_strength
                - recommendations: List[str] specific trading recommendations
                - market_data: Dict with technical analysis of major indices
                - news_sentiment: Dict with latest news analysis
                - sentiment_analysis: Dict with market sentiment data

        Analysis Process:
            1. Analyzes major indices (SPY, QQQ, IWM, DIA) for technical signals
            2. Gathers latest market news and sentiment
            3. Evaluates institutional and retail sentiment
            4. Synthesizes all data into actionable market assessment
            5. Provides specific trading recommendations

        Example Usage:
            conditions = agent.assess_market_conditions()
            if conditions['volatility_level'] == 'high':
                # Adjust position sizes
            if conditions['overall_condition'] == 'bullish':
                # Consider long positions
        """
        try:
            # Major market indices to analyze
            major_indices = ["SPY", "QQQ", "IWM", "DIA"]

            conditions = {
                "success": True,
                "timestamp": self.created_at.isoformat(),
                "market_indices": major_indices,
                "overall_condition": "neutral",
                "volatility_level": "medium",
                "trend_direction": "sideways",
                "market_sentiment": "neutral",
                "key_factors": [],
                "trading_environment": {},
                "recommendations": []
            }

            # Get market data for major indices
            market_data = self._get_market_data_overview(major_indices)
            conditions["market_data"] = market_data

            # Get news sentiment
            news_sentiment = self._get_news_sentiment()
            conditions["news_sentiment"] = news_sentiment

            # Get overall sentiment
            sentiment_data = self._get_market_sentiment(major_indices)
            conditions["sentiment_analysis"] = sentiment_data

            # Synthesize overall conditions
            conditions.update(self._synthesize_market_conditions(
                market_data, news_sentiment, sentiment_data
            ))

            return conditions

        except Exception as e:
            return {
                "success": False,
                "error": f"Error assessing market conditions: {str(e)}"
            }

    def _get_market_data_overview(self, symbols: List[str]) -> Dict[str, Any]:
        """Get market data overview for major indices."""
        try:
            query = f"Market overview and technical analysis for {', '.join(symbols)}"
            result = self.agent_manager.query_agent("market_data", query)

            if result.get("success"):
                return result.get("result", {})
            else:
                return {"error": "Market data unavailable"}

        except Exception as e:
            return {"error": f"Market data error: {str(e)}"}

    def _get_news_sentiment(self) -> Dict[str, Any]:
        """Get overall market news sentiment."""
        try:
            query = "Latest market news and overall market sentiment"
            result = self.agent_manager.query_agent("news", query)

            if result.get("success"):
                return result.get("result", {})
            else:
                return {"error": "News data unavailable"}

        except Exception as e:
            return {"error": f"News sentiment error: {str(e)}"}

    def _get_market_sentiment(self, symbols: List[str]) -> Dict[str, Any]:
        """Get market sentiment for major indices."""
        try:
            query = f"Market sentiment analysis for {', '.join(symbols)}"
            result = self.agent_manager.query_agent("sentiment", query)

            if result.get("success"):
                return result.get("result", {})
            else:
                return {"error": "Sentiment data unavailable"}

        except Exception as e:
            return {"error": f"Sentiment analysis error: {str(e)}"}

    def _synthesize_market_conditions(self, market_data: Dict[str, Any],
                                     news_sentiment: Dict[str, Any],
                                     sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize overall market conditions from multiple data sources."""
        synthesis = {
            "overall_condition": "neutral",
            "volatility_level": "medium",
            "trend_direction": "sideways",
            "market_sentiment": "neutral",
            "key_factors": [],
            "trading_environment": {
                "liquidity": "normal",
                "volatility": "medium",
                "trend_strength": "weak"
            },
            "recommendations": []
        }

        # Analyze market data
        if "error" not in market_data:
            if "volatility_analysis" in market_data:
                vol_analysis = market_data["volatility_analysis"]
                if "high volatility" in str(vol_analysis).lower():
                    synthesis["volatility_level"] = "high"
                    synthesis["trading_environment"]["volatility"] = "high"
                    synthesis["key_factors"].append("High market volatility detected")
                elif "low volatility" in str(vol_analysis).lower():
                    synthesis["volatility_level"] = "low"
                    synthesis["trading_environment"]["volatility"] = "low"

            if "trend_analysis" in market_data:
                trend_analysis = market_data["trend_analysis"]
                if "bullish" in str(trend_analysis).lower():
                    synthesis["trend_direction"] = "bullish"
                    synthesis["trading_environment"]["trend_strength"] = "strong"
                elif "bearish" in str(trend_analysis).lower():
                    synthesis["trend_direction"] = "bearish"
                    synthesis["trading_environment"]["trend_strength"] = "strong"

        # Analyze news sentiment
        if "error" not in news_sentiment:
            if "sentiment_score" in news_sentiment:
                score = news_sentiment.get("sentiment_score", 0)
                if score > 0.2:
                    synthesis["market_sentiment"] = "positive"
                elif score < -0.2:
                    synthesis["market_sentiment"] = "negative"

            if "headlines" in news_sentiment:
                headlines = news_sentiment["headlines"]
                if isinstance(headlines, list) and len(headlines) > 0:
                    synthesis["key_factors"].append(f"Key news: {headlines[0][:80]}...")

        # Analyze sentiment data
        if "error" not in sentiment_data:
            if "sentiment_data" in sentiment_data:
                sentiments = []
                for symbol, data in sentiment_data["sentiment_data"].items():
                    sentiment_score = data.get("composite_sentiment", 0)
                    sentiments.append(sentiment_score)

                if sentiments:
                    avg_sentiment = sum(sentiments) / len(sentiments)
                    if avg_sentiment > 0.3:
                        synthesis["overall_condition"] = "bullish"
                        synthesis["recommendations"].append("Market showing bullish sentiment")
                    elif avg_sentiment < -0.3:
                        synthesis["overall_condition"] = "bearish"
                        synthesis["recommendations"].append("Market showing bearish sentiment")

        # Generate trading recommendations
        if synthesis["volatility_level"] == "high":
            synthesis["recommendations"].append("Use smaller position sizes due to high volatility")
        if synthesis["trend_direction"] == "bullish":
            synthesis["recommendations"].append("Consider long positions in trending markets")
        elif synthesis["trend_direction"] == "bearish":
            synthesis["recommendations"].append("Consider defensive positioning")

        if not synthesis["recommendations"]:
            synthesis["recommendations"].append("Monitor for clearer directional signals")

        return synthesis

    def get_sector_conditions(self, sectors: Optional[List[str]] = None) -> Dict[str, Any]:
        """Get conditions for specific market sectors."""
        if not sectors:
            sectors = ["XLF", "XLK", "XLE", "XLV", "XLI"]  # Financial, Tech, Energy, Healthcare, Industrial

        return {
            "success": True,
            "sectors": sectors,
            "analysis": "Sector-specific analysis would require specialized data",
            "note": "This would typically connect to sector-specific data sources"
        }

    def check_volatility_regime(self) -> Dict[str, Any]:
        """Check current market volatility regime."""
        return {
            "success": True,
            "volatility_regime": "medium",
            "vix_level": "simulated_data",
            "regime_analysis": "Based on recent market movements and VIX levels",
            "trading_implications": [
                "Moderate position sizing appropriate",
                "Standard stop-loss levels applicable",
                "Options strategies feasible"
            ]
        }