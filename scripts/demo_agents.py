#!/usr/bin/env python3
"""AI Agents Demo Script

Demonstrates the capabilities of different AI agents with fake responses.
This script shows how to use the agent system independently of the main trading assistant.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import AgentManager


def demo_individual_agents():
    """Demonstrate individual agent capabilities."""
    print("🤖 AI TRADING AGENTS DEMONSTRATION")
    print("=" * 50)

    agent_manager = AgentManager()

    # News Agent Demo
    print("\n📰 NEWS AGENT DEMO")
    print("-" * 30)
    news_result = agent_manager.query_agent("news", "Get latest market news affecting tech stocks")

    if "news_stories" in news_result:
        print(f"✅ Found {news_result['stories_found']} news stories")
        print(f"📈 Market sentiment: {news_result['market_sentiment']['overall']}")

        for story in news_result["news_stories"][:2]:
            print(f"  • {story['headline']}")
            print(f"    Impact: {story['impact']} | Confidence: {story['confidence']:.0%}")

    time.sleep(1)

    # Market Data Agent Demo
    print("\n📊 MARKET DATA AGENT DEMO")
    print("-" * 30)
    market_result = agent_manager.query_agent("market_data", "Get current prices and technical analysis for AAPL, TSLA, NVDA")

    if "quotes" in market_result:
        print("✅ Market data retrieved:")
        for symbol, data in list(market_result["quotes"].items())[:3]:
            print(f"  • {symbol}: ${data['current_price']:.2f} ({data['change_percent']:+.1f}%)")

    time.sleep(1)

    # Sentiment Agent Demo
    print("\n💭 SENTIMENT AGENT DEMO")
    print("-" * 30)
    sentiment_result = agent_manager.query_agent("sentiment", "Analyze overall market sentiment and social media buzz")

    if "sentiment_data" in sentiment_result:
        print("✅ Sentiment analysis complete:")
        for symbol, data in list(sentiment_result["sentiment_data"].items())[:3]:
            print(f"  • {symbol}: {data['sentiment_label']} (score: {data['composite_sentiment']:+.2f})")

    time.sleep(1)

    # Risk Management Agent Demo
    print("\n⚠️ RISK MANAGEMENT AGENT DEMO")
    print("-" * 30)
    risk_result = agent_manager.query_agent("risk_management", "Analyze portfolio risk and suggest position sizing")

    if "portfolio_metrics" in risk_result:
        metrics = risk_result["portfolio_metrics"]
        print("✅ Risk assessment complete:")
        print(f"  • Portfolio Value: ${metrics['total_value']:,.0f}")
        print(f"  • Daily VaR (95%): ${metrics['daily_var_95']:,.0f}")
        print(f"  • Portfolio Beta: {metrics['beta']}")

    time.sleep(1)

    # Pattern Analysis Agent Demo
    print("\n🧠 PATTERN ANALYSIS AGENT DEMO")
    print("-" * 30)
    pattern_result = agent_manager.query_agent("pattern_analysis", "Analyze for FOMO and emotional trading patterns")

    if "detected_patterns" in pattern_result:
        patterns = pattern_result["detected_patterns"]
        print(f"✅ Pattern analysis complete: {len(patterns)} patterns detected")

        for pattern in patterns[:3]:
            print(f"  • {pattern['pattern_name'].replace('_', ' ').title()}: {pattern['severity']}")
            print(f"    Confidence: {pattern['confidence']:.0%}")


def demo_parallel_agents():
    """Demonstrate parallel agent execution."""
    print("\n\n🚀 PARALLEL AGENT EXECUTION DEMO")
    print("=" * 50)

    agent_manager = AgentManager()

    # Define multiple requests to run in parallel
    requests = [
        {
            "agent_type": "news",
            "request": "Get breaking news that could affect markets"
        },
        {
            "agent_type": "market_data",
            "request": "Check current market conditions and volatility"
        },
        {
            "agent_type": "sentiment",
            "request": "Analyze social media sentiment for major indices"
        },
        {
            "agent_type": "risk_management",
            "request": "Assess current market risk levels"
        }
    ]

    print("⏱️ Executing 4 agents in parallel...")
    start_time = time.time()

    results = agent_manager.query_multiple_agents(requests, parallel=True)

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"✅ Parallel execution completed in {execution_time:.1f} seconds")
    print(f"📊 Successful queries: {results['successful_queries']}/{results['agents_queried']}")

    # Show brief results
    for agent_type, result in results["results"].items():
        if "error" not in result:
            print(f"  ✓ {agent_type.replace('_', ' ').title()} agent: Success")
        else:
            print(f"  ✗ {agent_type.replace('_', ' ').title()} agent: Failed")


def demo_comprehensive_analysis():
    """Demonstrate comprehensive market analysis."""
    print("\n\n🎯 COMPREHENSIVE ANALYSIS DEMO")
    print("=" * 50)

    agent_manager = AgentManager()
    symbols = ["AAPL", "TSLA", "SPY"]

    print(f"🔍 Running comprehensive analysis for {', '.join(symbols)}...")

    start_time = time.time()
    analysis = agent_manager.comprehensive_analysis(symbols, analysis_depth="standard")
    end_time = time.time()

    print(f"✅ Analysis completed in {end_time - start_time:.1f} seconds")

    # Display synthesis results
    if "synthesis" in analysis:
        synthesis = analysis["synthesis"]

        print(f"\n📈 Overall Sentiment: {synthesis['overall_sentiment'].upper()}")
        print(f"🎯 Confidence Level: {synthesis['confidence_level']}")

        print(f"\n🔑 Key Insights:")
        for insight in synthesis["key_insights"][:3]:
            print(f"  • {insight}")

        print(f"\n📊 Trading Signals:")
        for symbol, signal in synthesis["trading_signals"].items():
            print(f"  • {symbol}: {signal['signal']} (confidence: {signal['confidence']:.0%})")

        print(f"\n💡 Recommendations:")
        for rec in synthesis["recommendations"][:3]:
            print(f"  • {rec}")


def demo_market_overview():
    """Demonstrate market overview functionality."""
    print("\n\n🌍 MARKET OVERVIEW DEMO")
    print("=" * 50)

    agent_manager = AgentManager()

    print("🔍 Getting comprehensive market overview...")
    overview = agent_manager.market_overview()

    # Display market snapshot
    if "market_snapshot" in overview:
        snapshot = overview["market_snapshot"]
        print(f"\n📊 Market Snapshot:")
        print(f"  • Trend: {snapshot.get('trend', 'unknown').upper()}")
        print(f"  • Volatility: {snapshot.get('volatility', 'normal').upper()}")

    # Display sentiment regime
    if "sentiment_regime" in overview:
        regime = overview["sentiment_regime"]
        print(f"\n💭 Sentiment Regime: {regime.get('regime', 'unknown').upper()}")
        print(f"  • Confidence: {regime.get('confidence', 0):.0%}")

    # Display key news
    if "key_news" in overview:
        print(f"\n📰 Key News Headlines:")
        for news in overview["key_news"][:3]:
            if isinstance(news, dict):
                print(f"  • {news.get('headline', 'No headline')}")

    # Display trading environment
    if "trading_environment" in overview:
        print(f"\n🎯 Trading Environment: {overview['trading_environment'].replace('_', ' ').title()}")


def demo_session_stats():
    """Demonstrate session statistics."""
    print("\n\n📊 SESSION STATISTICS DEMO")
    print("=" * 50)

    agent_manager = AgentManager()

    # Run a few queries first
    agent_manager.query_agent("news", "Test query")
    agent_manager.query_agent("market_data", "Another test")
    agent_manager.query_agent("sentiment", "Final test")

    stats = agent_manager.get_session_stats()

    print("📈 Session Statistics:")
    print(f"  • Total Interactions: {stats.get('total_interactions', 0)}")
    print(f"  • Success Rate: {stats.get('success_rate', 0):.0%}")
    print(f"  • Most Used Agent: {stats.get('most_used_agent', 'none')}")

    if "agent_usage" in stats:
        print(f"  • Agent Usage Breakdown:")
        for agent, count in stats["agent_usage"].items():
            print(f"    - {agent.replace('_', ' ').title()}: {count} queries")


def main():
    """Main demonstration function."""
    print("🚀 STARTING AI TRADING AGENTS DEMONSTRATION")
    print("This demo shows fake responses for testing purposes")
    print("=" * 60)

    try:
        # Run all demos
        demo_individual_agents()
        demo_parallel_agents()
        demo_comprehensive_analysis()
        demo_market_overview()
        demo_session_stats()

        print("\n" + "=" * 60)
        print("✅ DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("All agents are working with simulated data.")
        print("Ready for integration with real trading systems.")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Check agent configuration and try again.")


if __name__ == "__main__":
    main()