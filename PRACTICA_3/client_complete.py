import requests
import os

BASE_URL = "http://localhost:8080"

# ==============================
# GET: Prueba saludo con múltiples rutas
# ==============================

def test_get_saludo():
    response = requests.get(f"{BASE_URL}/saludo")
    print("GET /saludo:", response.text)

    response = requests.get(f"{BASE_URL}/saludo/Carlos")
    print("GET /saludo/Carlos:", response.text)

# ==============================
# GET: Obtener información
# ==============================

def test_get():
    """ Prueba el endpoint GET /productos """
    response = requests.get(f"{BASE_URL}/productos")
    print("GET /productos:", response.json())

    """ Prueba el endpoint GET /productos/1 """
    response = requests.get(f"{BASE_URL}/productos/1")
    print("GET /productos/1:", response.json())

# ==============================
# POST: Crear un nuevo producto
# ==============================

def test_create():
    """ Prueba el endpoint POST /productos """
    data = {"nombre": "Producto C", "precio": 300}
    response = requests.post(f"{BASE_URL}/productos", json=data)
    print("POST /productos:", response.json())

# ==============================
# PUT: Actualizar un producto
# ==============================

def test_update():
    """ Prueba el endpoint PUT /productos/1 """
    data = {"nombre": "Producto A Modificado", "precio": 150}
    response = requests.put(f"{BASE_URL}/productos/1", json=data)
    print("PUT /productos/1:", response.json())

# ==============================
# DELETE: Eliminar un producto
# ==============================

def test_delete():
    """ Prueba el endpoint DELETE /productos/2 """
    response = requests.delete(f"{BASE_URL}/productos/2")
    print("DELETE /productos/2:", response.json())


# ==============================
# POST: Subir un archivo
# ==============================

def test_upload():
    file_name = "test_upload.txt"

    if not os.path.exists(file_name):
        with open(file_name, "w") as file:
            file.write("Este es un archivo de prueba.")

    with open(file_name, 'rb') as file:
        response = requests.post(f"{BASE_URL}/subir", files={"archivo": file})
        print("POST /subir:", response.json())

if __name__ == "__main__":
    print("\n--- Prueba de saludo con múltiples rutas ---")
    test_get_saludo()

    print("\n--- Pruebas de GET ---")
    test_get()

    print("\n--- Pruebas de POST (Crear) ---")
    test_create()

    print("\n--- Pruebas de PUT (Actualizar) ---")
    test_update()

    print("\n--- Pruebas de DELETE (Eliminar) ---")
    test_delete()

    print("\n--- Pruebas finales de GET ---")
    test_get()

    print("\n--- Prueba de subida de archivos ---")
    test_upload()
