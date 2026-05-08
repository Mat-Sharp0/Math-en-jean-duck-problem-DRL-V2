import sys
import os
import json
import subprocess
import tempfile
from pathlib import Path

import requests
from packaging.version import Version
from rich.console import Console
from rich.progress import Progress, DownloadColumn, BarColumn, TransferSpeedColumn, TimeRemainingColumn

from src.utils.app_info import __version__, GITHUB_REPO, GITHUB_URL
from src.utils.paths import INSTALL_INFO_FILE

def check_for_update(console: Console) -> None:
    try:
        headers = {"User-Agent": "DuckAI-Updater/2.0"}
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
            headers=headers,
            timeout=5
        )
        
        if response.status_code != 200:
            console.print(f"[bold red]\nUnable to retrieve updates (HTTP {response.status_code})[/]")
            return

        release = response.json()
        latest_tag = release.get("tag_name", "").lstrip("v")

        if not latest_tag or Version(latest_tag) <= Version(__version__):
            return

        console.print(f"\n[bold yellow]New version available: v{latest_tag}[/]", highlight=False)
        console.print(f"[dim]Current version: v{__version__}[/]", highlight=False)

        console.print("\nDo you want to update now? [[bold green]y[/]/[bold red]n[/]] ", end="")
        if input().strip().lower() != "y":
            console.print("[dim]Update cancelled[/]")
            return

        variant = "cpu"
        try:
            if INSTALL_INFO_FILE.exists():
                data = json.loads(INSTALL_INFO_FILE.read_text())
                variant = data.get("variant", "cpu")
        except Exception:
            pass

        if sys.platform == "win32":

            asset_name = f"DuckAI_{latest_tag}_windows_{variant}_setup.exe"
        else:
            asset_name = f"DuckAI_{latest_tag}_linux_{variant}.deb"

        assets = release.get("assets", [])
        asset = next((a for a in assets if a["name"] == asset_name), None)

        if not asset:
            console.print(f"[bold red]File not found: {asset_name}[/]")
            console.print(f"[dim]Please download manually to {GITHUB_URL}/releases/latest[/]")
            return

        tmp_dir = Path(tempfile.mkdtemp())
        installer_path = tmp_dir / asset_name

        console.print(f"\n[cyan]Download of {asset_name}...[/]")
        
        try:
            with requests.get(asset["browser_download_url"], stream=True, timeout=60) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0))
                
                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                    console=console,
                ) as progress:
                    task = progress.add_task("Download...", total=total)
                    with open(installer_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=16384):
                            f.write(chunk)
                            progress.advance(task, len(chunk))
            
            console.print("[green]Download completed[/]")
            
            if sys.platform == "win32":
                subprocess.Popen([str(installer_path), "/SILENT", "/SUPPRESSMSGBOXES"])
            else:
                console.print("[yellow]A password may be required to install the .deb package[/]")
                subprocess.Popen(["pkexec", "dpkg", "-i", str(installer_path)])
                
            console.print("[bold green]The installer has started. Duck AI will now close[/]")
            sys.exit(0)

        except Exception as e:
            console.print(f"[bold red]Error during download or installation: {e}[/]")

    except Exception as e:
        console.print(f"[bold red]Error searching for updates: {e}[/]")
