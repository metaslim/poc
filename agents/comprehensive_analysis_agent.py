"""Comprehensive Analysis Agent

WHEN TO USE THIS AGENT:
- User asks for "comprehensive analysis", "complete analysis", "full analysis"
- User wants analysis from multiple perspectives (news + sentiment + technical + risk)
- User asks "analyze everything about AAPL" or "give me the full picture on these stocks"
- Need to coordinate multiple specialized agents for thorough analysis
- User wants a consolidated view combining different analysis types

WHAT THIS AGENT DOES:
- Orchestrates multiple specialized agents (news, market_data, sentiment, risk_management, pattern_analysis)
- Runs analyses in parallel for efficiency
- Synthesizes results into unified insights and recommendations
- Provides overall sentiment assessment and confidence ratings
- Generates actionable recommendations based on all analysis inputs

AGENTS THIS COORDINATES:
- news: Latest market news and events
- market_data: Technical analysis and price data
- sentiment: Social media, options flow, institutional sentiment
- risk_management: Portfolio risk and position sizing
- pattern_analysis: Trading psychology and behavioral patterns

ANALYSIS OUTPUT:
- Individual results from each agent
- Synthesized overall sentiment (bullish/bearish/neutral)
- Key insights extracted from all sources
- Consolidated recommendations
- Confidence level based on analysis success rate

EXAMPLE USE CASES:
- "Give me comprehensive analysis on AAPL and TSLA" → runs all agents on both symbols
- "Analyze the tech sector completely" → full analysis on tech ETFs/stocks
- "I need the full picture before trading SPY" → complete market analysis
- "Comprehensive analysis focusing on news and sentiment" → runs selected agents

WHEN NOT TO USE:
- User only wants specific type of analysis (use specialized agents instead)
- User asks for quick/simple information (use individual tools)
- Single-focus requests (news only, prices only, etc.)

Agent that coordinates multiple specialized agents to provide complete market analysis.
"""

from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from .agent_manager import AgentManager


