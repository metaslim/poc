"""Interactive Trading Assistant with Learning Capabilities

This module provides an interactive trading assistant that can ask follow-up questions,
learn from user responses, and store user behavior for future analysis.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

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
    extract_follow_up_questions,
    extract_severity_levels
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
        self.user_profile = None
        self.current_session = {
            "analysis_results": [],
            "follow_up_questions": [],
            "user_responses": [],
            "detected_patterns": [],
            "recommendations_given": [],
            "user_feedback": []
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
            "Be direct, insightful, and focus on behavioral psychology."
        )

        return base_prompt

    def analyze_with_context(self, trading_data: str, templates: Dict[str, str]) -> str:
        """Analyze trading data with user context and generate follow-up questions."""
        system_prompt = self.build_enhanced_system_prompt()

        user_prompt = "Analyze the following trading data for anti-patterns using these criteria:\n\n"
        for name, rule in sorted(templates.items()):
            user_prompt += f"• {name}: {rule}\n"

        user_prompt += f"\n--- Trading Data ---\n{trading_data}\n"
        user_prompt += "\nProvide analysis with specific examples and end with follow-up questions."

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_completion_tokens=1500,
                temperature=0.2
            )

            result = response.choices[0].message.content
            self.current_session["analysis_results"].append(result)
            return result

        except Exception as e:
            return f"Error analyzing trading data: {str(e)}"

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
                model="gpt-4",
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
            "user_feedback": []
        }


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