import json
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
import requests
from platformdirs import user_cache_dir, user_config_dir


class HHManager:
    """Core business logic for working with hh.ru API with caching support."""

    def __init__(self, app_name: str = "hh", app_author: str = None):
        self.base_url = "https://api.hh.ru"
        self.cache_dir = Path(user_cache_dir(app_name, app_author))
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Default cache TTL values (in seconds)
        self.default_cache_ttl = {
            "vacancy": 7 * 24 * 60 * 60,  # 7 days
            "employer": 7 * 24 * 60 * 60   # 7 days
        }

        self.config_dir = Path(user_config_dir(app_name, app_author))
        self.config_path = self.config_dir / "config.json"
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from platform-specific config directory."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if self.config_path.exists():
            return json.loads(self.config_path.read_text())

        # Create default config with default cache TTL values
        default_config = {
            "cache_ttl": self.default_cache_ttl
        }
        self.config_path.write_text(json.dumps(default_config, ensure_ascii=False, indent=2))
        return default_config

    def get_cache_ttl(self, data_type: str) -> int:
        """Get cache TTL for data type from config."""
        return self.config.get("cache_ttl", {}).get(data_type, self.default_cache_ttl.get(data_type, 7 * 24 * 60 * 60))

    def _get_cache_key(self, url: str) -> str:
        """Generate cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()

    def _is_cache_valid(self, cache_file: Path, ttl: int) -> bool:
        """Check if cached file is still valid."""
        if not cache_file.exists():
            return False

        file_age = time.time() - cache_file.stat().st_mtime
        return file_age < ttl

    def _get_cached_data(self, url: str, data_type: str) -> Optional[Dict[str, Any]]:
        """Get cached data if still valid."""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{data_type}_{cache_key}.json"

        ttl = self.get_cache_ttl(data_type)
        if self._is_cache_valid(cache_file, ttl):
            return json.loads(cache_file.read_text())
        return None

    def _cache_data(self, url: str, data_type: str, data: Dict[str, Any]) -> None:
        """Cache data with timestamp."""
        cache_key = self._get_cache_key(url)
        cache_file = self.cache_dir / f"{data_type}_{cache_key}.json"
        cache_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    def _fetch_data(self, url: str, data_type: str) -> Dict[str, Any]:
        """Fetch data from API with caching."""
        cached_data = self._get_cached_data(url, data_type)
        if cached_data:
            return cached_data

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        self._cache_data(url, data_type, data)
        return data

    def get_vacancy(self, vacancy_id: str) -> Dict[str, Any]:
        """Get vacancy data from hh.ru API."""
        url = f"{self.base_url}/vacancies/{vacancy_id}"
        return self._fetch_data(url, "vacancy")

    def get_employer(self, employer_id: str) -> Dict[str, Any]:
        """Get employer data from hh.ru API."""
        url = f"{self.base_url}/employers/{employer_id}"
        return self._fetch_data(url, "employer")

    def vacancy_to_json(self, data: Dict[str, Any]) -> str:
        """Convert vacancy data to JSON."""
        return json.dumps(data, ensure_ascii=False, indent=2)

    def employer_to_json(self, data: Dict[str, Any]) -> str:
        """Convert employer data to JSON."""
        return json.dumps(data, ensure_ascii=False, indent=2)

    def vacancy_to_markdown(self, data: Dict[str, Any]) -> str:
        """Convert vacancy data to Markdown."""
        from markdownify import markdownify

        md = f"""# {data.get('name', 'Vacancy')}

**Company:** {data.get('employer', {}).get('name', 'Unknown')}
**Location:** {self._format_address(data.get('address'))}
**Salary:** {self._format_salary(data.get('salary'))}
**Experience:** {data.get('experience', {}).get('name', 'Not specified')}
**Employment:** {data.get('employment', {}).get('name', 'Not specified')}
**Schedule:** {data.get('schedule', {}).get('name', 'Not specified')}

## Description
{markdownify(data.get('description', ''), strip=['a'])}

## Requirements
{markdownify(data.get('snippet', {}).get('requirement', ''), strip=['a'])}

## Responsibilities
{markdownify(data.get('snippet', {}).get('responsibility', ''), strip=['a'])}

**Published:** {self._format_date(data.get('published_at'))}
**URL:** {data.get('alternate_url', '')}
"""

        return md

    def employer_to_markdown(self, data: Dict[str, Any]) -> str:
        """Convert employer data to Markdown."""
        from markdownify import markdownify

        md = f"""# {data.get('name', 'Employer')}

**Type:** {data.get('type', 'Not specified')}
**Industry:** {data.get('industry', {}).get('name', 'Not specified')}
**Size:** {data.get('employees_count', 'Not specified')}
**Founded:** {data.get('opened_at', 'Not specified')}

## Description
{markdownify(data.get('description', ''), strip=['a'])}

**Website:** {data.get('site_url', '')}
**Vacancies:** {data.get('vacancies_url', '')}
"""

        return md

    def _format_address(self, address: Dict[str, Any]) -> str:
        """Format address from API response."""
        if not address:
            return "Not specified"
        return f"{address.get('city', '')}, {address.get('street', '')}"

    def _format_salary(self, salary: Dict[str, Any]) -> str:
        """Format salary from API response."""
        if not salary:
            return "Not specified"
        from_value = salary.get('from')
        to_value = salary.get('to')
        currency = salary.get('currency', '')
        if from_value and to_value:
            return f"{from_value} - {to_value} {currency}"
        elif from_value:
            return f"from {from_value} {currency}"
        elif to_value:
            return f"to {to_value} {currency}"
        return "Not specified"

    def _format_date(self, date_str: str) -> str:
        """Format date from API response."""
        if not date_str:
            return "Not specified"
        from datetime import datetime
        return datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')