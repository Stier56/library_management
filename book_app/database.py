import sqlite3
from flask import current_app, g

# データベースへの接続
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
    return g.db

# テーブルの作成
def create_table():
    con = get_db()
    sql = "CREATE TABLE books(isbn STRING PRIMARY KEY, title STRING, author STRING, publisher STRING, storage STRING, description STRING, thumbnail STRING)"
    con.execute(sql)



