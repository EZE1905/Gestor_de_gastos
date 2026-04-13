import json
from datetime import datetime

def leer_gastos():
    try:
        with open ("gastos.json") as archivo:
            #leemos el json
            gastos = json.load(archivo)
    except FileNotFoundError:
        with open("gastos.json", "w") as archivo:
            #gastos es lo que quiero guardar y archivo es en donde lo quiero guardar
            gastos = json.dump(gastos,archivo)
    return gastos
    
def agregar_gasto(gastos,gasto):
            gastos.append(gasto)
            with open ("gastos.json", "w") as archivo:
                json.dump(gastos,archivo,indent=4) 

def eliminar_gasto(gastos,indice):
    gastos.pop(indice)
    with open ("gastos.json", "w") as archivo:
        json.dump(gastos,archivo,indent=4) 
        return gastos

def ordenar_gastos(gastos):
    gastos.sort(key = lambda gasto: datetime.strptime(gasto["Fecha"],"%Y-%m-%d") , reverse = True)

def calcular_gastos(gastos):
    total_ingresos = 0
    total_gastado = 0
    for gasto in gastos:
        if gasto["Tipo"] == "ingreso":
            total_ingresos = total_ingresos + gasto["Monto"]
        elif gasto["Tipo"] == "gasto":
            total_gastado = total_gastado + gasto["Monto"]
    saldo = total_ingresos - total_gastado
    return saldo,total_gastado,total_ingresos

def calcular_por_categoria(gastos):
    cat_ingresos = {}
    cat_gastos = {}
    for gasto in gastos:
        categoria = gasto["Categoria"]
        monto = gasto["Monto"]
        if gasto["Tipo"] == "ingreso":
            if categoria in cat_ingresos:
                cat_ingresos[categoria] = cat_ingresos[categoria] + monto
            else:
                cat_ingresos[categoria] = monto
        elif gasto["Tipo"] == "gasto":
            if categoria in cat_gastos:
                cat_gastos[categoria] = cat_gastos[categoria] + monto
            else:
                cat_gastos[categoria] = monto
    return cat_gastos, cat_ingresos

def filtrar_mes(mes,gastos):
    gastos_mes = []
    if mes:
        for gasto in gastos:
            if gasto["Fecha"].startswith(mes):
                gastos_mes.append(gasto)
        return gastos_mes
    else:
        return gastos

def meses(mes):
    if mes: 
        resultado = mes.split("-")
        ano = resultado[0]
        mes_format = resultado[1]
        mesesformat = {
            "01" : "enero",
            "02" : "febrero",
            "03" : "marzo"
        }
        mesmarcado = mesesformat[mes_format].capitalize()
        mestitulo = mesmarcado + " " + ano
    else:
        mestitulo = "Todos los movimientos"
    return mestitulo