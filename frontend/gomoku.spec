# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Gomoku Game
# Usage (run from frontend/ on Windows after compiling backend):
#   pip install pyinstaller
#   pyinstaller gomoku.spec
import os

# SPECPATH is set by PyInstaller to the directory containing this spec file (frontend/)
_root = os.path.dirname(SPECPATH)  # project root

# Find backend executable: MSVC puts it in Release/, MinGW puts it directly in build/
_backend_candidates = [
    os.path.join(_root, "backend", "build", "Release", "gomoku.exe"),
    os.path.join(_root, "backend", "build", "gomoku.exe"),
]
_backend_exe = next((p for p in _backend_candidates if os.path.exists(p)), _backend_candidates[0])

a = Analysis(
    ["main.py"],
    pathex=[SPECPATH],
    binaries=[(_backend_exe, ".")],  # gomoku.exe extracted to _MEIPASS root
    datas=[
        (os.path.join(SPECPATH, "assets", "audio", "backgroundmusic"), "assets/audio/backgroundmusic"),
        (os.path.join(SPECPATH, "assets", "audio", "soundeffect"), "assets/audio/soundeffect"),
    ],
    hiddenimports=[
        "PySide6.QtMultimedia",
        "PySide6.QtMultimediaWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="gomoku",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,   # 不顯示黑色 terminal 視窗
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
