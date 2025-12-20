import re
import typer
from pathlib import Path

from hh.core.api_client import ApiClient
from hh.formatters.employer_markdown_formatter import EmployerMarkdownFormatter
import json


class EmployerCommands:
    """Commands for working with employers."""

    def __init__(self, api_client: ApiClient):
        self.api = api_client

    @staticmethod
    def extract_employer_id(url: str) -> str:
        """Extract employer ID from hh.ru URL."""
        match = re.search(r"/employer/(\d+)", url)
        if not match:
            raise ValueError(f"Invalid employer URL: {url}")
        return match.group(1)

    def get_employer(
        self,
        url: str = typer.Argument(..., help="URL of the employer"),
        output_format: str = typer.Option(
            "json", "--format", "-f", help="Output format: json or markdown"
        ),
        output: Path = typer.Option(
            None, "--output", "-o", help="Output file path (stdout if not specified)"
        ),
    ) -> None:
        """Get employer data by URL with caching."""
        try:
            employer_id = self.extract_employer_id(url)
            data = self.api.get_employer(employer_id)

            if output_format.lower() == "markdown":
                content = EmployerMarkdownFormatter.format_employer_to_markdown(data)
            else:
                content = json.dumps(data, ensure_ascii=False, indent=2)

            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(content)
                typer.echo(f"Employer saved to {output}")
            else:
                typer.echo(content)

        except Exception as e:
            typer.echo(f"Error: {e}", err=True)
            raise typer.Exit(1)
