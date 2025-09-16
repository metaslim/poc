"""Interactive Trading Assistant with Learning Capabilities

This module provides an interactive trading assistant that can ask follow-up questions,
learn from user responses, and store user behavior for future analysis.
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# Add parent directory to path for agent imports
sys.path.append(str(Path(__file__).parent.parent))

from agents import AgentManager

# Import the OpenAI with tools module
try:
    from openai_with_agent_tools import OpenAIWithAgentTools
except ImportError:
    # If not found, try to import from current directory
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
    from openai_with_agent_tools import OpenAIWithAgentTools

try:
    from openai import OpenAI
except ImportError:
    print("Error: OpenAI package not installed. Run: pip install openai")
    sys.exit(1)

from pro_trading_assistant import (
    load_trading_data,
    load_pattern_templates,
    validate_inputs
)
from pattern_extractor import (
    extract_detected_patterns,
    extract_follow_up_questions
)


class UserProfile:
    """Manages user behavior data and learning patterns."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.profile_dir = Path("user_profiles") / user_id
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.profile_file = self.profile_dir / "profile.json"
        self.sessions_dir = self.profile_dir / "past_sessions"
        self.sessions_dir.mkdir(exist_ok=True)

        self.profile_data = self.load_profile()

    def load_profile(self) -> Dict[str, Any]:
        """Load user profile data or create new profile."""
        if self.profile_file.exists():
            with open(self.profile_file, 'r') as f:
                return json.load(f)

        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "session_count": 0,
            "common_patterns": [],
            "risk_tolerance": "unknown",
            "experience_level": "unknown",
            "preferred_advice_style": "detailed",
            "recurring_anti_patterns": {},
            "improvement_areas": [],
            "follow_up_preferences": {}
        }

    def save_profile(self):
        """Save profile data to file."""
        with open(self.profile_file, 'w') as f:
            json.dump(self.profile_data, f, indent=2)

    def save_session(self, session_data: Dict[str, Any]):
        """Save session data for learning."""
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = self.sessions_dir / f"session_{session_id}.json"

        session_data.update({
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "user_id": self.user_id
        })

        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        self.profile_data["session_count"] += 1
        self.save_profile()

        return session_id


