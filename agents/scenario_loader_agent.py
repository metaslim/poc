"""Scenario Loader Agent

WHEN TO USE THIS AGENT:
- User asks to load/analyze a specific trading scenario (e.g., "load scenario1", "analyze scenario 3")
- User mentions "samples", "trading data", "scenario files", "CSV data"
- User wants to examine historical trading patterns from stored scenarios
- User asks about available scenarios or what scenarios exist
- Need to load trading data for pattern analysis

WHAT THIS AGENT DOES:
- Loads trading scenario data from CSV files in the samples/ folder
- Smart path resolution: accepts "1", "scenario1", or full paths
- Provides basic analysis of trade counts, symbols, buy/sell ratios
- Lists all available scenarios with descriptions
- Returns metadata about each scenario's focus (e.g., "FOMO patterns", "Risk management failures")

INPUT FORMATS ACCEPTED:
- Scenario numbers: "1", "2", "11" → converts to scenario1, scenario2, scenario11
- Scenario names: "scenario1", "scenario5"
- Partial matches: "fomo" might match scenario3 (FOMO patterns)
- Full paths: "samples/scenario1/sample_trades.csv"

OUTPUT FORMATS:
- "csv": Raw CSV data with metadata
- "analyzed": CSV data + basic trade analysis (counts, symbols, ratios)

EXAMPLE USE CASES:
- "Load scenario 1 for analysis" → loads scenario1 with basic stats
- "What scenarios are available?" → lists all scenarios with descriptions
- "Load FOMO scenario" → finds and loads scenario3 (FOMO patterns)
- "Analyze scenario5 trades" → loads scenario5 with trade analysis

Specialized agent for loading and analyzing trading scenarios from the samples folder.
"""

import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from .base_agent import BaseAgent


