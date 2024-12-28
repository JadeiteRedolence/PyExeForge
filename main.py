"""
Welcome to PyExeForge - Python Program Packaging Tool!

Author: Volkath@amazoncloud
Version: 1.0.0
Build Date: 2024.12.28

This is an easy-to-use Python program packaging tool. It can:

✓ Convert Python scripts to executable files
✓ Customize output filename and version info 
✓ Add UAC admin privileges
✓ Generate single-file programs
"""

from os import system as cmd, chdir, getcwd, popen as rcmd, rename, remove, _exit as quit, makedirs
from os.path import split as sp, splitext as spt, basename as bn, exists, expanduser
from tkinter.filedialog import askopenfilename
from datetime import datetime
import tkinter as tk
from time import sleep

# Get user input for version info
print("\nPlease enter program information:")
BASE_NAME = input("Program base name: ").strip()
VERSION = input("Program version (e.g. 1.0.0): ").strip()
BUILD_DATE = datetime.now().strftime("%Y.%m.%d")

root = tk.Tk()
root.attributes('-topmost', 1)
root.withdraw()

# Define constant directories
INIT_DIR = 'D:\\Proccess\\Python3\\'
makedirs(INIT_DIR, exist_ok=True)
OUTPUT_DIR = 'D:\\Proccess\\PyDevelopment\\'
makedirs(OUTPUT_DIR, exist_ok=True)
chdir(OUTPUT_DIR)

def pws(s):
    cmd(f'powershell -Command \"{s}\"')

def get_py_file():
    return askopenfilename(
        title='Select Python File to Convert',
        filetypes=[('Python Files', '*.py')],
        initialdir=INIT_DIR
    )

def get_custom_names(base_name):
    print("\nPlease enter custom names (press Enter to use defaults):")
    
    # Get custom output filename
    custom_output = input(f"Output filename (default: {BASE_NAME}_v{VERSION}_Build{BUILD_DATE}): ").strip()
    output_name = custom_output if custom_output else f"{BASE_NAME}_v{VERSION}_Build{BUILD_DATE}"
    
    # Get custom version filename
    custom_version = input(f"Version info filename (default: version_{BASE_NAME}.txt): ").strip()
    version_name = custom_version if custom_version else f"version_{BASE_NAME}.txt"
    
    return output_name, version_name

def generate_version_info(output_name, version_name):
    version_info = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Volkath@amazoncloud'),
         StringStruct(u'FileDescription', u'{output_name} Application'),
         StringStruct(u'FileVersion', u'{VERSION}'),
         StringStruct(u'InternalName', u'{output_name}'),
         StringStruct(u'LegalCopyright', u'© 2025 Volkath@amazoncloud. All rights reserved.'),
         StringStruct(u'OriginalFilename', u'{output_name}.exe'),
         StringStruct(u'ProductName', u'{output_name}'),
         StringStruct(u'ProductVersion', u'{VERSION}'),
         StringStruct(u'Comments', u'https://gitee.com/amazoncloud')])
    ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""
    with open(version_name, 'w', encoding='utf-8') as f:
        f.write(version_info)
    return version_name

def convert_to_exe(py_file):
    # Get base filename without extension
    base_name = spt(bn(py_file))[0]
    
    # Get custom filenames
    output_name, version_name = get_custom_names(base_name)
    
    # Generate version info file
    version_file = generate_version_info(output_name, version_name)
    
    # Build command with output to constant directory
    command = (
        f'pyinstaller '
        f'-F --uac-admin --uac-uiaccess '
        f'--version-file=\'{version_file}\' '
        f'--name \'{output_name}\' '
        f'--distpath . '
        f'--workpath . '
        f'--specpath . '
        f'\'{py_file}\''
    )
    
    print(f'\nExecuting command:\n{command}\n')
    pws(command)
    
    # Clean up version info file
    remove(version_file)

def main():
    py_file = get_py_file().replace('/', '\\')
    if py_file:
        convert_to_exe(py_file)
        print('\nConversion completed.')
    else:
        print('\nNo file selected.')
    pws('Start-Process .')
    quit(0)

if __name__ == '__main__':
    main()