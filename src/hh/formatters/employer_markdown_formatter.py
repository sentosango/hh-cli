from typing import Dict, Any, Optional
from hh.formatters.common_markdown_formatter import CommonMarkdownFormatter


class EmployerMarkdownFormatter:
    """Handles employer data formatting to Markdown with enhanced structure."""

    # Маппинг типов работодателей из справочника HH.ru
    EMPLOYER_TYPE_MAPPING = {
        "company": "Прямой работодатель",
        "agency": "Кадровое агентство",
        "project_director": "Руководитель проекта",
        "private_recruiter": "Частный рекрутер",
        "private_individual": "Частное лицо",
        "self_employed": "Самозанятый"
    }

    @staticmethod
    def format_employer_to_markdown(data: Dict[str, Any]) -> str:
        """Convert employer data to Markdown with enhanced structure."""
        # Basic information
        name = data.get("name", "Работодатель без названия")
        employer_type = EmployerMarkdownFormatter._format_employer_type(data.get("type"))

        # Format description
        description = data.get("description", "")
        if description:
            description = CommonMarkdownFormatter.html_to_markdown(description)

        # Get URLs
        website = data.get("site_url", "")
        hh_url = data.get("alternate_url", "")

        # Additional status information
        accredited_it = data.get("accredited_it_employer", False)
        has_divisions = data.get("has_divisions", False)

        # Format area/country information
        area = data.get("area", {})
        area_name = area.get("name", "") if area else ""
        country_code = data.get("country_code", "")

        # Format industries
        industries = data.get("industries", [])
        industries_list = [f"- {industry.get('name', '')}" for industry in industries if industry.get('name')]

        # Format open vacancies count
        open_vacancies = data.get("open_vacancies", 0)

        # Build markdown with enhanced structure
        md = f"""# Работодатель: {name}

## Основная информация

**Название работодателя:** {name}
**Тип:** {employer_type}
**Город:** {area_name}
**Страна:** {country_code}
**Количество открытых вакансий:** {open_vacancies}

**Статусы:**
- Аккредитованный IT-работодатель: {"Да" if accredited_it else "Нет"}
- Имеет подразделения: {"Да" if has_divisions else "Нет"}

## Отрасли деятельности

{chr(10).join(industries_list) if industries_list else "Не указаны"}

## Описание компании

{description}

## Ссылки

**Веб-сайт:** {website}
**Страница компании на HH.ru:** {hh_url}
"""

        return md

    
    @staticmethod
    def _format_employer_type(employer_type: Optional[str]) -> str:
        """Format employer type from API response."""
        if not employer_type:
            return "Не указан"
        return EmployerMarkdownFormatter.EMPLOYER_TYPE_MAPPING.get(employer_type, "Не указан")
