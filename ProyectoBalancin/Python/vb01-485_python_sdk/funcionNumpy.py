import numpy as np

def map_value_numpy(value, from_low, from_high, to_low, to_high):
    return np.interp(value, [from_low, from_high], [to_low, to_high])

while True:

    #Valor que esta obteniendo el acelerometro es decir current_position
    #Para pruebas se introducira el valor por el teclado
    valor_original = input("\nValor: ")  

    #Rango de valores del acelerometro en grados
    rango_original_min = 0
    rango_original_max = 180

    #Rango de valores de la velocidad del motor
    rango_nuevo_min = 1000
    rango_nuevo_max = 2000

    valor_mapeado = map_value_numpy(valor_original,rango_original_min, rango_original_max, rango_nuevo_min, rango_nuevo_max)

    print("Valor original: ",valor_original," \nValor mapeado: ", valor_mapeado)
