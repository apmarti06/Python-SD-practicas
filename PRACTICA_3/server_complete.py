import os
from bottle import Bottle, request, response, run

app = Bottle()

# Carpeta donde se guardarán los archivos subidos
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Diccionario para almacenar registros simulados
data_store = {
    "1": {"nombre": "Producto A", "precio": 100},
    "2": {"nombre": "Producto B", "precio": 200}
}
# ==============================
# GET: Método con múltiples rutas y texto plano
# ==============================


# @app.get('/saludo')
# @app.get('/saludo/<nombre>')
@app.route(['/saludo', '/saludo/<nombre>'])  # Múltiples rutas en un solo método
def saludo(nombre="invitado"):
    """
    Devuelve un saludo en texto plano.
    - Si accedes a `/saludo`, devuelve "Hola, invitado!".
    - Si accedes a `/saludo/Carlos`, devuelve "Hola, Carlos!".
    """
    response.content_type = 'text/plain'
    return f"Hola, {nombre}!"

# ==============================
# GET: Obtener información
# ==============================

# @app.get('/productos')
@app.route('/productos')  # GET por defecto
def get_productos():
    """ Devuelve la lista de productos en formato JSON. """
    response.status = 200  # 200 OK
    response.content_type = 'application/json'
    return {"productos": data_store}

# @app.get('/productos/<id>')
@app.route('/productos/<id>', method='GET')  # Especificando GET
def get_producto(id):
    """ Devuelve un producto específico por su ID. """
    if id not in data_store:
        response.status = 404  # 404 Not Found
        return {"error": f"Producto con ID {id} no encontrado"}

    response.status = 200  # 200 OK
    return {"producto": data_store[id]}

# ==============================
# POST: Crear un nuevo producto
# ==============================

# @app.post('/productos')
@app.route('/productos', method='POST')
def create_producto():
    """ Crea un nuevo producto. Espera un JSON con "nombre" y "precio". """
    data = request.json
    if not data or "nombre" not in data or "precio" not in data:
        response.status = 400  # 400 Bad Request
        return {"error": "Faltan datos requeridos (nombre, precio)"}

    new_id = str(len(data_store) + 1)  # Genera un ID único
    data_store[new_id] = {"nombre": data["nombre"], "precio": data["precio"]}

    response.status = 201  # 201 Created
    return {"mensaje": "Producto creado", "id": new_id, "producto": data_store[new_id]}

# ==============================
# PUT: Actualizar un producto existente
# ==============================

# @app.put('/productos/<id>')
@app.route('/productos/<id>', method='PUT')
def update_producto(id):
    """ Actualiza un producto existente por su ID. """
    if id not in data_store:
        response.status = 404  # 404 Not Found
        return {"error": f"Producto con ID {id} no encontrado"}

    data = request.json
    if not data:
        response.status = 400  # 400 Bad Request
        return {"error": "No se recibió JSON válido"}

    if "nombre" in data:
        data_store[id]["nombre"] = data["nombre"]
    if "precio" in data:
        data_store[id]["precio"] = data["precio"]

    response.status = 200  # 200 OK
    return {"mensaje": f"Producto {id} actualizado", "producto": data_store[id]}

# ==============================
# DELETE: Eliminar un recurso
# ==============================

# @app.delete('/productos/<id>')
@app.route('/productos/<id>', method='DELETE')
def delete_producto(id):
    """ Elimina un producto del almacén de datos por su ID. """
    if id not in data_store:
        response.status = 404  # 404 Not Found
        return {"error": f"Producto con ID {id} no encontrado"}

    del data_store[id]
    response.status = 200  # 200 OK
    return {"mensaje": f"Producto {id} eliminado"}

# ==============================
# POST: Subir archivos al servidor
# ==============================

# @app.post('/subir')
@app.route('/subir', method='POST')
def subir():
    """
    Recibe un archivo y lo guarda en la carpeta "uploads".
    - Si el archivo no se recibe, devuelve 400 Bad Request.
    - Si hay un error al guardar, devuelve 500 Internal Server Error.
    - Si se sube correctamente, devuelve 201 Created.
    """
    archivo = request.files.get('archivo')  # Obtiene el archivo

    if not archivo:
        response.status = 400  # 400 Bad Request
        return {"error": "No se envió ningún archivo"}

    try:
        file_path = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(file_path)
        response.status = 201  # 201 Created
        return {"mensaje": "Archivo subido con éxito", "nombre_archivo": archivo.filename}
    except Exception as e:
        response.status = 500  # 500 Internal Server Error
        return {"error": "Error al guardar el archivo", "detalle": str(e)}

# ==============================
# Arranque del servidor
# ==============================
run(app, host='localhost', port=8080, debug=True)