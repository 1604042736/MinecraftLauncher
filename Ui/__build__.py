import os


forget = ['__init__.py', '__build__.py']
path = os.path.dirname(__file__)
for filename in os.listdir(path):
    filepath = os.path.join(path, filename)
    root, ext = os.path.splitext(filepath)
    if os.path.isfile(filepath) and filename not in forget and ext == '.ui':
        os.system(f'pyuic5 {filepath} -o {root}_ui.py ')
