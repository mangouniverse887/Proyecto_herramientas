import json
import os

AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CELESTE = "\033[36m"
MORADO = "\033[35m"
RESET = "\033[0m"

DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(DIRECTORIO_BASE, "herramientas.json")

herramientas = []


def cargar_herramientas():
    global herramientas

    if os.path.exists(ARCHIVO):
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            herramientas = json.load(archivo)


def guardar_herramientas():
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(herramientas, archivo, indent=4, ensure_ascii=False)


def buscar_herramienta(id_herramienta):
    for herramienta in herramientas:
        if herramienta["id"] == id_herramienta:
            return herramienta

    return None


def crear_herramienta():
    print("\n--- REGISTRAR HERRAMIENTA ---")

    id_herramienta = int(input("ID: "))

    if buscar_herramienta(id_herramienta) is not None:
        print("Ya existe una herramienta con ese ID.")
        return

    nombre = input("Nombre: ")
    categoria = input("Categoría: ")
    stock = int(input("Cantidad disponible: "))
    estado = input(
        "Estado (activa, en reparación, fuera de servicio): "
    )
    valor_estimado = float(input("Valor estimado: "))

    herramienta = {
        "id": id_herramienta,
        "nombre": nombre,
        "categoria": categoria,
        "stock": stock,
        "estado": estado,
        "valor_estimado": valor_estimado
    }

    herramientas.append(herramienta)
    guardar_herramientas()

    print("Herramienta registrada correctamente.")


def listar_herramientas():
    print("\n--- LISTA DE HERRAMIENTAS ---")

    if len(herramientas) == 0:
        print("No hay herramientas registradas.")
        return

    for herramienta in herramientas:
        print("----------------------------")
        print("ID:", herramienta["id"])
        print("Nombre:", herramienta["nombre"])
        print("Categoría:", herramienta["categoria"])
        print("Stock disponible:", herramienta["stock"])
        reparacion = herramienta.get("en_reparacion", 0)
        if reparacion > 0:
            print(f"En Reparación: {reparacion}")
        print("Estado:", herramienta["estado"])
        print("Valor estimado:", herramienta["valor_estimado"])


def consultar_herramienta():
    print("\n--- BUSCAR HERRAMIENTA ---")

    id_buscar = int(input("Ingrese el ID de la herramienta: "))

    herramienta = buscar_herramienta(id_buscar)

    if herramienta is None:
        print("No se encontró la herramienta.")
        return

    print("\nHerramienta encontrada:")
    print("ID:", herramienta["id"])
    print("Nombre:", herramienta["nombre"])
    print("Categoría:", herramienta["categoria"])
    print("Stock:", herramienta["stock"])
    print("Estado:", herramienta["estado"])
    print("Valor estimado:", herramienta["valor_estimado"])


def actualizar_herramienta():
    print("\n--- ACTUALIZAR HERRAMIENTA ---")

    id_buscar = int(input("Ingrese el ID de la herramienta: "))

    herramienta = buscar_herramienta(id_buscar)

    if herramienta is None:
        print("No se encontró la herramienta.")
        return

    print("Deje el campo vacío si no desea modificarlo.")

    nombre = input("Nuevo nombre: ")
    categoria = input("Nueva categoría: ")
    stock = input("Nuevo stock: ")
    estado = input("Nuevo estado: ")
    valor = input("Nuevo valor estimado: ")

    if nombre != "":
        herramienta["nombre"] = nombre

    if categoria != "":
        herramienta["categoria"] = categoria

    if stock != "":
        herramienta["stock"] = int(stock)

    if estado != "":
        herramienta["estado"] = estado

    if valor != "":
        herramienta["valor_estimado"] = float(valor)

    guardar_herramientas()

    print("Herramienta actualizada correctamente.")


def inactivar_herramienta():
    print("\n--- INACTIVAR HERRAMIENTA ---")

    id_buscar = int(input("Ingrese el ID de la herramienta: "))

    herramienta = buscar_herramienta(id_buscar)

    if herramienta is None:
        print("No se encontró la herramienta.")
        return

    herramienta["estado"] = "fuera de servicio"

    guardar_herramientas()

    print("Herramienta inactivada correctamente.")

def enviar_reparacion():
    print("\n--- ENVIAR A REPARACIÓN ---")
    id_buscar = int(input("Ingrese el ID de la herramienta dañada: "))
    herramienta = buscar_herramienta(id_buscar)
    if herramienta is None:
        print("No se encontró la herramienta.")
        return
    cant_danada = int(input(f"¿Cuántas unidades se dañaron? (Stock disponible: {herramienta['stock']}): "))
    if cant_danada > herramienta["stock"]:
        print("ERROR: No puedes enviar a reparar más herramientas de las que hay en stock.")
        return
    herramienta["stock"] -= cant_danada
    herramienta["en_reparacion"] = herramienta.get("en_reparacion", 0) + cant_danada
    if herramienta["stock"] == 0:
        herramienta["estado"] = "agotado"
    else:
        herramienta["estado"] = "activa"
    guardar_herramientas()
    print(f"{VERDE}Se enviaron {cant_danada} unidades a reparación. Quedan {herramienta['stock']} Listas para uso.{RESET}")
def retornar_reparacion():
    print("\n--- RETORNAR HERRAMIENTAS DE REPARACIÓN ---")
    try:
        id_buscar = int(input("Ingrese el ID de la herramienta: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return
    herramienta = buscar_herramienta(id_buscar)
    if herramienta is None:
        print("No se encontró la herramienta con ese ID.")
        return
    en_rep = herramienta.get("en_reparacion", 0)
    if en_rep <= 0:
        print("Esta herramienta no tiene unidades registradas en reparación.")
        return
    try:
        cant_reparada = int(input(f"Cuántas unidades listas regresan al inventario? (En taller: {en_rep}): "))
    except ValueError:
        print("Error: Ingrese un número válido")
        return
    if cant_reparada <= 0:
        print("La cantidad debe ser mayor a 0")
        return
    if cant_reparada > en_rep:
        print(f"Error: No puedes retornar más unidades ({cant_reparada}) de las que hay en el taller ({en_rep}).")
        return
    herramienta["en_reparacion"] = en_rep - cant_reparada
    herramienta["stock"] += cant_reparada
    if herramienta["stock"] > 0:
        herramienta["estado"] = "activa"
        guardar_herramientas()
        print(f"Se reincorporaron {cant_reparada} unidad(es) de {herramienta['nombre']}. Stock activo actual: {herramienta['stock']}.")
cargar_herramientas()
