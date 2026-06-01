import socket

HOST = 'localhost'
PORT = 1025

def mostrar_menu():
    print("\n" + "="*50)
    print("COMANDOS DISPONIBLES:")
    print("="*50)
    print("  ls                     - Listar archivos")
    print("  rm <archivo>           - Eliminar archivo")
    print("  write <archivo> '<texto>' - Crear archivo")
    print("  cd <directorio>        - Cambiar directorio")
    print("  mv <origen> <destino>  - Mover archivo")
    print("  exit                   - Salir")
    print("  help                   - Mostrar este menú")
    print("="*50)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cliente:
        print("="*50)
        print("     CLIENTE UDP - SERVIDOR DE ARCHIVOS")
        print("="*50)
        print(f"Conectando a {HOST}:{PORT}")
        
        mostrar_menu()
        
        while True:
            # Pedir comando al usuario
            comando = input(f"\n> ").strip()
            
            if not comando:
                continue
            
            if comando.lower() == "help":
                mostrar_menu()
                continue
            
            # Enviar comando al servidor
            cliente.sendto(comando.encode('utf-8'), (HOST, PORT))
            
            # Recibir respuesta
            respuesta, _ = cliente.recvfrom(65535)
            mensaje = respuesta.decode('utf-8')
            
            # Verificar si es exit
            if mensaje == "EXIT" or comando.lower() == "exit":
                print("Desconectando del servidor...")
                break
            
            # Mostrar respuesta
            print("\n" + "="*50)
            print("RESPUESTA:")
            print("="*50)
            print(mensaje)
            print("="*50)

if __name__ == "__main__":
    main()