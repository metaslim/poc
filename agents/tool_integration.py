"""AI Agent Tool Integration

This module converts AI agents into tools that can be used by the main prompt agent.
The main agent can dynamically call specific agents based on analysis needs.
"""

import json
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from .agent_manager import AgentManager


class AgentToolRegistry:
    """Registry of AI agent tools for use by the main prompt agent."""

    def __init__(self):
        self.agent_manager = AgentManager()
        self.tools = self._register_tools()

    def _register_tools(self) -> Dict[str, Dict[str, Any]]:
        """Register AI agents as tools with descriptions and schemas."""
        return {
            "check_market_news": {
                "description": "Get latest market news and headlines that could affect trading decisions",
                "parameters": {
                    "query": {"type": "string", "description": "Specific news query or 'latest' for general news"},
                    "focus": {"type": "string", "description": "Optional focus area like 'tech', 'fed', 'earnings'"}
                },
                "function": self._check_market_news,
                "agent_type": "news"
            },
            "get_market_data": {
                "description": "Retrieve current market data, prices, and technical indicators",
                "parameters": {
                    "symbols": {"type": "array", "description": "List of symbols to analyze (e.g., ['AAPL', 'SPY'])"},
                    "analysis_type": {"type": "string", "description": "Type of analysis: 'prices', 'technical', 'overview'"}
                },
                "function": self._get_market_data,
                "agent_type": "market_data"
            },
            "analyze_market_sentiment": {
                "description": "Analyze market sentiment from social media, options flow, and institutional data",
                "parameters": {
                    "symbols": {"type": "array", "description": "Symbols to analyze sentiment for"},
                    "sentiment_type": {"type": "string", "description": "'social', 'options', 'institutional', or 'comprehensive'"}
                },
                "function": self._analyze_market_sentiment,
                "agent_type": "sentiment"
            },
            "assess_portfolio_risk": {
                "description": "Analyze portfolio risk, position sizing, and risk management recommendations",
                "parameters": {
                    "analysis_focus": {"type": "string", "description": "'portfolio', 'position_sizing', 'var', 'correlation'"},
                    "portfolio_data": {"type": "object", "description": "Optional portfolio positions data"}
                },
                "function": self._assess_portfolio_risk,
                "agent_type": "risk_management"
            },
            "detect_trading_patterns": {
                "description": "Analyze trading behavior for psychological patterns and anti-patterns",
                "parameters": {
                    "analysis_type": {"type": "string", "description": "'comprehensive', 'behavioral', 'specific'"},
                    "pattern_focus": {"type": "string", "description": "Specific pattern name or 'all'"},
                    "trading_data": {"type": "string", "description": "Trading history or behavior data"}
                },
                "function": self._detect_trading_patterns,
                "agent_type": "pattern_analysis"
            },
            "get_comprehensive_analysis": {
                "description": "Run comprehensive analysis using multiple agents in parallel",
                "parameters": {
                    "symbols": {"type": "array", "description": "Symbols to analyze comprehensively"},
                    "include_agents": {"type": "array", "description": "Agents to include: ['news', 'sentiment', 'market_data', 'risk']"}
                },
                "function": self._get_comprehensive_analysis,
                "agent_type": "multiple"
            },
            "check_market_conditions": {
                "description": "Get overall market conditions and trading environment assessment",
                "parameters": {},
                "function": self._check_market_conditions,
                "agent_type": "multiple"
            }
        }

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools.keys())

    def get_tool_description(self, tool_name: str) -> Dict[str, Any]:
        """Get detailed description and schema for a tool."""
        if tool_name not in self.tools:
            return {"error": f"Tool '{tool_name}' not found"}

        tool = self.tools[tool_name]
        return {
            "name": tool_name,
            "description": tool["description"],
            "parameters": tool["parameters"],
            "agent_type": tool["agent_type"]
        }

    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a specific tool with parameters."""
        if tool_name not in self.tools:
            return {
                "error": f"Tool '{tool_name}' not found",
                "available_tools": self.get_available_tools()
            }

        try:
            tool = self.tools[tool_name]
            result = tool["function"](**kwargs)

            return {
                "tool_name": tool_name,
                "agent_type": tool["agent_type"],
                "success": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            return {
                "tool_name": tool_name,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _check_market_news(self, query: str = "latest", focus: Optional[str] = None) -> Dict[str, Any]:
        """Tool implementation for checking market news."""
        request = f"Get {query} market news"
        if focus:
            request += f" focusing on {focus}"

        return self.agent_manager.query_agent("news", request)

    def _get_market_data(self, symbols: List[str], analysis_type: str = "prices") -> Dict[str, Any]:
        """Tool implementation for getting market data."""
        symbols_str = ", ".join(symbols)

        if analysis_type == "technical":
            request = f"Provide technical analysis for {symbols_str}"
        elif analysis_type == "overview":
            request = f"Provide market overview and conditions for {symbols_str}"
        else:
            request = f"Get current prices and quotes for {symbols_str}"

        return self.agent_manager.query_agent("market_data", request)

    def _analyze_market_sentiment(self, symbols: List[str], sentiment_type: str = "comprehensive") -> Dict[str, Any]:
        """Tool implementation for sentiment analysis."""
        symbols_str = ", ".join(symbols)

        if sentiment_type == "social":
            request = f"Analyze social media sentiment for {symbols_str}"
        elif sentiment_type == "options":
            request = f"Analyze options flow sentiment for {symbols_str}"
        elif sentiment_type == "institutional":
            request = f"Analyze institutional sentiment for {symbols_str}"
        else:
            request = f"Provide comprehensive sentiment analysis for {symbols_str}"

        return self.agent_manager.query_agent("sentiment", request)

    def _assess_portfolio_risk(self, analysis_focus: str = "portfolio", portfolio_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Tool implementation for risk assessment."""
        if analysis_focus == "position_sizing":
            request = "Calculate optimal position sizing recommendations"
        elif analysis_focus == "var":
            request = "Calculate Value at Risk and risk metrics"
        elif analysis_focus == "correlation":
            request = "Analyze portfolio correlation risks"
        else:
            request = "Provide comprehensive portfolio risk assessment"

        context = {"portfolio": portfolio_data} if portfolio_data else None
        return self.agent_manager.query_agent("risk_management", request, context)

    def _detect_trading_patterns(self, analysis_type: str = "comprehensive",
                                pattern_focus: str = "all",
                                trading_data: Optional[str] = None) -> Dict[str, Any]:
        """Tool implementation for pattern detection."""
        if analysis_type == "behavioral":
            request = "Analyze behavioral psychology patterns"
        elif analysis_type == "specific" and pattern_focus != "all":
            request = f"Analyze for {pattern_focus} pattern specifically"
        else:
            request = "Perform comprehensive trading pattern analysis"

        context = {"trading_data": trading_data} if trading_data else None
        return self.agent_manager.query_agent("pattern_analysis", request, context)

    def _get_comprehensive_analysis(self, symbols: List[str],
                                   include_agents: Optional[List[str]] = None) -> Dict[str, Any]:
        """Tool implementation for comprehensive analysis."""
        if not include_agents:
            include_agents = ["news", "market_data", "sentiment", "risk_management"]

        return self.agent_manager.comprehensive_analysis(symbols)

    def _check_market_conditions(self) -> Dict[str, Any]:
        """Tool implementation for market conditions check."""
        return self.agent_manager.market_overview()

    def generate_tool_prompt(self) -> str:
        """Generate a prompt describing available tools for the main agent."""
        prompt = "You have access to the following AI agent tools to help with trading analysis:\n\n"

        for tool_name, tool_info in self.tools.items():
            prompt += f"🔧 {tool_name}:\n"
            prompt += f"   Description: {tool_info['description']}\n"
            prompt += f"   Parameters: {json.dumps(tool_info['parameters'], indent=6)}\n"
            prompt += f"   Agent: {tool_info['agent_type']}\n\n"

        prompt += "Call these tools when you need specific analysis or data to answer user queries.\n"
        prompt += "Use the call_tool() method with the tool name and appropriate parameters."

        return prompt

    def get_tool_usage_stats(self) -> Dict[str, Any]:
        """Get statistics about tool usage."""
        return self.agent_manager.get_session_stats()


