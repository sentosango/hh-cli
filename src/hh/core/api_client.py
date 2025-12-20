import requests
from typing import Dict, Any
from hh.core.cache_manager import CacheManager
from hh.core.config_manager import ConfigManager


class ApiClient:
    """API client for working with hh.ru API with caching support."""

    def __init__(self, cache_manager: CacheManager, config_manager: ConfigManager):
        self.base_url = "https://api.hh.ru"
        self.cache_manager = cache_manager
        self.config_manager = config_manager

    def _fetch_data(self, url: str, data_type: str) -> Dict[str, Any]:
        """Fetch data from API with caching."""
        ttl = self.config_manager.get_cache_ttl(data_type)
        cached_data = self.cache_manager.get_cached_data(url, data_type, ttl)
        if cached_data:
            return cached_data

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        self.cache_manager.cache_data(url, data_type, data)
        return data

    def get_vacancy(self, vacancy_id: str) -> Dict[str, Any]:
        """Get vacancy data from hh.ru API."""
        url = f"{self.base_url}/vacancies/{vacancy_id}"
        return self._fetch_data(url, "vacancy")

    def get_employer(self, employer_id: str) -> Dict[str, Any]:
        """Get employer data from hh.ru API."""
        url = f"{self.base_url}/employers/{employer_id}"
        return self._fetch_data(url, "employer")