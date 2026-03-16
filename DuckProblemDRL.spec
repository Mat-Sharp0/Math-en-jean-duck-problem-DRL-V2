# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

sb3_datas,   sb3_binaries,   sb3_hidden   = collect_all('stable_baselines3')
gym_datas,   gym_binaries,   gym_hidden   = collect_all('gymnasium')
torch_datas, torch_binaries, torch_hidden = collect_all('torch')
numpy_datas, numpy_binaries, numpy_hidden = collect_all('numpy')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=sb3_binaries + gym_binaries + torch_binaries + numpy_binaries,
    datas=[
        ('defaults/configs', 'defaults/configs'),
        ('defaults/models',  'defaults/models'),
        ('src',              'src'),
        *sb3_datas,
        *gym_datas,
        *torch_datas,
        *numpy_datas,
    ],
    hiddenimports=[
        *sb3_hidden,
        *gym_hidden,
        *torch_hidden,
        *numpy_hidden,
        'stable_baselines3.common.policies',
        'stable_baselines3.common.torch_layers',
        'stable_baselines3.common.on_policy_algorithm',
        'stable_baselines3.common.off_policy_algorithm',
        'gymnasium.envs.registration',
        'gymnasium.utils.passive_env_checker',
        'tkinter',
        'tkinter.filedialog',
        'rich.prompt',
        'rich.console',
        'webbrowser',
    ],
    hookspath=['hooks'],
    runtime_hooks=['hooks/rthook_torch.py'],
    excludes=['matplotlib', 'IPython', 'jupyter'],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DuckProblemDRL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='DuckProblemDRL',
)