import Herramientas_p
import prestamos
AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
RESET = "\033[0m"

def consultar_herramienta():
    print(f"\n{AZUL}1. Listar todas las herramientas | 2. Buscar una específica{RESET}")
    sub_op = input("Elige acción: ")
    if sub_op == "1":
        Herramientas_p.listar_herramientas()
    elif sub_op == "2":
        Herramientas_p.consultar_herramienta()

def new_prestamo(id_ingreso):
    print(f"\n{VERDE}--- NUEVA SOLICITUD ---{RESET}")
    id_h = input("ID de la herramienta que desea: ")
    try:
        cant = int(input("Cantidad a solicitar: "))
        id_procesado = int(id_h) if id_h.isdigit() else id_h
        prestamos.solicitar_prestamo(id_ingreso, id_procesado, cant)
    except ValueError:
        print(f"{ROJO}Error: La cantidad ingresada debe ser un número entero.{RESET}")