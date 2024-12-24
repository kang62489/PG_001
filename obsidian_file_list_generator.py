## Author: Kang
## Established: 2024-12-02
## Last Updated: 2024-12-02
## Usage: To create a text table of files in a folder so that it can be directly copied and pasted to obsidian notes

## Module
from PySide6.QtWidgets import QFileDialog, QApplication
from pathlib import Path
from itertools import islice
from icecream import ic
ic.configureOutput(prefix="debug | ", includeContext=False)

## Funtions
space =  '    '
branch = '│   '
tee =    '├── '
last =   '└── '

def tree(dir_path: Path, level: int=-1, limit_to_directories: bool=False,
         length_limit: int=1000):
    """Given a directory Path object print a visual tree structure"""
    dir_path = Path(dir_path) # accept string coerceable to Path
    files = 0
    directories = 0
    def inner(dir_path: Path, prefix: str='', level=-1):
        nonlocal files, directories
        if not level: 
            return # 0, stop iterating
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else: 
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space 
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1
    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' + (f', {files} files' if files else ''))


# Generate a dialog to request file directory
def get_folder():
    caption = 'Please choose a directory of expdata which contains both ".tif" and ".rec" files.'
    init_dir = ""
    dialog = QFileDialog()
    dialog.setWindowTitle(caption)
    dialog.setDirectory(init_dir)
    dialog.setFileMode(QFileDialog.FileMode.Directory)
    check = dialog.exec()
    if check:
        return dialog.selectedFiles()[0]
    

# Set event handler
app = QApplication()

# Get a directory of experiment data
dir_files = get_folder()

if dir_files != None:
    print("<Dir Selected>", dir_files)
    tree(dir_files)
else:
    print('Selected directory = ',dir_files)
    print("Process cancelled!")