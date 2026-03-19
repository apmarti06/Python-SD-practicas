def interseccion_listas(lista_a, lista_b):
    #evauluamos que sean listas, y luego que ambas posean el mismo tamaño
    if type(lista_a) != list or type(lista_b) != list:
        raise TypeError("Ambos argumentos deben de ser listas")
    if len(lista_a) != len(lista_b):
        raise ValueError("Ambas listas han de ser de la misma longitud")
    
    resultado = []

    for a, b in zip(lista_a, lista_b):
        if (a == b):
            if a not in resultado:
                resultado.append(a)
            
    print(resultado)

    return resultado

interseccion_listas(( 2, 3, 2, 8, 1, 9) , ( 2, 9, 2, 7, 1, 9))


