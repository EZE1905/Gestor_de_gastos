import sqlite3 

def obtener_movimientos():
    with sqlite3.connect("database/gastos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos')
        movimientos = cursor.fetchall()
    return movimientos

def calcular_movimientos(movimientos):
    total_ingresos = 0
    total_gastado = 0
    for movimiento in movimientos:
        if movimiento["Tipo"] == "ingreso":
            total_ingresos = total_ingresos + movimiento["Monto"]
        elif movimiento["Tipo"] == "gasto":
            total_gastado = total_gastado + movimiento["Monto"]
    saldo = total_ingresos - total_gastado
    return saldo,total_gastado,total_ingresos

def agregar_movimiento(id_usuario,monto,categoria,tipo,fecha):
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO movimientos (id_usuario,monto,categoria,tipo,fecha) VALUES (?,?,?,?,?)',(id_usuario,monto,tipo,categoria,fecha))
        conn.commit()

def eliminar_movimiento(id_movimiento):
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movimientos WHERE id_movimiento = ?',(id_movimiento,))
        conn.commit()