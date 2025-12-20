import typer
from hh.commands.vacancy import VacancyCommands
from hh.commands.employer import EmployerCommands
from hh.core.cache_manager import CacheManager
from hh.core.config_manager import ConfigManager
from hh.core.api_client import ApiClient

# Initialize managers and API client
cache_manager = CacheManager()
config_manager = ConfigManager()
api_client = ApiClient(cache_manager, config_manager)

# Create command instances
vacancy_commands = VacancyCommands(api_client)
employer_commands = EmployerCommands(api_client)

# Create main app and add commands
app = typer.Typer(help="CLI tool for fetching data from hh.ru", no_args_is_help=True)

app.command("vacancy")(vacancy_commands.get_vacancy)
app.command("employer")(employer_commands.get_employer)

if __name__ == "__main__":
    app()
