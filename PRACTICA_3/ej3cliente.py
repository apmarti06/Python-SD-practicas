import requests

BASE_URL = "http://localhost:8080/rooms"


def mostrar_habitacion(h):
    estado = "Ocupada" if h["ocupada"] else "Libre"
    equipamiento = ", ".join(h["equipamiento"])

    print(f"Habitación {h['id']}:")
    print(f"  - {h['plazas']} plazas.")
    print(f"  - Equipamiento: {equipamiento}.")
    print(f"  - {estado}.")


def alta_habitacion():
    try:
        room_id = int(input("Introduce el identificador: "))
        plazas = int(input("Introduce el número de plazas: "))
        equipamiento = input("Introduce el equipamiento separado por comas: ").split(",")
        equipamiento = [e.strip() for e in equipamiento if e.strip() != ""]
        ocupada_txt = input("¿Está ocupada? (si/no): ").strip().lower()
        ocupada = ocupada_txt == "si"

        datos = {
            "id": room_id,
            "plazas": plazas,
            "equipamiento": equipamiento,
            "ocupada": ocupada
        }

        #aquí hacemos uso de las apis creadas del servidor
        r = requests.post(BASE_URL, json=datos)
        print(r.json())

    except ValueError:
        print("Error: debes introducir números válidos en id y plazas.")
    except requests.RequestException as e:
        print("Error de conexión:", e)


def modificar_habitacion():
    try:
        room_id = int(input("Introduce el identificador de la habitación a modificar: "))
        plazas = int(input("Introduce el nuevo número de plazas: "))
        equipamiento = input("Introduce el nuevo equipamiento separado por comas: ").split(",")
        equipamiento = [e.strip() for e in equipamiento if e.strip() != ""]
        ocupada_txt = input("¿Está ocupada? (si/no): ").strip().lower()
        ocupada = ocupada_txt == "si"

        datos = {
            "plazas": plazas,
            "equipamiento": equipamiento,
            "ocupada": ocupada
        }

        r = requests.put(f"{BASE_URL}/{room_id}", json=datos)
        print(r.json())

    except ValueError:
        print("Error: debes introducir números válidos en id y plazas.")
    except requests.RequestException as e:
        print("Error de conexión:", e)


def listar_habitaciones():
    try:
        r = requests.get(BASE_URL)
        datos = r.json()

        if "habitaciones" in datos and datos["habitaciones"]:
            for h in datos["habitaciones"]:
                mostrar_habitacion(h)
                print()
        else:
            print("No hay habitaciones registradas.")

    except requests.RequestException as e:
        print("Error de conexión:", e)


def consultar_habitacion():
    try:
        room_id = int(input("Introduce el identificador de la habitación: "))
        r = requests.get(f"{BASE_URL}/{room_id}")
        datos = r.json()

        if r.status_code == 200:
            mostrar_habitacion(datos["habitacion"])
        else:
            print(datos)

    except ValueError:
        print("Error: el identificador debe ser un número entero.")
    except requests.RequestException as e:
        print("Error de conexión:", e)


def consultar_por_estado():
    try:
        opcion = input("¿Qué quieres consultar? (ocupadas/desocupadas): ").strip().lower()
        r = requests.get(f"{BASE_URL}/status/{opcion}")
        datos = r.json()

        if r.status_code == 200:
            habitaciones = datos["habitaciones"]
            if habitaciones:
                for h in habitaciones:
                    mostrar_habitacion(h)
                    print()
            else:
                print("No hay habitaciones con ese estado.")
        else:
            print(datos)

    except requests.RequestException as e:
        print("Error de conexión:", e)


def menu():
    opcion = ""

    while opcion != "6":
        print("\nElige qué opción deseas realizar:")
        print("1. Dar de alta una nueva habitación")
        print("2. Modificar los datos de una habitación")
        print("3. Consultar la lista completa de habitaciones")
        print("4. Consultar una habitación mediante identificador")
        print("5. Consultar la lista de habitaciones ocupadas o desocupadas")
        print("6. Salir")

        opcion = input("> ").strip()

        match opcion:
            case "1":
                alta_habitacion()
            case "2":
                modificar_habitacion()
            case "3":
                listar_habitaciones()
            case "4":
                consultar_habitacion()
            case "5":
                consultar_por_estado()
            case "6":
                print("Saliendo del cliente...")
            case _:
                print("Opción no válida.")


if __name__ == "__main__":
    menu()