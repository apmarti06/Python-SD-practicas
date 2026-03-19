#ejercicio 8

import math #usamos libreria para usar la raíz, para verificar condición de parada

#funcion ajena que verifica si un número es primo
def es_primo(x):
    if (x <= 1):
        return False
    for i in range (2, int(math.sqrt(x)) + 1):
        if x % 2 == 0:
            return False
        
    return True
#verificación numero primo


def prime(a, b):
    if type(a) != int or type (b) != int:
        raise TypeError("Los tipos introducidos no son números enteros")
    
    if a == None or b == None:
        raise ValueError("Los valores han de ser positivo")

    my_list = []

    for i in range(a, b+1):
        if es_primo(i):
            my_list.append(i)

    print(my_list) #imprimimos el resultado

    return my_list

prime(3, 37)
