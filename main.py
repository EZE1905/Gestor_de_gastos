from m_gestor_de_gastos import leer_gastos,menu,agregar_gasto
import json

gastos = leer_gastos()
while True:
    menu()
    try:
        eleccion = int(input("Ingrese una opcion: "))
        print("")
    except Exception:
        print("Elija una de las opciones.")
    if eleccion not in [1,2,3]:
        print("Opcion inexistente")
    elif eleccion == 1:
        agregar_gasto(gastos)
    elif eleccion == 2:
        print(gastos)
    elif eleccion == 3:
        break