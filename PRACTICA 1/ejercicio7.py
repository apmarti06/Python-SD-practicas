#ejercicio 7
    # ver doc practica 1, para entender estos conceptos
def dict_add(my_dict, t):  # evaluamos las precondiciones 
    
    if t is None:
        raise ValueError("La tupla recibida no puede ser vacia")
    
    if type(t) != tuple or len(t) != 2:
        raise TypeError("Debe ser una tupla de dos elementos")
    
    #añadimos los nuevos valores a la clave, y al valor
    clave, valor = t
    my_dict[clave] = valor

    return my_dict

print(dict_add({1:'hola'}, {2:'mundo'}))

