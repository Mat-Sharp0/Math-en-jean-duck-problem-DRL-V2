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
        response = requests.get(
            f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest",
            timeout=3
        )
        if response.status_code != 200:
            console.print(f"[bold red]\nFailed to fetch releases (HTTP {response.status_code})[/]")
            return

        release = response.json()
        latest = release.get("tag_name", "").lstrip("v")

        if not latest or Version(latest) <= Version(__version__):
            return

        console.print(f"\n[bold yellow]New version available: v{latest}[/]", highlight=False)
        console.print(f"[dim]Current version: v{__version__}[/]", highlight=False)

        console.print("\nDo you want to update now? [[bold green]y[/]/[bold red]n[/]] ", end="")
        choice = input().strip().lower()
        if choice != "y":
            console.print("[dim]Update skipped.[/]")
            return

        try:
            if INSTALL_INFO_FILE.exists():
                data = json.loads(INSTALL_INFO_FILE.read_text())
                variant = data.get("variant", "cpu")
            else:
                variant = "cpu"
        except Exception:
            variant = "cpu"

        if sys.platform == "win32":
            asset_name = f"DuckAI_{latest}_windows_{variant}_setup.exe"
        else:
            asset_name = f"DuckAI_{latest}_linux_{variant}.deb"

        assets = release.get("assets", [])
        asset = next((a for a in assets if a["name"] == asset_name), None)

        if not asset:
            console.print(f"[bold red]Asset not found: {asset_name}[/]")
            console.print(f"[dim]Please download manually from {GITHUB_URL}/releases/latest[/]")
            return

        tmp_dir = Path(tempfile.mkdtemp())
        installer_path = tmp_dir / asset_name

        console.print(f"\n[cyan]Downloading {asset_name}...[/]")
        try:
            with requests.get(asset["browser_download_url"], stream=True, timeout=30) as r:
                if r.status_code != 200:
                    success = False
                else:
                    total = int(r.headers.get("content-length", 0))
                    with Progress(
                        "[progress.description]{task.description}",
                        BarColumn(),
                        DownloadColumn(),
                        TransferSpeedColumn(),
                        TimeRemainingColumn(),
                        console=console,
                    ) as progress:
                        task = progress.add_task("Downloading...", total=total)
                        with open(installer_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                                progress.advance(task, len(chunk))
                    success = True
        except Exception as e:
            console.print(f"[bold red]Download failed: {e}[/]")
            success = False


        if not success:
            console.print("[bold red]Download failed. Please try again later.[/]")
            return

        console.print("[green]Download complete.[/]")
        try:
            if sys.platform == "win32":
                subprocess.Popen([str(installer_path), "/SILENT"])
            else:
                subprocess.Popen(["pkexec", "dpkg", "-i", str(installer_path)])
            console.print("[green]Installer launched. Duck AI will close now.[/]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[bold red]Failed to launch installer: {e}[/]")

    except Exception as e:
        console.print(f"[bold red]Failed to check for update: {e}[/]")