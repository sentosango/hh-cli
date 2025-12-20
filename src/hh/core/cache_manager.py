import hashlib
import time
import json
from pathlib import Path
from typing import Dict, Any, Optional
from platformdirs import user_cache_dir


class CacheManager:
    """Handles caching of API responses with TTL support."""

    def __init__(self, app_name: str = "hh", app_author: str = None):
        self.cache_dir = Path(user_cache_dir(app_name, app_author))
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, url: str) -> str:
        """Generate cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()

    def _is_cache_valid(self, cache_file: Path, ttl: int) -> bool:
        """Check if cached file is still valid."""
        if not cache_file.exists():
            return False

        file_age = time.time() - cache_file.stat().st_mtime
        return file_age < ttl

    def get_cached_data(self, url: str, data_type: str, ttl: int) -> Optional[Dict[str, Any]]:
        """Get cached data if still valid."""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{data_type}_{cache_key}.json"

        if self._is_cache_valid(cache_file, ttl):
            return json.loads(cache_file.read_text())
        return None

    def cache_data(self, url: str, data_type: str, data: Dict[str, Any]) -> None:
        """Cache data with timestamp."""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{data_type}_{cache_key}.json"
        cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))