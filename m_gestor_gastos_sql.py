import sqlite3 

def obtener_movimientos():
    with sqlite3.connect("database/movimientos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos')
        movimientos = cursor.fetchall()
        return movimientos
