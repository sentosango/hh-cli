import re
import typer
from pathlib import Path
from hh.core.api_client import ApiClient
from hh.core.data_formatters import DataFormatters

app = typer.Typer(help="Commands for working with vacancies", no_args_is_help=True)
api = ApiClient()


def extract_vacancy_id(url: str) -> str:
    """Extract vacancy ID from hh.ru URL."""
    match = re.search(r'/vacancy/(\d+)', url)
    if not match:
        raise ValueError(f"Invalid vacancy URL: {url}")
    return match.group(1)


@app.command("get")
def get_vacancy(
    url: str = typer.Argument(..., help="URL of the vacancy"),
    format: str = typer.Option("json", "--format", "-f", help="Output format: json or markdown"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file path (stdout if not specified)")
) -> None:
    """Get vacancy data by URL with caching."""
    try:
        vacancy_id = extract_vacancy_id(url)
        data = api.get_vacancy(vacancy_id)

        if format.lower() == "markdown":
            content = DataFormatters.vacancy_to_markdown(data)
        else:
            content = DataFormatters.vacancy_to_json(data)

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content)
            typer.echo(f"Vacancy saved to {output}")
        else:
            typer.echo(content)

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)