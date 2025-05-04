import sqlite3

database = 'fishing.db'
tables = open('init_db.sql',"r")
sql_statements = tables.read()


try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.executescript(sql_statements)
        conn.commit()

except sqlite3.OperationalError as e:
    print(e)
