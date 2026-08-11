import json
import os

ARCHIVO = "herramientas.json"

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
        print("Stock:", herramienta["stock"])
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


cargar_herramientas()
