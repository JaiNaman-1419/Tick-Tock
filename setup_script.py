from pathlib import Path
from os import system as cmd
from os.path import isdir, isfile
from os.path import join as path_join
from database.migrations import create_database


BASE_DIR = Path(__file__).resolve().parent

if not isdir(path_join(BASE_DIR, 'venv')):
    cmd('python3 -m venv venv')

if isdir(path_join(BASE_DIR, 'venv')):
    cmd('source venv/bin/activate')

if isfile(path_join(BASE_DIR, 'requirements.txt')):
    cmd('pip install -r requirements.txt')

if not isfile(path_join(BASE_DIR, 'todos.db')):
    create_database()
