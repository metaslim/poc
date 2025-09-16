#!/usr/bin/env python3
"""OpenAI Agent with AI Tool Integration

Enhanced version that allows the OpenAI agent to actually call AI agent tools
as functions during its analysis.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import AgentToolRegistry

try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI package not installed. Run: pip install openai")
    sys.exit(1)


class OpenAIWithAgentTools:
    """OpenAI agent that can call AI agent tools as functions."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.tool_registry = AgentToolRegistry()
        self.conversation_history = []

    def get_function_definitions(self) -> List[Dict[str, Any]]:
        """Generate OpenAI function definitions from agent tools."""
        functions = []

        # Define each agent tool as an OpenAI function
        functions.extend([
            {
                "type": "function",
                "function": {
                    "name": "check_market_news",
                    "description": "Get latest market news and headlines that could affect trading decisions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Specific news query or 'latest' for general news"
                            },
                            "focus": {
                                "type": "string",
                                "description": "Optional focus area like 'tech', 'fed', 'earnings'"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_market_data",
                    "description": "Retrieve current market data, prices, and technical indicators",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbols": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of symbols to analyze (e.g., ['AAPL', 'SPY'])"
                            },
                            "analysis_type": {
                                "type": "string",
                                "description": "Type of analysis: 'prices', 'technical', 'overview'",
                                "enum": ["prices", "technical", "overview"]
                            }
                        },
                        "required": ["symbols"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_market_sentiment",
                    "description": "Analyze market sentiment from social media, options flow, and institutional data",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbols": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Symbols to analyze sentiment for"
                            },
                            "sentiment_type": {
                                "type": "string",
                                "description": "Type of sentiment analysis",
                                "enum": ["social", "options", "institutional", "comprehensive"]
                            }
                        },
                        "required": ["symbols"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "assess_portfolio_risk",
                    "description": "Analyze portfolio risk, position sizing, and risk management recommendations",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "analysis_focus": {
                                "type": "string",
                                "description": "Focus of risk analysis",
                                "enum": ["portfolio", "position_sizing", "var", "correlation"]
                            }
                        },
                        "required": ["analysis_focus"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "detect_trading_patterns",
                    "description": "Analyze trading behavior for psychological patterns and anti-patterns",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "analysis_type": {
                                "type": "string",
                                "description": "Type of pattern analysis",
                                "enum": ["comprehensive", "behavioral", "specific"]
                            },
                            "pattern_focus": {
                                "type": "string",
                                "description": "Specific pattern name or 'all'"
                            }
                        },
                        "required": ["analysis_type"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_market_conditions",
                    "description": "Get overall market conditions and trading environment assessment",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ])

        return functions

    def call_agent_tool(self, function_name: str, arguments: Dict[str, Any]) -> str:
        """Call an agent tool and return formatted results."""
        try:
            # Map function names to tool registry calls
            if function_name == "check_market_news":
                result = self.tool_registry.call_tool("check_market_news", **arguments)
            elif function_name == "get_market_data":
                result = self.tool_registry.call_tool("get_market_data", **arguments)
            elif function_name == "analyze_market_sentiment":
                result = self.tool_registry.call_tool("analyze_market_sentiment", **arguments)
            elif function_name == "assess_portfolio_risk":
                result = self.tool_registry.call_tool("assess_portfolio_risk", **arguments)
            elif function_name == "detect_trading_patterns":
                result = self.tool_registry.call_tool("detect_trading_patterns", **arguments)
            elif function_name == "check_market_conditions":
                result = self.tool_registry.call_tool("check_market_conditions", **arguments)
            else:
                return f"Unknown function: {function_name}"

            if result.get("success", False):
                # Format the result for OpenAI
                agent_result = result["result"]
                return self._format_agent_result(function_name, agent_result)
            else:
                return f"Error calling {function_name}: {result.get('error', 'Unknown error')}"

        except Exception as e:
            return f"Error executing {function_name}: {str(e)}"

    def _format_agent_result(self, function_name: str, result: Dict[str, Any]) -> str:
        """Format agent results for OpenAI consumption."""
        formatted = f"🤖 {function_name.replace('_', ' ').title()} Results:\n"

        if function_name == "check_market_news":
            if "news_stories" in result:
                formatted += f"Market Sentiment: {result.get('market_sentiment', {}).get('overall', 'neutral')}\n"
                formatted += f"Stories Found: {len(result['news_stories'])}\n"
                for story in result["news_stories"][:3]:
                    formatted += f"• {story['headline']} ({story['impact']}, {story['confidence']:.0%} confidence)\n"
            if "recommendations" in result:
                formatted += "Recommendations:\n"
                for rec in result["recommendations"][:3]:
                    formatted += f"• {rec}\n"

        elif function_name == "get_market_data":
            if "quotes" in result:
                formatted += "Market Data:\n"
                for symbol, data in list(result["quotes"].items())[:5]:
                    formatted += f"• {symbol}: ${data['current_price']:.2f} ({data['change_percent']:+.1f}%)\n"
            if "analysis" in result:
                formatted += "Technical Analysis:\n"
                for symbol, analysis in list(result["analysis"].items())[:3]:
                    formatted += f"• {symbol}: {analysis.get('recommendation', 'N/A')} (RSI: {analysis.get('rsi', 'N/A')})\n"

        elif function_name == "analyze_market_sentiment":
            if "sentiment_data" in result:
                formatted += "Sentiment Analysis:\n"
                for symbol, data in list(result["sentiment_data"].items())[:3]:
                    formatted += f"• {symbol}: {data['sentiment_label']} (score: {data['composite_sentiment']:+.2f})\n"

        elif function_name == "assess_portfolio_risk":
            if "portfolio_metrics" in result:
                metrics = result["portfolio_metrics"]
                formatted += f"Portfolio Risk Metrics:\n"
                formatted += f"• Total Value: ${metrics.get('total_value', 0):,.0f}\n"
                formatted += f"• Daily VaR (95%): ${metrics.get('daily_var_95', 0):,.0f}\n"
                formatted += f"• Portfolio Beta: {metrics.get('beta', 'N/A')}\n"
                formatted += f"• Max Drawdown: {metrics.get('max_drawdown', 0):.1%}\n"

        elif function_name == "detect_trading_patterns":
            if "detected_patterns" in result:
                patterns = result["detected_patterns"]
                formatted += f"Trading Patterns Detected: {len(patterns)}\n"
                for pattern in patterns[:5]:
                    formatted += f"• {pattern['pattern_name'].replace('_', ' ').title()}: {pattern['severity']} ({pattern['confidence']:.0%})\n"

        elif function_name == "check_market_conditions":
            if "market_snapshot" in result:
                snapshot = result["market_snapshot"]
                formatted += f"Market Conditions:\n"
                formatted += f"• Trend: {snapshot.get('trend', 'unknown').upper()}\n"
                formatted += f"• Volatility: {snapshot.get('volatility', 'normal').upper()}\n"
            if "trading_environment" in result:
                formatted += f"• Environment: {result['trading_environment'].replace('_', ' ').title()}\n"

        return formatted

    def analyze_with_tools(self, user_query: str, trading_data: Optional[str] = None) -> str:
        """Analyze using OpenAI with access to agent tools."""

        system_prompt = """You are an elite trading psychology analyst and risk management expert.

You have access to specialized AI agent tools that provide real-time market data and analysis:
• check_market_news: Get latest market news and headlines
• get_market_data: Retrieve market data and technical indicators
• analyze_market_sentiment: Analyze sentiment from multiple sources
• assess_portfolio_risk: Portfolio risk analysis and recommendations
• detect_trading_patterns: Detect psychological trading patterns
• check_market_conditions: Overall market conditions assessment

Use these tools strategically to gather relevant information before providing your analysis.
Call multiple tools if needed to get a comprehensive view.
Integrate the tool results into your final analysis and recommendations.

Focus on:
1. Identifying self-destructive trading patterns
2. Providing actionable psychological insights
3. Risk management recommendations
4. Evidence-based conclusions using tool data
"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Query: {user_query}\n\nTrading Data: {trading_data or 'No specific trading data provided'}"}
        ]

        # Get function definitions
        functions = self.get_function_definitions()

        try:
            # Initial call to OpenAI
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=messages,
                tools=functions,
                tool_choice="auto",
                max_completion_tokens=2000,
                temperature=0.3
            )

            # Process the response
            result_text = ""

            while True:
                message = response.choices[0].message

                # Add assistant message to conversation
                messages.append({
                    "role": "assistant",
                    "content": message.content,
                    "tool_calls": message.tool_calls
                })

                if message.content:
                    result_text += message.content + "\n\n"

                # Check if there are tool calls to execute
                if message.tool_calls:
                    # Execute tool calls
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)

                        print(f"🔧 Calling tool: {function_name} with args: {function_args}")

                        # Execute the tool
                        tool_result = self.call_agent_tool(function_name, function_args)

                        # Add tool result to conversation
                        messages.append({
                            "role": "tool",
                            "content": tool_result,
                            "tool_call_id": tool_call.id
                        })

                    # Continue the conversation with tool results
                    response = self.client.chat.completions.create(
                        model="gpt-5",
                        messages=messages,
                        tools=functions,
                        tool_choice="auto",
                        max_completion_tokens=2000,
                        temperature=0.3
                    )
                else:
                    # No more tool calls, we're done
                    break

            return result_text.strip()

        except Exception as e:
            return f"Error in analysis with tools: {str(e)}"

    def interactive_session(self):
        """Start an interactive session."""
        print("🤖 OPENAI AGENT WITH AI TOOLS")
        print("=" * 50)
        print("This agent can call specialized AI tools during analysis.")
        print("Type 'quit' to exit.")
        print("=" * 50)

        while True:
            try:
                user_input = input("\n💬 Your trading question: ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    break

                if not user_input:
                    continue

                print(f"\n⏳ Analyzing with AI tools...")
                response = self.analyze_with_tools(user_input)

                print(f"\n📊 ANALYSIS RESULT:")
                print("-" * 30)
                print(response)

            except KeyboardInterrupt:
                print("\n\n👋 Session ended.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python openai_with_agent_tools.py <openai_api_key>")
        print("\nExample:")
        print("  python openai_with_agent_tools.py sk-your-api-key")
        sys.exit(1)

    api_key = sys.argv[1]

    agent = OpenAIWithAgentTools(api_key)

    # Test with a specific query
    if len(sys.argv) > 2:
        query = " ".join(sys.argv[2:])
        print(f"🔍 Testing query: {query}")
        result = agent.analyze_with_tools(query)
        print(f"\n📊 Result:\n{result}")
    else:
        agent.interactive_session()


if __name__ == "__main__":
    main()