import math
def calculate_mldt (t1, t2, T1, T2):
    ##Primera evaluación Si t2 es mayo que T2, se genera error. la temperatura de salida del fluido frio no puede ser superior a la temperatura de salida del fluido caliente
    if t2>T2:
       return "esto no es posible, la temperaura de salida del fluido frio no puede ser superior a la temperauta de salida del fluido caliente."
    
    ##Se intenta realizar el calculo de la MLDT 
    try:
        delta_T1 = T2-t1
        delta_T2= T1-t2
        mldt = (delta_T2-delta_T1)/math.log(delta_T2/delta_T1)
        return mldt
    
    ##Si el resultado del intento de calcular la MLDT es negativo se envía mensaje de error
    except ValueError:
        return "Error: las diferencias de temperatura deben ser positivas."
    
u_t1=float(input("Ingrese la temperatura de entrada del fluido frio: "))
u_t2=float(input("Ingrese la temperatura de salida del fluido frio: "))
u_T1=float(input("Ingrese la temperatura de entrada del fluido caliente: "))
u_T2=float(input("Ingrese la temperatura de salida del fluido caliente: "))

lmdt = calculate_mldt(u_t1, u_t2, u_T1, u_T2)

print(f"la temperatura media a contracorriente es {lmdt} °F")