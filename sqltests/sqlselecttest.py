import sqlite3



def main ():
    s = open("selecttest.sql","r")
    statements = s.read()

    try:
        with sqlite3.connect("fishing.db") as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(statements)
            rows = cur.fetchall()
            for row in rows:
                print(f"Name: {row['name']}, Common name: {row['common_name']}, Region: {row['region']}")
            cur.close()
            return
    except sqlite3.OperationalError as e:
        print(e)

if __name__ == '__main__':
    main()
