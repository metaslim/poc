"""Configuration Management

Centralized configuration management using environment variables.
"""

import os
from typing import Optional
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class Config:
    """Configuration class that loads settings from environment variables."""

    def __init__(self):
        """Initialize configuration by loading .env file if available."""
        if load_dotenv:
            env_path = Path(__file__).parent / '.env'
            if env_path.exists():
                load_dotenv(env_path)

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment."""
        return os.getenv('OPENAI_API_KEY')

    @property
    def openai_model(self) -> str:
        """Get OpenAI model name."""
        return os.getenv('OPENAI_MODEL', 'gpt-4.1')

    @property
    def openai_max_completion_tokens(self) -> int:
        """Get max completion tokens."""
        return int(os.getenv('OPENAI_MAX_COMPLETION_TOKENS', '1500'))

    @property
    def openai_temperature(self) -> float:
        """Get OpenAI temperature setting."""
        return float(os.getenv('OPENAI_TEMPERATURE', '1.0'))

    @property
    def openai_top_p(self) -> float:
        """Get OpenAI top_p setting."""
        return float(os.getenv('OPENAI_TOP_P', '1.0'))

    @property
    def openai_frequency_penalty(self) -> float:
        """Get OpenAI frequency penalty."""
        return float(os.getenv('OPENAI_FREQUENCY_PENALTY', '0.0'))

    @property
    def openai_presence_penalty(self) -> float:
        """Get OpenAI presence penalty."""
        return float(os.getenv('OPENAI_PRESENCE_PENALTY', '0.0'))

    @property
    def ai_agent_min_delay(self) -> float:
        """Get minimum AI agent processing delay."""
        return float(os.getenv('AI_AGENT_PROCESSING_MIN_DELAY', '0.5'))

    @property
    def ai_agent_max_delay(self) -> float:
        """Get maximum AI agent processing delay."""
        return float(os.getenv('AI_AGENT_PROCESSING_MAX_DELAY', '2.0'))

    @property
    def default_user_id(self) -> str:
        """Get default user ID."""
        return os.getenv('DEFAULT_USER_ID', 'default_trader')

    @property
    def default_scenario(self) -> str:
        """Get default trading scenario."""
        return os.getenv('DEFAULT_SCENARIO', 'samples/scenario1')

    @property
    def default_risk_per_trade(self) -> float:
        """Get default risk per trade percentage."""
        return float(os.getenv('DEFAULT_RISK_PER_TRADE', '0.02'))

    @property
    def default_stop_loss_pct(self) -> float:
        """Get default stop loss percentage."""
        return float(os.getenv('DEFAULT_STOP_LOSS_PCT', '0.05'))

    @property
    def default_account_size(self) -> float:
        """Get default account size."""
        return float(os.getenv('DEFAULT_ACCOUNT_SIZE', '100000'))

    @property
    def debug_mode(self) -> bool:
        """Get debug mode setting."""
        return os.getenv('DEBUG_MODE', 'false').lower() == 'true'

    @property
    def log_level(self) -> str:
        """Get logging level."""
        return os.getenv('LOG_LEVEL', 'INFO')

    @property
    def enable_session_logging(self) -> bool:
        """Get session logging setting."""
        return os.getenv('ENABLE_SESSION_LOGGING', 'true').lower() == 'true'

    def get_openai_config(self) -> dict:
        """Get OpenAI configuration as a dictionary."""
        return {
            'model': self.openai_model,
            'max_completion_tokens': self.openai_max_completion_tokens,
            'temperature': self.openai_temperature,
            'top_p': self.openai_top_p,
            'frequency_penalty': self.openai_frequency_penalty,
            'presence_penalty': self.openai_presence_penalty
        }

    def get_risk_management_config(self) -> dict:
        """Get risk management configuration as a dictionary."""
        return {
            'risk_per_trade': self.default_risk_per_trade,
            'stop_loss_pct': self.default_stop_loss_pct,
            'account_size': self.default_account_size
        }

    def validate_config(self) -> bool:
        """Validate that required configuration is present."""
        if not self.openai_api_key:
            print("❌ Error: OPENAI_API_KEY not found in environment variables")
            print("💡 Please set your OpenAI API key in the .env file or environment")
            return False

        if not self.openai_api_key.startswith('sk-'):
            print("❌ Error: Invalid OpenAI API key format")
            print("💡 OpenAI API keys should start with 'sk-'")
            return False

        return True

    def print_config_summary(self):
        """Print a summary of current configuration."""
        print("🔧 CONFIGURATION SUMMARY")
        print("-" * 30)
        print(f"Model: {self.openai_model}")
        print(f"Max Tokens: {self.openai_max_completion_tokens}")
        print(f"Temperature: {self.openai_temperature}")
        print(f"API Key: {'✅ Set' if self.openai_api_key else '❌ Missing'}")
        print(f"Default Scenario: {self.default_scenario}")
        print(f"Debug Mode: {self.debug_mode}")
        print(f"Session Logging: {self.enable_session_logging}")


# Global configuration instance
config = Config()