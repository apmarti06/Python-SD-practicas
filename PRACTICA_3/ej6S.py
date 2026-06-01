from bottle import Bottle, request, response, run
import json

app = Bottle()

# Bases de datos en memoria
vehiculos = []
usuarios = []
contador_vehiculos = 1
contador_usuarios = 1

# =========================
# FUNCIONES AUXILIARES
# =========================

def buscar_vehiculo_por_id(id_vehiculo):
    """Busca un vehículo por su ID"""
    for v in vehiculos:
        if v["id"] == id_vehiculo:
            return v
    return None

def buscar_usuario_por_id(id_usuario):
    """Busca un usuario por su ID"""
    for u in usuarios:
        if u["id"] == id_usuario:
            return u
    return None

def buscar_vehiculo_libre():
    """Busca el primer vehículo libre (no alquilado)"""
    for v in vehiculos:
        if not v["alquilado"]:
            return v
    return None

def respuesta_json(codigo, datos):
    """Respuesta JSON estandarizada"""
    response.content_type = "application/json"
    response.status = codigo
    return json.dumps(datos, ensure_ascii=False, indent=4)

# =========================
# ENDPOINTS PRINCIPALES
# =========================

@app.post("/usuarios")
def registro_usuario():
    """
    Registro de usuario: se añade un nuevo usuario asignándole
    automáticamente un ID único e inicializando el número de alquileres a 0.
    """
    global contador_usuarios
    
    nuevo_usuario = {
        "id": contador_usuarios,
        "veces_alquilado": 0
    }
    
    usuarios.append(nuevo_usuario)
    contador_usuarios += 1
    
    return respuesta_json(201, {
        "mensaje": "Usuario registrado correctamente",
        "usuario": nuevo_usuario
    })

@app.post("/vehiculos")
def registro_vehiculo():
    """
    Registro de vehículo: se añade un nuevo vehículo a la flota disponible.
    Se le asigna automáticamente un ID único.
    Se debe pasar marca y modelo mediante JSON.
    """
    global contador_vehiculos
    
    datos = request.json
    
    # Validar que se reciben los datos necesarios
    if datos is None:
        return respuesta_json(400, {"error": "Se requiere un JSON con marca y modelo"})
    
    if "marca" not in datos:
        return respuesta_json(400, {"error": "Falta el campo 'marca'"})
    
    if "modelo" not in datos:
        return respuesta_json(400, {"error": "Falta el campo 'modelo'"})
    
    nuevo_vehiculo = {
        "id": contador_vehiculos,
        "marca": datos["marca"],
        "modelo": datos["modelo"],
        "alquilado": False,
        "ultimo_usuario": None
    }
    
    vehiculos.append(nuevo_vehiculo)
    contador_vehiculos += 1
    
    return respuesta_json(201, {
        "mensaje": "Vehículo registrado correctamente",
        "vehiculo": nuevo_vehiculo
    })

@app.post("/alquiler/libre")
def alquiler_vehiculo_libre():
    """
    Alquiler de un vehículo libre: dado un ID de usuario, localizar un
    vehículo cualquiera libre y asignárselo al usuario.
    """
    datos = request.json
    
    if datos is None or "id_usuario" not in datos:
        return respuesta_json(400, {"error": "Falta el campo 'id_usuario' en el JSON"})
    
    id_usuario = datos["id_usuario"]
    
    # Buscar usuario
    usuario = buscar_usuario_por_id(id_usuario)
    if usuario is None:
        return respuesta_json(404, {"error": f"No existe el usuario con ID {id_usuario}"})
    
    # Buscar vehículo libre
    vehiculo = buscar_vehiculo_libre()
    if vehiculo is None:
        return respuesta_json(409, {"error": "No hay vehículos disponibles para alquilar"})
    
    # Realizar alquiler
    vehiculo["alquilado"] = True
    vehiculo["ultimo_usuario"] = id_usuario
    usuario["veces_alquilado"] += 1
    
    return respuesta_json(200, {
        "mensaje": "Vehículo alquilado correctamente",
        "usuario": usuario,
        "vehiculo": {
            "id": vehiculo["id"],
            "marca": vehiculo["marca"],
            "modelo": vehiculo["modelo"]
        }
    })

@app.post("/alquiler/especifico")
def alquiler_vehiculo_especifico():
    """
    Alquiler de un vehículo específico: dados los IDs de usuario y vehículo,
    asignar el vehículo al usuario.
    """
    datos = request.json
    
    if datos is None:
        return respuesta_json(400, {"error": "Se requiere un JSON con id_usuario e id_vehiculo"})
    
    if "id_usuario" not in datos:
        return respuesta_json(400, {"error": "Falta el campo 'id_usuario'"})
    
    if "id_vehiculo" not in datos:
        return respuesta_json(400, {"error": "Falta el campo 'id_vehiculo'"})
    
    id_usuario = datos["id_usuario"]
    id_vehiculo = datos["id_vehiculo"]
    
    # Buscar usuario
    usuario = buscar_usuario_por_id(id_usuario)
    if usuario is None:
        return respuesta_json(404, {"error": f"No existe el usuario con ID {id_usuario}"})
    
    # Buscar vehículo
    vehiculo = buscar_vehiculo_por_id(id_vehiculo)
    if vehiculo is None:
        return respuesta_json(404, {"error": f"No existe el vehículo con ID {id_vehiculo}"})
    
    # Verificar que el vehículo esté libre
    if vehiculo["alquilado"]:
        return respuesta_json(409, {"error": f"El vehículo {id_vehiculo} ya está alquilado"})
    
    # Realizar alquiler
    vehiculo["alquilado"] = True
    vehiculo["ultimo_usuario"] = id_usuario
    usuario["veces_alquilado"] += 1
    
    return respuesta_json(200, {
        "mensaje": "Vehículo alquilado correctamente",
        "usuario": usuario,
        "vehiculo": {
            "id": vehiculo["id"],
            "marca": vehiculo["marca"],
            "modelo": vehiculo["modelo"]
        }
    })