class ComprehensiveAnalysisAgent(BaseAgent):
    """Agent that orchestrates comprehensive analysis using multiple specialized agents."""

    def __init__(self):
        super().__init__("ComprehensiveAnalysis", "comprehensive")
        self.agent_manager = AgentManager()

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process comprehensive analysis requests."""
        self.simulate_processing_delay(1.0, 3.0)

        # Extract symbols from request
        symbols = self.extract_symbols_from_request(request)

        # Determine which agents to include
        include_agents = self._determine_agents_from_request(request, context)

        result = self.run_comprehensive_analysis(symbols, include_agents)

        self.log_request(request, result)
        return result

    def run_comprehensive_analysis(self, symbols: List[str],
                                  include_agents: Optional[List[str]] = None) -> Dict[str, Any]:
        """Run comprehensive analysis using multiple specialized agents.

        This method orchestrates multiple AI agents to provide a complete analysis
        of the specified symbols from different perspectives (news, technical, sentiment, risk).

        Args:
            symbols (List[str]): Stock symbols to analyze (e.g., ['AAPL', 'SPY', 'TSLA'])
            include_agents (Optional[List[str]]): Specific agents to run. Options:
                - 'news': Latest market news and headlines
                - 'market_data': Technical analysis and price data
                - 'sentiment': Social media, options flow, institutional sentiment
                - 'risk_management': Portfolio risk and position sizing
                - 'pattern_analysis': Trading psychology and behavioral patterns
                Defaults to: ['news', 'market_data', 'sentiment', 'risk_management']

        Returns:
            Dict containing:
                - success: bool indicating overall success
                - symbols: List[str] symbols that were analyzed
                - agents_used: List[str] agents that were executed
                - analysis: Dict with results from each agent (keyed by agent type)
                - summary: Dict with synthesized insights including:
                  * overall_sentiment: "bullish", "bearish", or "neutral"
                  * key_insights: List[str] important findings
                  * recommendations: List[str] actionable recommendations
                  * risk_level: "low", "medium", or "high"
                  * confidence: "low", "medium", or "high" based on success rate

        Analysis Flow:
            1. Runs specified agents in parallel for efficiency
            2. Gathers results from each agent
            3. Synthesizes findings into unified insights
            4. Generates overall sentiment assessment
            5. Provides actionable recommendations

        Example Usage:
            # Full analysis on tech stocks
            result = agent.run_comprehensive_analysis(['AAPL', 'TSLA', 'NVDA'])

            # Focused analysis with specific agents
            result = agent.run_comprehensive_analysis(
                ['SPY'],
                include_agents=['news', 'sentiment']
            )
        """
        if not include_agents:
            include_agents = ["news", "market_data", "sentiment", "risk_management"]

        results = {
            "success": True,
            "symbols": symbols,
            "agents_used": include_agents,
            "analysis": {},
            "summary": {}
        }

        # Run analysis from each requested agent
        for agent_type in include_agents:
            try:
                if agent_type == "news":
                    query = f"Latest news affecting {', '.join(symbols)}"
                    analysis = self.agent_manager.query_agent("news", query)
                elif agent_type == "market_data":
                    query = f"Market data and technical analysis for {', '.join(symbols)}"
                    analysis = self.agent_manager.query_agent("market_data", query)
                elif agent_type == "sentiment":
                    query = f"Market sentiment analysis for {', '.join(symbols)}"
                    analysis = self.agent_manager.query_agent("sentiment", query)
                elif agent_type == "risk_management":
                    query = f"Risk assessment for portfolio with {', '.join(symbols)}"
                    analysis = self.agent_manager.query_agent("risk_management", query)
                elif agent_type == "pattern_analysis":
                    query = f"Trading pattern analysis for {', '.join(symbols)}"
                    analysis = self.agent_manager.query_agent("pattern_analysis", query)
                else:
                    continue

                results["analysis"][agent_type] = analysis

            except Exception as e:
                results["analysis"][agent_type] = {
                    "success": False,
                    "error": f"Error running {agent_type} analysis: {str(e)}"
                }

        # Generate comprehensive summary
        results["summary"] = self._generate_comprehensive_summary(results["analysis"])

        return results

    def _determine_agents_from_request(self, request: str,
                                      context: Optional[Dict[str, Any]] = None) -> List[str]:
        """Determine which agents to use based on request content."""
        if context and "include_agents" in context:
            return context["include_agents"]

        request_lower = request.lower()
        agents = []

        # Default comprehensive set
        default_agents = ["news", "market_data", "sentiment", "risk_management"]

        # Check for specific agent requests
        if any(word in request_lower for word in ["news", "headlines", "announcement"]):
            agents.append("news")
        if any(word in request_lower for word in ["price", "technical", "chart", "data"]):
            agents.append("market_data")
        if any(word in request_lower for word in ["sentiment", "social", "buzz"]):
            agents.append("sentiment")
        if any(word in request_lower for word in ["risk", "portfolio", "var"]):
            agents.append("risk_management")
        if any(word in request_lower for word in ["pattern", "psychology", "behavior"]):
            agents.append("pattern_analysis")

        # If no specific agents requested, use defaults
        if not agents:
            agents = default_agents

        return agents

    def _generate_comprehensive_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive summary from all analysis results."""
        summary = {
            "overall_sentiment": "neutral",
            "key_insights": [],
            "recommendations": [],
            "risk_level": "medium",
            "confidence": "medium"
        }

        successful_analyses = [r for r in analysis_results.values() if r.get("success", False)]

        if not successful_analyses:
            summary["key_insights"].append("Unable to complete comprehensive analysis")
            return summary

        # Extract insights from each analysis
        for agent_type, result in analysis_results.items():
            if not result.get("success", False):
                continue

            result_data = result.get("result", {})

            # Extract sentiment
            if agent_type == "sentiment" and "sentiment_data" in result_data:
                sentiments = []
                for symbol_data in result_data["sentiment_data"].values():
                    sentiments.append(symbol_data.get("composite_sentiment", 0))
                if sentiments:
                    avg_sentiment = sum(sentiments) / len(sentiments)
                    if avg_sentiment > 0.2:
                        summary["overall_sentiment"] = "bullish"
                    elif avg_sentiment < -0.2:
                        summary["overall_sentiment"] = "bearish"

            # Extract recommendations
            if "recommendations" in result_data:
                recommendations = result_data["recommendations"]
                if isinstance(recommendations, list):
                    summary["recommendations"].extend(recommendations[:2])

            # Extract key insights
            if "analysis" in result_data:
                summary["key_insights"].append(f"{agent_type.title()}: {result_data['analysis'][:100]}...")

        # Determine overall confidence
        success_rate = len(successful_analyses) / len(analysis_results)
        if success_rate >= 0.8:
            summary["confidence"] = "high"
        elif success_rate >= 0.6:
            summary["confidence"] = "medium"
        else:
            summary["confidence"] = "low"

        return summary

    def get_market_overview(self) -> Dict[str, Any]:
        """Get overall market conditions overview."""
        symbols = ["SPY", "QQQ", "IWM"]  # Major market indices
        return self.run_comprehensive_analysis(symbols, ["news", "market_data", "sentiment"])

    def analyze_specific_symbols(self, symbols: List[str],
                                focus_areas: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze specific symbols with optional focus areas."""
        if not focus_areas:
            focus_areas = ["market_data", "sentiment", "risk_management"]

        return self.run_comprehensive_analysis(symbols, focus_areas)