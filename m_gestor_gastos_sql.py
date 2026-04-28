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
        cursor.execute('INSERT INTO movimientos (id_usuario,monto,categoria,tipo,fecha) VALUES (?,?,?,?,?)',(id_usuario,monto,categoria,tipo,fecha))
        conn.commit()

def eliminar_movimiento(id_movimiento):
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movimientos WHERE id_movimiento = ?',(id_movimiento,))
        conn.commit()

def obtener_un_movimiento(id_movimiento):
    with sqlite3.connect("database/gastos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos WHERE id_movimiento = ?',(id_movimiento,))
        movimiento = cursor.fetchone()
    return movimiento

def editar_movimiento(id_movimiento,monto,tipo,categoria,fecha):
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE movimientos SET monto = ?,categoria = ?,tipo = ?,fecha = ? WHERE id_movimiento = ?',(monto,categoria,tipo,fecha,id_movimiento))
        conn.commit()

def obtener_movimientos_por_mes(mes):
    if mes:
        mes_sql = mes + "%"
        with sqlite3.connect("database/gastos.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM movimientos WHERE fecha LIKE ?',(mes_sql,))
            movimientos_por_mes = cursor.fetchall()
        return movimientos_por_mes
    else:
        movimientos = obtener_movimientos()
        return movimientos
    
def meses(mes):
    if mes: 
        resultado = mes.split("-")
        ano = resultado[0]
        mes_format = resultado[1]
        mesesformat = {
            "01": "Enero",
            "02": "Febrero",
            "03": "Marzo",
            "04": "Abril",
            "05": "Mayo",
            "06": "Junio",
            "07": "Julio",
            "08": "Agosto",
            "09": "Septiembre",
            "10": "Octubre",
            "11": "Noviembre",
            "12": "Diciembre"
        }
        mesmarcado = mesesformat[mes_format].capitalize()
        mestitulo = f"Movimientos de {mesmarcado} {ano}"
    else:
        mestitulo = "Todos los movimientos"
    return mestitulo

def total_meses(movimientos):
    ingresos_meses = {}
    movimientos_meses = {}
    for gasto in movimientos:
        fecha = gasto["Fecha"].split("-")
        fecha_mes = fecha[0] + "-" + fecha[1]
        monto = gasto["Monto"]
        if gasto["Tipo"] == "ingreso":
            if fecha_mes in ingresos_meses:
                ingresos_meses[fecha_mes] = ingresos_meses[fecha_mes] + monto
            else:
                ingresos_meses[fecha_mes] = monto
        elif gasto["Tipo"] == "gasto":
            if fecha_mes in movimientos_meses:
                movimientos_meses[fecha_mes] = movimientos_meses[fecha_mes] + monto
            else:
                movimientos_meses[fecha_mes] = monto
    return ingresos_meses, movimientos_meses