from bottle import Bottle, request, response, run
import json
import os
import re

# atributos dni, nombre completo (usamos diccionario), correo electronico, departamento, categoria (PAS/PDI/becario), lista asignaturas
# endpoints necesarios por el servidor(dar de alta un miembri nuevo, modificar los datos de un miembro, Consultar la lista de todos los miembros de la Universidad,
#  Hacer una búsqueda por DNI, Obtener una lista de miembros según categoría)

app = Bottle()
data_file = "directorio_uca.json"

#cargamos el servicio web de directorio, con su listado de cada miembro
def cargar_miembros(): 
    if not os.path.exists(data_file):
        return [] # no devolvemos ningun dato
    
    try: 
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

#pasamos una lista actualizada de los miembros en nuestro json
def guardar_miembros(lista_miembros):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(lista_miembros, f, indent=4, ensure_ascii=False)

# Ahora nuestro identificador va a ser nuestro dni para buscar cosas
def validar_dni(dni):
    """Valida el formato del DNI (8 números + letra)"""
    patron = r'^[0-9]{8}[A-Z]$' 

    if not re.match(patron, dni):
        return False, "El DNI debe tener 8 números y una letra mayúscula (ej: 12345678Z)"
    
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    numeros = int(dni[:-1])
    letra_correcta = letras[numeros % 23]

    if dni[-1] != letra_correcta:
        return False, f"La letra del dni es incorrecta, deberia ser:{letra_correcta}"
    
    return True, ""

def buscar_por_dni(miembros, dni):
    """Busca un miembro por su DNI"""
    for miembro in miembros:
        if miembro["dni"] == dni:
            return miembro
    return None

def validar_miembro(datos, exigir_dni=True):
    #isinstance verifica que el tipo de diccionario, lista etc sea correcto definido en el ejercicio asignaturas strings, etc
    """Valida los datos de un miembro"""
    if not isinstance(datos, dict):
        return False, "Los datos deben ser un objeto JSON"
    
    campos = ["nombre_completo", "email", "departamento", "categoria"]
    # aveces se mandara el dni por parametro formal
    if exigir_dni:
        campos.insert(0, "dni")
    
    # Verificar campos obligatorios
    for campo in campos:
        if campo not in datos:
            return False, f"Falta el campo obligatorio: {campo}"
    
    # Validar DNI
    if exigir_dni:
        valido, mensaje = validar_dni(datos["dni"])
        if not valido:
            return False, mensaje
    
    # Validar nombre completo, debe de ser 3 palabras maximo
    if not isinstance(datos["nombre_completo"], str) or len(datos["nombre_completo"].strip()) < 3:
        return False, "El nombre completo debe tener al menos 3 caracteres"
    
    # Validar email
    if not isinstance(datos["email"], str) or "@" not in datos["email"]:
        return False, "El email debe ser válido (debe contener @)"
    
    # Validar departamento, ponemos limite 4 palabras (Departamento de fisica cuantica)
    if not isinstance(datos["departamento"], str) or len(datos["departamento"].strip()) < 4:
        return False, "El departamento debe tener al menos 2 caracteres"  # Nota: el mensaje dice 2 pero la condición es 4
    
    # Validar categoría, 3 tipos unicos
    categorias_validas = ["PAS", "PDI", "BECARIO"]
    if datos["categoria"] not in categorias_validas:
        return False, f"La categoría debe ser una de: {', '.join(categorias_validas)}"
    
    # Validar lista de asignaturas (solo para PDI)
    if datos["categoria"] == "PDI":
        if "asignaturas" not in datos:
            return False, "Para categoría PDI es obligatorio el campo 'asignaturas'"
        if not isinstance(datos["asignaturas"], list):
            return False, "El campo 'asignaturas' debe ser una lista"
        if not all(isinstance(a, str) for a in datos["asignaturas"]):
            return False, "Todas las asignaturas deben ser cadenas de texto"
    else:
        # Si no es PDI, no debería tener asignaturas
        if "asignaturas" in datos and datos["asignaturas"]:
            return False, "Solo los miembros de categoría PDI pueden tener asignaturas"
    
    return True, ""

