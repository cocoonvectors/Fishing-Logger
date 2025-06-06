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
                print(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])
            cur.close()
            return
    except sqlite3.OperationalError as e:
        print(e)

if __name__ == '__main__':
    main()
