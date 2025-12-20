import json
from pathlib import Path
from typing import Dict, Any
from platformdirs import user_config_dir


class ConfigManager:
    """Handles application configuration with platform-specific storage."""

    def __init__(self, app_name: str = "hh", app_author: str = None):
        self.config_dir = Path(user_config_dir(app_name, app_author))
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.config_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from platform-specific config directory."""
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())

        # Create default config with default cache TTL values
        default_config = {
            "cache_ttl": {
                "vacancy": 7 * 24 * 60 * 60,  # 7 days
                "employer": 7 * 24 * 60 * 60,  # 7 days
            }
        }
        self.config_path.write_text(
            json.dumps(default_config, ensure_ascii=False, indent=2)
        )
        return default_config

    def get_cache_ttl(self, data_type: str) -> int:
        """Get cache TTL for data type from config."""
        return self.config.get("cache_ttl", {}).get(data_type, 7 * 24 * 60 * 60)
