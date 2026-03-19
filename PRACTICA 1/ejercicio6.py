#6to ejercicio

def lista_del(my_list, e):
    #verificamos que no sea none
    if e is None:
        raise ValueError("El valor introducido no es valido")

    i = 0 #inicializamos el índice
    while i < len(my_list): #usamos while para controlar las iteraciones al borrar elementos de la lista
        if my_list[i] == e:
            print("Se ha encontrado una ocurrencia en la posicion:", i)
            my_list.pop(i) #se actualiza automaticamente (recordad como funciona una pila)
        else:
            i += 1

    print(my_list)

lista_del([3, 4, 1, 6, 8, 2, 2], 2)