"""AI Agents Package

Collection of specialized AI agents for trading analysis and decision making.
"""

from .base_agent import BaseAgent
from .news_agent import NewsAgent
from .market_data_agent import MarketDataAgent
from .sentiment_agent import SentimentAgent
from .risk_management_agent import RiskManagementAgent
from .pattern_analysis_agent import PatternAnalysisAgent
from .scenario_loader_agent import ScenarioLoaderAgent
from .comprehensive_analysis_agent import ComprehensiveAnalysisAgent
from .market_conditions_agent import MarketConditionsAgent
from .agent_manager import AgentManager
from .tool_integration import AgentToolRegistry, SmartTradingAgent

__all__ = [
    "BaseAgent",
    "NewsAgent",
    "MarketDataAgent",
    "SentimentAgent",
    "RiskManagementAgent",
    "PatternAnalysisAgent",
    "ScenarioLoaderAgent",
    "ComprehensiveAnalysisAgent",
    "MarketConditionsAgent",
    "AgentManager",
    "AgentToolRegistry",
    "SmartTradingAgent"
]