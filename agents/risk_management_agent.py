"""Risk Management Agent

Agent specialized in portfolio risk assessment, position sizing, and risk mitigation strategies.
"""

import random
import math
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent


class RiskManagementAgent(BaseAgent):
    """Agent for portfolio risk management and position sizing."""

    def __init__(self):
        super().__init__("RiskBot", "risk_management")

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process risk management request."""
        self.simulate_processing_delay(0.8, 2.0)

        request_lower = request.lower()

        if "portfolio" in request_lower and ("risk" in request_lower or "var" in request_lower):
            response_data = self._analyze_portfolio_risk(context)
        elif "position" in request_lower and "size" in request_lower:
            response_data = self._calculate_position_sizing(context)
        elif "correlation" in request_lower:
            response_data = self._analyze_correlations(context)
        elif "volatility" in request_lower or "vol" in request_lower:
            response_data = self._analyze_volatility_risk(context)
        elif "drawdown" in request_lower:
            response_data = self._analyze_drawdown_risk(context)
        else:
            response_data = self._comprehensive_risk_assessment(context)

        response_data.update({
            "agent": self.agent_name,
            "type": "risk_management",
            "timestamp": datetime.now().isoformat()
        })

        self.log_request(request, response_data)
        return response_data

    def _analyze_portfolio_risk(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall portfolio risk metrics."""
        # Simulate portfolio positions if not provided
        portfolio = context.get("portfolio") if context else self._generate_sample_portfolio()

        portfolio_value = sum(pos["market_value"] for pos in portfolio["positions"])
        daily_var_95 = self._calculate_var(portfolio["positions"], 0.95)
        daily_var_99 = self._calculate_var(portfolio["positions"], 0.99)

        return {
            "analysis_type": "portfolio_risk",
            "portfolio_metrics": {
                "total_value": portfolio_value,
                "position_count": len(portfolio["positions"]),
                "daily_var_95": daily_var_95,
                "daily_var_99": daily_var_99,
                "expected_shortfall": daily_var_99 * 1.3,  # Simplified ES calculation
                "beta": self._calculate_portfolio_beta(portfolio["positions"]),
                "sharpe_ratio": round(random.uniform(0.5, 2.5), 2),
                "max_drawdown": round(random.uniform(0.05, 0.25), 3),
                "volatility": round(random.uniform(0.15, 0.35), 3)
            },
            "concentration_risk": self._analyze_concentration(portfolio["positions"]),
            "sector_exposure": self._analyze_sector_exposure(portfolio["positions"]),
            "risk_warnings": self._generate_risk_warnings(portfolio["positions"]),
            "recommendations": self._generate_risk_recommendations(portfolio["positions"])
        }

    def _calculate_position_sizing(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate optimal position sizing based on risk parameters."""
        # Default risk parameters if not provided in context
        risk_params = {
            "account_size": 100000,
            "risk_per_trade": 0.02,  # 2% risk per trade
            "stop_loss_pct": 0.05,   # 5% stop loss
            "target_symbol": "AAPL",
            "entry_price": 175.0,
            "volatility": 0.25
        }

        if context:
            risk_params.update(context.get("risk_params", {}))

        # Kelly Criterion calculation
        win_rate = random.uniform(0.45, 0.65)
        avg_win = random.uniform(1.5, 3.0)
        avg_loss = 1.0  # Normalized
        kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win

        # Position sizing calculations
        risk_amount = risk_params["account_size"] * risk_params["risk_per_trade"]
        stop_loss_distance = risk_params["entry_price"] * risk_params["stop_loss_pct"]
        shares_risk_based = int(risk_amount / stop_loss_distance)

        # Volatility-based sizing
        target_vol = 0.15  # Target 15% portfolio volatility
        vol_based_weight = target_vol / risk_params["volatility"]
        shares_vol_based = int((risk_params["account_size"] * vol_based_weight) / risk_params["entry_price"])

        # Kelly-based sizing (conservative)
        kelly_conservative = max(0.05, min(0.25, kelly_fraction * 0.5))  # Cap Kelly at 25%
        shares_kelly = int((risk_params["account_size"] * kelly_conservative) / risk_params["entry_price"])

        return {
            "analysis_type": "position_sizing",
            "symbol": risk_params["target_symbol"],
            "entry_price": risk_params["entry_price"],
            "sizing_methods": {
                "risk_based": {
                    "shares": shares_risk_based,
                    "position_value": shares_risk_based * risk_params["entry_price"],
                    "portfolio_weight": (shares_risk_based * risk_params["entry_price"]) / risk_params["account_size"],
                    "max_loss": risk_amount
                },
                "volatility_based": {
                    "shares": shares_vol_based,
                    "position_value": shares_vol_based * risk_params["entry_price"],
                    "portfolio_weight": vol_based_weight,
                    "expected_volatility": risk_params["volatility"]
                },
                "kelly_based": {
                    "shares": shares_kelly,
                    "position_value": shares_kelly * risk_params["entry_price"],
                    "portfolio_weight": kelly_conservative,
                    "kelly_fraction": kelly_fraction,
                    "win_rate": win_rate,
                    "reward_risk_ratio": avg_win
                }
            },
            "recommended_sizing": {
                "shares": min(shares_risk_based, shares_vol_based),  # Conservative approach
                "rationale": "Using minimum of risk-based and volatility-based sizing for conservative approach",
                "stop_loss_price": risk_params["entry_price"] * (1 - risk_params["stop_loss_pct"]),
                "risk_reward_ratio": "1:2 minimum recommended"
            }
        }

    def _analyze_correlations(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze correlation risks in portfolio."""
        # Generate correlation matrix for common assets
        assets = ["SPY", "QQQ", "IWM", "GLD", "TLT", "VIX", "BTC", "USD"]
        correlation_matrix = {}

        for asset1 in assets:
            correlation_matrix[asset1] = {}
            for asset2 in assets:
                if asset1 == asset2:
                    correlation_matrix[asset1][asset2] = 1.0
                else:
                    # Generate realistic correlations
                    if (asset1, asset2) in [("SPY", "QQQ"), ("QQQ", "SPY")]:
                        corr = round(random.uniform(0.85, 0.95), 3)
                    elif (asset1, asset2) in [("SPY", "GLD"), ("GLD", "SPY")]:
                        corr = round(random.uniform(-0.3, -0.1), 3)
                    elif (asset1, asset2) in [("SPY", "VIX"), ("VIX", "SPY")]:
                        corr = round(random.uniform(-0.8, -0.6), 3)
                    else:
                        corr = round(random.uniform(-0.5, 0.7), 3)
                    correlation_matrix[asset1][asset2] = corr

        # Identify high correlation clusters
        high_corr_pairs = []
        for asset1 in assets:
            for asset2 in assets:
                if asset1 < asset2 and abs(correlation_matrix[asset1][asset2]) > 0.7:
                    high_corr_pairs.append({
                        "asset1": asset1,
                        "asset2": asset2,
                        "correlation": correlation_matrix[asset1][asset2],
                        "type": "positive" if correlation_matrix[asset1][asset2] > 0 else "negative"
                    })

        return {
            "analysis_type": "correlation_analysis",
            "correlation_matrix": correlation_matrix,
            "high_correlation_pairs": high_corr_pairs,
            "diversification_score": round(random.uniform(0.4, 0.8), 2),
            "risk_clusters": {
                "technology_cluster": ["QQQ", "TECH_STOCKS"],
                "safe_haven_cluster": ["GLD", "TLT"],
                "risk_on_cluster": ["SPY", "IWM", "BTC"]
            },
            "correlation_warnings": self._generate_correlation_warnings(high_corr_pairs),
            "diversification_suggestions": [
                "Consider adding uncorrelated assets like commodities",
                "International exposure could reduce US market correlation",
                "Alternative investments (REITs, crypto) may provide diversification",
                "Consider currency hedged positions for international exposure"
            ]
        }

    def _analyze_volatility_risk(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze volatility-based risks."""
        # Generate volatility data for different timeframes
        vol_data = {
            "realized_vol_30d": round(random.uniform(0.15, 0.45), 3),
            "realized_vol_90d": round(random.uniform(0.18, 0.35), 3),
            "implied_vol": round(random.uniform(0.20, 0.50), 3),
            "vol_of_vol": round(random.uniform(0.05, 0.15), 3),
            "vol_regime": random.choice(["low", "normal", "elevated", "high"])
        }

        vol_percentile = random.randint(15, 85)

        return {
            "analysis_type": "volatility_risk",
            "volatility_metrics": vol_data,
            "volatility_percentile": vol_percentile,
            "volatility_forecast": {
                "1_week": round(vol_data["realized_vol_30d"] * random.uniform(0.9, 1.1), 3),
                "1_month": round(vol_data["realized_vol_30d"] * random.uniform(0.95, 1.05), 3),
                "3_months": round(vol_data["realized_vol_90d"], 3)
            },
            "volatility_trading_signals": {
                "vol_mean_reversion": "vol likely to decrease" if vol_percentile > 70 else "vol may increase",
                "term_structure": random.choice(["backwardation", "contango", "flat"]),
                "volatility_risk_premium": round(random.uniform(0.02, 0.08), 3)
            },
            "position_adjustments": self._suggest_vol_adjustments(vol_data, vol_percentile)
        }

    def _analyze_drawdown_risk(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze potential drawdown scenarios."""
        # Generate drawdown scenarios
        scenarios = {
            "mild_correction": {"probability": 0.35, "drawdown": round(random.uniform(0.05, 0.10), 3)},
            "moderate_correction": {"probability": 0.25, "drawdown": round(random.uniform(0.10, 0.20), 3)},
            "bear_market": {"probability": 0.15, "drawdown": round(random.uniform(0.20, 0.35), 3)},
            "crash_scenario": {"probability": 0.05, "drawdown": round(random.uniform(0.35, 0.55), 3)}
        }

        portfolio_value = 100000  # Default portfolio value
        if context and "portfolio" in context:
            portfolio_value = sum(pos["market_value"] for pos in context["portfolio"]["positions"])

        scenario_impacts = {}
        for scenario, data in scenarios.items():
            loss_amount = portfolio_value * data["drawdown"]
            scenario_impacts[scenario] = {
                "probability": data["probability"],
                "drawdown_percent": data["drawdown"],
                "loss_amount": loss_amount,
                "recovery_time": self._estimate_recovery_time(data["drawdown"])
            }

        return {
            "analysis_type": "drawdown_risk",
            "current_portfolio_value": portfolio_value,
            "drawdown_scenarios": scenario_impacts,
            "historical_context": {
                "avg_correction_frequency": "Every 1.5 years",
                "avg_bear_market_frequency": "Every 7-10 years",
                "typical_recovery_time": "6-18 months for corrections, 2-4 years for bear markets"
            },
            "protection_strategies": [
                "Maintain 10-20% cash position for opportunities",
                "Consider put protection for large positions",
                "Diversify across asset classes and geographies",
                "Use stop losses on individual positions",
                "Regular rebalancing to maintain target allocations"
            ],
            "stress_test_results": self._run_stress_tests(portfolio_value)
        }

    def _comprehensive_risk_assessment(self, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive risk analysis combining all risk factors."""
        portfolio = context.get("portfolio") if context else self._generate_sample_portfolio()

        risk_score = self._calculate_overall_risk_score(portfolio)

        return {
            "analysis_type": "comprehensive_risk",
            "overall_risk_score": risk_score,
            "risk_breakdown": {
                "market_risk": round(random.uniform(0.3, 0.8), 2),
                "concentration_risk": round(random.uniform(0.2, 0.7), 2),
                "liquidity_risk": round(random.uniform(0.1, 0.5), 2),
                "currency_risk": round(random.uniform(0.1, 0.4), 2),
                "sector_risk": round(random.uniform(0.2, 0.6), 2)
            },
            "risk_capacity": self._assess_risk_capacity(),
            "risk_tolerance_mismatch": random.choice([True, False]),
            "immediate_actions": self._suggest_immediate_actions(risk_score),
            "long_term_recommendations": self._suggest_long_term_risk_management()
        }

    def _generate_sample_portfolio(self) -> Dict[str, Any]:
        """Generate sample portfolio for demonstration."""
        positions = [
            {"symbol": "AAPL", "shares": 100, "avg_cost": 170.0, "market_price": 175.0, "market_value": 17500, "sector": "Technology"},
            {"symbol": "MSFT", "shares": 50, "avg_cost": 330.0, "market_price": 338.0, "market_value": 16900, "sector": "Technology"},
            {"symbol": "GOOGL", "shares": 75, "avg_cost": 135.0, "market_price": 139.0, "market_value": 10425, "sector": "Technology"},
            {"symbol": "JPM", "shares": 60, "avg_cost": 145.0, "market_price": 150.0, "market_value": 9000, "sector": "Finance"},
            {"symbol": "JNJ", "shares": 80, "avg_cost": 160.0, "market_price": 155.0, "market_value": 12400, "sector": "Healthcare"}
        ]
        return {"positions": positions}

    def _calculate_var(self, positions: List[Dict[str, Any]], confidence: float) -> float:
        """Calculate Value at Risk for portfolio."""
        total_value = sum(pos["market_value"] for pos in positions)
        # Simplified VaR calculation using normal distribution assumption
        portfolio_vol = random.uniform(0.15, 0.25)  # Assume portfolio volatility
        from scipy.stats import norm
        var_multiplier = norm.ppf(confidence)
        daily_var = total_value * portfolio_vol * var_multiplier / math.sqrt(252)
        return round(abs(daily_var), 2)

    def _calculate_portfolio_beta(self, positions: List[Dict[str, Any]]) -> float:
        """Calculate portfolio beta."""
        # Simplified beta calculation with assumed individual betas
        beta_map = {"AAPL": 1.2, "MSFT": 0.9, "GOOGL": 1.1, "JPM": 1.3, "JNJ": 0.7}
        total_value = sum(pos["market_value"] for pos in positions)

        weighted_beta = 0
        for pos in positions:
            weight = pos["market_value"] / total_value
            beta = beta_map.get(pos["symbol"], 1.0)
            weighted_beta += weight * beta

        return round(weighted_beta, 2)

    def _analyze_concentration(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze portfolio concentration risk."""
        total_value = sum(pos["market_value"] for pos in positions)
        largest_position = max(pos["market_value"] for pos in positions) / total_value

        # Sector concentration
        sector_exposure = {}
        for pos in positions:
            sector = pos.get("sector", "Unknown")
            sector_exposure[sector] = sector_exposure.get(sector, 0) + pos["market_value"]

        largest_sector = max(sector_exposure.values()) / total_value

        return {
            "largest_position_pct": round(largest_position, 3),
            "largest_sector_pct": round(largest_sector, 3),
            "sector_breakdown": {k: round(v/total_value, 3) for k, v in sector_exposure.items()},
            "concentration_score": round((largest_position + largest_sector) / 2, 2),
            "is_concentrated": largest_position > 0.2 or largest_sector > 0.4
        }

    def _analyze_sector_exposure(self, positions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sector exposure and diversification."""
        sector_weights = {}
        total_value = sum(pos["market_value"] for pos in positions)

        for pos in positions:
            sector = pos.get("sector", "Unknown")
            sector_weights[sector] = sector_weights.get(sector, 0) + pos["market_value"] / total_value

        return {
            "sector_weights": {k: round(v, 3) for k, v in sector_weights.items()},
            "diversification_score": round(1 - sum(w**2 for w in sector_weights.values()), 3),
            "overweight_sectors": [k for k, v in sector_weights.items() if v > 0.25],
            "underweight_sectors": ["Energy", "Utilities", "Real Estate"]  # Sectors not in portfolio
        }

    def _generate_risk_warnings(self, positions: List[Dict[str, Any]]) -> List[str]:
        """Generate risk warnings based on portfolio analysis."""
        warnings = []
        concentration_data = self._analyze_concentration(positions)

        if concentration_data["largest_position_pct"] > 0.2:
            warnings.append(f"High single-position concentration: {concentration_data['largest_position_pct']:.1%}")

        if concentration_data["largest_sector_pct"] > 0.5:
            warnings.append(f"Excessive sector concentration: {concentration_data['largest_sector_pct']:.1%}")

        # Check for tech overweight
        tech_weight = concentration_data["sector_breakdown"].get("Technology", 0)
        if tech_weight > 0.4:
            warnings.append(f"Technology sector overweight: {tech_weight:.1%}")

        return warnings

    def _generate_risk_recommendations(self, positions: List[Dict[str, Any]]) -> List[str]:
        """Generate risk management recommendations."""
        recommendations = [
            "Consider rebalancing if any position exceeds 15% of portfolio",
            "Add defensive sectors like utilities or consumer staples",
            "Consider international diversification",
            "Maintain 5-10% cash position for opportunities",
            "Review and update stop losses quarterly"
        ]
        return recommendations

    def _generate_correlation_warnings(self, high_corr_pairs: List[Dict[str, Any]]) -> List[str]:
        """Generate warnings about high correlations."""
        warnings = []
        for pair in high_corr_pairs:
            if pair["correlation"] > 0.8:
                warnings.append(f"Very high positive correlation between {pair['asset1']} and {pair['asset2']}: {pair['correlation']:.2f}")
        return warnings

    def _suggest_vol_adjustments(self, vol_data: Dict[str, Any], percentile: int) -> List[str]:
        """Suggest position adjustments based on volatility."""
        suggestions = []

        if percentile > 80:
            suggestions.append("Consider reducing position sizes due to elevated volatility")
            suggestions.append("Tighten stop losses to account for increased risk")
        elif percentile < 20:
            suggestions.append("Low volatility environment - consider increasing position sizes")
            suggestions.append("Look for volatility selling opportunities")

        if vol_data["vol_regime"] == "high":
            suggestions.append("High volatility regime - focus on defensive strategies")

        return suggestions

    def _estimate_recovery_time(self, drawdown: float) -> str:
        """Estimate recovery time from drawdown."""
        if drawdown < 0.1:
            return "2-6 months"
        elif drawdown < 0.2:
            return "6-12 months"
        elif drawdown < 0.35:
            return "1-3 years"
        else:
            return "3-5 years"

    def _run_stress_tests(self, portfolio_value: float) -> Dict[str, Any]:
        """Run various stress test scenarios."""
        return {
            "2008_financial_crisis": {"loss_pct": 0.37, "loss_amount": portfolio_value * 0.37},
            "2020_covid_crash": {"loss_pct": 0.34, "loss_amount": portfolio_value * 0.34},
            "2000_dotcom_crash": {"loss_pct": 0.49, "loss_amount": portfolio_value * 0.49},
            "interest_rate_shock": {"loss_pct": 0.15, "loss_amount": portfolio_value * 0.15}
        }

    def _calculate_overall_risk_score(self, portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall risk score (1-10 scale)."""
        base_score = random.uniform(4, 8)
        return {
            "score": round(base_score, 1),
            "scale": "1 (very low risk) to 10 (very high risk)",
            "category": "moderate" if base_score < 6 else "high" if base_score < 8 else "very high"
        }

    def _assess_risk_capacity(self) -> Dict[str, Any]:
        """Assess investor's risk capacity."""
        return {
            "time_horizon": random.choice(["short-term (<3 years)", "medium-term (3-10 years)", "long-term (>10 years)"]),
            "liquidity_needs": random.choice(["low", "moderate", "high"]),
            "income_stability": random.choice(["stable", "variable", "uncertain"]),
            "overall_capacity": random.choice(["conservative", "moderate", "aggressive"])
        }

    def _suggest_immediate_actions(self, risk_score: Dict[str, Any]) -> List[str]:
        """Suggest immediate risk management actions."""
        if risk_score["score"] > 7:
            return [
                "Reduce position sizes immediately",
                "Implement stop losses on all positions",
                "Consider hedging strategies",
                "Increase cash allocation"
            ]
        else:
            return [
                "Review and update risk management rules",
                "Monitor correlation changes",
                "Rebalance if needed"
            ]

    def _suggest_long_term_risk_management(self) -> List[str]:
        """Suggest long-term risk management strategies."""
        return [
            "Develop and stick to asset allocation policy",
            "Regular portfolio rebalancing (quarterly)",
            "Diversify across asset classes and geographies",
            "Consider alternative investments for diversification",
            "Regular risk assessment and adjustment"
        ]