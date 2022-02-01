# 29 January 2022 - Modified by KuschAoe
"""
This manages compiling the app with Nuitka and packaging it

"""

import os
import shutil
from zipfile import ZIP_DEFLATED, ZipFile

# Run nuitka
os.system('cmd /c "python -m nuitka'
          ' --plugin-enable=pyqt5'
          ' --standalone'
          ' --windows-disable-console'
          ' --windows-icon-from-ico=src/img/icon.ico'
          ' --include-data-dir=src/img=img'
          ' --include-data-dir=src/AoE4LuaScript=AoE4LuaScript'
          ' src/AoE4_ReplayOverlay.py')

# Zip
file_name = f"AoE4_ReplayOverlay.zip"

to_zip = []
folder = 'AoE4_ReplayOverlay.dist'
for root, directories, files in os.walk(folder):
    for f in files:
        to_zip.append(os.path.join(root, f))

print('Compressing files...')
with ZipFile(file_name, 'w', compression=ZIP_DEFLATED) as zip:
    for f in to_zip:
        zip.write(f, f"AoE4_ReplayOverlay/{f[len(folder)+1:]}")

# Cleanup
for item in (folder, ):
    if os.path.isdir(item):
        shutil.rmtree(item)
