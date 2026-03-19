# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs
import stable_baselines3, gymnasium, os

block_cipher = None

sb3_datas     = collect_data_files('stable_baselines3')
gym_datas     = collect_data_files('gymnasium')
tb_datas = collect_data_files('tensorboard')

# Update value here, in installer.iss and in src/utils/app_info.py

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=collect_dynamic_libs('torch'),
    datas=[
        ('defaults', 'defaults'),

        *sb3_datas,
        *gym_datas,
        *tb_datas,
    ],
    hiddenimports=[
        'stable_baselines3',
        'stable_baselines3.common',
        'stable_baselines3.common.vec_env',
        'stable_baselines3.common.noise',
        'stable_baselines3.ppo',
        'stable_baselines3.td3',
        'stable_baselines3.sac',

        'gymnasium',
        'gymnasium.spaces',
        'gymnasium.envs',

        'torch',
        'torch.nn',
        'torch.optim',

        'tensorboard',
        'tensorboard.summary',
        'tensorboard.plugins',
        'tensorboard.plugins.scalar',
        'google.protobuf',
        'absl',
        'absl.logging',
        'absl.flags',
        'werkzeug',
        'grpc',

        'numpy',
        'yaml',
        'rich',
        'rich.prompt',
        'rich.console',
        'tkinter',
        'tkinter.filedialog',
        'pygame',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tensorflow',
        'keras',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DuckAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
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
    name='DuckAI',
)