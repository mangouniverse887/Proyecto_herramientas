#para limpiar la pantalla
import os
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
limpiar_pantalla()

import usuarios
from menu_residente_funciones import consultar_herramienta, new_prestamo
from menu_admin_funciones import menu_reportes, gestionar_usuarios, gestionar_herramientas, prestamos_aprobar_devolver
AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CELESTE = "\033[36m"
MORADO = "\033[35m"
RESET = "\033[0m"

def iniciar_sistema():
    print("="*40)
    print("--- SISTEMA DE PRÉSTAMOS ---")
    print("="*40)
    id_ingreso = input("Por favor, ingrese su ID (cédula) para iniciar: ")
    usuario_actual = usuarios.buscar_usuario(id_ingreso)
    if not usuario_actual:
        print("Usuario no encontrado. Contacte a un administrador para registrarse.")
        return
    print(f"\n ¡Hola, {usuario_actual['nombres']} {usuario_actual['apellidos']}!")
    while True:
        tipo = usuario_actual.get("tipo_usuario", "").lower()
        if tipo == "administrador":
            print("\n--- MENÚ ADMINISTRADOR ---")
            print(f"{AZUL}1. Gestionar Usuarios{RESET}")
            print(f"{VERDE}2. Gestionar Herramientas{RESET}")
            print(f"{AMARILLO}3. Préstamos{RESET}")
            print(f"{MORADO}4. Ver Reportes del Sistema{RESET}")
            print(f"{ROJO}5. Salir{RESET}")
            opcion = input("\nElige una opción (1-5): ")
            if opcion == "1":
                gestionar_usuarios()
            elif opcion == "2":
                gestionar_herramientas()
            elif opcion == "3":
                prestamos_aprobar_devolver()
            elif opcion == "4":
                menu_reportes()
            elif opcion == "5":
                print("Cerrando sesión... Vuelva pronto")
                break
            else:
                print("Opción inválida.")

        elif tipo == "residente":
            print("\n--- MENÚ RESIDENTE ---")
            print(f"{AZUL}1. Consultar Catálogo de Herramientas{RESET}")
            print(f"{VERDE}2. Solicitar un Préstamo{RESET}")
            print(f"{ROJO}3. Salir{RESET}")
            opcion = input("\nElige una opción (1-3): ")
            if opcion == "1":
                consultar_herramienta()
            elif opcion == "2":
                new_prestamo(id_ingreso)
            if opcion == "3":
                print("Cerrando sesión... ¡Vuelva Pronto!")
                break
            else:
                print("Opción inválida.")

if __name__ == "__main__":
    iniciar_sistema()