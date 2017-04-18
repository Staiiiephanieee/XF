# -*- mode: python -*-

block_cipher = None


a = Analysis(['main_window.py'],
             pathex=['/Users/XuZiQi/Desktop/study/computer science/Coding Competition/practice/The_Tragedy_of_the_Hanged_King'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas += Tree('resources', prefix='resources')
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main_window',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main_window')
