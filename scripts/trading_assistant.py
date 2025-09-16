#!/usr/bin/env python3
"""Unified Trading Assistant - All-in-One Solution

Comprehensive AI-powered trading assistant with:
- Professional anti-pattern analysis
- Interactive learning sessions
- AI tool calling with parallel execution
- Self-learning user profiles
- Market analysis and sentiment tracking
"""

import os
import sys
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import AgentToolRegistry, AgentManager

try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI package not installed. Run: pip install openai")
    sys.exit(1)

try:
    from config import config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False


class ToolCache:
    """Thread-safe cache for AI tool results with TTL."""

    def __init__(self, ttl_seconds=600):
        self._cache = {}
        self._timestamps = {}
        self._ttl = ttl_seconds
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key not in self._cache:
                return None
            if time.time() - self._timestamps[key] > self._ttl:
                del self._cache[key]
                del self._timestamps[key]
                return None
            return self._cache[key]

    def set(self, key: str, value: Any):
        with self._lock:
            self._cache[key] = value
            self._timestamps[key] = time.time()


class SmartToolSelector:
    """Intelligently selects AI tools based on query analysis."""

    TOOL_KEYWORDS = {
        'check_market_news': ['news', 'headlines', 'announcement'],
        'get_market_data': ['price', 'data', 'technical', 'chart'],
        'analyze_market_sentiment': ['sentiment', 'bullish', 'bearish'],
        'assess_portfolio_risk': ['risk', 'portfolio', 'var', 'drawdown'],
        'detect_trading_patterns': ['pattern', 'psychology', 'bias', 'fomo'],
        'get_comprehensive_analysis': ['comprehensive', 'complete', 'detailed'],
        'check_market_conditions': ['market', 'condition', 'trend']
    }

    DEFAULT_TOOLS = ['check_market_conditions', 'detect_trading_patterns']

    def select_tools(self, query: str) -> List[str]:
        query_lower = query.lower()
        selected_tools = set()

        for tool_name, keywords in self.TOOL_KEYWORDS.items():
            if any(keyword in query_lower for keyword in keywords):
                selected_tools.add(tool_name)

        if not selected_tools:
            selected_tools.update(self.DEFAULT_TOOLS)

        return list(selected_tools)


