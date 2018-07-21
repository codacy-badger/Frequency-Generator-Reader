# -*- mode: python -*-

block_cipher = None


a = Analysis(['controller.py'],
             pathex=['C:\\Users\\david\\Dropbox\\Work\\Yura Program'],
             binaries=[],
             datas=[],
             hiddenimports=['wtforms', 'scanner.scan', 'scanner.bin_to_csv',
             'scanner.gen_png', 'pathlib', 'pickle', 'sys', 'threading', 'shutil',
             'os', 'numpy', 'scanner.hantekdds.htdds_wrapepr', 'ctypes', 'csv', 'matplotlib',
             'io', 'base64', 'model'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))
    return extra_datas
a.datas += extra_datas("static")
a.datas += extra_datas("templates")
a.datas += extra_datas("scanner")

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='controller',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
