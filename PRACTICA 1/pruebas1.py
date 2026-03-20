import os

print("Hola")
print("Verificando directorio...")

try:
    current_dir = os.getcwdb()  # Intentamos obtener el directorio de trabajo
    print(f"Directorio actual: {current_dir}")
except Exception as e:
    print(f"Error al obtener el directorio: {e}")

print("Verificación completa")