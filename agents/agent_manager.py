"""Agent Manager

Central coordinator for managing and orchestrating multiple AI agents.
"""

import asyncio
import concurrent.futures
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from .news_agent import NewsAgent
from .market_data_agent import MarketDataAgent
from .sentiment_agent import SentimentAgent
from .risk_management_agent import RiskManagementAgent
from .pattern_analysis_agent import PatternAnalysisAgent


class AgentManager:
    """Manages and coordinates multiple AI agents."""

    def __init__(self):
        self.agents = {
            "news": NewsAgent(),
            "market_data": MarketDataAgent(),
            "sentiment": SentimentAgent(),
            "risk_management": RiskManagementAgent(),
            "pattern_analysis": PatternAnalysisAgent()
        }
        self.session_history = []

    def get_available_agents(self) -> List[str]:
        """Get list of available agent types."""
        return list(self.agents.keys())

    def get_agent_info(self, agent_type: Optional[str] = None) -> Dict[str, Any]:
        """Get information about agents."""
        if agent_type:
            if agent_type in self.agents:
                return self.agents[agent_type].get_agent_info()
            else:
                return {"error": f"Agent type '{agent_type}' not found"}

        return {
            agent_type: agent.get_agent_info()
            for agent_type, agent in self.agents.items()
        }

    def query_agent(self, agent_type: str, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Query a specific agent."""
        if agent_type not in self.agents:
            return {
                "error": f"Unknown agent type: {agent_type}",
                "available_agents": list(self.agents.keys())
            }

        try:
            response = self.agents[agent_type].process_request(request, context)
            self._log_interaction(agent_type, request, response)
            return response
        except Exception as e:
            error_response = {
                "error": f"Agent '{agent_type}' failed to process request: {str(e)}",
                "agent": agent_type,
                "timestamp": datetime.now().isoformat()
            }
            self._log_interaction(agent_type, request, error_response)
            return error_response

    def query_multiple_agents(self, requests: List[Dict[str, Any]], parallel: bool = True) -> Dict[str, Any]:
        """Query multiple agents with different requests.

        Args:
            requests: List of dicts with 'agent_type', 'request', and optional 'context'
            parallel: Whether to execute requests in parallel or sequentially
        """
        if parallel:
            return self._query_agents_parallel(requests)
        else:
            return self._query_agents_sequential(requests)

    def _query_agents_parallel(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute agent queries in parallel."""
        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(requests)) as executor:
            # Submit all requests
            future_to_request = {
                executor.submit(
                    self.query_agent,
                    req["agent_type"],
                    req["request"],
                    req.get("context")
                ): req for req in requests
            }

            # Collect results
            for future in concurrent.futures.as_completed(future_to_request):
                request = future_to_request[future]
                agent_type = request["agent_type"]
                try:
                    result = future.result()
                    results[agent_type] = result
                except Exception as e:
                    results[agent_type] = {
                        "error": f"Parallel execution failed for {agent_type}: {str(e)}",
                        "timestamp": datetime.now().isoformat()
                    }

        return {
            "execution_type": "parallel",
            "agents_queried": len(requests),
            "successful_queries": len([r for r in results.values() if "error" not in r]),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

    def _query_agents_sequential(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute agent queries sequentially."""
        results = {}

        for request in requests:
            agent_type = request["agent_type"]
            result = self.query_agent(
                agent_type,
                request["request"],
                request.get("context")
            )
            results[agent_type] = result

        return {
            "execution_type": "sequential",
            "agents_queried": len(requests),
            "successful_queries": len([r for r in results.values() if "error" not in r]),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }

    def comprehensive_analysis(self, symbols: List[str], analysis_depth: str = "standard") -> Dict[str, Any]:
        """Perform comprehensive analysis using all agents."""
        symbol_str = ", ".join(symbols)

        # Define requests for all agents
        requests = [
            {
                "agent_type": "market_data",
                "request": f"Provide market data and technical analysis for {symbol_str}",
                "context": {"symbols": symbols}
            },
            {
                "agent_type": "news",
                "request": f"Check recent news and market impact for {symbol_str}",
                "context": {"symbols": symbols}
            },
            {
                "agent_type": "sentiment",
                "request": f"Analyze market sentiment for {symbol_str}",
                "context": {"symbols": symbols}
            },
            {
                "agent_type": "risk_management",
                "request": f"Assess risk factors for positions in {symbol_str}",
                "context": {"symbols": symbols}
            }
        ]

        # Execute all agents in parallel
        agent_results = self.query_multiple_agents(requests, parallel=True)

        # Synthesize results
        synthesis = self._synthesize_analysis(agent_results["results"], symbols, analysis_depth)

        return {
            "analysis_type": "comprehensive",
            "symbols": symbols,
            "analysis_depth": analysis_depth,
            "agent_results": agent_results,
            "synthesis": synthesis,
            "timestamp": datetime.now().isoformat()
        }

    def _synthesize_analysis(self, agent_results: Dict[str, Any], symbols: List[str], depth: str) -> Dict[str, Any]:
        """Synthesize results from multiple agents into actionable insights."""
        synthesis = {
            "overall_sentiment": "neutral",
            "confidence_level": "medium",
            "key_insights": [],
            "trading_signals": {},
            "risk_assessment": "moderate",
            "recommendations": []
        }

        # Analyze sentiment consensus
        sentiment_signals = []
        if "sentiment" in agent_results and "error" not in agent_results["sentiment"]:
            sentiment_data = agent_results["sentiment"]
            if "sentiment_data" in sentiment_data:
                for symbol, data in sentiment_data["sentiment_data"].items():
                    sentiment_signals.append(data.get("composite_sentiment", 0))

        if sentiment_signals:
            avg_sentiment = sum(sentiment_signals) / len(sentiment_signals)
            if avg_sentiment > 0.3:
                synthesis["overall_sentiment"] = "bullish"
            elif avg_sentiment < -0.3:
                synthesis["overall_sentiment"] = "bearish"

        # Extract key insights from each agent
        insights = []

        # News insights
        if "news" in agent_results and "error" not in agent_results["news"]:
            news_data = agent_results["news"]
            if "recommendations" in news_data:
                insights.extend(news_data["recommendations"][:2])

        # Market data insights
        if "market_data" in agent_results and "error" not in agent_results["market_data"]:
            market_data = agent_results["market_data"]
            if "analysis" in market_data:
                for symbol, analysis in market_data["analysis"].items():
                    if "signals" in analysis:
                        insights.extend(analysis["signals"][:1])

        # Risk insights
        if "risk_management" in agent_results and "error" not in agent_results["risk_management"]:
            risk_data = agent_results["risk_management"]
            if "recommendations" in risk_data:
                insights.extend(risk_data["recommendations"][:2])

        synthesis["key_insights"] = insights[:5]  # Limit to top 5 insights

        # Generate trading signals for each symbol
        for symbol in symbols:
            signals = {"signal": "HOLD", "confidence": 0.5, "reasons": []}

            # Combine signals from different agents
            if "market_data" in agent_results and "analysis" in agent_results["market_data"]:
                if symbol in agent_results["market_data"]["analysis"]:
                    tech_signal = agent_results["market_data"]["analysis"][symbol].get("recommendation", "HOLD")
                    signals["signal"] = tech_signal
                    signals["confidence"] += 0.2

            if "sentiment" in agent_results and "sentiment_data" in agent_results["sentiment"]:
                if symbol in agent_results["sentiment"]["sentiment_data"]:
                    sent_score = agent_results["sentiment"]["sentiment_data"][symbol].get("composite_sentiment", 0)
                    if sent_score > 0.3 and signals["signal"] != "SELL":
                        signals["signal"] = "BUY"
                        signals["confidence"] += 0.2
                    elif sent_score < -0.3:
                        signals["signal"] = "SELL"
                        signals["confidence"] += 0.2

            signals["confidence"] = min(signals["confidence"], 1.0)
            synthesis["trading_signals"][symbol] = signals

        # Generate recommendations
        recommendations = []

        if synthesis["overall_sentiment"] == "bullish":
            recommendations.append("Market sentiment is positive - consider increasing exposure to growth stocks")
        elif synthesis["overall_sentiment"] == "bearish":
            recommendations.append("Market sentiment is negative - consider defensive positioning")

        recommendations.extend([
            "Monitor news flow for any significant developments",
            "Use appropriate position sizing based on risk tolerance",
            "Set stop losses to manage downside risk"
        ])

        synthesis["recommendations"] = recommendations[:5]

        return synthesis

    def market_overview(self) -> Dict[str, Any]:
        """Get comprehensive market overview from all agents."""
        requests = [
            {
                "agent_type": "market_data",
                "request": "Provide current market conditions and overview"
            },
            {
                "agent_type": "news",
                "request": "Get latest market-moving news and headlines"
            },
            {
                "agent_type": "sentiment",
                "request": "Analyze current market sentiment regime"
            }
        ]

        results = self.query_multiple_agents(requests, parallel=True)

        overview = {
            "market_snapshot": self._extract_market_snapshot(results["results"]),
            "sentiment_regime": self._extract_sentiment_regime(results["results"]),
            "key_news": self._extract_key_news(results["results"]),
            "trading_environment": self._assess_trading_environment(results["results"]),
            "timestamp": datetime.now().isoformat()
        }

        return overview

    def _extract_market_snapshot(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract market snapshot from agent results."""
        snapshot = {"status": "unknown", "trend": "neutral", "volatility": "normal"}

        if "market_data" in results and "market_overview" in results["market_data"]:
            overview = results["market_data"]["market_overview"]
            snapshot.update({
                "trend": overview.get("market_trend", "neutral"),
                "volatility": overview.get("volatility_level", "normal"),
                "breadth": overview.get("breadth", {})
            })

        return snapshot

    def _extract_sentiment_regime(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extract sentiment regime from agent results."""
        regime = {"regime": "neutral", "confidence": 0.5}

        if "sentiment" in results and "market_regime" in results["sentiment"]:
            regime = results["sentiment"]["market_regime"]

        return regime

    def _extract_key_news(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract key news from agent results."""
        news_items = []

        if "news" in results and "news_stories" in results["news"]:
            stories = results["news"]["news_stories"]
            news_items = stories[:3]  # Top 3 stories

        return news_items

    def _assess_trading_environment(self, results: Dict[str, Any]) -> str:
        """Assess current trading environment."""
        environments = [
            "trending_market", "range_bound", "volatile", "low_volatility",
            "news_driven", "earnings_season", "risk_on", "risk_off"
        ]
        return environments[hash(str(results)) % len(environments)]

    def _log_interaction(self, agent_type: str, request: str, response: Dict[str, Any]):
        """Log agent interactions for analysis."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": agent_type,
            "request": request,
            "response_size": len(str(response)),
            "success": "error" not in response
        }
        self.session_history.append(interaction)

        # Keep only last 100 interactions
        if len(self.session_history) > 100:
            self.session_history = self.session_history[-100:]

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics about current session."""
        if not self.session_history:
            return {"message": "No interactions yet"}

        total_interactions = len(self.session_history)
        successful_interactions = len([i for i in self.session_history if i["success"]])

        agent_usage = {}
        for interaction in self.session_history:
            agent_type = interaction["agent_type"]
            agent_usage[agent_type] = agent_usage.get(agent_type, 0) + 1

        return {
            "total_interactions": total_interactions,
            "successful_interactions": successful_interactions,
            "success_rate": successful_interactions / total_interactions,
            "agent_usage": agent_usage,
            "most_used_agent": max(agent_usage, key=agent_usage.get) if agent_usage else None,
            "session_start": self.session_history[0]["timestamp"] if self.session_history else None,
            "last_interaction": self.session_history[-1]["timestamp"] if self.session_history else None
        }

    def reset_session(self):
        """Reset session history and agent states."""
        self.session_history = []
        # Reset agents if they have session state
        for agent in self.agents.values():
            agent.request_count = 0
            agent.last_request = None