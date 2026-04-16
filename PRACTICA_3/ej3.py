from bottle import Bottle, request, response, run
import json
import os

app = Bottle()
data_file = "rooms.json" # constistencia de la base de datos 

#Hacemos cada funcion auxiliar requerida para la persistencia del hotel

#cargamos las habitaciones existentes del hotel
def cargar_habitaciones(): 
    if not os.path.exists(data_file):
        return [] # no devolvemos ningun dato
    
    try: 
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

#pasamos una lista actualizada de habitaciones en nuestro json
def guardar_habitaciones(lista_habitaciones):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(lista_habitaciones, f, indent=4, ensure_ascii=False)

# buscamos una habitacion especifica si existe
def buscar_habitaciones_id(habitaciones, id):
    for habitacion in habitaciones:
        if habitacion["id"] == id: # buscamos en el archivo de la web si encontramos el id deseado, si es así le mandamos la referencia
            return habitacion
    return None 

#vemos si los datos del usuario concuerda con el json (claves)
def validar_habitacion(datos, exigir_id = True):
    if not isinstance(datos, dict): # si los datos no se trata de un diccionario no son válidps
        return False
    
    campos = ["plazas", "equipamiento", "ocupada"]
    if exigir_id:
        campos.insert(0, "id")

    #prueba que los datos existan
    for campo in campos:
        if campo not in datos:
            return False, f"Falta el campo obligatorio: {campo}"

    # Manejador que los tipos sean correctos
    if exigir_id and not isinstance(datos["id"], int):
        return False, "El campo 'id' debe ser un entero."

    if not isinstance(datos["plazas"], int) or datos["plazas"] <= 0:
        return False, "El campo 'plazas' debe ser un entero mayor que 0."

    if not isinstance(datos["equipamiento"], list):
        return False, "El campo 'equipamiento' debe ser una lista."

    if not all(isinstance(elem, str) for elem in datos["equipamiento"]):
        return False, "Todos los elementos de 'equipamiento' deben ser cadenas."

    if not isinstance(datos["ocupada"], bool):
        return False, "El campo 'ocupada' debe ser booleano (true/false)."

    return True, ""

def respuesta_json(codigo, datos):
    response.content_type = "application/json"
    response.status = codigo
    return json.dumps(datos, ensure_ascii=False, indent=4)


#CREAMOS AHORA LOS ENDPOINTS QUE PIDEN OBLIGATORIOS

@app.post("/rooms")
def alta_habitacion(): #a) Dar de alta una nueva habitación.
    datos = request.json

    valido, mensaje = validar_habitacion(datos)
    if not valido:
        return respuesta_json(400, {"error": mensaje})

    habitaciones = cargar_habitaciones()

    if buscar_habitaciones_id(habitaciones, datos["id"]) is not None:
        return respuesta_json(409, {"error": "Ya existe una habitación con ese identificador."})
    
    nueva = {
        "id" : datos["id"],
        "plazas" : datos["plazas"],
        "equipamiento" : datos["equipamiento"],
        "ocupada" : datos["ocupada"]
    }

    habitaciones.append(nueva)
    guardar_habitaciones(habitaciones)

    return respuesta_json(201, {"mensaje": "Habitación creada correctamente.", "habitacion": nueva})

# usamos lo que nos pide el enunciado en b, d y e, que incluya parametros en el path de la url

@app.put("/rooms/<room_id>:<int>") 
def modificar_habitacion(room_id):
    datos = request.json

    valido, mensaje = validar_habitacion(datos, exigir_id=False) #usamos el false en vez de por defecto, ya que conocemos el id deseado

    if not valido:
        respuesta_json(400, {"error": mensaje})
    
    habitaciones = cargar_habitaciones()
    habitacion = buscar_habitaciones_id(habitaciones, room_id)

    if habitacion is None: # si existe la habitacion qe estoy buscando la guardo sino lanzo responsejson
        return respuesta_json(404, {"error": "La habitación no existe."})

    habitacion["plazas"] = datos["plazas"]
    habitacion["equipamiento"] = datos["equipamiento"]
    habitacion["ocupada"] = datos["ocupada"]

    guardar_habitaciones(habitaciones)

    return respuesta_json(200, {"mensaje": "Habitación modificada correctamente.", "habitacion": habitacion})

# como damos todos no necesitamos ningun parametro de url
@app.get("/rooms")
def listar_habitaciones():
    #solo listamos toda todas las habitaciones
    habitaciones = cargar_habitaciones()
    return respuesta_json(200, {"habitaciones": habitaciones})

# apartado d
@app.get("/rooms/<room_id>:<int>")
def consultar_habitacion(room_id):

    habitaciones = cargar_habitaciones()
    habitacion = buscar_habitaciones_id(habitaciones, room_id)

    if habitacion is None:
        respuesta_json(400, {"error": "La habitacion no existe"})

    return respuesta_json(200, {"habitacion" : habitacion})

#apartado e
@app.get("/rooms/status/<estado>")
def consultar_por_estado(estado):
    """
    GET /rooms/status/<estado>
    Consulta habitaciones ocupadas o desocupadas.
    El estado va en el path, como pide el enunciado.
    """
    estado = estado.lower()

    if estado not in ("ocupadas", "desocupadas"):
        return respuesta_json(400, {"error": "El estado debe ser 'ocupadas' o 'desocupadas'."})

    habitaciones = cargar_habitaciones()

    if estado == "ocupadas":
        filtradas = [h for h in habitaciones if h["ocupada"]]
    else:
        filtradas = [h for h in habitaciones if not h["ocupada"]]

    return respuesta_json(200, {"habitaciones": filtradas})


# =========================
# GESTIÓN DE ERRORES
# =========================

@app.error(404)
def error_404(error):
    return respuesta_json(404, {"error": "Endpoint no encontrado."})


@app.error(405)
def error_405(error):
    return respuesta_json(405, {"error": "Método HTTP no permitido."})


# =========================
# MAIN
# =========================

run(app, host="localhost", port=8080, debug=True)


