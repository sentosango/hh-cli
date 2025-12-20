import json
from typing import Dict, Any, Optional
from markdownify import markdownify
from datetime import datetime


class DataFormatters:
    """Handles data formatting and conversion to different formats."""

    @staticmethod
    def vacancy_to_json(data: Dict[str, Any]) -> str:
        """Convert vacancy data to JSON."""
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def employer_to_json(data: Dict[str, Any]) -> str:
        """Convert employer data to JSON."""
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def vacancy_to_markdown(data: Dict[str, Any]) -> str:
        """Convert vacancy data to Markdown."""
        md = f"""# {data.get("name", "Vacancy")}

**Company:** {data.get("employer", {}).get("name", "Unknown")}
**Location:** {DataFormatters._format_address(data.get("address"))}
**Salary:** {DataFormatters._format_salary(data.get("salary"))}
**Experience:** {data.get("experience", {}).get("name", "Not specified")}
**Employment:** {data.get("employment", {}).get("name", "Not specified")}
**Schedule:** {data.get("schedule", {}).get("name", "Not specified")}

## Description
{markdownify(data.get("description", ""), strip=["a"])}

## Requirements
{markdownify(data.get("snippet", {}).get("requirement", ""), strip=["a"])}

## Responsibilities
{markdownify(data.get("snippet", {}).get("responsibility", ""), strip=["a"])}

**Published:** {DataFormatters._format_date(data.get("published_at"))}
**URL:** {data.get("alternate_url", "")}
"""

        return md

    @staticmethod
    def employer_to_markdown(data: Dict[str, Any]) -> str:
        """Convert employer data to Markdown."""
        md = f"""# {data.get("name", "Employer")}

**Type:** {data.get("type", "Not specified")}
**Industry:** {data.get("industry", {}).get("name", "Not specified")}
**Size:** {data.get("employees_count", "Not specified")}
**Founded:** {data.get("opened_at", "Not specified")}

## Description
{markdownify(data.get("description", ""), strip=["a"])}

**Website:** {data.get("site_url", "")}
**Vacancies:** {data.get("vacancies_url", "")}
"""

        return md

    @staticmethod
    def _format_address(address: Optional[Dict[str, Any]]) -> str:
        """Format address from API response."""
        if not address:
            return "Not specified"
        return f"{address.get('city', '')}, {address.get('street', '')}"

    @staticmethod
    def _format_salary(salary: Optional[Dict[str, Any]]) -> str:
        """Format salary from API response."""
        if not salary:
            return "Not specified"
        from_value = salary.get("from")
        to_value = salary.get("to")
        currency = salary.get("currency", "")
        if from_value and to_value:
            return f"{from_value} - {to_value} {currency}"
        elif from_value:
            return f"from {from_value} {currency}"
        elif to_value:
            return f"to {to_value} {currency}"
        return "Not specified"

    @staticmethod
    def _format_date(date_str: str) -> str:
        """Format date from API response."""
        if not date_str:
            return "Not specified"
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime(
            "%Y-%m-%d"
        )
