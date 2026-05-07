import sqlite3 
from werkzeug.security import generate_password_hash, check_password_hash

def crear_tabla_usuarios():
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def agregar_usuario(username, password):
    password_hash = generate_password_hash(password)
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (username, password_hash) VALUES (?, ?)', (username, password_hash))
        conn.commit()

def verificar_usuario(username, password):
    with sqlite3.connect("database/gastos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE username = ?', (username,))
        usuario = cursor.fetchone()
        if usuario and check_password_hash(usuario['password_hash'], password):
            return usuario
    return None

def obtener_usuario_por_id(id_usuario):
    with sqlite3.connect("database/gastos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id_usuario = ?', (id_usuario,))
        usuario = cursor.fetchone()
    return usuario 

def obtener_movimientos(id_usuario):
    with sqlite3.connect("database/gastos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos WHERE id_usuario = ?', (id_usuario,))
        movimientos = cursor.fetchall()
    return movimientos

def calcular_movimientos(movimientos_por_mes):
    total_ingresos = 0
    total_gastado = 0
    for movimiento in movimientos_por_mes:
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

def eliminar_movimiento(id_movimiento, id_usuario):
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM movimientos WHERE id_movimiento = ? AND id_usuario = ?', (id_movimiento, id_usuario))
        conn.commit()

def obtener_un_movimiento(id_movimiento, id_usuario):
    with sqlite3.connect("database/gastos.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movimientos WHERE id_movimiento = ? AND id_usuario = ?', (id_movimiento, id_usuario))
        movimiento = cursor.fetchone()
    return movimiento

def editar_movimiento(id_movimiento,monto,tipo,categoria,fecha, id_usuario):
    with sqlite3.connect("database/gastos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE movimientos SET monto = ?,categoria = ?,tipo = ?,fecha = ? WHERE id_movimiento = ? AND id_usuario = ?',(monto,categoria,tipo,fecha,id_movimiento, id_usuario))
        conn.commit()

def obtener_movimientos_por_mes(mes, id_usuario):
    if mes:
        mes_sql = mes + "%"
        with sqlite3.connect("database/gastos.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM movimientos WHERE fecha LIKE ? AND id_usuario = ?', (mes_sql, id_usuario))
            movimientos_por_mes = cursor.fetchall()
        return movimientos_por_mes
    else:
        movimientos = obtener_movimientos(id_usuario)
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
    gastos_meses = {}
    for movimiento in movimientos:
        fecha = movimiento["Fecha"].split("-")
        fecha_mes = fecha[0] + "-" + fecha[1]
        monto = movimiento["Monto"]
        if movimiento["Tipo"] == "ingreso":
            if fecha_mes in ingresos_meses:
                ingresos_meses[fecha_mes] = ingresos_meses[fecha_mes] + monto
            else:
                ingresos_meses[fecha_mes] = monto
        elif movimiento["Tipo"] == "gasto":
            if fecha_mes in gastos_meses:
                gastos_meses[fecha_mes] = gastos_meses[fecha_mes] + monto
            else:
                gastos_meses[fecha_mes] = monto
    return ingresos_meses, gastos_meses

def calcular_por_categoria(movimientos_por_mes):
    cat_ingresos = {}
    cat_gastos = {}
    for movimiento in movimientos_por_mes:
        categoria = movimiento["Categoria"]
        monto = movimiento["Monto"]
        if movimiento["Tipo"] == "ingreso":
            if categoria in cat_ingresos:
                cat_ingresos[categoria] = cat_ingresos[categoria] + monto
            else:
                cat_ingresos[categoria] = monto
        elif movimiento["Tipo"] == "gasto":
            if categoria in cat_gastos:
                cat_gastos[categoria] = cat_gastos[categoria] + monto
            else:
                cat_gastos[categoria] = monto
    return cat_gastos, cat_ingresos