# =========================
# ENDPOINTS ADICIONALES PARA CONSULTA
# =========================

@app.get("/vehiculos")
def listar_vehiculos():
    """Listar todos los vehículos (útil para depuración)"""
    return respuesta_json(200, {
        "total_vehiculos": len(vehiculos),
        "vehiculos": vehiculos
    })

@app.get("/usuarios")
def listar_usuarios():
    """Listar todos los usuarios (útil para depuración)"""
    return respuesta_json(200, {
        "total_usuarios": len(usuarios),
        "usuarios": usuarios
    })

@app.get("/vehiculos/libres")
def listar_vehiculos_libres():
    """Listar vehículos disponibles para alquilar"""
    libres = [v for v in vehiculos if not v["alquilado"]]
    return respuesta_json(200, {
        "vehiculos_libres": len(libres),
        "vehiculos": libres
    })

@app.get("/vehiculos/alquilados")
def listar_vehiculos_alquilados():
    """Listar vehículos actualmente alquilados"""
    alquilados = [v for v in vehiculos if v["alquilado"]]
    return respuesta_json(200, {
        "vehiculos_alquilados": len(alquilados),
        "vehiculos": alquilados
    })

@app.get("/usuarios/<id_usuario:int>/historial")
def historial_usuario(id_usuario):
    """Ver historial de alquileres de un usuario (últimos vehículos alquilados)"""
    usuario = buscar_usuario_por_id(id_usuario)
    if usuario is None:
        return respuesta_json(404, {"error": f"No existe el usuario con ID {id_usuario}"})
    
    # Buscar vehículos que ha alquilado este usuario
    vehiculos_alquilados = [v for v in vehiculos if v["ultimo_usuario"] == id_usuario]
    
    return respuesta_json(200, {
        "usuario": usuario,
        "total_vehiculos_alquilados": len(vehiculos_alquilados),
        "vehiculos": vehiculos_alquilados
    })

@app.post("/devolucion")
def devolver_vehiculo():
    """
    Endpoint adicional: devolver un vehículo (ponerlo como no alquilado)
    """
    datos = request.json
    
    if datos is None or "id_vehiculo" not in datos:
        return respuesta_json(400, {"error": "Falta el campo 'id_vehiculo' en el JSON"})
    
    id_vehiculo = datos["id_vehiculo"]
    
    vehiculo = buscar_vehiculo_por_id(id_vehiculo)
    if vehiculo is None:
        return respuesta_json(404, {"error": f"No existe el vehículo con ID {id_vehiculo}"})
    
    if not vehiculo["alquilado"]:
        return respuesta_json(409, {"error": f"El vehículo {id_vehiculo} ya está libre"})
    
    vehiculo["alquilado"] = False
    # Nota: no borramos el último usuario para mantener el historial
    
    return respuesta_json(200, {
        "mensaje": f"Vehículo {id_vehiculo} devuelto correctamente",
        "vehiculo": vehiculo
    })

# =========================
# GESTIÓN DE ERRORES
# =========================

@app.error(404)
def error_404(error):
    return respuesta_json(404, {"error": "Endpoint no encontrado"})

@app.error(405)
def error_405(error):
    return respuesta_json(405, {"error": "Método HTTP no permitido"})

@app.error(500)
def error_500(error):
    return respuesta_json(500, {"error": "Error interno del servidor"})

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("=" * 60)
    print("   SERVICIO DE ALQUILER DE VEHÍCULOS")
    print("=" * 60)
    print("Servidor iniciado en: http://localhost:8080")
    print("\n📋 ENDPOINTS DISPONIBLES:")
    print("  POST   /usuarios                    - Registrar nuevo usuario")
    print("  POST   /vehiculos                   - Registrar nuevo vehículo")
    print("  POST   /alquiler/libre              - Alquilar cualquier vehículo libre")
    print("  POST   /alquiler/especifico         - Alquilar vehículo específico")
    print("  POST   /devolucion                  - Devolver vehículo")
    print("  GET    /vehiculos                   - Listar todos los vehículos")
    print("  GET    /usuarios                    - Listar todos los usuarios")
    print("  GET    /vehiculos/libres            - Listar vehículos libres")
    print("  GET    /vehiculos/alquilados        - Listar vehículos alquilados")
    print("  GET    /usuarios/<id>/historial     - Historial de alquileres")
    print("=" * 60)
    print("\n💡 Las bases de datos están en memoria (vacías al iniciar)")
    print("=" * 60)
    run(app, host="localhost", port=8080, debug=True)