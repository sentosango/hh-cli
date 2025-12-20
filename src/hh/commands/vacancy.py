import re
import typer
import json
from pathlib import Path

from hh.core.api_client import ApiClient
from hh.formatters.vacancy_markdown_formatter import VacancyMarkdownFormatter


class VacancyCommands:
    """Commands for working with vacancies."""

    def __init__(self, api_client: ApiClient):
        self.api = api_client

    @staticmethod
    def extract_vacancy_id(url: str) -> str:
        """Extract vacancy ID from hh.ru URL."""
        match = re.search(r"/vacancy/(\d+)", url)
        if not match:
            raise ValueError(f"Invalid vacancy URL: {url}")
        return match.group(1)

    def get_vacancy(
        self,
        url: str = typer.Argument(..., help="URL of the vacancy"),
        output_format: str = typer.Option(
            "json", "--format", "-f", help="Output format: json or markdown"
        ),
        output: Path = typer.Option(
            None, "--output", "-o", help="Output file path (stdout if not specified)"
        ),
    ) -> None:
        """Get vacancy data by URL with caching."""
        try:
            vacancy_id = self.extract_vacancy_id(url)
            data = self.api.get_vacancy(vacancy_id)

            if output_format.lower() == "markdown":
                content = VacancyMarkdownFormatter.format_vacancy_to_markdown(data)
            else:
                content = json.dumps(data, ensure_ascii=False, indent=2)

            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(content)
                typer.echo(f"Vacancy saved to {output}")
            else:
                typer.echo(content)

        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1)
