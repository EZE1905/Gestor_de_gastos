from m_gestor_de_gastos import leer_gastos,menu,agregar_gasto,mostrar_gastos,eliminar_gasto,filter_cat


gastos = leer_gastos()
while True:
    menu()
    try:
        eleccion = int(input("Ingrese una opcion: "))
        print("")
        if eleccion not in [1,2,3,4,5]:
            print("Opcion inexistente")
        elif eleccion == 1:
            agregar_gasto(gastos)
        elif eleccion == 2:
            if len(gastos) > 0:
                eliminar_gasto(gastos)
            else:
                print("No hay gastos que eliminar")
        elif eleccion == 3:
            mostrar_gastos(gastos)
            print("solo otro commit")
        elif eleccion == 4:
            filter_cat(gastos)
            print("solo para no perder el push del dia")
        elif eleccion == 5:
            break
    except Exception:
        print("")
        print("Elija una de las opciones.")
        print("")