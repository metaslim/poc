#!/usr/bin/env python3
"""Smart Trading Assistant with AI Agent Tools

Enhanced trading assistant that uses AI agents as tools for comprehensive market analysis.
The main agent intelligently selects and calls appropriate AI agent tools based on user requests.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents.tool_integration import SmartTradingAgent, AgentToolRegistry


class EnhancedTradingAssistant:
    """Enhanced trading assistant with AI agent tool integration."""

    def __init__(self, api_key: Optional[str] = None):
        self.smart_agent = SmartTradingAgent(api_key)
        self.tool_registry = AgentToolRegistry()
        self.session_log = []

    def start_interactive_session(self):
        """Start an interactive session with the smart trading assistant."""
        print("🤖 SMART TRADING ASSISTANT WITH AI AGENT TOOLS")
        print("=" * 60)
        print("This assistant uses specialized AI agents as tools for comprehensive analysis.")
        print("Available tools:", ", ".join(self.tool_registry.get_available_tools()))
        print("=" * 60)

        while True:
            try:
                user_input = input("\n💬 Your request (or 'quit' to exit): ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    self.end_session()
                    break

                if user_input.lower() in ['help', 'h']:
                    self.show_help()
                    continue

                if user_input.lower() == 'tools':
                    self.show_available_tools()
                    continue

                if user_input.lower() == 'stats':
                    self.show_session_stats()
                    continue

                if not user_input:
                    continue

                # Process the request
                print(f"\n⏳ Processing request...")
                response = self.smart_agent.interactive_query(user_input)
                print(response)

                # Log the interaction
                self.session_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_input": user_input,
                    "response_length": len(response)
                })

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                self.end_session()
                break
            except Exception as e:
                print(f"\n❌ Error processing request: {e}")
                print("Please try again or type 'help' for assistance.")

    def show_help(self):
        """Display help information."""
        print("\n📚 SMART TRADING ASSISTANT HELP")
        print("=" * 40)
        print("Available commands:")
        print("  • help, h          - Show this help message")
        print("  • tools            - Show available AI agent tools")
        print("  • stats            - Show session statistics")
        print("  • quit, exit, q    - End session")
        print()
        print("Example requests:")
        print("  • 'Check latest market news for tech stocks'")
        print("  • 'Analyze AAPL sentiment and price action'")
        print("  • 'Assess risk for my TSLA position'")
        print("  • 'Detect emotional trading patterns'")
        print("  • 'Get comprehensive analysis for SPY'")
        print("  • 'What are current market conditions?'")

    def show_available_tools(self):
        """Show available AI agent tools and their descriptions."""
        print("\n🔧 AVAILABLE AI AGENT TOOLS")
        print("=" * 40)

        tools = self.tool_registry.get_available_tools()
        for tool_name in tools:
            tool_info = self.tool_registry.get_tool_description(tool_name)
            print(f"\n📋 {tool_name}:")
            print(f"   {tool_info['description']}")
            print(f"   Agent: {tool_info['agent_type']}")

    def show_session_stats(self):
        """Show current session statistics."""
        print("\n📊 SESSION STATISTICS")
        print("=" * 30)

        if not self.session_log:
            print("No interactions yet in this session.")
            return

        print(f"Total interactions: {len(self.session_log)}")
        print(f"Session duration: {self._get_session_duration()}")

        # Show tool usage stats
        tool_stats = self.tool_registry.get_tool_usage_stats()
        if "agent_usage" in tool_stats:
            print("\nAgent tool usage:")
            for agent, count in tool_stats["agent_usage"].items():
                print(f"  • {agent.replace('_', ' ').title()}: {count} queries")

    def _get_session_duration(self) -> str:
        """Calculate session duration."""
        if len(self.session_log) < 1:
            return "0 minutes"

        first_interaction = datetime.fromisoformat(self.session_log[0]["timestamp"])
        last_interaction = datetime.fromisoformat(self.session_log[-1]["timestamp"])
        duration = last_interaction - first_interaction

        minutes = duration.total_seconds() / 60
        return f"{minutes:.1f} minutes"

    def demo_mode(self):
        """Run demonstration of various capabilities."""
        print("🚀 SMART TRADING ASSISTANT DEMO MODE")
        print("=" * 50)

        demo_requests = [
            "Check latest market news affecting tech stocks",
            "Analyze AAPL and TSLA sentiment",
            "What are current market conditions?",
            "Assess portfolio risk factors",
            "Detect FOMO trading patterns"
        ]

        for i, request in enumerate(demo_requests, 1):
            print(f"\n🎯 Demo Request {i}: {request}")
            print("-" * 40)

            response = self.smart_agent.interactive_query(request)
            print(response)

            if i < len(demo_requests):
                print("\n" + "="*50)

    def batch_analyze(self, requests: List[str]) -> Dict[str, Any]:
        """Process multiple requests in batch mode."""
        print(f"📋 BATCH ANALYSIS MODE - Processing {len(requests)} requests")
        print("=" * 50)

        batch_results = {}

        for i, request in enumerate(requests, 1):
            print(f"\n🔄 Processing request {i}/{len(requests)}: {request}")

            analysis = self.smart_agent.execute_analysis(request)
            batch_results[f"request_{i}"] = {
                "request": request,
                "analysis": analysis,
                "tools_used": analysis["tools_used"],
                "success": analysis["summary"]["successful_tools"] > 0
            }

        # Generate batch summary
        successful_requests = len([r for r in batch_results.values() if r["success"]])
        all_tools_used = set()
        for result in batch_results.values():
            all_tools_used.update(result["tools_used"])

        batch_summary = {
            "total_requests": len(requests),
            "successful_requests": successful_requests,
            "success_rate": successful_requests / len(requests),
            "unique_tools_used": list(all_tools_used),
            "timestamp": datetime.now().isoformat()
        }

        print(f"\n✅ BATCH ANALYSIS COMPLETE")
        print(f"Success Rate: {batch_summary['success_rate']:.0%}")
        print(f"Tools Used: {', '.join(batch_summary['unique_tools_used'])}")

        return {
            "batch_results": batch_results,
            "batch_summary": batch_summary
        }

    def end_session(self):
        """End the current session and show summary."""
        print("\n📊 SESSION SUMMARY")
        print("=" * 30)

        if self.session_log:
            print(f"Total interactions: {len(self.session_log)}")
            print(f"Session duration: {self._get_session_duration()}")
            print(f"First interaction: {self.session_log[0]['timestamp'][:19]}")
            print(f"Last interaction: {self.session_log[-1]['timestamp'][:19]}")

            # Save session log if desired
            save_log = input("\n💾 Save session log? (y/n): ").lower().strip()
            if save_log == 'y':
                self.save_session_log()

        print("\n👋 Thank you for using the Smart Trading Assistant!")
        print("All AI agent tools are ready for your next session.")

    def save_session_log(self):
        """Save session log to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"session_log_{timestamp}.json"
        log_path = Path("logs") / log_filename

        # Create logs directory if it doesn't exist
        log_path.parent.mkdir(exist_ok=True)

        session_data = {
            "session_id": timestamp,
            "start_time": self.session_log[0]["timestamp"] if self.session_log else None,
            "end_time": datetime.now().isoformat(),
            "interactions": self.session_log,
            "tool_stats": self.tool_registry.get_tool_usage_stats()
        }

        with open(log_path, 'w') as f:
            json.dump(session_data, f, indent=2)

        print(f"📁 Session log saved to: {log_path}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "interactive"

    assistant = EnhancedTradingAssistant()

    try:
        if mode == "demo":
            assistant.demo_mode()
        elif mode == "batch":
            # Example batch requests
            batch_requests = [
                "Check latest market news",
                "Analyze market sentiment for major indices",
                "Assess current market risk levels",
                "Check for common trading patterns"
            ]
            assistant.batch_analyze(batch_requests)
        else:
            assistant.start_interactive_session()

    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()