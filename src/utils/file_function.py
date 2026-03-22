import subprocess
import sys, os
import stat
import copy
import shutil
import yaml

from pathlib import Path
import tkinter as tk
from tkinter import filedialog

from src.utils.paths import CONFIG_DIR
from tkinter import filedialog

import yaml



def open_folder(path: Path) -> None:
    """Open a folder in file explorer"""
    if sys.platform == "win32":
        subprocess.Popen(f'explorer "{path}"')
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])



def open_file(file_path: Path) -> None:
    """Open a file with default app"""
    if sys.platform == "win32":
        os.startfile(file_path)
    elif sys.platform == "darwin":
        subprocess.run(["open", file_path])
    else:
        subprocess.run(["xdg-open", file_path])


def creat_config(template_path: Path) -> Path:
    """Creat a new config file frome a template config file"""
    with open(template_path, "r", encoding="utf-8") as template_f:
        template = yaml.safe_load(template_f)
    
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.asksaveasfilename(
    title=f"""Creat new {template['algo']} config""",
    initialdir=CONFIG_DIR,
    initialfile=f"""new_config_{template["algo"]}.yaml""",
    defaultextension=".yaml",
    filetypes=[
        ("YAML file", "*.yaml *.yml"),
        ("All file", "*.*")
    ])

    root.destroy()
    
    if not file_path:
        raise ValueError("Canceled")
    data = copy.deepcopy(template)
    data["meta"]["run_name"] = Path(file_path).stem
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

    return Path(file_path)


def clear_dir(path: Path, exclude: set[str] = {}) -> None:
    """Remove all content of a directory"""

    for i in path.iterdir():
        if i.name in exclude:
            continue
        if i.is_file() or i.is_symlink():
            i.chmod(stat.S_IWRITE | stat.S_IREAD)
            i.unlink()
        elif i.is_dir():
            for f in i.rglob("*"):
                if f.is_file():
                    f.chmod(stat.S_IWRITE | stat.S_IREAD)
            shutil.rmtree(i)