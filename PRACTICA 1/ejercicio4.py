def accum(x, y, z) : 
    # verifica que los tipos sean correctos, si es incorrecto genera un error
    if type(x) != int or type(y) != int or type(z) != int:
        raise TypeError("Todos los argumentos han de ser enteros")
    #cuerpo de la función
    suma = 0
    
    if x % 2 == 0:
        suma += x
    if y % 2 == 0:
        suma += y
    if z % 2 == 0:
        suma += z
    
    return suma

print(accum(6, 4, 2))

    #otra forma def accum(x, y, z):
    