def respuesta_json(codigo, datos):
    """Respuesta JSON estandarizada"""
    response.content_type = "application/json"
    response.status = codigo
    return json.dumps(datos, ensure_ascii=False, indent=4)

@app.post("/miembros")
def alta_miembro():
    datos = request.json
    valido, mensaje = validar_miembro(datos) # el dni aqui se exige, dentro de funcion pues metodo post no requiere parametros

    if not valido:
        return respuesta_json(400, {"error" : mensaje})
    
    miembros = cargar_miembros() #verificamos que no exista
    if buscar_por_dni(miembros, datos["dni"]) is not None:
        return respuesta_json(409, {"error": "Ya existe un miembro con ese DNI"})
    
    #actualizamos si todo esta correcto, verificando si es PDI añadimos las asignaturas cuando sea necesario
    nuevo_miembro = {
        "dni": datos["dni"],
        "nombre_completo": datos["nombre_completo"],
        "email": datos["email"],
        "departamento": datos["departamento"],
        "categoria": datos["categoria"]
    }

    if datos["categoria"] == "PDI":
        nuevo_miembro["asignaturas"] = datos.get("asignaturas", [])

    # actualizamos el json
    miembros.append(nuevo_miembro)
    guardar_miembros(miembros)

    return respuesta_json(201, {"mensaje" : "Miembro creado correctamente",
        "miembro" : nuevo_miembro})

# CORREGIDO: quitado :<int> porque el DNI tiene letras
@app.put("/miembros/<dni>")
def modificar_miembro(dni):
    datos = request.json
    # CORREGIDO: cambiar "dni" por "exigir_dni=False"
    valido, mensaje = validar_miembro(datos, exigir_dni=False)

    # especificamos porque no es valido
    if not valido:
        return respuesta_json(400, {"respuesta ": mensaje})
    
    #buscamos el miembro haber si existe para modificarlo
    miembros = cargar_miembros()
    miembro = buscar_por_dni(miembros, dni)

    if miembro is None:
        return respuesta_json(404, {"error": "No existe un miembro con ese dni"})
    
    # actualizamos sino campos
    miembro["nombre_completo"] = datos["nombre_completo"]
    miembro["email"] = datos["email"]
    miembro["departamento"] = datos["departamento"]
    miembro["categoria"] = datos["categoria"]
    
    if datos["categoria"] == "PDI":
        miembro["asignaturas"] = datos.get("asignaturas", [])
    else:
        # Eliminar asignaturas si cambia a otra categoría
        miembro.pop("asignaturas", None)
    
    guardar_miembros(miembros)
    return respuesta_json(200, {"mensaje" : "Miembro actualizado", "miembro" : miembro})

# creamos metodos get endpoints de busqueda especifica o listar todoss los miembros
@app.get("/miembros")
def listar_miembros():
    miembros = cargar_miembros()
    return respuesta_json(200, {"miembros": miembros})

# busqueda especifica por dni
# CORREGIDO: quitado :<int> porque el DNI tiene letras
@app.get("/miembros/<dni>")
def buscar_dni_endpoint(dni):
    # no necesitamos ningun parametro que sea el dni del miembro, por lo que no llamamos al cliente
    miembros = cargar_miembros()
    # CORREGIDO: añadido "miembros," como primer argumento
    miembro = buscar_por_dni(miembros, dni)

    if miembro is None:
        return respuesta_json(404, {"error": "No existe un miembro con ese dni"})

    return respuesta_json(200, {"miembro" : miembro})

# buscamos por categoria
# CORREGIDO: "miembro" -> "miembros" (añadida la 's')
@app.get("/miembros/categoria/<categoria>") # incluir el parametro <PDI> AL LADO DE CATEGORIA
def buscar_por_categoria(categoria):
    categoria = categoria.upper()
    categoria_validas = ["PAS", "PDI", "BECARIO"]

    if categoria not in categoria_validas:
        return respuesta_json(400, {
            "error": f"Categoría no válida. Debe ser: {', '.join(categoria_validas)}"
        })
    
    miembros = cargar_miembros()
    filtrados = [m for m in miembros if m["categoria"] == categoria]
    
    return respuesta_json(200, {
        "categoria": categoria,
        "total": len(filtrados),
        "miembros": filtrados
    })

# =========================
# ENDPOINTS ADICIONALES
# =========================

