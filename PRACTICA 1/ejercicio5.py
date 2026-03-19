#ejercicio 5

def lista_add(my_list, e):
    #verificamos que no sea none
    if e is None or not my_list: #verifica si el elemento es nulo, o la lista está vacia
        raise ValueError("El valor introducido no es valido")
    
    # recorremos toda la lista entera, verificando si es nuevo
    verdadero = True
    for i in my_list:
        if i == e:
            verdadero = False
            break
    
    if verdadero == True:
        print(my_list)
        my_list.add(e)

lista_add([3, 4, 1, 6, 8, 2, 2], 2)


