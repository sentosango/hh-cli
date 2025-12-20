from typing import Optional
from markdownify import markdownify
from datetime import datetime


class CommonMarkdownFormatter:
    """Handles common data formatting and conversion to different formats."""

    @staticmethod
    def html_to_markdown(html: str) -> str:
        """Convert HTML to markdown with proper error handling."""
        try:
            return markdownify(html, strip=["a"])
        except Exception:
            return html

    @staticmethod
    def format_date(date_str: Optional[str]) -> str:
        """Format date from API response with error handling."""
        if not date_str:
            return "Не указана"
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            return "Не указана"