import math

def seleccionar_fluidos():
    # Lista de fluidos de hidrocarburos
    fluidos = [
        "Metano (CH4)",
        "Etano (C2H6)",
        "Propano (C3H8)",
        "Butano (C4H10)",
        "Pentano (C5H12)",
        "Hexano (C6H14)",
        "Heptano (C7H16)",
        "Octano (C8H18)",
        "Nonano (C9H20)",
        "Decano (C10H22)"
    ]

    # Mostrar la lista de fluidos disponibles
    print("Lista de fluidos de hidrocarburos disponibles:")
    for i, fluido in enumerate(fluidos, 1):
        print(f"{i}. {fluido}")

    # Pedir al usuario que elija dos fluidos
    try:
        seleccion1 = int(input("Selecciona el número del primer fluido: ")) - 1
        seleccion2 = int(input("Selecciona el número del segundo fluido: ")) - 1

        # Verificar que las selecciones sean válidas
        if seleccion1 not in range(len(fluidos)) or seleccion2 not in range(len(fluidos)):
            print("Selección inválida. Inténtalo de nuevo.\n")
            return seleccionar_fluidos()  # Llamar de nuevo a la función si la selección no es válida

        if seleccion1 == seleccion2:
            print("Por favor, selecciona dos fluidos diferentes.\n")
            return seleccionar_fluidos()

        # Mostrar los fluidos seleccionados
        fluido1 = fluidos[seleccion1]
        fluido2 = fluidos[seleccion2]
        print(f"Has seleccionado: {fluido1} y {fluido2}")

        # Devolver los fluidos seleccionados
        return fluido1, fluido2

    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.\n")
        return seleccionar_fluidos()  # Llamar de nuevo a la función si ocurre un error de tipo

# Ejemplo de uso
fluido1, fluido2 = seleccionar_fluidos()

def calculate_mldt():
    try:
        temp_ff1 = float(input(f"Indica la temperatura de entrada del fluido frio {fluido1}: "))
        temp_ff2 = float(input(f"Indica la temperatura de salida del fluido frio {fluido1}: "))
        temp_fc1 = float(input(f"Indica la temperatura de entrada del fluido caliente {fluido2}: "))
        temp_fc2 = float(input(f"Indica la temperatura de salida del fluido caliente {fluido2}: "))
        if temp_ff2>temp_fc2:
            print("Esto no es posible, la temperatura de salida del fluido frio no puede ser superior a la temperatura de salida del fluido caliente. Por vaor intentalo de nuevo\n")
            return calculate_mldt()
        u_t1 = temp_ff1
        u_t2 = temp_ff2
        u_T1 = temp_fc1
        u_T2 = temp_fc2
        try:
            delta_T1 = u_T2-u_t1
            delta_T2 =  u_T1-u_t2
            mldt = (delta_T2-delta_T1)/math.log(delta_T2/delta_T1)
            print(f"La temperatura media logaritmica es {mldt} °F")
        except ValueError:
            print("Error: las diferencias de temperatura deben ser positivas.\n")
            return calculate_mldt()
        mldtValue = mldt
        print(f"La temperatura media logaritmica es {mldtValue} °F")
        return mldtValue 
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.\n")
        return calculate_mldt()

mldtValue = calculate_mldt()

