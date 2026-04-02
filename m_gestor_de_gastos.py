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

def menu():
    print("")
    print("----- MENU -----")
    print("1. Agregar gasto")
    print("2. Eliminar gasto")
    print("3. Mostrar gastos")
    print("4. Mostrar total gastado")
    print("5. Salir")
    print("")
    
def agregar_gasto(gastos):
    while True: 
        try:
            monto = int(input("ingrese el monto: "))
            categoria = input("ingrese una categoria: ").capitalize()
            ahora = datetime.now()
            #agregando la fecha del ingreso del gasto nuevo
            fecha = ahora.strftime("%d/%m/%Y")
            gasto_nuevo = {
                "Monto" : monto,
                "Categoria" : f"{categoria}",
                "Fecha" : f"{fecha}"
            }
            gastos.append(gasto_nuevo)
            with open ("gastos.json", "w") as archivo:
                json.dump(gastos,archivo,indent=4) 
                print("")
                print("GASTO AGREGADO CORRECTAMENTE")
            break
        except Exception:
            print("")
            print("ERROR INTENTE DE NUEVO")
            print("")


def mostrar_gastos(gastos):
    if len(gastos) > 0:
        print("----- GASTOS -----")
        for i,gasto in enumerate(gastos):
            print(f"{i + 1}. ${gasto['Monto']} {gasto['Categoria']} {gasto['Fecha']}")
        print("-----------------")
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

def total_gastado(gastos):
    if len(gastos) > 0:
        total = 0
        print("----- TOTAL GASTADO -----")
        for gasto in gastos:
            total = total + gasto['Monto']
        print(f"El total gastado es de ${total}")
        print("-----------------")
        return total
    else: 
        print("No hay gastos que sumar")