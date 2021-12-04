import sys
from cx_Freeze import setup, Executable
import os

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

## The image and sound files are added manually into the zip file
## A fix for this would be released

setup (
    name="ImageNameExplorer",
    version="0.1",
    description="Program to put a tag on a photo using pyqt5",
    author="Morteza Abdollahi",
    author_email="mortezaabdollahi1385@gmail.com",
    options={   
        "build_exe": {
            "packages": ["os", "PyQt5", "Pillow", "Sqlite3", "slugify"],
            "include_files": [
                # uis files
                "app/uis/main.ui",
                "app/uis/splash_screen.ui",
                "app/uis/image_dialog.ui",
                # gss files
                "Combinear.qss",
                # icon files
                "app/icons/tag-icon.png",
                # python files
                "app/ui_functions.py",
                "import_db.py"
            ]
        },
    },
    executables=[Executable("app/main.py", base=base)]
)
