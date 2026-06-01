import socket

HOST = 'localhost'
PORT = 1025

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        servidor.bind((HOST, PORT))
        print(f"Servidor UDP escuchando en {HOST}:{PORT}")
        print("Esperando mensajes...\n")
        
        # Diccionario para recordar clientes y sus nombres
        clientes = {}
        
        while True:
            try:
                # Recibir mensaje del cliente
                mensaje, addr = servidor.recvfrom(1024)
                mensaje_decodificado = mensaje.decode('utf-8')
                print(f"Mensaje recibido de {addr}: {mensaje_decodificado}")
                
                # Verificar si el cliente ya ha dado su nombre
                if addr not in clientes:
                    # Primer mensaje: debe ser el nombre, guardandolo como clave en clientes
                    nombre = mensaje_decodificado
                    clientes[addr] = nombre
                    respuesta = f"{nombre}, ¿en qué puedo ayudarte?"
                    servidor.sendto(respuesta.encode('utf-8'), addr)
                    print(f"Respuesta enviada a {addr}: {respuesta}")
                
                else:
                    # Cliente ya registrado, donde su direccion+puerto --> id unico
                    nombre = clientes[addr]
                    
                    # Verificar si el cliente quiere salir
                    if mensaje_decodificado.lower() == "exit":
                        print(f"Cliente {nombre} ({addr}) se ha desconectado")
                        del clientes[addr]  # Eliminar al cliente
                        # No enviamos respuesta, solo cerramos la comunicación
                        continue
                    
                    # Cualquier otro mensaje
                    respuesta = "Debe ponerse en contacto con el servicio de atención de dudas cuya dirección es dudas@ejemplo.com"
                    servidor.sendto(respuesta.encode('utf-8'), addr)
                    print(f"Respuesta enviada a {nombre}: {respuesta[:50]}...")
            
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()