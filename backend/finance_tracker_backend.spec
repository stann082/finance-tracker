# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for the Finance Tracker backend.
# Built by `npm run build:backend`; output lands in backend/dist/finance-tracker-backend/
# and is bundled into the installer via the extraResources entry in package.json.

a = Analysis(
    ['run_server.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        # uvicorn resolves these at runtime via string lookups, so PyInstaller
        # cannot discover them from the import graph
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.http.h11_impl',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
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
    [],
    exclude_binaries=True,
    name='finance-tracker-backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    disable_windowed_traceback=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name='finance-tracker-backend',
)
