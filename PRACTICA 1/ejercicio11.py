def union_listas(lista_a, lista_b):
    #evauluamos que sean listas, y luego que ambas posean el mismo tamaño
    if type(lista_a) != list or type(lista_b) != list:
        raise TypeError("Ambos argumentos deben de ser listas")
    if len(lista_a) != len(lista_b):
        raise ValueError("Ambas listas han de ser de la misma longitud")
    
    #creamos la lista vacia
    resultado = [] 
    #concatenamos cadenas!!!
    for e in lista_a + lista_b:
        if e not in resultado:
            resultado.append(e)

    print(resultado)

    return resultado

#Alternativa se podria crear variable:
# vistos = set()  
# for e in lista_a + lista_b:
#   if e not in vistos:
#  añadimos tanto en vistos y en resultado, siendo código más leible


union_listas((2, 3, 2, 8, 1, 9) , (2, 9, 2, 7, 1, 9))