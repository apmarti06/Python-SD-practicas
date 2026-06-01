import requests
import json

BASE_URL = "http://localhost:8080"

def mostrar_vehiculo(v):
    """Muestra un vehículo formateado"""
    estado = "🚗 Alquilado" if v["alquilado"] else "✅ Libre"
    ultimo = f" (Último usuario: {v['ultimo_usuario']})" if v["ultimo_usuario"] else ""
    print(f"  [{v['id']}] {v['marca']} {v['modelo']} - {estado}{ultimo}")

def mostrar_usuario(u):
    """Muestra un usuario formateado"""
    print(f"  [{u['id']}] Alquileres realizados: {u['veces_alquilado']}")

def registrar_usuario():
    """Registrar un nuevo usuario"""
    print("\n--- REGISTRAR NUEVO USUARIO ---")
    try:
        r = requests.post(f"{BASE_URL}/usuarios")
        if r.status_code == 201:
            datos = r.json()
            print(f"✅ {datos['mensaje']}")
            print(f"📌 ID de usuario: {datos['usuario']['id']}")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def registrar_vehiculo():
    """Registrar un nuevo vehículo"""
    print("\n--- REGISTRAR NUEVO VEHÍCULO ---")
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    
    datos = {"marca": marca, "modelo": modelo}
    
    try:
        r = requests.post(f"{BASE_URL}/vehiculos", json=datos)
        if r.status_code == 201:
            datos_resp = r.json()
            print(f"✅ {datos_resp['mensaje']}")
            print(f"📌 ID de vehículo: {datos_resp['vehiculo']['id']}")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def alquiler_libre():
    """Alquilar un vehículo libre cualquiera"""
    print("\n--- ALQUILAR VEHÍCULO LIBRE ---")
    try:
        id_usuario = int(input("ID del usuario: "))
    except ValueError:
        print("❌ El ID debe ser un número entero")
        return
    
    datos = {"id_usuario": id_usuario}
    
    try:
        r = requests.post(f"{BASE_URL}/alquiler/libre", json=datos)
        if r.status_code == 200:
            datos_resp = r.json()
            print(f"✅ {datos_resp['mensaje']}")
            print(f"📌 Vehículo asignado: {datos_resp['vehiculo']['marca']} {datos_resp['vehiculo']['modelo']} (ID: {datos_resp['vehiculo']['id']})")
            print(f"📌 El usuario ahora tiene {datos_resp['usuario']['veces_alquilado']} alquiler(es)")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def alquiler_especifico():
    """Alquilar un vehículo específico"""
    print("\n--- ALQUILAR VEHÍCULO ESPECÍFICO ---")
    try:
        id_usuario = int(input("ID del usuario: "))
        id_vehiculo = int(input("ID del vehículo: "))
    except ValueError:
        print("❌ Los IDs deben ser números enteros")
        return
    
    datos = {"id_usuario": id_usuario, "id_vehiculo": id_vehiculo}
    
    try:
        r = requests.post(f"{BASE_URL}/alquiler/especifico", json=datos)
        if r.status_code == 200:
            datos_resp = r.json()
            print(f"✅ {datos_resp['mensaje']}")
            print(f"📌 Vehículo: {datos_resp['vehiculo']['marca']} {datos_resp['vehiculo']['modelo']}")
            print(f"📌 El usuario ahora tiene {datos_resp['usuario']['veces_alquilado']} alquiler(es)")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def devolver_vehiculo():
    """Devolver un vehículo"""
    print("\n--- DEVOLVER VEHÍCULO ---")
    try:
        id_vehiculo = int(input("ID del vehículo a devolver: "))
    except ValueError:
        print("❌ El ID debe ser un número entero")
        return
    
    datos = {"id_vehiculo": id_vehiculo}
    
    try:
        r = requests.post(f"{BASE_URL}/devolucion", json=datos)
        if r.status_code == 200:
            print(f"✅ {r.json()['mensaje']}")
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def listar_vehiculos():
    """Listar todos los vehículos"""
    print("\n--- LISTA DE VEHÍCULOS ---")
    try:
        r = requests.get(f"{BASE_URL}/vehiculos")
        if r.status_code == 200:
            datos = r.json()
            print(f"Total de vehículos: {datos['total_vehiculos']}")
            for v in datos['vehiculos']:
                mostrar_vehiculo(v)
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def listar_usuarios():
    """Listar todos los usuarios"""
    print("\n--- LISTA DE USUARIOS ---")
    try:
        r = requests.get(f"{BASE_URL}/usuarios")
        if r.status_code == 200:
            datos = r.json()
            print(f"Total de usuarios: {datos['total_usuarios']}")
            for u in datos['usuarios']:
                mostrar_usuario(u)
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def listar_vehiculos_libres():
    """Listar vehículos disponibles"""
    print("\n--- VEHÍCULOS LIBRES ---")
    try:
        r = requests.get(f"{BASE_URL}/vehiculos/libres")
        if r.status_code == 200:
            datos = r.json()
            print(f"Vehículos libres: {datos['vehiculos_libres']}")
            for v in datos['vehiculos']:
                mostrar_vehiculo(v)
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def listar_vehiculos_alquilados():
    """Listar vehículos alquilados"""
    print("\n--- VEHÍCULOS ALQUILADOS ---")
    try:
        r = requests.get(f"{BASE_URL}/vehiculos/alquilados")
        if r.status_code == 200:
            datos = r.json()
            print(f"Vehículos alquilados: {datos['vehiculos_alquilados']}")
            for v in datos['vehiculos']:
                mostrar_vehiculo(v)
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def historial_usuario():
    """Ver historial de alquileres de un usuario"""
    print("\n--- HISTORIAL DE ALQUILERES ---")
    try:
        id_usuario = int(input("ID del usuario: "))
    except ValueError:
        print("❌ El ID debe ser un número entero")
        return
    
    try:
        r = requests.get(f"{BASE_URL}/usuarios/{id_usuario}/historial")
        if r.status_code == 200:
            datos = r.json()
            print(f"Usuario ID: {datos['usuario']['id']}")
            print(f"Alquileres totales: {datos['usuario']['veces_alquilado']}")
            print(f"Vehículos alquilados: {datos['total_vehiculos_alquilados']}")
            for v in datos['vehiculos']:
                mostrar_vehiculo(v)
        else:
            print(f"❌ Error: {r.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"❌ Error de conexión: {e}")

def menu():
    """Menú principal del cliente"""
    opcion = ""
    
    while opcion != "0":
        print("\n" + "=" * 50)
        print("   ALQUILER DE VEHÍCULOS - CLIENTE")
        print("=" * 50)
        print("1. Registrar nuevo usuario")
        print("2. Registrar nuevo vehículo")
        print("3. Alquilar vehículo libre (cualquiera)")
        print("4. Alquilar vehículo específico")
        print("5. Devolver vehículo")
        print("6. Listar todos los vehículos")
        print("7. Listar todos los usuarios")
        print("8. Listar vehículos libres")
        print("9. Listar vehículos alquilados")
        print("10. Ver historial de un usuario")
        print("0. Salir")
        print("=" * 50)
        
        opcion = input("Selecciona una opción: ").strip()
        
        match opcion:
            case "1":
                registrar_usuario()
            case "2":
                registrar_vehiculo()
            case "3":
                alquiler_libre()
            case "4":
                alquiler_especifico()
            case "5":
                devolver_vehiculo()
            case "6":
                listar_vehiculos()
            case "7":
                listar_usuarios()
            case "8":
                listar_vehiculos_libres()
            case "9":
                listar_vehiculos_alquilados()
            case "10":
                historial_usuario()
            case "0":
                print("\n👋 ¡Hasta luego!")
            case _:
                print("❌ Opción no válida")

if __name__ == "__main__":
    print("=" * 50)
    print("   CLIENTE DE ALQUILER DE VEHÍCULOS")
    print("=" * 50)
    print("Conectando al servidor en:", BASE_URL)
    print("\n💡 Los IDs se generan automáticamente")
    print("   - Los usuarios empiezan con ID 1")
    print("   - Los vehículos empiezan con ID 1")
    print("=" * 50)
    menu()