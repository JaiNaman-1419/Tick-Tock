from pathlib import Path
from os import system as cmd
from config import SqliteConfig
from os.path import isdir, isfile
from os.path import join as pathjoiner
from database.migrations import create_database


BASE_DIR = Path(__file__).resolve().parent


if not isdir(pathjoiner(BASE_DIR, 'venv')):
    cmd('python3 -m venv venv')

if isdir(pathjoiner(BASE_DIR, 'venv')):
    cmd('source venv/bin/activate')

if isfile(pathjoiner(BASE_DIR, 'requirements.txt')):
    cmd('pip install -r requirements.txt')

if not isfile(pathjoiner(BASE_DIR, SqliteConfig().get_database_file_name)):
    create_database()
