# -*- mode: python ; coding: utf-8 -*-
"""
pyprofex PyInstaller spec.

构建命令（两种运行位置都支持）:
    pyinstaller pyprofex/pyprofex.spec     # 从仓库根
    pyinstaller pyprofex.spec              # 从 pyprofex/ 目录内

包目录定位做了兼容处理：旧写法直接假定 spec 位于仓库根，
从 pyprofex/ 目录内运行时会把 PYPROFEX_DIR 解析成不存在的
pyprofex/pyprofex。现按 profex_cli.py 的实际位置判断。
"""
import os, sys

# PyInstaller 执行 spec 时注入 __file__；其他 exec 场景回退到 cwd
_SPEC_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else os.getcwd()

# spec 与包内容同层（pyprofex/ 内含 profex_cli.py）→ 包目录即 spec 目录
if os.path.exists(os.path.join(_SPEC_DIR, 'profex_cli.py')):
    PYPROFEX_DIR = _SPEC_DIR
    BASE_DIR = os.path.dirname(_SPEC_DIR)
else:
    BASE_DIR = _SPEC_DIR
    PYPROFEX_DIR = os.path.join(BASE_DIR, 'pyprofex')

# The pickle data file
DATA_PKL = os.path.join(PYPROFEX_DIR, 'fingerprints_unified.pkl')

block_cipher = None

a = Analysis(
    [os.path.join(PYPROFEX_DIR, 'profex_cli.py')],
    pathex=[PYPROFEX_DIR, BASE_DIR],
    binaries=[],
    datas=[
        (DATA_PKL, 'pyprofex'),
    ],
    hiddenimports=[
        'search_match',
        'cif2fingerprint',
        'peaks',
        'mcp_server',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'matplotlib', 'scipy', 'PIL', 'numpy',
        'Jinja2', 'sphinx', 'PyQt5', 'PyQt6', 'qtpy',
        'sqlite3', 'pandas', 'sympy', 'cv2',
    ],
    win_no_prefer_redirects=False,
    win_no_default_exclude_redirects=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='pyprofex',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