class InteractiveTradingAssistant:
    """Interactive trading assistant with learning capabilities."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.openai_with_tools = OpenAIWithAgentTools(api_key)
        self.user_profile = None
        self.agent_manager = AgentManager()
        self.current_session = {
            "analysis_results": [],
            "follow_up_questions": [],
            "user_responses": [],
            "detected_patterns": [],
            "recommendations_given": [],
            "user_feedback": [],
            "agent_insights": []
        }

    def set_user(self, user_id: str):
        """Set the current user and load their profile."""
        self.user_profile = UserProfile(user_id)
        print(f"Loaded profile for user: {user_id}")
        print(f"Previous sessions: {self.user_profile.profile_data['session_count']}")

    def build_enhanced_system_prompt(self) -> str:
        """Build system prompt enhanced with user profile data."""
        base_prompt = (
            "You are an elite trading psychology analyst and risk management expert with 20+ years of experience. "
            "Your mission is to identify self-destructive trading patterns and help traders improve.\n\n"
        )

        if self.user_profile:
            profile = self.user_profile.profile_data
            base_prompt += f"USER CONTEXT:\n"
            base_prompt += f"• Experience Level: {profile.get('experience_level', 'unknown')}\n"
            base_prompt += f"• Risk Tolerance: {profile.get('risk_tolerance', 'unknown')}\n"
            base_prompt += f"• Previous Sessions: {profile.get('session_count', 0)}\n"

            if profile.get('recurring_anti_patterns'):
                base_prompt += f"• Known Recurring Patterns: {', '.join(profile['recurring_anti_patterns'].keys())}\n"

            base_prompt += "\n"

        # Add AI agent tools information
        base_prompt += (
            "AI AGENT TOOLS AVAILABLE:\n"
            "You have access to specialized AI agents that provide market insights:\n"
            "• News Agent: Latest market news and impact analysis\n"
            "• Market Data Agent: Real-time prices, technical indicators, volatility\n"
            "• Sentiment Agent: Social media, options flow, institutional sentiment\n"
            "• Risk Management Agent: Portfolio risk, VaR, position sizing\n"
            "• Pattern Analysis Agent: Trading psychology pattern detection\n\n"
            "These agents provide additional context and data to supplement your analysis.\n"
            "The system automatically calls relevant agents during analysis.\n\n"
        )

        base_prompt += (
            "ANALYSIS FRAMEWORK:\n"
            "For each anti-pattern you detect, provide:\n"
            "• EVIDENCE: Specific trades/data points that demonstrate the pattern\n"
            "• PSYCHOLOGY: The emotional/cognitive bias driving this behavior\n"
            "• CONSEQUENCES: Quantified impact on performance\n"
            "• SOLUTION: Concrete, actionable steps to eliminate this pattern\n\n"
            "FOLLOW-UP QUESTIONS:\n"
            "After your analysis, ask 2-3 specific follow-up questions to:\n"
            "1. Understand the trader's mindset during problematic trades\n"
            "2. Identify root causes of the anti-patterns\n"
            "3. Gauge their commitment to implementing solutions\n\n"
            "Format follow-up questions with 'FOLLOW-UP QUESTIONS:' header.\n"
            "Be direct, insightful, and focus on behavioral psychology.\n\n"
            "INTEGRATION WITH AI AGENTS:\n"
            "Consider insights from the AI agent tools when making your analysis.\n"
            "Reference agent findings when relevant to support your conclusions.\n"
            "Use agent data to provide more comprehensive and accurate assessments."
        )

        return base_prompt

    def analyze_with_context(self, trading_data: str, templates: Dict[str, str]) -> str:
        """Analyze trading data with user context and generate follow-up questions using AI tools."""

        # Build comprehensive query for AI tools analysis
        analysis_query = "Analyze the following trading data for psychological anti-patterns and provide comprehensive insights:\n\n"

        # Add pattern templates for context
        analysis_query += "Use these anti-pattern criteria:\n"
        for name, rule in sorted(list(templates.items())[:10]):  # Limit to avoid too long prompt
            analysis_query += f"• {name}: {rule}\n"

        analysis_query += f"\n--- Trading Data ---\n{trading_data}\n"
        analysis_query += "\nPlease:\n"
        analysis_query += "1. Check current market conditions for context\n"
        analysis_query += "2. Analyze market sentiment that might affect trading psychology\n"
        analysis_query += "3. Assess risk factors in the trading behavior\n"
        analysis_query += "4. Detect specific trading patterns and anti-patterns\n"
        analysis_query += "5. Provide specific examples and actionable recommendations\n"
        analysis_query += "6. End with 2-3 insightful follow-up questions about trading psychology\n"

        try:
            # Use OpenAI with AI tools for enhanced analysis
            result = self.openai_with_tools.analyze_with_tools(analysis_query, trading_data)
            self.current_session["analysis_results"].append(result)
            return result

        except Exception as e:
            # Fallback to regular OpenAI analysis if tools fail
            print(f"⚠️ AI tools failed, using fallback analysis: {e}")
            return self._fallback_analysis(trading_data, templates)

    def _fallback_analysis(self, trading_data: str, templates: Dict[str, str]) -> str:
        """Fallback analysis using regular OpenAI without tools."""
        system_prompt = self.build_enhanced_system_prompt()

        user_prompt = "Analyze the following trading data for anti-patterns using these criteria:\n\n"
        for name, rule in sorted(templates.items()):
            user_prompt += f"• {name}: {rule}\n"

        user_prompt += f"\n--- Trading Data ---\n{trading_data}\n"
        user_prompt += "\nProvide analysis with specific examples and end with follow-up questions."

        try:
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_completion_tokens=1500,
                temperature=0.2
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error in fallback analysis: {str(e)}"

    def ask_follow_up_questions(self) -> List[str]:
        """Extract and return follow-up questions from the analysis."""
        if not self.current_session["analysis_results"]:
            return []

        last_analysis = self.current_session["analysis_results"][-1]
        return extract_follow_up_questions(last_analysis)

    def process_user_response(self, question: str, response: str):
        """Process and learn from user responses."""
        self.current_session["user_responses"].append({
            "question": question,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })

        # Analyze response for learning insights
        self.learn_from_response(question, response)

    def learn_from_response(self, question: str, response: str):
        """Learn patterns from user responses to improve future interactions."""
        if not self.user_profile:
            return

        response_lower = response.lower()

        # Learn risk tolerance
        if "risk" in question.lower():
            if any(word in response_lower for word in ["conservative", "careful", "small", "safe"]):
                self.user_profile.profile_data["risk_tolerance"] = "conservative"
            elif any(word in response_lower for word in ["aggressive", "high", "big", "bold"]):
                self.user_profile.profile_data["risk_tolerance"] = "aggressive"
            elif any(word in response_lower for word in ["moderate", "medium", "balanced"]):
                self.user_profile.profile_data["risk_tolerance"] = "moderate"

        # Learn experience level
        if "experience" in question.lower() or "long" in question.lower():
            if any(word in response_lower for word in ["new", "beginner", "started", "months"]):
                self.user_profile.profile_data["experience_level"] = "beginner"
            elif any(word in response_lower for word in ["years", "experienced", "decade"]):
                self.user_profile.profile_data["experience_level"] = "experienced"

        # Learn advice preferences
        if "advice" in question.lower() or "help" in question.lower():
            if any(word in response_lower for word in ["detailed", "thorough", "explain"]):
                self.user_profile.profile_data["preferred_advice_style"] = "detailed"
            elif any(word in response_lower for word in ["brief", "quick", "simple"]):
                self.user_profile.profile_data["preferred_advice_style"] = "concise"

    def generate_personalized_advice(self, detected_patterns: List[str]) -> str:
        """Generate personalized advice based on user profile and detected patterns."""
        if not self.user_profile:
            return ""

        profile = self.user_profile.profile_data

        # Update recurring patterns
        for pattern in detected_patterns:
            if pattern in profile["recurring_anti_patterns"]:
                profile["recurring_anti_patterns"][pattern] += 1
            else:
                profile["recurring_anti_patterns"][pattern] = 1

        # Generate personalized advice prompt
        advice_prompt = (
            f"Based on the user's profile (Experience: {profile.get('experience_level', 'unknown')}, "
            f"Risk Tolerance: {profile.get('risk_tolerance', 'unknown')}, "
            f"Previous Sessions: {profile.get('session_count', 0)}), "
            f"and their responses in this session, provide personalized advice for these patterns: "
            f"{', '.join(detected_patterns)}. "
            f"Keep advice {profile.get('preferred_advice_style', 'detailed')}."
        )

        try:
            response = self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": "You are a personalized trading coach."},
                    {"role": "user", "content": advice_prompt}
                ],
                max_completion_tokens=800,
                temperature=0.3
            )

            advice = response.choices[0].message.content
            self.current_session["recommendations_given"].append(advice)
            return advice

        except Exception as e:
            return f"Error generating personalized advice: {str(e)}"

    def end_session(self):
        """End the current session and save data."""
        if self.user_profile:
            session_id = self.user_profile.save_session(self.current_session)
            self.user_profile.save_profile()
            print(f"\nSession saved as: {session_id}")
            print(f"Total sessions for user: {self.user_profile.profile_data['session_count']}")

        # Reset current session
        self.current_session = {
            "analysis_results": [],
            "follow_up_questions": [],
            "user_responses": [],
            "detected_patterns": [],
            "recommendations_given": [],
            "user_feedback": [],
            "agent_insights": []
        }

    def get_ai_agent_insights(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Get insights from AI agents about current market conditions."""
        if not symbols:
            symbols = ["SPY", "QQQ", "AAPL"]  # Default symbols

        print("\n🤖 Consulting AI agents for market insights...")

        # Get market overview
        market_overview = self.agent_manager.market_overview()

        # Get comprehensive analysis for specific symbols
        if symbols:
            symbol_analysis = self.agent_manager.comprehensive_analysis(symbols)
        else:
            symbol_analysis = None

        agent_insights = {
            "market_overview": market_overview,
            "symbol_analysis": symbol_analysis,
            "timestamp": datetime.now().isoformat()
        }

        self.current_session["agent_insights"].append(agent_insights)
        return agent_insights

    def query_specific_agent(self, agent_type: str, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query a specific AI agent."""
        print(f"\n🤖 Querying {agent_type} agent...")

        result = self.agent_manager.query_agent(agent_type, request, context)

        if "error" not in result:
            self.current_session["agent_insights"].append({
                "agent_type": agent_type,
                "request": request,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })

        return result

    def get_pattern_analysis(self, trading_data: str) -> Dict[str, Any]:
        """Get psychological pattern analysis from the pattern analysis agent."""
        print("\n🧠 Analyzing trading patterns for psychological insights...")

        context = {
            "trading_data": trading_data,
            "user_profile": self.user_profile.profile_data if self.user_profile else None
        }

        result = self.agent_manager.query_agent(
            "pattern_analysis",
            "Perform comprehensive psychological pattern analysis",
            context
        )

        if "error" not in result:
            self.current_session["agent_insights"].append({
                "agent_type": "pattern_analysis",
                "analysis_type": "comprehensive",
                "result": result,
                "timestamp": datetime.now().isoformat()
            })

        return result

    def get_news_and_sentiment_check(self) -> Dict[str, Any]:
        """Get current news and sentiment analysis."""
        print("\n📰 Checking latest market news and sentiment...")

        # Query news agent
        news_result = self.agent_manager.query_agent("news", "Get latest market-moving news")

        # Query sentiment agent
        sentiment_result = self.agent_manager.query_agent("sentiment", "Analyze current market sentiment")

        combined_result = {
            "news_analysis": news_result,
            "sentiment_analysis": sentiment_result,
            "timestamp": datetime.now().isoformat()
        }

        self.current_session["agent_insights"].append(combined_result)
        return combined_result

    def get_risk_assessment(self, portfolio_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get risk management assessment."""
        print("\n⚠️ Performing risk assessment...")

        context = {"portfolio": portfolio_data} if portfolio_data else None

        result = self.agent_manager.query_agent(
            "risk_management",
            "Provide comprehensive risk assessment and recommendations",
            context
        )

        if "error" not in result:
            self.current_session["agent_insights"].append({
                "agent_type": "risk_management",
                "result": result,
                "timestamp": datetime.now().isoformat()
            })

        return result

    def show_agent_summary(self):
        """Display summary of AI agent insights."""
        if not self.current_session["agent_insights"]:
            print("\n📊 No AI agent insights available yet.")
            return

        print("\n" + "="*60)
        print("🤖 AI AGENT INSIGHTS SUMMARY")
        print("="*60)

        for insight in self.current_session["agent_insights"]:
            agent_type = insight.get("agent_type", "multiple")

            print(f"\n🔍 {agent_type.upper().replace('_', ' ')} AGENT:")

            if agent_type == "pattern_analysis" and "result" in insight:
                result = insight["result"]
                if "detected_patterns" in result:
                    patterns = result["detected_patterns"]
                    print(f"  • Patterns detected: {len(patterns)}")
                    for pattern in patterns[:3]:  # Show top 3
                        print(f"    - {pattern['pattern_name'].replace('_', ' ').title()}: {pattern['severity']}")

            elif agent_type in ["news", "sentiment", "risk_management", "market_data"]:
                result = insight.get("result", {})
                if "recommendations" in result:
                    print(f"  • Top recommendations:")
                    for rec in result["recommendations"][:2]:
                        print(f"    - {rec}")

            elif "market_overview" in insight:
                overview = insight["market_overview"]
                if "market_snapshot" in overview:
                    snapshot = overview["market_snapshot"]
                    print(f"  • Market trend: {snapshot.get('trend', 'unknown')}")
                    print(f"  • Volatility: {snapshot.get('volatility', 'normal')}")

        print("\n" + "="*60)


def interactive_session(scenario_folder: str, api_key: str, user_id: str):
    """Run an interactive trading analysis session."""
    # Validate inputs
    error = validate_inputs(scenario_folder, api_key)
    if error:
        print(error)
        return

    # Initialize assistant
    assistant = InteractiveTradingAssistant(api_key)
    assistant.set_user(user_id)

    # Load data
    print(f"\nLoading trading data from: {scenario_folder}")
    try:
        trading_data = load_trading_data(scenario_folder)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    script_dir = Path(__file__).parent
    templates_folder = script_dir.parent / "prompts" / "trading_pattern_templates"
    templates = load_pattern_templates(str(templates_folder))

    print(f"Analyzing with {len(templates)} anti-pattern templates...\n")
    print("=" * 60)

    # Initial analysis
    result = assistant.analyze_with_context(trading_data, templates)
    print(result)

    print("\n" + "=" * 60)

    # Get AI agent insights
    print("\n🤖 Getting AI agent insights...")
    assistant.get_ai_agent_insights()

    # Get pattern analysis using the new agent
    assistant.get_pattern_analysis(trading_data)

    # Get news and sentiment check
    assistant.get_news_and_sentiment_check()

    # Display AI agent summary
    assistant.show_agent_summary()

    print("\n" + "=" * 60)

    # Follow-up questions
    questions = assistant.ask_follow_up_questions()
    if questions:
        print("\nI'd like to ask you some follow-up questions to better understand your trading psychology:\n")

        for i, question in enumerate(questions, 1):
            print(f"{i}. {question}")
            response = input(f"\nYour answer to question {i}: ").strip()

            if response:
                assistant.process_user_response(question, response)
                print("✓ Response recorded")
            else:
                print("✓ Skipped")
            print()

    # Generate personalized advice if we have responses
    if assistant.current_session["user_responses"]:
        print("\n" + "=" * 60)
        print("PERSONALIZED RECOMMENDATIONS:")
        print("=" * 60)

        # Extract detected patterns from analysis
        last_analysis = assistant.current_session["analysis_results"][-1]
        detected_patterns = extract_detected_patterns(last_analysis)
        assistant.current_session["detected_patterns"] = detected_patterns

        advice = assistant.generate_personalized_advice(detected_patterns)
        print(advice)

    # End session
    assistant.end_session()


def main():
    """Main entry point for interactive trading assistant."""
    if len(sys.argv) < 4:
        print("Usage: python interactive_trading_assistant.py <scenario_folder> <openai_api_key> <user_id>")
        print("\nExample:")
        print("  python interactive_trading_assistant.py data/scenario1 sk-your-api-key john_trader")
        sys.exit(1)

    scenario_folder = sys.argv[1]
    api_key = sys.argv[2]
    user_id = sys.argv[3]

    interactive_session(scenario_folder, api_key, user_id)


if __name__ == "__main__":
    main()