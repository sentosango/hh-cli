# HH.ru CLI Tool

CLI tool for fetching and caching data from hh.ru (HeadHunter API).

## Features

- Fetch vacancy data by URL with caching (default 7 days)
- Fetch employer data by URL with caching (default 7 days)
- Output formats: JSON or Markdown
- Configurable cache duration per data type
- Cross-platform cache storage

## Installation

```bash
uv build --wheel --clear
uv tool install dist/hh-*.whl
```

## Usage

### Get Vacancy Data

```bash
# Get JSON output to stdout
hh vacancy https://perm.hh.ru/vacancy/12345678

# Get Markdown output to file
hh vacancy --format=markdown --output=vacancies/12345678.md https://perm.hh.ru/vacancy/12345678
```

### Get Employer Data

```bash
# Get JSON output to stdout
hh employer https://spb.hh.ru/employer/123456

# Get Markdown output to file
hh employer --format=markdown --output=employers/123456.md https://spb.hh.ru/employer/123456
```

## Configuration

Create a config file at `~/.config/hh/config.json`:

```json
{
  "cache_ttl": {
    "vacancy": 604800,
    "employer": 604800
  }
}
```

This sets cache TTL to 7 days for vacancies and 7 days for employers.