import os
from datetime import datetime
from loguru import logger
from pathlib import Path
from dotenv import load_dotenv
from peewee import SqliteDatabase

load_dotenv()

BASE_DIR = Path(__file__).parent
DICTIONARY_PATH = BASE_DIR / 'data/dictionary.json'
NOTIFIER_ICON_PATH = None
NOTIFIER_DURATION = 5
LINGVO_API_KEY = os.environ.get('LINGVO_API_KEY')

DB_PATH = BASE_DIR / 'data/db.sqlite3'
DB = SqliteDatabase(DB_PATH)

logger.add(
    (BASE_DIR / f'data/logs/work.log').as_posix(),
    rotation='10 mb',
    compression='zip'
)