class TradingAssistant:
    """Unified Trading Assistant - All functionality in one class."""

    def __init__(self, api_key: str, user_id: Optional[str] = None):
        self.api_key = api_key
        self.user_id = user_id or "default_user"
        self.client = OpenAI(api_key=api_key)

        # Initialize components
        self.tool_registry = AgentToolRegistry()
        self.tool_selector = SmartToolSelector()
        self.cache = ToolCache(ttl_seconds=600)
        self.agent_manager = AgentManager()

        # User profile and learning
        self.user_profile = self._load_user_profile()
        self.session_data = {
            "start_time": datetime.now(),
            "interactions": [],
            "analysis_results": [],
            "learning_points": []
        }

        # Performance tracking
        self.stats = {
            'tools_called': 0,
            'cache_hits': 0,
            'analyses_completed': 0,
            'total_time': 0
        }

    def _load_user_profile(self) -> Dict:
        """Load user profile for personalized learning."""
        profile_dir = Path(__file__).parent / "user_profiles" / self.user_id
        profile_file = profile_dir / "profile.json"

        if profile_file.exists():
            with open(profile_file, 'r') as f:
                return json.load(f)

        # Create default profile
        default_profile = {
            "user_id": self.user_id,
            "created_date": datetime.now().isoformat(),
            "trading_experience": "unknown",
            "risk_tolerance": "medium",
            "learning_preferences": {},
            "detected_patterns": {},
            "improvement_areas": [],
            "session_history": []
        }

        # Create directory and save
        profile_dir.mkdir(parents=True, exist_ok=True)
        with open(profile_file, 'w') as f:
            json.dump(default_profile, f, indent=2)

        return default_profile

    def _save_user_profile(self):
        """Save updated user profile."""
        profile_dir = Path(__file__).parent / "user_profiles" / self.user_id
        profile_file = profile_dir / "profile.json"

        profile_dir.mkdir(parents=True, exist_ok=True)
        with open(profile_file, 'w') as f:
            json.dump(self.user_profile, f, indent=2)

    def _execute_tool_with_cache(self, tool_name: str, args: Dict) -> str:
        """Execute AI tool with caching."""
        cache_key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"

        cached_result = self.cache.get(cache_key)
        if cached_result:
            self.stats['cache_hits'] += 1
            return f"📋 [Cached] {cached_result}"

        try:
            tool_result = self.tool_registry.call_tool(tool_name, **args)
            if tool_result.get("success"):
                result = tool_result.get("result", {})
                # Convert dict result to string if needed for compatibility
                if isinstance(result, dict):
                    result = json.dumps(result, indent=2)
                self.cache.set(cache_key, result)
                self.stats['tools_called'] += 1
                return result
            else:
                error_msg = tool_result.get("error", "Unknown error")
                return f"Tool {tool_name} failed: {error_msg}"
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    def _execute_tools_parallel(self, tool_calls: List[Tuple[str, Dict]]) -> Dict[str, str]:
        """Execute multiple AI tools in parallel."""
        results = {}

        if len(tool_calls) <= 1:
            if tool_calls:
                tool_name, args = tool_calls[0]
                results[tool_name] = self._execute_tool_with_cache(tool_name, args)
            return results

        with ThreadPoolExecutor(max_workers=min(len(tool_calls), 4)) as executor:
            future_to_tool = {
                executor.submit(self._execute_tool_with_cache, tool_name, args): tool_name
                for tool_name, args in tool_calls
            }

            for future in as_completed(future_to_tool):
                tool_name = future_to_tool[future]
                try:
                    result = future.result(timeout=30)
                    results[tool_name] = result
                    print(f"✅ {tool_name}: Completed")
                except Exception as e:
                    results[tool_name] = f"Error: {str(e)}"
                    print(f"❌ {tool_name}: Failed - {str(e)}")

        return results

    def _get_openai_config(self) -> Dict:
        """Get OpenAI configuration."""
        if CONFIG_AVAILABLE:
            return config.get_openai_config()
        else:
            return {
                'model': 'gpt-4.1',
                'max_completion_tokens': 1500,
                'temperature': 1.0
            }

    def analyze_trading_data(self, trading_data: str, analysis_mode: str = "comprehensive") -> str:
        """Professional trading analysis with anti-pattern detection."""
        start_time = time.time()

        print("🚀 Starting AI-powered trading analysis...")

        # Load pattern templates
        script_dir = Path(__file__).parent.parent
        templates_folder = script_dir / "prompts" / "trading_pattern_templates"

        templates = {}
        if templates_folder.exists():
            for template_file in templates_folder.glob("*.txt"):
                with open(template_file, 'r') as f:
                    content = f.read().strip()
                    if content.startswith("Prompt:"):
                        templates[template_file.stem] = content[7:].strip()

        # Build comprehensive analysis query
        analysis_query = "Perform comprehensive trading psychology analysis:\n\n"

        # Add pattern templates
        analysis_query += "Anti-pattern criteria to check:\n"
        for name, rule in sorted(templates.items()):
            analysis_query += f"• {name}: {rule}\n"

        analysis_query += f"\n--- Trading Data ---\n{trading_data}\n"
        analysis_query += "\nFor each detected pattern, provide:\n"
        analysis_query += "- EVIDENCE: Quote exact trades (symbol, times, prices, notes)\n"
        analysis_query += "- PATTERN PROOF: Show specific behavior that triggers this pattern\n"
        analysis_query += "- CONSEQUENCES: Quantified impact with percentages and amounts\n"
        analysis_query += "- SOLUTION: Concrete actionable steps\n"
        analysis_query += "- SEVERITY: Critical/Warning/Improvement\n"

        # Smart tool selection based on analysis mode
        if analysis_mode == "quick":
            selected_tools = ['detect_trading_patterns']
        else:
            selected_tools = self.tool_selector.select_tools(analysis_query)
            if 'detect_trading_patterns' not in selected_tools:
                selected_tools.append('detect_trading_patterns')

        print(f"🧠 Using {len(selected_tools)} AI tools: {', '.join(selected_tools)}")

        # Prepare tool calls
        tool_calls = []
        for tool_name in selected_tools:
            if tool_name == 'detect_trading_patterns':
                args = {'analysis_type': 'comprehensive', 'pattern_focus': 'all'}
            elif tool_name == 'analyze_market_sentiment':
                # Extract symbols from trading data
                symbols = self._extract_symbols(trading_data)
                args = {'symbols': symbols, 'sentiment_type': 'comprehensive'}
            elif tool_name == 'get_market_data':
                symbols = self._extract_symbols(trading_data)
                args = {'symbols': symbols, 'data_type': 'overview'}
            else:
                args = {}

            tool_calls.append((tool_name, args))

        # Execute AI tools in parallel
        print("🔧 Executing AI tools in parallel...")
        tool_results = self._execute_tools_parallel(tool_calls)

        # Use OpenAI to synthesize results
        system_prompt = (
            "You are an elite trading psychology analyst. Analyze the trading data "
            "using the AI tool results to detect anti-patterns and provide actionable insights. "
            "Focus on specific evidence from the trades and quantified impact."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": analysis_query}
        ]

        # Add tool results to context
        tool_context = "\n\nAI Tool Results:\n"
        for tool_name, result in tool_results.items():
            tool_context += f"\n{tool_name.upper()}:\n{result}\n"

        messages.append({"role": "user", "content": tool_context})

        try:
            openai_config = self._get_openai_config()
            response = self.client.chat.completions.create(
                messages=messages,
                **openai_config
            )

            result = response.choices[0].message.content

            # Update stats and learning
            analysis_time = time.time() - start_time
            self.stats['analyses_completed'] += 1
            self.stats['total_time'] += analysis_time

            # Store result in session
            self.session_data["analysis_results"].append({
                "timestamp": datetime.now().isoformat(),
                "analysis_mode": analysis_mode,
                "tools_used": selected_tools,
                "result": result,
                "duration": analysis_time
            })

            print(f"📊 Analysis completed in {analysis_time:.1f}s")
            print(f"🎯 Performance: {self.stats['tools_called']} tools called, {self.stats['cache_hits']} cache hits")

            return result

        except Exception as e:
            return f"Error in analysis: {str(e)}"

    def _extract_symbols(self, trading_data: str) -> List[str]:
        """Extract trading symbols from data."""
        symbols = set()
        common_symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'GOOGL']

        for symbol in common_symbols:
            if symbol in trading_data.upper():
                symbols.add(symbol)

        return list(symbols) if symbols else ['SPY', 'QQQ']

    def _discover_scenarios(self) -> Dict[str, str]:
        """Discover available trading scenarios using the AI agent tool."""
        # Use the new scenario loading tool for consistency
        tool_result = self.tool_registry.call_tool("load_scenario", scenario="1", format="csv")

        if tool_result.get("success") and "available_scenarios" in tool_result.get("result", {}):
            scenarios = {}
            for scenario_data in tool_result["result"]["available_scenarios"]:
                scenarios[scenario_data["name"]] = scenario_data["path"]
            return scenarios

        # Fallback to direct implementation if tool fails
        scenarios = {}
        samples_dir = Path(__file__).parent.parent / "samples"

        if samples_dir.exists():
            for scenario_dir in sorted(samples_dir.glob("scenario*")):
                if scenario_dir.is_dir():
                    csv_file = scenario_dir / "sample_trades.csv"
                    if csv_file.exists():
                        scenario_name = scenario_dir.name
                        scenarios[scenario_name] = str(csv_file)

        return scenarios

    def _smart_file_path(self, user_input: str) -> Optional[str]:
        """Smart file path resolution using the AI agent tool."""
        # Use the scenario loading tool for resolution
        tool_result = self.tool_registry.call_tool("load_scenario", scenario=user_input, format="csv")

        if tool_result.get("success"):
            result_data = tool_result.get("result", {})
            if "scenario_path" in result_data:
                return result_data["scenario_path"]

        # Fallback to direct file path check
        if os.path.exists(user_input):
            return user_input

        return None

    def interactive_session(self):
        """Start interactive learning session."""
        print("🤖 INTERACTIVE TRADING ASSISTANT")
        print("=" * 50)
        print(f"👤 User: {self.user_id}")
        print(f"📊 Profile: {self.user_profile.get('trading_experience', 'unknown')} trader")

        # Show available scenarios
        scenarios = self._discover_scenarios()
        if scenarios:
            print(f"📁 Available scenarios: {len(scenarios)} found")
            print("💡 Use: analyze <scenario_name> or analyze <number>")

        print("💬 Type 'help' for commands, 'quit' to exit")
        print("=" * 50)

        while True:
            try:
                user_input = input("\n🔍 Enter your question or command: ").strip()

                if user_input.lower() in ['quit', 'exit']:
                    self._end_session()
                    break

                if user_input.lower() == 'help':
                    self._show_help()
                    continue

                if user_input.lower().startswith('analyze '):
                    # Handle smart file analysis
                    file_spec = user_input[8:].strip()
                    resolved_path = self._smart_file_path(file_spec)

                    if resolved_path:
                        try:
                            with open(resolved_path, 'r') as f:
                                trading_data = f.read()
                            print(f"📊 Analyzing: {resolved_path}")
                            result = self.analyze_trading_data(trading_data)
                            print(f"\n📈 ANALYSIS RESULT:\n{result}")
                        except Exception as e:
                            print(f"❌ Error reading file: {e}")
                    else:
                        print(f"❌ Could not find scenario or file: {file_spec}")
                        print("💡 Try: 'analyze 1', 'analyze scenario1', or 'list scenarios'")
                    continue

                if user_input.lower() in ['scenarios', 'list scenarios', 'list']:
                    scenarios = self._discover_scenarios()
                    if scenarios:
                        print(f"\n📁 AVAILABLE SCENARIOS ({len(scenarios)} found):")
                        print("-" * 50)
                        for i, (scenario_name, file_path) in enumerate(scenarios.items(), 1):
                            # Try to get description from scenario folder
                            description = self._get_scenario_description(scenario_name)
                            print(f"  {i:2d}. {scenario_name} - {description}")
                        print(f"\n💡 Usage examples:")
                        print(f"   analyze 1          # Analyze first scenario")
                        print(f"   analyze scenario1  # Analyze by name")
                    else:
                        print("❌ No scenarios found in samples/ folder")
                    continue

                # Handle general queries with AI tools
                response = self.query_with_tools(user_input)
                print(f"\n💡 RESPONSE:\n{response}")

                # Learn from interaction
                self._update_learning(user_input, response)

            except KeyboardInterrupt:
                print("\n👋 Session interrupted by user")
                self._end_session()
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    def query_with_tools(self, query: str) -> str:
        """Process general query using AI tools."""
        selected_tools = self.tool_selector.select_tools(query)

        if not selected_tools:
            # Direct OpenAI query without tools
            try:
                openai_config = self._get_openai_config()
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful trading assistant."},
                        {"role": "user", "content": query}
                    ],
                    **openai_config
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"Error: {str(e)}"

        print(f"🧠 Using {len(selected_tools)} AI tools: {', '.join(selected_tools)}")

        # Prepare tool calls
        tool_calls = []
        for tool_name in selected_tools:
            if 'sentiment' in tool_name:
                symbols = self._extract_symbols(query)
                args = {'symbols': symbols, 'sentiment_type': 'comprehensive'}
            elif 'market_data' in tool_name:
                symbols = self._extract_symbols(query)
                args = {'symbols': symbols, 'data_type': 'overview'}
            elif 'news' in tool_name:
                args = {'query': query}
            else:
                args = {}

            tool_calls.append((tool_name, args))

        # Execute tools
        tool_results = self._execute_tools_parallel(tool_calls)

        # Synthesize with OpenAI
        system_prompt = (
            "You are an expert trading analyst. Use the AI tool results to provide "
            "comprehensive answers with actionable insights and specific recommendations."
        )

        tool_context = "AI Tool Results:\n"
        for tool_name, result in tool_results.items():
            tool_context += f"\n{tool_name}:\n{result}\n"

        try:
            openai_config = self._get_openai_config()
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Query: {query}\n\n{tool_context}"}
                ],
                **openai_config
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error synthesizing results: {str(e)}"

    def _get_scenario_description(self, scenario_name: str) -> str:
        """Get description for a scenario using the AI agent tool."""
        # Use the scenario loading tool to get metadata
        tool_result = self.tool_registry.call_tool("load_scenario", scenario=scenario_name, format="csv")

        if tool_result.get("success"):
            result_data = tool_result.get("result", {})
            metadata = result_data.get("metadata", {})
            if "description" in metadata:
                return metadata["description"]

        # Fallback description
        return 'Trading psychology analysis'

    def _show_help(self):
        """Show help information."""
        print("\n🆘 HELP - Available Commands:")
        print("-" * 40)
        print("analyze <scenario>     - Analyze trading scenario (smart path resolution)")
        print("  • analyze 1          - Analyze scenario by number")
        print("  • analyze scenario1  - Analyze scenario by name")
        print("  • analyze samples/scenario1/sample_trades.csv - Full path")
        print("scenarios / list       - Show all available scenarios")
        print("help                  - Show this help message")
        print("stats                 - Show performance statistics")
        print("profile              - Show user profile information")
        print("quit/exit            - End session and save data")
        print("\n💡 You can also ask questions like:")
        print("- 'What are current market conditions?'")
        print("- 'Analyze AAPL sentiment'")
        print("- 'Check latest market news'")
        print("- 'What are the biggest risks in tech stocks?'")
        print("\n🚀 Smart Features:")
        print("- Auto-discovers scenarios from samples/ folder")
        print("- Supports scenario numbers (1-11) and names")
        print("- Intelligent file path resolution")
        print("- Personalized learning and session tracking")

    def _update_learning(self, query: str, response: str):
        """Update user learning profile."""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response_length": len(response),
            "tools_used": self.stats['tools_called']
        }

        self.session_data["interactions"].append(interaction)

        # Simple learning: track query types
        if "sentiment" in query.lower():
            self.user_profile["learning_preferences"]["sentiment_queries"] = \
                self.user_profile["learning_preferences"].get("sentiment_queries", 0) + 1

        if "risk" in query.lower():
            self.user_profile["learning_preferences"]["risk_queries"] = \
                self.user_profile["learning_preferences"].get("risk_queries", 0) + 1

    def _end_session(self):
        """End session and save learning data."""
        print("\n📊 SESSION SUMMARY")
        print("-" * 30)
        print(f"Duration: {datetime.now() - self.session_data['start_time']}")
        print(f"Interactions: {len(self.session_data['interactions'])}")
        print(f"Analyses completed: {self.stats['analyses_completed']}")
        print(f"AI tools called: {self.stats['tools_called']}")
        print(f"Cache hits: {self.stats['cache_hits']}")

        # Save session to user profile
        session_summary = {
            "date": datetime.now().isoformat(),
            "duration_minutes": (datetime.now() - self.session_data['start_time']).total_seconds() / 60,
            "interactions": len(self.session_data['interactions']),
            "analyses": self.stats['analyses_completed']
        }

        self.user_profile["session_history"].append(session_summary)
        self._save_user_profile()
        print("💾 Session saved to user profile")
        print("👋 Goodbye!")

    def get_stats(self) -> Dict:
        """Get performance statistics."""
        return self.stats.copy()


