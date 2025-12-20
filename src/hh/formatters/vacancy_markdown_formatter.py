from typing import Dict, Any, Optional
from hh.formatters.common_markdown_formatter import CommonMarkdownFormatter


class VacancyMarkdownFormatter:
    """Handles vacancy data formatting to Markdown with enhanced structure."""

    @staticmethod
    def format_vacancy_to_markdown(data: Dict[str, Any]) -> str:
        """Convert vacancy data to Markdown with enhanced structure."""
        # Basic information
        title = data.get("name", "Вакансия без названия")
        vacancy_id = data.get("id", "")
        employer = data.get("employer", {}).get("name", "Не указан")
        employer_url = data.get("employer", {}).get("alternate_url", "")

        # Format salary with currency symbols and gross handling
        salary = VacancyMarkdownFormatter._format_salary(data.get("salary"))

        # Format address
        address = VacancyMarkdownFormatter._format_address(data.get("address"))

        # Format area (region)
        area = data.get("area", {})
        area_name = area.get("name", "") if area else ""

        # Format experience, employment, and schedule
        experience = data.get("experience", {}).get("name", "Не указан")
        employment = data.get("employment", {}).get("name", "Не указан")
        schedule = data.get("schedule", {}).get("name", "Не указан")

        # Format professional roles
        professional_roles = VacancyMarkdownFormatter._format_professional_roles(data.get("professional_roles", []))

        # Format description
        description = data.get("description", "")
        if description:
            description = CommonMarkdownFormatter.html_to_markdown(description)

        # Format branded description
        branded_description = data.get("branded_description", "")
        if branded_description:
            branded_description = CommonMarkdownFormatter.html_to_markdown(branded_description)

        # Format key skills
        key_skills = VacancyMarkdownFormatter._format_key_skills(data.get("key_skills", []))

        # Format dates
        created_date = CommonMarkdownFormatter.format_date(data.get("created_at"))
        published_date = CommonMarkdownFormatter.format_date(data.get("published_at"))

        # Get URLs and status
        url = data.get("alternate_url", "")

        # State
        archived = data.get("archived", False)

        # Build markdown with enhanced structure
        md = f"""# {title}

## Основная информация

**Профессиональная роль:** {professional_roles}
**Зарплата:** {salary}

**Опыт работы:** {experience}
**Тип занятости:** {employment}
**График работы:** {schedule}

**Компания:** {employer}
**Регион:** {area_name}
**Адрес:** {address}


## Ключевые навыки

{key_skills}


## Описание вакансии

{description}


"""

        # Add branded description if available
        if branded_description:
            md += f"""## Дополнительная информация

{branded_description}


"""

        # Add vacancy state section
        md += f"""## Состояние вакансии

**Дата публикации:** {published_date}
**Дата создания:** {created_date}
**Статус:** {'Неактуальная вакансия (архив)' if archived else 'Актуальная вакансия'}


## Ссылки

**Страница вакансии на HH.ru:** {url}
{'**Страница компании на HH.ru:** ' + employer_url if employer_url else ''}
"""

        return md

    
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
    def _format_professional_roles(professional_roles: list) -> str:
        """Format professional roles list."""
        if not professional_roles:
            return "Не указано"

        roles = []
        for role in professional_roles:
            if isinstance(role, dict) and "name" in role:
                roles.append(role["name"])

        return ", ".join(roles) if roles else "Не указано"