@app.delete("/miembros/<dni>")
def eliminar_miembro(dni):
    """Eliminar un miembro mediante DELETE"""
    miembros = cargar_miembros()
    miembro = buscar_por_dni(miembros, dni)
    
    if miembro is None:
        return respuesta_json(404, {"error": "No existe un miembro con ese DNI"})
    
    miembros.remove(miembro)
    guardar_miembros(miembros)
    
    return respuesta_json(200, {"mensaje": f"Miembro con DNI {dni} eliminado correctamente"})

# más casos de get
@app.get("/miembros/buscar/nombre/<parcial>")
def buscar_por_nombre_parcial(parcial):
    """Búsqueda parcial por nombre"""
    if len(parcial) < 2:
        return respuesta_json(400, {"error": "El término de búsqueda debe tener al menos 2 caracteres"})
    
    miembros = cargar_miembros()
    parcial_lower = parcial.lower()
    filtrados = [m for m in miembros if parcial_lower in m["nombre_completo"].lower()]
    
    return respuesta_json(200, {
        "termino_busqueda": parcial,
        "total": len(filtrados),
        "miembros": filtrados
    })

@app.get("/miembros/buscar/parametrica")
def busqueda_parametrica():
    """
    Búsqueda paramétrica por múltiples criterios
    Parámetros query: dni, nombre, departamento, categoria, email
    Ejemplo: /miembros/buscar/parametrica?categoria=PDI&departamento=Informática
    """
    params = request.query
    miembros = cargar_miembros()
    resultado = miembros.copy()
    
    # Aplicar filtros
    if params.get("dni"):
        resultado = [m for m in resultado if params["dni"].upper() in m["dni"]]
    
    if params.get("nombre"):
        resultado = [m for m in resultado if params["nombre"].lower() in m["nombre_completo"].lower()]
    
    if params.get("departamento"):
        resultado = [m for m in resultado if params["departamento"].lower() in m["departamento"].lower()]
    
    if params.get("categoria"):
        categoria_filtro = params["categoria"].upper()
        if categoria_filtro in ["PAS", "PDI", "BECARIO"]:
            resultado = [m for m in resultado if m["categoria"] == categoria_filtro]
    
    if params.get("email"):
        resultado = [m for m in resultado if params["email"].lower() in m["email"].lower()]
    
    return respuesta_json(200, {
        "filtros_aplicados": dict(params),
        "total": len(resultado),
        "miembros": resultado
    })

@app.get("/miembros/buscar/asignatura/<asignatura>")
def buscar_por_asignatura(asignatura):
    """Búsqueda inversa por asignatura (solo PDI)"""
    miembros = cargar_miembros()
    filtrados = []
    
    for m in miembros:
        if m["categoria"] == "PDI" and "asignaturas" in m:
            if any(asignatura.lower() in a.lower() for a in m["asignaturas"]):
                filtrados.append(m)
    
    if not filtrados:
        return respuesta_json(200, {
            "asignatura": asignatura,
            "total": 0,
            "mensaje": "No se encontraron PDI que impartan esa asignatura",
            "miembros": []
        })
    
    return respuesta_json(200, {
        "asignatura": asignatura,
        "total": len(filtrados),
        "miembros": filtrados
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
    print("=" * 50)
    print("SERVICIO WEB DIRECTORIO UCA")
    print("=" * 50)
    print("Servidor iniciado en: http://localhost:8080")
    print("Endpoints disponibles:")
    print("  POST   /miembros                           - Alta de miembro")
    print("  PUT    /miembros/<dni>                     - Modificar miembro")
    print("  GET    /miembros                           - Listar todos")
    print("  GET    /miembros/<dni>                     - Buscar por DNI")
    print("  GET    /miembros/categoria/<categoria>     - Buscar por categoría")
    print("  DELETE /miembros/<dni>                     - Eliminar miembro")
    print("  GET    /miembros/buscar/nombre/<parcial>   - Búsqueda parcial por nombre")
    print("  GET    /miembros/buscar/parametrica        - Búsqueda paramétrica")
    print("  GET    /miembros/buscar/asignatura/<asig>  - Búsqueda por asignatura")
    print("=" * 50)
    run(app, host="localhost", port=8080, debug=True)