def load_trading_data(file_path: str) -> str:
    """Load trading data from CSV file."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error loading file: {str(e)}"


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("🤖 UNIFIED TRADING ASSISTANT")
        print("=" * 40)
        print("Usage modes:")
        print("  python trading_assistant.py interactive <api_key> [user_id]")
        print("  python trading_assistant.py analyze <file> <api_key> [user_id]")
        print("  python trading_assistant.py query <api_key> '<question>' [user_id]")
        print("")
        print("Examples:")
        print("  python trading_assistant.py interactive sk-your-key john_trader")
        print("  python trading_assistant.py analyze samples/scenario1/sample_trades.csv sk-your-key")
        print("  python trading_assistant.py query sk-your-key 'Check AAPL market conditions'")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "interactive":
        if len(sys.argv) < 3:
            print("❌ API key required for interactive mode")
            sys.exit(1)

        api_key = sys.argv[2]
        user_id = sys.argv[3] if len(sys.argv) > 3 else "default_user"

        assistant = TradingAssistant(api_key, user_id)
        assistant.interactive_session()

    elif mode == "analyze":
        if len(sys.argv) < 4:
            print("❌ File path and API key required for analyze mode")
            sys.exit(1)

        file_path = sys.argv[2]
        api_key = sys.argv[3]
        user_id = sys.argv[4] if len(sys.argv) > 4 else "default_user"

        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            sys.exit(1)

        trading_data = load_trading_data(file_path)
        assistant = TradingAssistant(api_key, user_id)

        print(f"📊 Analyzing trading data from: {file_path}")
        result = assistant.analyze_trading_data(trading_data)
        print(f"\n📈 ANALYSIS RESULT:\n{result}")

    elif mode == "query":
        if len(sys.argv) < 4:
            print("❌ API key and query required")
            sys.exit(1)

        api_key = sys.argv[2]
        query = sys.argv[3]
        user_id = sys.argv[4] if len(sys.argv) > 4 else "default_user"

        assistant = TradingAssistant(api_key, user_id)
        print(f"🔍 Processing query: {query}")
        result = assistant.query_with_tools(query)
        print(f"\n💡 RESULT:\n{result}")

    else:
        print(f"❌ Unknown mode: {mode}")
        print("Available modes: interactive, analyze, query")
        sys.exit(1)


if __name__ == "__main__":
    main()