from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup


# Create an MCP server
mcp = FastMCP("PyPI Info Demo")


# MCP tool for PyPI package info
@mcp.tool()
def get_pypi_package_info(package_name: str) -> dict:
    """
    Fetches package info from PyPI for the given package name.
    Returns a dictionary with maintainers, version, changelog, and description.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError(f"Package '{package_name}' not found on PyPI.")
    data = resp.json()
    info = data.get("info", {})
    # Maintainers: PyPI does not always provide maintainers, fallback to author/maintainer fields
    maintainers = info.get("maintainer")
    if not maintainers:
        maintainers = info.get("author")
    version = info.get("version")
    description = info.get("summary") or info.get("description")
    project_description = info.get("description")
    # Try to get changelog from project_urls or homepage
    changelog = None
    project_urls = info.get("project_urls", {})
    for key in project_urls:
        if "changelog" in key.lower() or "changes" in key.lower():
            changelog = project_urls[key]
            break
    if not changelog:
        # Try to find a changelog in the homepage or repository
        for key in project_urls:
            if "home" in key.lower() or "repo" in key.lower():
                homepage_url = project_urls[key]
                try:
                    page = requests.get(homepage_url, timeout=5)
                    if page.ok:
                        soup = BeautifulSoup(page.text, "html.parser")
                        for a in soup.find_all("a", href=True):
                            if (
                                "changelog" in a.text.lower()
                                or "changes" in a.text.lower()
                            ):
                                changelog = a["href"]
                                break
                        if changelog:
                            break
                except Exception:
                    pass
    return {
        "maintainers": maintainers,
        "version": version,
        "changelog": changelog,
        "description": description,
        "project_description": project_description,
    }


if __name__ == "__main__":
    # Start the MCP server
    mcp.run(transport="sse")

    # Example usage to call the function directly
    print(get_pypi_package_info("requests"))
