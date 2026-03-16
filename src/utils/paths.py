import sys
import shutil
import stat
from pathlib import Path

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent.parent
    
def get_resource_dir():
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent.parent.parent
    
APP_DIR = get_app_dir()
RESOURCE_DIR = get_resource_dir()

CONTENT_DIR = APP_DIR / "user_content"
CONFIG_DIR = CONTENT_DIR / "config"
LOGS_DIR = CONTENT_DIR / "logs"
TENSORBOARD_DIR = LOGS_DIR / "tensorboard"
MODELS_DIR = CONTENT_DIR / "models"

DEFAULTS_DIR = RESOURCE_DIR / "defaults" 
DEFAULT_CONFIG_DIR = DEFAULTS_DIR / "configs" 
PRETRAINED_DIR = DEFAULTS_DIR / "models"

def _copy_exemples(source_dir: Path, dest_dir: Path, exclude: set[str] = {}):
    if not source_dir.exists():
        return
    for source in source_dir.iterdir():
        if source.name in exclude:
            continue
        dest = dest_dir / source.name
        if not dest.exists():
            shutil.copy(source, dest)
            dest.chmod(stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)

def init_content_dirs():
    for d in [CONFIG_DIR, LOGS_DIR, TENSORBOARD_DIR, MODELS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
    
    _copy_exemples(DEFAULT_CONFIG_DIR, CONFIG_DIR)
    _copy_exemples(PRETRAINED_DIR, MODELS_DIR, {"PPO_circle_world_legacy.zip", "SAC_run_SAC_big_legacy.zip"})
