import json
from pathlib import Path


ARCHIVO = Path(__file__).with_name("herramientas.json")
ESTADOS_VALIDOS = ("activa", "en reparación", "fuera de servicio")
herramientas = []


def cargar_herramientas():
    """Carga las herramientas guardadas. Si no hay archivo, inicia vacío."""
    global herramientas

    if not ARCHIVO.exists():
        herramientas = []
        return

    try:
        with ARCHIVO.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        herramientas = datos if isinstance(datos, list) else []
    except (OSError, json.JSONDecodeError):
        print("Aviso: no fue posible leer herramientas.json.")
        herramientas = []


def guardar_herramientas():
    """Guarda toda la información en formato JSON."""
    try:
        with ARCHIVO.open("w", encoding="utf-8") as archivo:
            json.dump(herramientas, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Error: no fue posible guardar las herramientas.")
        return False


def leer_entero(mensaje, minimo=0, permitir_vacio=False):
    while True:
        entrada = input(mensaje).strip()
        if permitir_vacio and entrada == "":
            return None
        try:
            valor = int(entrada)
            if valor < minimo:
                print(f"Ingrese un número mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Debe escribir un número entero.")


def leer_decimal(mensaje, minimo=0, permitir_vacio=False):
    while True:
        entrada = input(mensaje).strip().replace(",", ".")
        if permitir_vacio and entrada == "":
            return None
        try:
            valor = float(entrada)
            if valor < minimo:
                print(f"Ingrese un valor mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Debe escribir un número.")


def leer_texto_obligatorio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Este campo no puede quedar vacío.")


def leer_estado(permitir_vacio=False):
    while True:
        print("Estados: 1. Activa | 2. En reparación | 3. Fuera de servicio")
        opcion = input("Seleccione el estado: ").strip()

        if permitir_vacio and opcion == "":
            return None

        opciones = {
            "1": "activa",
            "2": "en reparación",
            "3": "fuera de servicio",
        }
        if opcion in opciones:
            return opciones[opcion]
        print("Opción de estado inválida.")


def buscar_herramienta(id_herramienta):
    for herramienta in herramientas:
        if herramienta["id"] == id_herramienta:
            return herramienta
    return None


def mostrar_herramienta(herramienta):
    print("-" * 42)
    print(f'ID: {herramienta["id"]}')
    print(f'Nombre: {herramienta["nombre"]}')
    print(f'Categoría: {herramienta["categoria"]}')
    print(f'Cantidad disponible: {herramienta["cantidad_disponible"]}')
    print(f'Estado: {herramienta["estado"]}')
    print(f'Valor estimado: ${herramienta["valor_estimado"]:,.2f}')


def crear_herramienta():
    print("\n--- REGISTRAR HERRAMIENTA ---")
    id_herramienta = leer_entero("ID: ", minimo=1)

    if buscar_herramienta(id_herramienta) is not None:
        print("Ya existe una herramienta con ese ID.")
        return

    herramienta = {
        "id": id_herramienta,
        "nombre": leer_texto_obligatorio("Nombre: "),
        "categoria": leer_texto_obligatorio("Categoría: "),
        "cantidad_disponible": leer_entero("Cantidad disponible: ", minimo=0),
        "estado": leer_estado(),
        "valor_estimado": leer_decimal("Valor estimado: ", minimo=0),
    }

    herramientas.append(herramienta)
    if guardar_herramientas():
        print("Herramienta registrada correctamente.")


def listar_herramientas():
    print("\n--- LISTA DE HERRAMIENTAS ---")
    if not herramientas:
        print("No hay herramientas registradas.")
        return

    for herramienta in herramientas:
        mostrar_herramienta(herramienta)


def consultar_herramienta():
    print("\n--- BUSCAR HERRAMIENTA ---")
    id_buscar = leer_entero("Ingrese el ID: ", minimo=1)
    herramienta = buscar_herramienta(id_buscar)

    if herramienta is None:
        print("No se encontró la herramienta.")
        return

    mostrar_herramienta(herramienta)


def actualizar_herramienta():
    print("\n--- ACTUALIZAR HERRAMIENTA ---")
    id_buscar = leer_entero("Ingrese el ID: ", minimo=1)
    herramienta = buscar_herramienta(id_buscar)

    if herramienta is None:
        print("No se encontró la herramienta.")
        return

    print("Presione Enter para conservar el valor actual.")
    nombre = input(f'Nombre [{herramienta["nombre"]}]: ').strip()
    categoria = input(f'Categoría [{herramienta["categoria"]}]: ').strip()
    cantidad = leer_entero(
        f'Cantidad disponible [{herramienta["cantidad_disponible"]}]: ',
        minimo=0,
        permitir_vacio=True,
    )
    estado = leer_estado(permitir_vacio=True)
    valor = leer_decimal(
        f'Valor estimado [{herramienta["valor_estimado"]}]: ',
        minimo=0,
        permitir_vacio=True,
    )

    if nombre:
        herramienta["nombre"] = nombre
    if categoria:
        herramienta["categoria"] = categoria
    if cantidad is not None:
        herramienta["cantidad_disponible"] = cantidad
    if estado is not None:
        herramienta["estado"] = estado
    if valor is not None:
        herramienta["valor_estimado"] = valor

    if guardar_herramientas():
        print("Herramienta actualizada correctamente.")


def inactivar_herramienta():
    print("\n--- INACTIVAR HERRAMIENTA ---")
    id_buscar = leer_entero("Ingrese el ID: ", minimo=1)
    herramienta = buscar_herramienta(id_buscar)

    if herramienta is None:
        print("No se encontró la herramienta.")
        return

    if herramienta["estado"] == "fuera de servicio":
        print("La herramienta ya está fuera de servicio.")
        return

    confirmar = input("¿Confirma la inactivación? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Operación cancelada.")
        return

    herramienta["estado"] = "fuera de servicio"
    if guardar_herramientas():
        print("Herramienta inactivada correctamente.")


def listar_stock_bajo():
    print("\n--- HERRAMIENTAS CON STOCK BAJO ---")
    resultado = [
        herramienta
        for herramienta in herramientas
        if herramienta["cantidad_disponible"] < 3
    ]

    if not resultado:
        print("No hay herramientas con menos de 3 unidades.")
        return

    for herramienta in resultado:
        mostrar_herramienta(herramienta)


def descontar_stock(id_herramienta, cantidad):
    """Función que podrá llamar el módulo de préstamos."""
    herramienta = buscar_herramienta(id_herramienta)
    if herramienta is None or cantidad <= 0:
        return False
    if herramienta["estado"] != "activa":
        return False
    if herramienta["cantidad_disponible"] < cantidad:
        return False

    herramienta["cantidad_disponible"] -= cantidad
    return guardar_herramientas()


def restaurar_stock(id_herramienta, cantidad):
    """Restaura unidades cuando se devuelve un préstamo."""
    herramienta = buscar_herramienta(id_herramienta)
    if herramienta is None or cantidad <= 0:
        return False

    herramienta["cantidad_disponible"] += cantidad
    return guardar_herramientas()


def menu_herramientas():
    cargar_herramientas()

    while True:
        print("\n=== GESTIÓN DE HERRAMIENTAS ===")
        print("1. Registrar herramienta")
        print("2. Listar herramientas")
        print("3. Buscar herramienta")
        print("4. Actualizar herramienta")
        print("5. Inactivar herramienta")
        print("6. Consultar stock bajo")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            crear_herramienta()
        elif opcion == "2":
            listar_herramientas()
        elif opcion == "3":
            consultar_herramienta()
        elif opcion == "4":
            actualizar_herramienta()
        elif opcion == "5":
            inactivar_herramienta()
        elif opcion == "6":
            listar_stock_bajo()
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_herramientas()
