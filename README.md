# PyPI Info Demo

This project is a simple Model Context Protocol (MCP) server that provides information about Python packages on PyPI. It exposes a tool to fetch package maintainers, version, changelog, summary, and full project description using the PyPI JSON API.

## Features
- Query PyPI for package metadata
- Returns maintainers, version, changelog URL, summary, and full project description
- Attempts to find changelog links from project homepages if not directly available

## Usage

1. **Install dependencies:**
using the python environments extension run the command "create environment"
or install via `pip install -e .`

2. **Run the server:**
   ```sh
   python server.py
   ```

3. **Call the tool:**
   You can call the `get_pypi_package_info` tool via the MCP protocol, or directly in Python:
   ```python
   from server import get_pypi_package_info
   print(get_pypi_package_info("requests"))
   ```

## File Overview
- `server.py`: Main MCP server and PyPI info tool implementation
- `pyproject.toml`: Project metadata and dependencies

## Requirements
- Python 3.7+
- `mcp`, `requests`, `beautifulsoup4`

## License
MIT
