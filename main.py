#!/usr/bin/env python3
"""
Unified Trading Assistant Main Entry Point

This script provides a single entry point for all trading assistant functionality,
including AI agent tools, pattern analysis, and interactive sessions.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def show_banner():
    """Display the trading assistant banner."""
    print("=" * 80)
    print("🤖 ADVANCED TRADING ASSISTANT WITH AI AGENT TOOLS")
    print("=" * 80)
    print("Enhanced with specialized AI agents for comprehensive market analysis:")
    print("📰 News Agent | 📊 Market Data | 💭 Sentiment | ⚠️ Risk Management | 🧠 Pattern Analysis")
    print("=" * 80)

def show_help():
    """Display help information."""
    print("\n📚 USAGE:")
    print("  python main.py <mode> [options]")
    print()
    print("🔧 AVAILABLE MODES:")
    print()
    print("1️⃣  demo-agents")
    print("     Show AI agent capabilities with fake data")
    print("     Example: python main.py demo-agents")
    print()
    print("2️⃣  test-agents")
    print("     Run comprehensive AI agent test suite")
    print("     Example: python main.py test-agents")
    print()
    print("3️⃣  smart-assistant [demo|batch|interactive]")
    print("     Smart assistant with automatic tool selection")
    print("     Examples:")
    print("       python main.py smart-assistant demo")
    print("       python main.py smart-assistant batch")
    print("       python main.py smart-assistant interactive")
    print()
    print("4️⃣  openai-tools <api_key> [query]")
    print("     OpenAI agent that can call AI tools as functions")
    print("     Examples:")
    print("       python main.py openai-tools sk-your-key")
    print("       python main.py openai-tools sk-your-key 'Check market conditions'")
    print()
    print("5️⃣  analyze <scenario> <api_key> [user_id]")
    print("     Professional trading analysis with AI tools")
    print("     Examples:")
    print("       python main.py analyze samples/scenario1 sk-your-key")
    print("       python main.py analyze samples/scenario1 sk-your-key trader123")
    print()
    print("6️⃣  interactive <api_key> [user_id]")
    print("     Interactive trading assistant with smart scenario loading")
    print("     Example: python main.py interactive sk-your-key [username]")
    print()
    print("7️⃣  list-scenarios")
    print("     Show available trading scenarios")
    print()
    print("📋 EXAMPLES:")
    print("  # Quick demo of AI agents")
    print("  python main.py demo-agents")
    print()
    print("  # Test with your OpenAI key")
    print("  python main.py openai-tools sk-your-key 'Analyze AAPL sentiment'")
    print()
    print("  # Full analysis of trading scenario")
    print("  python main.py analyze samples/scenario1 sk-your-key")

def list_scenarios():
    """List available trading scenarios."""
    print("\n📁 AVAILABLE TRADING SCENARIOS:")
    print("-" * 40)

    samples_dir = Path("samples")
    if not samples_dir.exists():
        print("❌ No samples directory found")
        return

    scenarios = sorted([d for d in samples_dir.iterdir() if d.is_dir()])

    if not scenarios:
        print("❌ No scenarios found in samples directory")
        return

    for i, scenario in enumerate(scenarios, 1):
        csv_file = scenario / "sample_trades.csv"
        status = "✅" if csv_file.exists() else "❌"
        print(f"{i:2d}. {status} {scenario.name}")

    print(f"\n📊 Total scenarios: {len(scenarios)}")
    print("\n💡 Use format: python main.py analyze samples/scenario1 your-api-key")

def run_demo_agents():
    """Run the AI agents demo."""
    try:
        from scripts.demo_agents import main
        main()
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False
    return True

def run_test_agents():
    """Run the AI agents demo and validation."""
    try:
        from scripts.demo_agents import main
        print("🧪 Running AI agents validation through demonstrations...")
        main()
        return True
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_smart_assistant(mode: str = "interactive"):
    """Run smart trading assistant using optimized tools."""
    try:
        if mode == "demo":
            print("🎯 Running smart assistant demo with AI tools...")
            from scripts.demo_agents import main
            sys.argv = ["demo_agents.py"]
            main()
        else:
            print(f"💬 Smart assistant mode '{mode}' - use openai-tools instead")
            print("Example: python main.py openai-tools your-api-key 'your question'")
    except Exception as e:
        print(f"❌ Error running smart assistant: {e}")
        return False
    return True

def run_openai_tools(api_key: str, query: Optional[str] = None):
    """Run unified trading assistant for queries."""
    try:
        from scripts.trading_assistant import main
        if query:
            sys.argv = ["trading_assistant.py", "query", api_key, query]
        else:
            sys.argv = ["trading_assistant.py", "interactive", api_key]
        main()
    except Exception as e:
        print(f"❌ Error running trading assistant: {e}")
        return False
    return True

def run_analyze(scenario: str, api_key: str):
    """Run professional trading analysis."""
    try:
        from scripts.trading_assistant import main
        file_path = f"{scenario}/sample_trades.csv"
        sys.argv = ["trading_assistant.py", "analyze", file_path, api_key]
        main()
    except Exception as e:
        print(f"❌ Error running analysis: {e}")
        return False
    return True

def run_interactive(scenario: str, api_key: str, user_id: str):
    """Run interactive trading assistant (legacy with scenario)."""
    try:
        from scripts.trading_assistant import main
        sys.argv = ["trading_assistant.py", "interactive", api_key, user_id]
        print(f"📊 Scenario data available at: {scenario}/sample_trades.csv")
        print("💡 Use 'analyze <file>' command in interactive mode to analyze the scenario")
        main()
    except Exception as e:
        print(f"❌ Error running interactive assistant: {e}")
        return False
    return True

def run_interactive_simple(api_key: str, user_id: Optional[str] = None):
    """Run interactive trading assistant with smart scenario loading."""
    try:
        from scripts.trading_assistant import main
        if user_id:
            sys.argv = ["trading_assistant.py", "interactive", api_key, user_id]
        else:
            sys.argv = ["trading_assistant.py", "interactive", api_key]
        print("🎯 Interactive session with smart scenario loading")
        print("💡 Use 'scenarios' to list all available scenarios, 'analyze 1' to load scenario1")
        main()
    except Exception as e:
        print(f"❌ Error running interactive assistant: {e}")
        return False
    return True

def validate_api_key(api_key: str) -> bool:
    """Validate OpenAI API key format."""
    if not api_key or not api_key.startswith('sk-'):
        print("❌ Invalid OpenAI API key format. Key should start with 'sk-'")
        return False
    return True

def validate_scenario(scenario: str) -> bool:
    """Validate trading scenario path."""
    scenario_path = Path(scenario)
    if not scenario_path.exists():
        print(f"❌ Scenario folder not found: {scenario}")
        return False

    csv_file = scenario_path / "sample_trades.csv"
    if not csv_file.exists():
        print(f"❌ Trading data file not found: {csv_file}")
        return False

    return True

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_banner()
        show_help()
        return 1

    mode = sys.argv[1].lower()

    try:
        if mode in ['help', '-h', '--help']:
            show_banner()
            show_help()
            return 0

        elif mode == 'demo-agents':
            show_banner()
            print("🚀 Running AI Agents Demo...")
            return 0 if run_demo_agents() else 1

        elif mode == 'test-agents':
            show_banner()
            print("🧪 Running AI Agents Test Suite...")
            return 0 if run_test_agents() else 1

        elif mode == 'smart-assistant':
            show_banner()
            assistant_mode = sys.argv[2] if len(sys.argv) > 2 else "interactive"
            print(f"🤖 Running Smart Assistant in {assistant_mode} mode...")
            return 0 if run_smart_assistant(assistant_mode) else 1

        elif mode == 'openai-tools':
            if len(sys.argv) < 3:
                print("❌ OpenAI API key required")
                print("Usage: python main.py openai-tools <api_key> [query]")
                return 1

            api_key = sys.argv[2]
            if not validate_api_key(api_key):
                return 1

            query = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None

            show_banner()
            print("🤖 Running OpenAI Agent with Tools...")
            return 0 if run_openai_tools(api_key, query) else 1

        elif mode == 'analyze':
            if len(sys.argv) < 4:
                print("❌ Missing required arguments")
                print("Usage: python main.py analyze <scenario> <api_key>")
                return 1

            scenario = sys.argv[2]
            api_key = sys.argv[3]

            if not validate_scenario(scenario) or not validate_api_key(api_key):
                return 1

            show_banner()
            print(f"📊 Running Professional Analysis on {scenario}...")
            return 0 if run_analyze(scenario, api_key) else 1

        elif mode == 'interactive':
            if len(sys.argv) < 3:
                print("❌ Missing required arguments")
                print("Usage: python main.py interactive <api_key> [user_id]")
                return 1

            api_key = sys.argv[2]
            user_id = sys.argv[3] if len(sys.argv) > 3 else None

            if not validate_api_key(api_key):
                return 1

            show_banner()
            print(f"💬 Starting Interactive Session...")
            if user_id:
                print(f"👤 User: {user_id}")
            return 0 if run_interactive_simple(api_key, user_id) else 1

        elif mode == 'list-scenarios':
            show_banner()
            list_scenarios()
            return 0

        else:
            print(f"❌ Unknown mode: {mode}")
            print("Use 'python main.py help' for usage information")
            return 1

    except KeyboardInterrupt:
        print("\n\n👋 Operation cancelled by user")
        return 0
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())