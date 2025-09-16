"""Market Data Agent

Agent specialized in providing real-time market data, price analysis, and technical indicators.
"""

import random
from typing import Dict, Any, Optional, List
from datetime import datetime
from .base_agent import BaseAgent


class MarketDataAgent(BaseAgent):
    """Agent for market data and price analysis."""

    def __init__(self):
        super().__init__("MarketDataBot", "market_analysis")
        self.fake_market_data = self._generate_fake_market_data()

    def _generate_fake_market_data(self) -> Dict[str, Any]:
        """Generate realistic fake market data."""
        base_prices = {
            "SPY": 450.25,
            "QQQ": 375.80,
            "IWM": 195.45,
            "AAPL": 175.30,
            "MSFT": 338.50,
            "GOOGL": 138.75,
            "TSLA": 248.90,
            "NVDA": 465.20,
            "META": 325.15,
            "AMZN": 145.60,
            "BTC": 43250.00,
            "ETH": 2650.00,
            "GLD": 185.90,
            "TLT": 95.40,
            "VIX": 16.25
        }

        market_data = {}
        for symbol, base_price in base_prices.items():
            change_percent = random.uniform(-3.0, 3.0)
            current_price = base_price * (1 + change_percent / 100)
            change_dollar = current_price - base_price

            market_data[symbol] = {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "change_dollar": round(change_dollar, 2),
                "change_percent": round(change_percent, 2),
                "volume": random.randint(1000000, 50000000),
                "high_52w": round(base_price * random.uniform(1.1, 1.5), 2),
                "low_52w": round(base_price * random.uniform(0.6, 0.9), 2),
                "market_cap": f"{random.randint(50, 3000)}B" if symbol in ["AAPL", "MSFT", "GOOGL"] else f"{random.randint(10, 500)}B",
                "pe_ratio": round(random.uniform(15, 35), 1),
                "beta": round(random.uniform(0.5, 2.0), 2),
                "rsi": round(random.uniform(30, 70), 1),
                "sma_50": round(current_price * random.uniform(0.95, 1.05), 2),
                "sma_200": round(current_price * random.uniform(0.90, 1.10), 2),
                "last_updated": datetime.now().isoformat()
            }

        return market_data

    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process market data request."""
        self.simulate_processing_delay(0.5, 2.0)

        request_lower = request.lower()
        response_data = {"agent": self.agent_name, "type": "market_data", "timestamp": datetime.now().isoformat()}

        # Context can be used for specific symbols or data requests in future versions
        _ = context  # Acknowledge parameter for future use

        if "price" in request_lower or "quote" in request_lower:
            symbols = self.extract_symbols_from_request(request)
            response_data["data_type"] = "price_quotes"
            response_data["symbols"] = symbols
            response_data["quotes"] = {symbol: self.fake_market_data.get(symbol, self._get_unknown_symbol_data(symbol)) for symbol in symbols}

        elif "technical" in request_lower or "indicators" in request_lower:
            symbols = self.extract_symbols_from_request(request)
            response_data["data_type"] = "technical_analysis"
            response_data["analysis"] = self._generate_technical_analysis(symbols)

        elif "market" in request_lower and ("condition" in request_lower or "overview" in request_lower):
            response_data["data_type"] = "market_conditions"
            response_data["market_overview"] = self._generate_market_overview()

        elif "volatility" in request_lower or "vix" in request_lower:
            response_data["data_type"] = "volatility_analysis"
            response_data["volatility_data"] = self._generate_volatility_analysis()

        elif "sector" in request_lower or "rotation" in request_lower:
            response_data["data_type"] = "sector_analysis"
            response_data["sector_performance"] = self._generate_sector_performance()

        else:
            # Default: provide market summary
            response_data["data_type"] = "market_summary"
            response_data["summary"] = self._generate_market_summary()

        self.log_request(request, response_data)
        return response_data


    def _get_unknown_symbol_data(self, symbol: str) -> Dict[str, Any]:
        """Generate fake data for unknown symbols."""
        base_price = random.uniform(10, 200)
        change_percent = random.uniform(-5.0, 5.0)
        current_price = base_price * (1 + change_percent / 100)

        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "change_dollar": round(current_price - base_price, 2),
            "change_percent": round(change_percent, 2),
            "volume": random.randint(100000, 10000000),
            "rsi": round(random.uniform(30, 70), 1),
            "last_updated": datetime.now().isoformat(),
            "note": "Simulated data for unknown symbol"
        }

    def _generate_technical_analysis(self, symbols: List[str]) -> Dict[str, Any]:
        """Generate technical analysis for given symbols."""
        analysis = {}

        for symbol in symbols:
            data = self.fake_market_data.get(symbol, self._get_unknown_symbol_data(symbol))

            # Generate technical signals
            signals = []
            if data["rsi"] > 70:
                signals.append("Overbought - potential sell signal")
            elif data["rsi"] < 30:
                signals.append("Oversold - potential buy signal")

            if data["current_price"] > data["sma_50"] > data["sma_200"]:
                signals.append("Bullish trend - price above moving averages")
            elif data["current_price"] < data["sma_50"] < data["sma_200"]:
                signals.append("Bearish trend - price below moving averages")

            support_level = round(data["current_price"] * random.uniform(0.95, 0.98), 2)
            resistance_level = round(data["current_price"] * random.uniform(1.02, 1.05), 2)

            analysis[symbol] = {
                "symbol": symbol,
                "current_price": data["current_price"],
                "rsi": data["rsi"],
                "sma_50": data["sma_50"],
                "sma_200": data["sma_200"],
                "support_level": support_level,
                "resistance_level": resistance_level,
                "signals": signals,
                "recommendation": random.choice(["BUY", "SELL", "HOLD"]),
                "confidence": round(random.uniform(0.6, 0.9), 2)
            }

        return analysis

    def _generate_market_overview(self) -> Dict[str, Any]:
        """Generate overall market conditions analysis."""
        spy_data = self.fake_market_data["SPY"]
        vix_data = self.fake_market_data["VIX"]

        market_trend = "bullish" if spy_data["change_percent"] > 0 else "bearish"
        volatility_level = "high" if vix_data["current_price"] > 20 else "low" if vix_data["current_price"] < 15 else "moderate"

        return {
            "market_trend": market_trend,
            "spy_performance": {
                "price": spy_data["current_price"],
                "change_percent": spy_data["change_percent"]
            },
            "volatility_level": volatility_level,
            "vix_reading": vix_data["current_price"],
            "breadth": {
                "advancing": random.randint(1500, 2500),
                "declining": random.randint(1200, 2000),
                "unchanged": random.randint(200, 500)
            },
            "sector_leaders": random.sample(["Technology", "Healthcare", "Finance", "Energy", "Consumer"], 2),
            "sector_laggards": random.sample(["Utilities", "REITs", "Materials", "Industrial"], 2)
        }

    def _generate_volatility_analysis(self) -> Dict[str, Any]:
        """Generate volatility analysis."""
        vix_data = self.fake_market_data["VIX"]

        return {
            "vix_current": vix_data["current_price"],
            "vix_change": vix_data["change_percent"],
            "interpretation": self._interpret_vix(vix_data["current_price"]),
            "historical_percentile": random.randint(25, 85),
            "term_structure": {
                "vix9d": round(vix_data["current_price"] * random.uniform(0.9, 1.1), 2),
                "vix": vix_data["current_price"],
                "vix3m": round(vix_data["current_price"] * random.uniform(1.0, 1.2), 2),
                "vix6m": round(vix_data["current_price"] * random.uniform(1.1, 1.3), 2)
            },
            "volatility_regime": "low" if vix_data["current_price"] < 15 else "high" if vix_data["current_price"] > 25 else "normal"
        }

    def _interpret_vix(self, vix_level: float) -> str:
        """Interpret VIX level."""
        if vix_level < 12:
            return "Extremely low fear - potential complacency"
        elif vix_level < 15:
            return "Low fear - generally bullish environment"
        elif vix_level < 20:
            return "Normal volatility levels"
        elif vix_level < 30:
            return "Elevated fear - market uncertainty"
        else:
            return "High fear - potential market stress"

    def _generate_sector_performance(self) -> Dict[str, Any]:
        """Generate sector performance data."""
        sectors = [
            "Technology", "Healthcare", "Finance", "Consumer Discretionary",
            "Industrial", "Energy", "Materials", "Utilities", "REITs",
            "Communication", "Consumer Staples"
        ]

        performance = {}
        for sector in sectors:
            performance[sector] = {
                "change_percent": round(random.uniform(-2.5, 2.5), 2),
                "relative_strength": round(random.uniform(0.8, 1.2), 2),
                "momentum": random.choice(["Strong", "Moderate", "Weak"]),
                "outlook": random.choice(["Bullish", "Neutral", "Bearish"])
            }

        # Sort by performance
        sorted_sectors = sorted(performance.items(), key=lambda x: x[1]["change_percent"], reverse=True)

        return {
            "sector_performance": performance,
            "top_performers": [sector[0] for sector in sorted_sectors[:3]],
            "worst_performers": [sector[0] for sector in sorted_sectors[-3:]],
            "rotation_signal": random.choice([
                "Growth to Value rotation detected",
                "Value to Growth rotation detected",
                "Defensive rotation underway",
                "Risk-on sentiment prevailing",
                "No clear rotation pattern"
            ])
        }

    def _generate_market_summary(self) -> Dict[str, Any]:
        """Generate comprehensive market summary."""
        major_indices = ["SPY", "QQQ", "IWM"]
        summary = {
            "indices_performance": {},
            "key_movers": self._get_key_movers(),
            "market_breadth": self._generate_market_breadth(),
            "key_levels": self._generate_key_levels()
        }

        for index in major_indices:
            data = self.fake_market_data[index]
            summary["indices_performance"][index] = {
                "price": data["current_price"],
                "change_percent": data["change_percent"],
                "volume": data["volume"]
            }

        return summary

    def _get_key_movers(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get top gainers and losers."""
        stocks = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META", "AMZN"]
        stock_data = [(symbol, self.fake_market_data[symbol]) for symbol in stocks]

        sorted_by_change = sorted(stock_data, key=lambda x: x[1]["change_percent"], reverse=True)

        return {
            "top_gainers": [
                {"symbol": item[0], "change_percent": item[1]["change_percent"]}
                for item in sorted_by_change[:3]
            ],
            "top_losers": [
                {"symbol": item[0], "change_percent": item[1]["change_percent"]}
                for item in sorted_by_change[-3:]
            ]
        }

    def _generate_market_breadth(self) -> Dict[str, Any]:
        """Generate market breadth indicators."""
        return {
            "advance_decline_ratio": round(random.uniform(0.8, 1.5), 2),
            "new_highs": random.randint(50, 300),
            "new_lows": random.randint(20, 150),
            "up_volume_ratio": round(random.uniform(0.4, 0.8), 2),
            "breadth_momentum": random.choice(["Positive", "Negative", "Neutral"])
        }

    def _generate_key_levels(self) -> Dict[str, Any]:
        """Generate key support and resistance levels for major indices."""
        spy_price = self.fake_market_data["SPY"]["current_price"]

        return {
            "SPY": {
                "current": spy_price,
                "support": round(spy_price * 0.98, 2),
                "resistance": round(spy_price * 1.02, 2),
                "key_level": round(spy_price * random.choice([0.95, 1.05]), 2)
            }
        }