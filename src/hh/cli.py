import typer
from hh.commands.vacancy import VacancyCommands
from hh.commands.employer import EmployerCommands
from hh.core.cache_manager import CacheManager
from hh.core.config_manager import ConfigManager
from hh.core.api_client import ApiClient

app = typer.Typer(help="CLI tool for fetching and caching data from hh.ru", no_args_is_help=True)

# Initialize managers and API client
cache_manager = CacheManager()
config_manager = ConfigManager()
api_client = ApiClient(cache_manager, config_manager)

# Create command instances with dependency injection
vacancy_commands = VacancyCommands(api_client)
employer_commands = EmployerCommands(api_client)

# Add command instances to main app
app.add_typer(vacancy_commands.app, name="vacancy", help="Commands for working with vacancies")
app.add_typer(employer_commands.app, name="employer", help="Commands for working with employers")

if __name__ == "__main__":
    app()
