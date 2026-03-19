# Python program to convert two lists into a dictionary

index = [1, 2, 3]
languages = ['python', 'c', 'c++']

# Crea un diccionario con los elementos de las listas
# zip() crea un iterador que combina los elementos de dos o más listas
# dict() crea un diccionario a partir de una lista de pares clave-valor
dictionary = dict(zip(index, languages))
print(dictionary)