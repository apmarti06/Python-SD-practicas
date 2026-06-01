import requests
import json

BASE_URL = "http://localhost:8080/miembros"

def mostrar_miembro(m):
    """Muestra un miembro de forma formateada"""
    print("=" * 50)
    print(f"DNI: {m['dni']}")
    print(f"Nombre: {m['nombre_completo']}")
    print(f"Email: {m['email']}")
    print(f"Departamento: {m['departamento']}")
    print(f"Categoría: {m['categoria']}")
    
    if m['categoria'] == 'PDI' and 'asignaturas' in m and m['asignaturas']:
        print(f"Asignaturas: {', '.join(m['asignaturas'])}")
    print("=" * 50)

def mostrar_lista_miembros(miembros, titulo="Miembros"):
    """Muestra una lista de miembros"""
    if not miembros:
        print("No hay miembros para mostrar.")
        return
    
    print(f"\n{titulo} (Total: {len(miembros)})")
    print("-" * 50)
    for m in miembros:
        print(f"📌 {m['nombre_completo']} (DNI: {m['dni']}) - {m['categoria']}")

def alta_miembro():
    """Dar de alta un nuevo miembro"""
    print("\n--- ALTA DE NUEVO MIEMBRO ---")
    
    dni = input("DNI (8 números + letra): ").strip().upper()
    nombre = input("Nombre completo: ").strip()
    email = input("Email: ").strip()
    departamento = input("Departamento: ").strip()
    
    print("Categorías disponibles: PAS, PDI, becario")
    categoria = input("Categoría: ").strip().upper()
    
    datos = {
        "dni": dni,
        "nombre_completo": nombre,
        "email": email,
        "departamento": departamento,
        "categoria": categoria
    }
    
    if categoria == "PDI":
        print("Asignaturas (separadas por comas):")
        asignaturas_input = input("> ").strip()
        if asignaturas_input:
            asignaturas = [a.strip() for a in asignaturas_input.split(",")]
            datos["asignaturas"] = asignaturas
    
    try:
        r = requests.post(BASE_URL, json=datos)
        if r.status_code == 201:
            print("✅", r.json()["mensaje"])
        else:
            print("❌ Error:", r.json().get("error", "Error desconocido"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def modificar_miembro():
    """Modificar un miembro existente"""
    print("\n--- MODIFICAR MIEMBRO ---")
    dni = input("DNI del miembro a modificar: ").strip().upper()
    
    # Primero obtener el miembro actual
    try:
        r = requests.get(f"{BASE_URL}/{dni}")
        if r.status_code != 200:
            print("❌", r.json().get("error", "Miembro no encontrado"))
            return
        
        miembro_actual = r.json()["miembro"]
        print(f"Modificando a: {miembro_actual['nombre_completo']}")
        print("(Deja en blanco para mantener el valor actual)")
        
        nombre = input(f"Nuevo nombre [{miembro_actual['nombre_completo']}]: ").strip()
        email = input(f"Nuevo email [{miembro_actual['email']}]: ").strip()
        departamento = input(f"Nuevo departamento [{miembro_actual['departamento']}]: ").strip()
        
        print(f"Categoría actual: {miembro_actual['categoria']}")
        categoria = input("Nueva categoría (PAS/PDI/becario): ").strip().upper()
        
        datos = {}
        datos["nombre_completo"] = nombre if nombre else miembro_actual["nombre_completo"]
        datos["email"] = email if email else miembro_actual["email"]
        datos["departamento"] = departamento if departamento else miembro_actual["departamento"]
        datos["categoria"] = categoria if categoria else miembro_actual["categoria"]
        
        if datos["categoria"] == "PDI":
            print("Asignaturas actuales:", ", ".join(miembro_actual.get("asignaturas", [])))
            asignaturas_input = input("Nuevas asignaturas (separadas por comas): ").strip()
            if asignaturas_input:
                datos["asignaturas"] = [a.strip() for a in asignaturas_input.split(",")]
        
        r = requests.put(f"{BASE_URL}/{dni}", json=datos)
        if r.status_code == 200:
            print("✅", r.json()["mensaje"])
        else:
            print("❌ Error:", r.json().get("error", "Error desconocido"))
            
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def listar_miembros():
    """Listar todos los miembros"""
    print("\n--- LISTA COMPLETA DE MIEMBROS ---")
    try:
        r = requests.get(BASE_URL)
        if r.status_code == 200:
            miembros = r.json().get("miembros", [])
            if miembros:
                for m in miembros:
                    mostrar_miembro(m)
            else:
                print("No hay miembros registrados.")
        else:
            print("❌ Error al obtener la lista")
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def buscar_por_dni():
    """Buscar miembro por DNI"""
    print("\n--- BÚSQUEDA POR DNI ---")
    dni = input("Introduce el DNI: ").strip().upper()
    
    try:
        r = requests.get(f"{BASE_URL}/{dni}")
        if r.status_code == 200:
            mostrar_miembro(r.json()["miembro"])
        else:
            print("❌", r.json().get("error", "Miembro no encontrado"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def buscar_por_categoria():
    """Buscar miembros por categoría"""
    print("\n--- BÚSQUEDA POR CATEGORÍA ---")
    print("Categorías: PAS, PDI, becario")
    categoria = input("Categoría: ").strip().upper()
    
    try:
        r = requests.get(f"{BASE_URL}/categoria/{categoria}")
        if r.status_code == 200:
            datos = r.json()
            print(f"\n✅ Encontrados {datos['total']} miembros en categoría {categoria}")
            for m in datos["miembros"]:
                mostrar_miembro(m)
        else:
            print("❌", r.json().get("error", "Error en la búsqueda"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def eliminar_miembro():
    """Eliminar un miembro"""
    print("\n--- ELIMINAR MIEMBRO ---")
    dni = input("DNI del miembro a eliminar: ").strip().upper()
    
    confirmar = input(f"¿Seguro que quieres eliminar al miembro con DNI {dni}? (si/no): ").strip().lower()
    if confirmar != "si":
        print("Operación cancelada")
        return
    
    try:
        r = requests.delete(f"{BASE_URL}/{dni}")
        if r.status_code == 200:
            print("✅", r.json()["mensaje"])
        else:
            print("❌", r.json().get("error", "Error al eliminar"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def buscar_por_nombre_parcial():
    """Búsqueda parcial por nombre"""
    print("\n--- BÚSQUEDA PARCIAL POR NOMBRE ---")
    nombre = input("Introduce parte del nombre: ").strip()
    
    if len(nombre) < 2:
        print("❌ El término de búsqueda debe tener al menos 2 caracteres")
        return
    
    try:
        r = requests.get(f"{BASE_URL}/buscar/nombre/{nombre}")
        if r.status_code == 200:
            datos = r.json()
            if datos["total"] > 0:
                print(f"✅ Encontrados {datos['total']} miembros")
                mostrar_lista_miembros(datos["miembros"])
            else:
                print("No se encontraron miembros con ese nombre")
        else:
            print("❌", r.json().get("error", "Error en la búsqueda"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def busqueda_parametrica():
    """Búsqueda paramétrica avanzada"""
    print("\n--- BÚSQUEDA PARAMÉTRICA ---")
    print("Puedes buscar por: dni, nombre, departamento, categoria, email")
    print("(Deja en blanco los criterios que no quieras usar)")
    
    params = {}
    
    dni = input("DNI (parcial): ").strip()
    if dni:
        params["dni"] = dni
    
    nombre = input("Nombre (parcial): ").strip()
    if nombre:
        params["nombre"] = nombre
    
    departamento = input("Departamento (parcial): ").strip()
    if departamento:
        params["departamento"] = departamento
    
    categoria = input("Categoría (PAS/PDI/becario): ").strip().upper()
    if categoria and categoria in ["PAS", "PDI", "BECARIO"]:
        params["categoria"] = categoria
    
    email = input("Email (parcial): ").strip()
    if email:
        params["email"] = email
    
    if not params:
        print("❌ Debes introducir al menos un criterio de búsqueda")
        return
    
    try:
        r = requests.get(f"{BASE_URL}/buscar/parametrica", params=params)
        if r.status_code == 200:
            datos = r.json()
            print(f"\n✅ Encontrados {datos['total']} miembros")
            if datos["total"] > 0:
                mostrar_lista_miembros(datos["miembros"])
            else:
                print("No se encontraron miembros con esos criterios")
        else:
            print("❌", r.json().get("error", "Error en la búsqueda"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def buscar_por_asignatura():
    """Buscar PDI por asignatura"""
    print("\n--- BÚSQUEDA POR ASIGNATURA ---")
    asignatura = input("Introduce el nombre de la asignatura: ").strip()
    
    if not asignatura:
        print("❌ Debes introducir una asignatura")
        return
    
    try:
        r = requests.get(f"{BASE_URL}/buscar/asignatura/{asignatura}")
        if r.status_code == 200:
            datos = r.json()
            if datos["total"] > 0:
                print(f"✅ Encontrados {datos['total']} PDI que imparten '{asignatura}':")
                for m in datos["miembros"]:
                    mostrar_miembro(m)
            else:
                print(f"No se encontraron PDI que impartan '{asignatura}'")
        else:
            print("❌", r.json().get("error", "Error en la búsqueda"))
    except requests.RequestException as e:
        print("❌ Error de conexión:", e)

def menu():
    """Menú principal del cliente"""
    opcion = ""
    
    while opcion != "0":
        print("\n" + "=" * 50)
        print("   DIRECTORIO UCA - CLIENTE")
        print("=" * 50)
        print("1. Dar de alta un miembro")
        print("2. Modificar un miembro")
        print("3. Listar todos los miembros")
        print("4. Buscar por DNI")
        print("5. Buscar por categoría")
        print("6. Eliminar un miembro")
        print("7. Búsqueda parcial por nombre")
        print("8. Búsqueda paramétrica (múltiples criterios)")
        print("9. Búsqueda inversa por asignatura")
        print("0. Salir")
        print("=" * 50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        match opcion:
            case "1":
                alta_miembro()
            case "2":
                modificar_miembro()
            case "3":
                listar_miembros()
            case "4":
                buscar_por_dni()
            case "5":
                buscar_por_categoria()
            case "6":
                eliminar_miembro()
            case "7":
                buscar_por_nombre_parcial()
            case "8":
                busqueda_parametrica()
            case "9":
                buscar_por_asignatura()
            case "0":
                print("\n👋 ¡Hasta luego!")
            case _:
                print("❌ Opción no válida")

if __name__ == "__main__":
    print("=" * 50)
    print("   CLIENTE DIRECTORIO UCA")
    print("=" * 50)
    print("Conectando al servidor en:", BASE_URL)
    menu()