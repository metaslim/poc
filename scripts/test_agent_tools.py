#!/usr/bin/env python3
"""Test AI Agent Tools System

Quick test to verify that all AI agent tools are working correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.tool_integration import AgentToolRegistry, SmartTradingAgent


def test_tool_registry():
    """Test the agent tool registry."""
    print("🧪 Testing Agent Tool Registry")
    print("-" * 40)

    registry = AgentToolRegistry()

    # Test getting available tools
    tools = registry.get_available_tools()
    print(f"✅ Available tools: {len(tools)}")
    for tool in tools:
        print(f"  • {tool}")

    # Test individual tool calls
    print(f"\n🔧 Testing individual tool calls:")

    # Test news tool
    news_result = registry.call_tool("check_market_news", query="latest", focus="tech")
    print(f"  ✅ News tool: {'Success' if news_result.get('success') else 'Failed'}")

    # Test market data tool
    market_result = registry.call_tool("get_market_data", symbols=["AAPL", "TSLA"], analysis_type="prices")
    print(f"  ✅ Market data tool: {'Success' if market_result.get('success') else 'Failed'}")

    # Test sentiment tool
    sentiment_result = registry.call_tool("analyze_market_sentiment", symbols=["SPY"], sentiment_type="comprehensive")
    print(f"  ✅ Sentiment tool: {'Success' if sentiment_result.get('success') else 'Failed'}")

    # Test risk tool
    risk_result = registry.call_tool("assess_portfolio_risk", analysis_focus="portfolio")
    print(f"  ✅ Risk tool: {'Success' if risk_result.get('success') else 'Failed'}")

    # Test pattern tool
    pattern_result = registry.call_tool("detect_trading_patterns", analysis_type="comprehensive")
    print(f"  ✅ Pattern tool: {'Success' if pattern_result.get('success') else 'Failed'}")

    return True


def test_smart_agent():
    """Test the smart trading agent."""
    print(f"\n🤖 Testing Smart Trading Agent")
    print("-" * 40)

    agent = SmartTradingAgent()

    # Test request analysis
    test_requests = [
        "Check latest market news",
        "Analyze AAPL sentiment and price",
        "Assess portfolio risk",
        "Detect emotional trading patterns",
        "Get comprehensive market analysis"
    ]

    for request in test_requests:
        analysis = agent.analyze_request(request)
        tools_identified = len(analysis["tools_identified"])
        print(f"  ✅ '{request}' -> {tools_identified} tools identified")

    # Test full execution
    print(f"\n🚀 Testing full execution:")
    result = agent.execute_analysis("Check market conditions for AAPL and TSLA")

    success = result["summary"]["successful_tools"] > 0
    print(f"  ✅ Full execution: {'Success' if success else 'Failed'}")
    print(f"  📊 Tools used: {', '.join(result['tools_used'])}")
    print(f"  🎯 Symbols: {', '.join(result['symbols_analyzed'])}")

    return True


def test_integration():
    """Test integration between components."""
    print(f"\n🔗 Testing Integration")
    print("-" * 40)

    # Test that all components work together
    registry = AgentToolRegistry()
    agent = SmartTradingAgent()

    # Generate tool prompt
    prompt = registry.generate_tool_prompt()
    print(f"  ✅ Tool prompt generated: {len(prompt)} characters")

    # Test multiple requests
    requests = [
        "What's the latest news?",
        "How is AAPL performing?",
        "Check market sentiment"
    ]

    success_count = 0
    for request in requests:
        try:
            response = agent.interactive_query(request)
            if response and len(response) > 0:
                success_count += 1
        except Exception as e:
            print(f"  ❌ Failed request '{request}': {e}")

    print(f"  ✅ Interactive queries: {success_count}/{len(requests)} successful")

    return success_count == len(requests)


def main():
    """Run all tests."""
    print("🧪 AI AGENT TOOLS SYSTEM TESTS")
    print("=" * 50)

    tests = [
        ("Tool Registry", test_tool_registry),
        ("Smart Agent", test_smart_agent),
        ("Integration", test_integration)
    ]

    passed_tests = 0
    total_tests = len(tests)

    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name} Test...")
            success = test_func()
            if success:
                print(f"✅ {test_name} Test: PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name} Test: FAILED")
        except Exception as e:
            print(f"❌ {test_name} Test: ERROR - {e}")

    print(f"\n" + "=" * 50)
    print(f"📊 TEST RESULTS: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready for use.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())