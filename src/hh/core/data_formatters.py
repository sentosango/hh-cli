import json
from typing import Dict, Any, Optional
from markdownify import markdownify
from datetime import datetime


class DataFormatters:
    """Handles data formatting and conversion to different formats."""

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
    def vacancy_to_json(data: Dict[str, Any]) -> str:
        """Convert vacancy data to JSON."""
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def employer_to_json(data: Dict[str, Any]) -> str:
        """Convert employer data to JSON."""
        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def vacancy_to_markdown(data: Dict[str, Any]) -> str:
        """Convert vacancy data to Markdown with enhanced structure."""
        # Basic information
        title = data.get("name", "Вакансия без названия")
        employer = data.get("employer", {}).get("name", "Не указан")

        # Format salary with currency symbols and gross handling
        salary = DataFormatters._format_salary(data.get("salary"))

        # Format address
        address = DataFormatters._format_address(data.get("address"))

        # Format experience, employment, and schedule
        experience = data.get("experience", {}).get("name", "Не указан")
        employment = data.get("employment", {}).get("name", "Не указан")
        schedule = data.get("schedule", {}).get("name", "Не указан")

        # Format description
        description = data.get("description", "")
        if description:
            description = DataFormatters._html_to_markdown(description)

        # Format branded description
        branded_description = data.get("branded_description", "")
        if branded_description:
            branded_description = DataFormatters._html_to_markdown(branded_description)

        # Format key skills
        key_skills = DataFormatters._format_key_skills(data.get("key_skills", []))

        # Format date
        published_date = DataFormatters._format_date(data.get("published_at"))

        # Get URL
        url = data.get("alternate_url", "")

        # Build markdown with proper structure
        md = f"""# {title}

## Основная информация

**Компания:** {employer}
**Зарплата:** {salary}
**Адрес:** {address}
**Опыт работы:** {experience}
**Тип занятости:** {employment}
**График работы:** {schedule}

## Описание вакансии

{description}

"""

        # Add branded description if available
        if branded_description:
            md += f"""## Дополнительная информация

{branded_description}

"""

        # Add key skills
        md += f"""## Ключевые навыки

{key_skills}

**Дата публикации:** {published_date}
**URL:** {url}
"""

        return md

    @staticmethod
    def employer_to_markdown(data: Dict[str, Any]) -> str:
        """Convert employer data to Markdown with enhanced structure."""
        # Basic information
        name = data.get("name", "Работодатель без названия")
        employer_type = DataFormatters._format_employer_type(data.get("type"))

        # Format description
        description = data.get("description", "")
        if description:
            description = DataFormatters._html_to_markdown(description)

        # Get URLs
        website = data.get("site_url", "")
        hh_url = data.get("alternate_url", "")

        # Additional status information
        trusted = data.get("trusted", False)
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
        md = f"""# {name}

## Основная информация

**Тип:** {employer_type}
**Город:** {area_name}
**Страна:** {country_code}
**Количество открытых вакансий:** {open_vacancies}

**Статусы:**
- Работодатель доверенный: {"Да" if trusted else "Нет"}
- Аккредитованный IT-работодатель: {"Да" if accredited_it else "Нет"}
- Имеет подразделения: {"Да" if has_divisions else "Нет"}

## Отрасли деятельности

{chr(10).join(industries_list) if industries_list else "Не указаны"}

## Описание компании

{description}

## Ссылки

**Веб-сайт:** {website}
**Страница на HH.ru:** {hh_url}
"""

        return md

    @staticmethod
    def _html_to_markdown(html: str) -> str:
        """Convert HTML to markdown with proper error handling."""
        try:
            return markdownify(html, strip=["a"])
        except Exception:
            return html

    @staticmethod
    def _format_address(address: Optional[Dict[str, Any]]) -> str:
        """Format address from API response with proper handling."""
        if not address:
            return "Не указан"

        city = address.get("city", "")
        street = address.get("street", "")
        building = address.get("building", "")

        parts = []
        if city:
            parts.append(city)
        if street:
            parts.append(street)
        if building:
            parts.append(building)

        return ", ".join(parts) if parts else "Не указан"

    @staticmethod
    def _format_salary(salary: Optional[Dict[str, Any]]) -> str:
        """Format salary from API response with proper currency support."""
        if not salary:
            return "Не указана"

        currency = salary.get("currency", "")
        currency_symbol = {
            "RUR": "₽",
            "USD": "$",
            "EUR": "€",
            "KZT": "₸"
        }.get(currency, currency)

        from_amount = salary.get("from")
        to_amount = salary.get("to")
        gross = salary.get("gross", True)

        parts = []
        if from_amount:
            parts.append(f"от {from_amount:,}".replace(",", " "))
        if to_amount:
            parts.append(f"до {to_amount:,}".replace(",", " "))
        if not from_amount and not to_amount:
            return "Не указана"

        salary_text = " ".join(parts)
        if currency_symbol:
            salary_text += f" {currency_symbol}"
        if gross:
            salary_text += " (до вычета налогов)"
        else:
            salary_text += " (на руки)"

        return salary_text

    @staticmethod
    def _format_key_skills(key_skills: list) -> str:
        """Format key skills list."""
        if not key_skills:
            return "Не указаны"

        skills = []
        for skill in key_skills:
            if isinstance(skill, dict) and "name" in skill:
                skills.append(skill["name"])

        return ", ".join(skills) if skills else "Не указаны"

    @staticmethod
    def _format_date(date_str: Optional[str]) -> str:
        """Format date from API response with error handling."""
        if not date_str:
            return "Не указана"
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            return "Не указана"

    @staticmethod
    def _format_employer_type(employer_type: Optional[str]) -> str:
        """Format employer type from API response."""
        if not employer_type:
            return "Не указан"
        return DataFormatters.EMPLOYER_TYPE_MAPPING.get(employer_type, "Не указан")
