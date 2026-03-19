# algoritmo que me pide el enunciado: Imprima por pantalla el listado de directorios de inicio de los usuarios
# que hay en el sistema (p. ej., /home/root , /home/osboxes, . . . ). Pista: hayun fichero con esta información. 
with open("/etc/passwd", "r") as f:
    for linea in f:
        datos = linea.strip().split(":")
        if len(datos) > 5:
            print(datos[5])
