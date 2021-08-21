from peewee import SqliteDatabase
from bottle import hook

# SQLite database using WAL journal mode and 64MB cache.
db = SqliteDatabase('database.db')

# @hook('before_request')
# def _connect_db():
#     db.connect()

# @hook('after_request')
# def _close_db():
#     if not db.is_closed():
#         db.close()