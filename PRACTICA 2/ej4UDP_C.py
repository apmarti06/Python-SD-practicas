import socket
import time

HOST = 'localhost'
PORT = 1025

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        print("=== CLIENTE UDP ===")
        print(f"Conectando al servidor {HOST}:{PORT}\n")
        
        # Paso 1: El servidor envía el mensaje de bienvenida
        # Como UDP no tiene conexión, el cliente tiene que pedir el mensaje
        # Enviamos un primer mensaje vacío o un saludo inicial
        cliente.sendto(b"HOLA", (HOST, PORT))
        
        # Recibir mensaje de bienvenida del servidor
        mensaje, _ = cliente.recvfrom(1024)
        print(f"Servidor: {mensaje.decode('utf-8')}")
        
        # Paso 2: El cliente envía su nombre
        nombre = input("Tú: ")
        cliente.sendto(nombre.encode('utf-8'), (HOST, PORT))
        
        # Recibir respuesta personalizada
        respuesta, _ = cliente.recvfrom(1024)
        print(f"Servidor: {respuesta.decode('utf-8')}")
        
        # Pasos 3 y 4: Bucle de preguntas y respuestas
        while True:
            # El cliente envía una pregunta
            pregunta = input("\nTú: ")
            cliente.sendto(pregunta.encode('utf-8'), (HOST, PORT))
            
            # Verificar si el cliente quiere salir
            if pregunta.lower() == "exit":
                print("Desconectando del servidor...")
                break
            
            # Recibir respuesta del servidor
            respuesta, _ = cliente.recvfrom(1024)
            print(f"Servidor: {respuesta.decode('utf-8')}")
        
        print("Conexión cerrada")

if __name__ == "__main__":
    main()