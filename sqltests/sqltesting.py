import sqlite3

def main():

    try:
        with sqlite3.connect("fishing.db") as conn:
            tables = '''INSERT INTO species(id, name, common_name, region)
                        VALUES("1","test","test","test")'''

            cur = conn.cursor()
            cur.execute(tables)
            conn.commit()

            return cur.lastrowid

    except sqlite3.OperationalError as e:
        print(e)

if __name__ == '__main__':
    main()
