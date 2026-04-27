import json
from datetime import datetime

def leer_movimientos():
    try:
        with open ("movimientos.json") as archivo:
            #leemos el json
            movimientos = json.load(archivo)
    except FileNotFoundError:
        with open("movimientos.json", "w") as archivo:
            #movimientos es lo que quiero guardar y archivo es en donde lo quiero guardar
            movimientos = json.dump(movimientos,archivo)
    return movimientos
    
def agregar_gasto(movimientos,gasto):
            movimientos.append(gasto)
            with open ("movimientos.json", "w") as archivo:
                json.dump(movimientos,archivo,indent=4) 

def eliminar_gasto(movimientos,indice):
    movimientos.pop(indice)
    with open ("movimientos.json", "w") as archivo:
        json.dump(movimientos,archivo,indent=4) 
        return movimientos

def ordenar_movimientos(movimientos):
    movimientos.sort(key = lambda gasto: datetime.strptime(gasto["Fecha"],"%Y-%m-%d") , reverse = True)

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

def calcular_por_categoria(movimientos_mes):
    cat_ingresos = {}
    cat_movimientos = {}
    for gasto in movimientos_mes:
        categoria = gasto["Categoria"]
        monto = gasto["Monto"]
        if gasto["Tipo"] == "ingreso":
            if categoria in cat_ingresos:
                cat_ingresos[categoria] = cat_ingresos[categoria] + monto
            else:
                cat_ingresos[categoria] = monto
        elif gasto["Tipo"] == "gasto":
            if categoria in cat_movimientos:
                cat_movimientos[categoria] = cat_movimientos[categoria] + monto
            else:
                cat_movimientos[categoria] = monto
    return cat_movimientos, cat_ingresos

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
        mestitulo = mesmarcado + " " + ano
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