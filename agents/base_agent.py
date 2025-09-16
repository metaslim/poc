"""Base Agent Interface

Abstract base class for all AI agents with common functionality.
"""

import json
import time
import random
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for AI agents."""

    def __init__(self, agent_name: str, agent_type: str):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.created_at = datetime.now()
        self.last_request = None
        self.request_count = 0

    @abstractmethod
    def process_request(self, request: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a request and return response."""
        pass

    def simulate_processing_delay(self, min_seconds: float = 0.5, max_seconds: float = 2.0):
        """Simulate realistic processing delay."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)

    def log_request(self, request: str, response: Dict[str, Any]):
        """Log request and response for tracking."""
        self.last_request = {
            "request": request,
            "response": response,
            "timestamp": datetime.now().isoformat()
        }
        self.request_count += 1

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "name": self.agent_name,
            "type": self.agent_type,
            "created_at": self.created_at.isoformat(),
            "request_count": self.request_count,
            "last_request_time": self.last_request["timestamp"] if self.last_request else None
        }

    def extract_symbols_from_request(self, request: str) -> List[str]:
        """Extract stock symbols from request string."""
        common_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "META", "AMZN", "SPY", "QQQ", "IWM"]
        request_upper = request.upper()

        symbols = [symbol for symbol in common_symbols if symbol in request_upper]

        if not symbols:
            symbols = ["SPY", "QQQ", "AAPL"]  # Default symbols

        return symbols