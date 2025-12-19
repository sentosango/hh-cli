import re
import typer
from pathlib import Path
from hh.core.business_logic import HHManager

app = typer.Typer(help="Commands for working with employers", no_args_is_help=True)
manager = HHManager()


def extract_employer_id(url: str) -> str:
    """Extract employer ID from hh.ru URL."""
    match = re.search(r'/employer/(\d+)', url)
    if not match:
        raise ValueError(f"Invalid employer URL: {url}")
    return match.group(1)


@app.command("get")
def get_employer(
    url: str = typer.Argument(..., help="URL of the employer"),
    format: str = typer.Option("json", "--format", "-f", help="Output format: json or markdown"),
    output: Path = typer.Option(None, "--output", "-o", help="Output file path (stdout if not specified)")
) -> None:
    """Get employer data by URL with caching."""
    try:
        employer_id = extract_employer_id(url)
        data = manager.get_employer(employer_id)

        if format.lower() == "markdown":
            content = manager.employer_to_markdown(data)
        else:
            content = manager.employer_to_json(data)

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content)
            typer.echo(f"Employer saved to {output}")
        else:
            typer.echo(content)

    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)