class SmartTradingAgent:
    """Main trading agent that uses AI agent tools intelligently."""

    def __init__(self, api_key: Optional[str] = None):
        self.tool_registry = AgentToolRegistry()
        self.api_key = api_key
        self.conversation_history = []

    def analyze_request(self, user_request: str) -> Dict[str, Any]:
        """Analyze user request and determine which tools to use."""
        request_lower = user_request.lower()

        # Determine which tools are needed based on request content
        tools_needed = []

        if any(word in request_lower for word in ["news", "headlines", "announcement", "event"]):
            tools_needed.append("check_market_news")

        if any(word in request_lower for word in ["price", "quote", "technical", "chart", "market data"]):
            tools_needed.append("get_market_data")

        if any(word in request_lower for word in ["sentiment", "social", "buzz", "options flow"]):
            tools_needed.append("analyze_market_sentiment")

        if any(word in request_lower for word in ["risk", "portfolio", "position size", "var", "correlation"]):
            tools_needed.append("assess_portfolio_risk")

        if any(word in request_lower for word in ["pattern", "behavior", "psychology", "bias", "fomo"]):
            tools_needed.append("detect_trading_patterns")

        if any(word in request_lower for word in ["comprehensive", "complete", "full analysis"]):
            tools_needed.append("get_comprehensive_analysis")

        if any(word in request_lower for word in ["market condition", "overview", "environment"]):
            tools_needed.append("check_market_conditions")

        # If no specific tools identified, default to market conditions
        if not tools_needed:
            tools_needed.append("check_market_conditions")

        return {
            "request": user_request,
            "tools_identified": tools_needed,
            "analysis": f"Identified {len(tools_needed)} relevant tools based on request content"
        }

    def execute_analysis(self, user_request: str, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute analysis by calling appropriate tools."""
        if not symbols:
            symbols = self._extract_symbols_from_request(user_request)

        request_analysis = self.analyze_request(user_request)
        tools_needed = request_analysis["tools_identified"]

        results = {}

        for tool_name in tools_needed:
            if tool_name == "check_market_news":
                results[tool_name] = self.tool_registry.call_tool(tool_name, query="latest")

            elif tool_name == "get_market_data":
                results[tool_name] = self.tool_registry.call_tool(tool_name, symbols=symbols, analysis_type="technical")

            elif tool_name == "analyze_market_sentiment":
                results[tool_name] = self.tool_registry.call_tool(tool_name, symbols=symbols, sentiment_type="comprehensive")

            elif tool_name == "assess_portfolio_risk":
                results[tool_name] = self.tool_registry.call_tool(tool_name, analysis_focus="portfolio")

            elif tool_name == "detect_trading_patterns":
                results[tool_name] = self.tool_registry.call_tool(tool_name, analysis_type="comprehensive")

            elif tool_name == "get_comprehensive_analysis":
                results[tool_name] = self.tool_registry.call_tool(tool_name, symbols=symbols)

            elif tool_name == "check_market_conditions":
                results[tool_name] = self.tool_registry.call_tool(tool_name)

        return {
            "user_request": user_request,
            "symbols_analyzed": symbols,
            "tools_used": tools_needed,
            "tool_results": results,
            "timestamp": datetime.now().isoformat(),
            "summary": self._generate_analysis_summary(results)
        }

    def _extract_symbols_from_request(self, request: str) -> List[str]:
        """Extract stock symbols from user request."""
        # Use the agent manager's first available agent for symbol extraction
        if hasattr(self.tool_registry.agent_manager, 'agents'):
            first_agent = next(iter(self.tool_registry.agent_manager.agents.values()))
            return first_agent.extract_symbols_from_request(request)

        # Fallback implementation
        request_upper = request.upper()
        common_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META", "AMZN", "SPY", "QQQ", "IWM"]
        found_symbols = [symbol for symbol in common_symbols if symbol in request_upper]

        if not found_symbols:
            return ["SPY", "QQQ", "AAPL"]  # Default symbols

        return found_symbols[:5]  # Limit to 5 symbols

    def _generate_analysis_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of analysis results."""
        summary = {
            "tools_executed": len(results),
            "successful_tools": len([r for r in results.values() if r.get("success", False)]),
            "key_insights": [],
            "recommendations": [],
            "overall_sentiment": "neutral"
        }

        # Extract key insights from tool results
        for tool_name, tool_result in results.items():
            if not tool_result.get("success", False):
                continue

            result_data = tool_result.get("result", {})

            if tool_name == "check_market_news":
                if "recommendations" in result_data:
                    summary["recommendations"].extend(result_data["recommendations"][:2])

            elif tool_name == "analyze_market_sentiment":
                if "sentiment_data" in result_data:
                    # Extract overall sentiment
                    sentiments = []
                    for symbol_data in result_data["sentiment_data"].values():
                        sentiments.append(symbol_data.get("composite_sentiment", 0))
                    if sentiments:
                        avg_sentiment = sum(sentiments) / len(sentiments)
                        if avg_sentiment > 0.2:
                            summary["overall_sentiment"] = "bullish"
                        elif avg_sentiment < -0.2:
                            summary["overall_sentiment"] = "bearish"

            elif tool_name == "detect_trading_patterns":
                if "detected_patterns" in result_data:
                    patterns = result_data["detected_patterns"]
                    critical_patterns = [p for p in patterns if p.get("severity") == "critical"]
                    if critical_patterns:
                        summary["key_insights"].append(f"{len(critical_patterns)} critical trading patterns detected")

        return summary

    def interactive_query(self, user_request: str) -> str:
        """Process user query and return formatted response."""
        analysis = self.execute_analysis(user_request)

        response = f"🤖 Analysis for: {user_request}\n"
        response += f"{'='*50}\n\n"

        # Show tools used
        response += f"🔧 Tools Used: {', '.join(analysis['tools_used'])}\n"
        response += f"📊 Symbols Analyzed: {', '.join(analysis['symbols_analyzed'])}\n\n"

        # Show summary
        summary = analysis["summary"]
        response += f"📈 Overall Sentiment: {summary['overall_sentiment'].upper()}\n"

        if summary["key_insights"]:
            response += f"\n🔑 Key Insights:\n"
            for insight in summary["key_insights"]:
                response += f"  • {insight}\n"

        if summary["recommendations"]:
            response += f"\n💡 Recommendations:\n"
            for rec in summary["recommendations"][:3]:
                response += f"  • {rec}\n"

        response += f"\n✅ Analysis completed using {summary['tools_executed']} agent tools"

        # Store in conversation history
        self.conversation_history.append({
            "request": user_request,
            "response": analysis,
            "timestamp": datetime.now().isoformat()
        })

        return response