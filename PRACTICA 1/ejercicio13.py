# algoritmo que me pide el enunciado: Imprima por pantalla el listado de directorios de inicio de los usuarios
# que hay en el sistema (p. ej., /home/root , /home/osboxes, . . . ). Pista: hay un fichero con esta información. 

with open("/etc/passwd", "r") as f:
    for linea in f:
        if linea != "":
            campos = linea.split(":")
            print(campos[5])

