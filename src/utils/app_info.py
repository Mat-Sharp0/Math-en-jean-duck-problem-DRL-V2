import sys
import tomllib
from src.utils.paths import RESOURCE_DIR

__version__ = "dev"

def _get_version():
    if __version__ != "dev":
        return __version__
    
    try:
        with open(RESOURCE_DIR / "pyproject.toml", "rb") as f:
            return tomllib.load(f)["project"]["version"]
    except Exception :
        return "unknown"

APP_NAME = "Duck AI"
__version__ = _get_version()
AUTHOR = "HIOLLE Mateo"
GITHUB_REPO = "Mat-Sharp0/Math-en-jean-duck-problem-DRL-V2"
GITHUB_URL = f"https://github.com/{GITHUB_REPO}"
