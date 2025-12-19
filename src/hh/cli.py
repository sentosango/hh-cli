import typer
from hh.commands import vacancy, employer

app = typer.Typer(help="CLI tool for fetching and caching data from hh.ru", no_args_is_help=True)

app.add_typer(vacancy.app, name="vacancy", help="Commands for working with vacancies")
app.add_typer(employer.app, name="employer", help="Commands for working with employers")

if __name__ == "__main__":
    app()
