import json
from datetime import datetime,timedelta

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
    print("-----MENU-----")
    print("1. Agregar gasto")
    print("2. Mostrar gastos")
    print("3. Salir")
    print("")
    
def agregar_gasto(gastos):
    while True: 
        try:
            monto = int(input("ingrese el monto: "))
            categoria = input("ingrese una categoria: ").lower()
            ahora = datetime.now()
            #agregando la fecha del ingreso del gasto nuevo
            fecha = ahora.strftime("%d/%m/%Y")
            gasto_nuevo = {
                "Monto" : f"$ {monto}",
                "Categoria" : f"{categoria}",
                "Fecha" : f"{fecha}"
            }
            gastos.append(gasto_nuevo)
            with open ("gastos.json", "w") as archivo:
                json.dump(gastos,archivo) 
                print("")
                print("GASTO AGREGADO CORRECTAMENTE")
            break
        except Exception:
            print("ERROR INTENTE DE NUEVO")