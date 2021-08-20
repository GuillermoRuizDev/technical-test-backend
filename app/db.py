from peewee import SqliteDatabase

# SQLite database using WAL journal mode and 64MB cache.
db = SqliteDatabase('database.db')

