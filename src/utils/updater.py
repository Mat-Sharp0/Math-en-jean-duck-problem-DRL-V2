import requests

from rich.console import Console

from src.utils.app_info import __version__, GITHUB_REPO, GITHUB_URL

console = Console()

def check_for_update() -> None:
    """Check if new version is available on GitHub"""
    try:
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
            timeout=3
        )
        if response.status_code != 200:
            console.print(f"[bold red]\nFailed to fetch releases (HTTP {response.status_code})")
            return
        
        latest = response.json().get("tag_name", "").lstrip("v")
        
        if latest and latest != __version__:
            console.print(f"[bold red]\nNew version available: v{latest}[/]", highlight=False)
            console.print(f"[dim]Current version: v{__version__}[/]", highlight=False)
            console.print(f"[cyan]Download: {GITHUB_URL}/releases/latest[/]")

    except Exception:
        pass