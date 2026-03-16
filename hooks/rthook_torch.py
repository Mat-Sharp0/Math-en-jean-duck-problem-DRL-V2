import os
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    torch_lib = Path(sys._MEIPASS) / 'torch' / 'lib'
    if torch_lib.exists():
        os.add_dll_directory(str(torch_lib))