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


def mostrar_gastos(gastos):
    if len(gastos) > 0:
        total = 0
        print("----- GASTOS -----")
        for i,gasto in enumerate(gastos):
            print(f"{i + 1}. ${gasto['Monto']} {gasto['Categoria']} {gasto['Fecha']}")
            total = total + gasto['Monto']
        print("")
        print(f"Total gastado: ${total}")
        print("---------------------")
        return total
    else: 
        print("No hay gastos que mostrar")

def eliminar_gasto(gastos):
    mostrar_gastos(gastos)
    try:
        gasto_eliminado = int(input("Ingrese el gasto que desea eliminar: "))
        if gasto_eliminado < 1 or gasto_eliminado > len(gastos):
            print("Opcion inexistente")
        else:
            eliminacion = gastos.pop(gasto_eliminado - 1)
            print("")
            print(f"Se elimino: ${eliminacion ['Monto']} {eliminacion['Categoria']} {eliminacion['Fecha']}")
            with open ("gastos.json", "w") as archivo:
                json.dump(gastos,archivo,indent=4) 
                print("GASTO ELIMINADO CORRECTAMENTE")
            return gastos
    except Exception:
        print("")
        print("ERROR INTENTE DE NUEVO")
        print("")

def filter_cat(gastos):
    search_cat = input("Ingrese la categoria: ").capitalize()
    encontrado = False
    print("")
    for gasto in gastos:
        if gasto["Categoria"] == search_cat:
            if encontrado == False:
                print(f"----- {search_cat} -----")
            print(f"{gasto['Monto']} {gasto['Categoria']} {gasto['Fecha']}")
            encontrado = True
    if encontrado == False:
        print("No hay gastos en esa categoria")

def ordenar_gastos(gastos):
    gastos.sort(key = lambda gasto: datetime.strptime(gasto["Fecha"],"%Y-%m-%d") , reverse = True)
