import os

def get_file_info(filename):
    if filename is None:
        raise ValueError("Filename es None") 
    if type(filename) != str:
        raise TypeError("El filename ha de declararse como string")
    if not os.path.exists(filename): 
        raise FileNotFoundError("El fichero no existe")

    tamano = os.path.getsize(filename)

    palabras_buscadas = []
    entrada = input("Ingresa la letra que buscamos la ocurrencia:")

    while True:
        if (len(entrada) == 1 and entrada.isalpha()):
            letra = entrada
            break
        else:
            print("No es valido el caracter, intentelo de nuevo")
            entrada = input("Ingresa la letra que buscamos la ocurrencia: ")

    with open(filename, "r") as f: 
        texto = f.read()

    palabras = texto.split()

    for palabra in palabras:
        if palabra.endswith(letra):
            palabras_buscadas.append(palabra)

    print(f"Tamano del archivo: {tamano} bytes")
    print(f"Palabras que terminan en '{letra}': {palabras_buscadas}")
    
    return (tamano, palabras_buscadas)

# Llamada a la funcion
get_file_info("prueba_ej9.txt")