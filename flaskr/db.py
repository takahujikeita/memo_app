import sqlite3

DATABASE='database.db'

def create_books_table():
    connection=sqlite3.connect(DATABASE)
    connection.execute("create table if not exists books (title , price , arrival_day)")
    connection.close()