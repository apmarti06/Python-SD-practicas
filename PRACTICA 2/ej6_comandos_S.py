import socket
import os
import shutil

HOST = 'localhost'
PORT = 1025

def main():
    # Crear socket UDP
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as servidor:
        servidor.bind((HOST, PORT))
        
        # Directorio donde estamos trabajando
        directorio_actual = os.getcwd()
        
        print("="*60)
        print("SERVIDOR UDP DE ARCHIVOS")
        print("="*60)
        print(f"Servidor escuchando en {HOST}:{PORT}")
        print(f"Directorio actual: {directorio_actual}")
        print("Esperando comandos del cliente...")
        print("-"*60)
        
        while True:
            # Recibir comando del cliente
            datos, addr = servidor.recvfrom(65535)
            comando = datos.decode('utf-8')
            print(f"\n[{addr[1]}] Comando: {comando}")
            
            
            # 1. COMANDO: ls
            # PROCESAR COMANDO
            if comando == "ls":
                #listamos todos los directorios del directorio actual
                archivos = os.listdir(directorio_actual)
                if len(archivos) == 0:
                    respuesta = "Directorio vacío"
                else:
                    respuesta = f"Contenido de {directorio_actual}:\n"
                    for item in archivos:
                        ruta = os.path.join(directorio_actual, item)
                        # mostramos la carpeta su ruta, o el fichero en si
                        if os.path.isdir(ruta):
                            respuesta += f"{item}/\n"
                        else:
                            tamaño = os.path.getsize(ruta)
                            respuesta += f"{item} ({tamaño} bytes)\n"
            
            # 2. COMANDO: rm <archivo>
            elif comando.startswith("rm "):
                nombre = comando[3:]  # Quitar "rm "
                ruta = os.path.join(directorio_actual, nombre) 
                
                if not os.path.exists(ruta):
                    respuesta = f"Error: El archivo '{nombre}' no existe"
                elif os.path.isdir(ruta):
                    respuesta = f"Error: '{nombre}' es un directorio"
                else:
                    os.remove(ruta)
                    respuesta = f"Correcto: Archivo '{nombre}' eliminado"
            
            # 3. COMANDO: write <archivo> '<mensaje>'
            elif comando.startswith("write "):
                # Extraer nombre y mensaje
                resto = comando[6:]  # Quitar "write "
                
                # Buscar la primera comilla simple
                if "'" in resto:
                    nombre = resto[:resto.index("'")].strip()
                    mensaje = resto[resto.index("'")+1:resto.rindex("'")]
                    
                    ruta = os.path.join(directorio_actual, nombre)
                    with open(ruta, 'w', encoding='utf-8') as f:
                        f.write(mensaje)
                    respuesta = f"Correcto: Archivo '{nombre}' creado con {len(mensaje)} caracteres"
                else:
                    respuesta = "Error: Formato incorrecto. Use: write <archivo> '<mensaje>'"
            
            # 4. COMANDO: exit
            elif comando == "exit":
                print(f"\nCliente {addr[1]} se desconectó")
                servidor.sendto(b"EXIT", addr)
                break
            
            # 5. COMANDO: cd <directorio>
            elif comando.startswith("cd "):
                nombre = comando[3:]  # Quitar "cd "
                
                if nombre == "..":
                    nuevo_dir = os.path.dirname(directorio_actual)
                elif nombre == ".":
                    nuevo_dir = directorio_actual
                else:
                    nuevo_dir = os.path.join(directorio_actual, nombre)
                
                if not os.path.exists(nuevo_dir):
                    respuesta = f"Error: El directorio '{nombre}' no existe"
                elif not os.path.isdir(nuevo_dir):
                    respuesta = f"Error: '{nombre}' no es un directorio"
                else:
                    directorio_actual = nuevo_dir
                    respuesta = f"Correcto: Cambiado a {directorio_actual}"
            
            # 6. COMANDO: mv <origen> <destino>
            elif comando.startswith("mv "):
                partes = comando[3:].split()
                if len(partes) != 2:
                    respuesta = "Error: Use: mv <origen> <destino>"
                else:
                    origen, destino = partes
                    ruta_origen = os.path.join(directorio_actual, origen)
                    ruta_destino = os.path.join(directorio_actual, destino)
                    
                    if not os.path.exists(ruta_origen):
                        respuesta = f"Error: El archivo '{origen}' no existe"
                    elif os.path.isdir(ruta_origen):
                        respuesta = f"Error: '{origen}' es un directorio"
                    elif os.path.dirname(ruta_origen) == os.path.dirname(ruta_destino):
                        respuesta = f"Error: Origen y destino en el mismo directorio"
                    else:
                        # Crear directorio destino si no existe
                        os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
                        shutil.move(ruta_origen, ruta_destino)
                        respuesta = f"Correcto: '{origen}' movido a '{destino}'"
            
            else:
                respuesta = "Error: Comando no reconocido. Usa: ls, rm, write, cd, mv, exit"
            
            # Enviar respuesta al cliente
            servidor.sendto(respuesta.encode('utf-8'), addr)
            print(f"[{addr[1]}] Respuesta: {respuesta[:50]}..." if len(respuesta) > 50 else f"[{addr[1]}] Respuesta: {respuesta}")

if __name__ == "__main__":
    main()