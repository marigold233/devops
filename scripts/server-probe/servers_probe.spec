# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('sanic')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


block_cipher = None

a = Analysis(
    ['samservers_probe.py'],       # 修改成你的打包文件
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
#    runtime_hooks=['hook.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)


# ============================魔改部分=================================================
# 将需要排除的模块写到一个列表（不带 .py）
my_modules = ['servers_probe_main', ]

# 将被排除的模块添加到 a.datas
for name in my_modules:
    source_file = name + '.py'
    dest_file = name + '.py'
    a.datas.append((source_file, dest_file, 'DATA'))

# 筛选 a.pure
a.pure = [x for x in a.pure if x[0] not in my_modules]
# =============================================================================




pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='servers_probe',        # 输出可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
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
    upx=True,
    upx_exclude=[],
    name='servers_probe',   # 输出可执行文件到的目录
)
