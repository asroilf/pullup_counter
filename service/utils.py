import sys, logging
from peewee import SqliteDatabase

logging.basicConfig(level=logging.INFO, filename="bot_logs.log", format="%(asctime)s - %(levelname)s - %(message)s")
LOG = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s | %(levelname)s: %(message)s')
console_handler.setFormatter(console_formatter)

LOG.addHandler(console_handler)

