import os
    #devolveremos el número de bytes del fichero, y la lista de palabras acabadas en s (tupla de elementos 2)
def get_file_info(filename): #verificamos precondiciones
    if filename is None:
        raise ValueError("Filename es None") 
    if type(filename) != str:
        raise TypeError("El filename ha de declararse como string")
    if not os.path.exists(filename): #verificamos que el fichero exista 
        raise FileNotFoundError("El fichero no existe")
    
    # cumplimos lo que nos pide de la función si las precondiciones son correctas

    tamano = os.path.getsize(filename)

    palabras_buscadas = [] #guardamos aquí las palabras buscadas
    entrada = input("Ingresa la letra que buscamos la ocurrencia")

    while True: #bucle infinito para recibir la entrada
        if (len(entrada) == 1 and entrada.isalpha()): # si se verifica ambas la entrada ha de ser correcta
            letra = entrada
            break
        else:
            print("No es valido el caracter, intentelo de nuevo")
            entrada = input("Ingresa la letra que buscamos la ocurrencia: ")

    #abrimos el fichero en modo lectura (read), y guardamos contenido en variable texto
    with open(filename, "r") as f: 
        texto = f.read()
    
    #buscamos que las palabras sean correctas, guardamos trozo a trozo las palabras
    palabras = texto.split()

    for palabra in palabras:
        if palabra.endswith(letra):
            palabras_buscadas.append(palabra)

    # retornamos lo que buscamoo
    return (tamano, palabras_buscadas)

get_file_info("prueba_ej9.txt")