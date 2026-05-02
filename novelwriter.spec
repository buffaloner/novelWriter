# -*- mode: python ; coding: utf-8 -*-
# https://github.com/paulocoutinhox/pyinstaller-sample/blob/master/My%20App.spec
# TODO: https://github.com/pyinstaller/pyinstaller/wiki/Recipe-OSX-Code-Signing
import os
import shutil
import platform

def create_sample_zip():
    base_dir = os.path.abspath(os.getcwd())
    src = os.path.join(base_dir, "sample")
    dest = os.path.join(base_dir, "novelwriter", "assets", "sample")
    if os.path.exists(src):
        shutil.make_archive(dest, 'zip', src)

create_sample_zip()

def get_path(filename):
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    if platform.system() == "Darwin":
        from AppKit import NSBundle
        file = NSBundle.mainBundle().pathForResource_ofType_(name, ext)
        return file or os.path.realpath(filename)
    else:
        return os.path.realpath(filename)


# general
root_dir = os.path.abspath(os.getcwd())
platform_name = platform.system().lower()
extras_dir = os.path.join(root_dir, "novelwriter/assets/")

# platform data
program_name = "novelWriter"
icon_path = None
program_file = None

if platform_name == "darwin":
    icon_path = os.path.join(extras_dir,"icons", "icon.iconset", "novelwriter.icns")
    program_file = "{0}.app".format(program_name)
elif platform_name == "linux":
    icon_path = os.path.join(extras_dir, "linux", "icon.png")
    program_file = "{0}".format(program_name)
elif platform_name == "windows":
    icon_path = os.path.join(extras_dir, "windows", "icon.ico")
    program_file = "{0}.exe".format(program_name)

# pyinstaller
block_cipher = None

a = Analysis(
    [
        os.path.join(
            "novelWriter.py",
        )
    ],
    pathex=[
        root_dir,
        os.path.join(root_dir, "novelWriter.py"),
    ],
    binaries=[],
    datas=[
        (os.path.join(root_dir, "novelwriter/assets"), "novelwriter/assets"),
    ],
    # hiddenimports=[
    #     "modules.app",
    #     "modules.datetime",
    #     "modules.net",
    #     "modules.system",
    #     "clr_loader",
    #     "pythonnet",
    # ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=program_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=program_name,
)

app = BUNDLE(
    coll,
    name=program_file,
    icon=icon_path,
    bundle_identifier="com.buffaloner.novelwriter",
    onedir=True,
    info_plist={
    'NSPrincipalClass': 'NSApplication',
    'NSAppleScriptEnabled': False,
    'CFBundleDocumentTypes': [
        {
            # 'CFBundleTypeName': 'My File Format',
            # 'CFBundleTypeIconFile': 'MyFileIcon.icns',
            # 'LSItemContentTypes': ['com.example.myformat'],
            'LSHandlerRank': 'Owner'
            }
        ]
    },
)

    # info_plist = {
    #     'CFBundleName': program_name, # This sets the application name
    #     'CFBundleShortVersionString': '1.0.0a', # Your app version


    #     'NSStatusItem Preferred Position': 0,
    #     'LSUIElement': True, # This makes it a background app
    #     # Add other plist entries here
    # }


    #      )