class ScenarioLoaderAgent(BaseAgent):
    """Agent specialized in loading trading scenarios and sample data."""

    def __init__(self):
        super().__init__("ScenarioLoader", "scenario_loader")

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process scenario loading requests."""
        self.simulate_processing_delay(0.2, 0.5)

        # Extract scenario identifier from request or context
        scenario = self._extract_scenario_from_request(request, context)

        if scenario:
            result = self.load_scenario(scenario)
        else:
            result = {
                "success": False,
                "error": "No scenario identifier found in request",
                "available_scenarios": self.list_available_scenarios()
            }

        self.log_request(request, result)
        return result

    def load_scenario(self, scenario: str, format: str = "csv") -> Dict[str, Any]:
        """Load trading scenario data from samples folder.

        This method loads trading scenarios from CSV files in the samples/ directory.
        It supports flexible input formats and provides optional analysis.

        Args:
            scenario (str): Scenario identifier. Accepts:
                          - Numbers: "1", "2", "11" → scenario1, scenario2, scenario11
                          - Names: "scenario1", "scenario5"
                          - Partial matches: searches scenario names/descriptions
                          - Full paths: "samples/scenario1/sample_trades.csv"
            format (str): Output format:
                         - "csv": Raw CSV data with metadata
                         - "analyzed": CSV data + trade analysis (counts, symbols, ratios)

        Returns:
            Dict containing:
                - success: bool indicating if load was successful
                - scenario_name: name of loaded scenario (e.g., "scenario1")
                - scenario_path: full file path to CSV
                - data: raw CSV content as string
                - metadata: scenario description and category info
                - analysis: (if format="analyzed") trade counts, symbols, buy/sell ratios
                - available_scenarios: (if scenario not found) list of available scenarios

        Example Usage:
            # Load scenario 1 with basic analysis
            result = agent.load_scenario("1", "analyzed")

            # Load scenario by name
            result = agent.load_scenario("scenario5", "csv")

            # Find scenario by pattern description
            result = agent.load_scenario("FOMO", "analyzed")  # finds scenario3
        """
        try:
            # Get scenario file path
            scenario_path = self._resolve_scenario_path(scenario)

            if not scenario_path or not os.path.exists(scenario_path):
                return {
                    "success": False,
                    "error": f"Scenario not found: {scenario}",
                    "available_scenarios": self.list_available_scenarios()
                }

            # Load scenario data
            with open(scenario_path, 'r') as f:
                scenario_data = f.read().strip()

            # Get scenario metadata
            scenario_name = Path(scenario_path).parent.name
            metadata = self.get_scenario_metadata(scenario_name)

            result = {
                "success": True,
                "scenario_name": scenario_name,
                "scenario_path": scenario_path,
                "data": scenario_data,
                "metadata": metadata,
                "format": format
            }

            # If analyzed format requested, add basic analysis
            if format == "analyzed":
                result["analysis"] = self.analyze_scenario_data(scenario_data, scenario_name)

            return result

        except Exception as e:
            return {
                "success": False,
                "error": f"Error loading scenario: {str(e)}",
                "scenario": scenario
            }

    def _resolve_scenario_path(self, scenario: str) -> Optional[str]:
        """Resolve scenario identifier to file path."""
        samples_dir = Path(__file__).parent.parent / "samples"

        if not samples_dir.exists():
            return None

        # Direct path provided
        if os.path.exists(scenario):
            return scenario

        # Check if it's a full path relative to project
        full_path = Path(__file__).parent.parent / scenario
        if full_path.exists():
            return str(full_path)

        # Scenario name (e.g., "scenario1")
        if scenario.startswith("scenario"):
            scenario_dir = samples_dir / scenario
            if scenario_dir.exists():
                csv_file = scenario_dir / "sample_trades.csv"
                if csv_file.exists():
                    return str(csv_file)

        # Scenario number (e.g., "1" -> "scenario1")
        try:
            scenario_num = int(scenario)
            scenario_name = f"scenario{scenario_num}"
            scenario_dir = samples_dir / scenario_name
            if scenario_dir.exists():
                csv_file = scenario_dir / "sample_trades.csv"
                if csv_file.exists():
                    return str(csv_file)
        except ValueError:
            pass

        # Partial name match
        for scenario_dir in samples_dir.iterdir():
            if scenario_dir.is_dir() and scenario.lower() in scenario_dir.name.lower():
                csv_file = scenario_dir / "sample_trades.csv"
                if csv_file.exists():
                    return str(csv_file)

        return None

    def list_available_scenarios(self) -> List[Dict[str, str]]:
        """List all available scenarios."""
        scenarios = []
        samples_dir = Path(__file__).parent.parent / "samples"

        if not samples_dir.exists():
            return scenarios

        for scenario_dir in sorted(samples_dir.iterdir()):
            if scenario_dir.is_dir():
                csv_file = scenario_dir / "sample_trades.csv"
                if csv_file.exists():
                    scenarios.append({
                        "name": scenario_dir.name,
                        "path": str(csv_file),
                        "description": self.get_scenario_description(scenario_dir.name)
                    })

        return scenarios

    def get_scenario_metadata(self, scenario_name: str) -> Dict[str, str]:
        """Get metadata for a scenario."""
        descriptions = {
            'scenario1': 'Premature profit-taking patterns',
            'scenario2': 'Averaging down addiction',
            'scenario3': 'FOMO and momentum chasing',
            'scenario4': 'Overtrading and impatience',
            'scenario5': 'Revenge trading behavior',
            'scenario6': 'Risk management failures',
            'scenario7': 'Emotional decision making',
            'scenario8': 'Market timing issues',
            'scenario9': 'Position sizing errors',
            'scenario10': 'Confirmation bias patterns',
            'scenario11': 'Correlation blindness'
        }

        return {
            "description": descriptions.get(scenario_name, "Trading psychology analysis"),
            "category": "trading_patterns",
            "analysis_focus": "behavioral_psychology"
        }

    def get_scenario_description(self, scenario_name: str) -> str:
        """Get description for a scenario."""
        return self.get_scenario_metadata(scenario_name)["description"]

    def analyze_scenario_data(self, scenario_data: str, scenario_name: str) -> Dict[str, Any]:
        """Provide basic analysis of scenario data."""
        lines = scenario_data.strip().split('\n')

        if len(lines) <= 1:
            return {"error": "Insufficient data for analysis"}

        # Count trades and extract basic stats
        trades = []
        symbols = set()
        actions = {"BUY": 0, "SELL": 0}

        for line in lines[1:]:  # Skip header
            parts = line.split(',')
            if len(parts) >= 6:
                action = parts[1].strip()
                symbol = parts[2].strip()
                quantity = parts[3].strip()
                price = parts[4].strip()

                trades.append({
                    "action": action,
                    "symbol": symbol,
                    "quantity": int(quantity) if quantity.isdigit() else 0,
                    "price": float(price) if price.replace('.', '').isdigit() else 0.0
                })

                symbols.add(symbol)
                actions[action] = actions.get(action, 0) + 1

        return {
            "total_trades": len(trades),
            "unique_symbols": len(symbols),
            "symbols": list(symbols),
            "buy_trades": actions.get("BUY", 0),
            "sell_trades": actions.get("SELL", 0),
            "scenario_focus": self.get_scenario_metadata(scenario_name)["description"],
            "ready_for_pattern_analysis": len(trades) > 0
        }

    def _extract_scenario_from_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Extract scenario identifier from request or context."""
        # Check context first
        if context and "scenario" in context:
            return str(context["scenario"])

        # Extract from request
        request_lower = request.lower()

        # Look for scenario patterns
        import re
        scenario_patterns = [
            r'scenario\s*(\d+)',
            r'scenario(\d+)',
            r'sample\s*(\d+)',
            r'load\s+(\d+)',
            r'analyze\s+(\d+)'
        ]

        for pattern in scenario_patterns:
            match = re.search(pattern, request_lower)
            if match:
                return match.group(1)

        # Look for explicit scenario names
        for i in range(1, 12):
            scenario_name = f"scenario{i}"
            if scenario_name in request_lower:
                return str(i)

        # Look for general scenario loading requests
        if any(word in request_lower for word in ["scenario", "sample", "load", "trading data"]):
            return "1"  # Default to scenario 1

        return None