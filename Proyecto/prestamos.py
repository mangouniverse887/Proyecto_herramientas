from logs import registrar_log
from Herramientas_p import herramientas, guardar_herramientas
import datetime
import json
import os

ARCHIVO_PRESTAMOS = "prestamos.json"
prestamos = []

def cargar_prestamos():
    global prestamos
    if os.path.exists(ARCHIVO_PRESTAMOS):
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            prestamos = json.load(archivo)
    else:
        prestamos = []

def guardar_prestamos():
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        json.dump(prestamos, archivo, indent=4, ensure_ascii=False)

def solicitar_prestamo(id_usuario, id_herramienta, cantidad_solicitada):
    herramienta_encontrada = None
    for h in herramientas:
        if str(h["id"]) == str(id_herramienta):
            herramienta_encontrada = h
            break
    if not herramienta_encontrada:
        print("Error: La herramienta no existe.")
        return
    if herramienta_encontrada["stock"] < cantidad_solicitada:
        print(f"Error: Stock insuficiente. Solo hay {herramienta_encontrada['stock']} disponibles de {herramienta_encontrada['nombre']}.")
        return
    if herramienta_encontrada["estado"] != "activa":
        print(f"Error: La herramienta no se puede prestar por que está '{herramienta_encontrada['estado']}.")
        return

    nuevo_id_prestamo = f"P{len(prestamos) + 1}"
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")

    nuevo_prestamo = {
        "id_prestamo": nuevo_id_prestamo,
        "id_usuario": id_usuario,
        "id_herramienta": id_herramienta,
        "cantidad": cantidad_solicitada,
        "fecha_inicio": fecha_hoy,
        "fecha_estimada_devolucion": "Pendiente",
        "estado": "pendiente",
        "observaciones": "Solicitud pendiente de aprobación"
    }
    prestamos.append(nuevo_prestamo)
    guardar_prestamos()
    print(f"\nSolicitud {nuevo_id_prestamo} creada exitosamente. Esperando aprobación del Administrador.")

def aprobar_prestamo(id_prestamo):
    prestamo_encontrado = None
    for p in prestamos:
        if p["id_prestamo"] == id_prestamo:
            prestamo_encontrado = p
            break
    if not prestamo_encontrado:
        print(f"Error: No se encontró la solicitud {id_prestamo}.")
        return
    if prestamo_encontrado["estado"] != "pendiente":
        print(f"La solicitud {id_prestamo} ya se encuentra {prestamo_encontrado['estado']}.")
        return
    id_herramienta = prestamo_encontrado["id_herramienta"]
    cantidad_solicitada = prestamo_encontrado["cantidad"]
    herramienta_encontrada = None
    for h in herramientas:
        if str(h["id"]) == str(id_herramienta):
            herramienta_encontrada = h
            break
    if herramienta_encontrada["stock"] < cantidad_solicitada:
        mensaje_error = f"Error al aprobar {id_prestamo}: Stock insuficiente de {herramienta_encontrada['nombre']}."
        print(mensaje_error)
        registrar_log(mensaje_error)
        prestamo_encontrado["estado"] = "rechazado"
        guardar_prestamos()
        return
    herramienta_encontrada["stock"] -= cantidad_solicitada
    if herramienta_encontrada["stock"] == 0:
        herramienta_encontrada["estado"] = "agotado"
    prestamo_encontrado["estado"] = "activo"
    prestamo_encontrado["observaciones"] = "Aprobado y entregado en buenas condiciones"

    guardar_prestamos()
    guardar_herramientas()

    mensaje_exito = f"\nPrestamo {id_prestamo} aprobado exitosamente. Nuevo stock de {herramienta_encontrada['nombre']}: {herramienta_encontrada['stock']}"
    print(mensaje_exito)
    registrar_log(mensaje_exito)


def registrar_devolucion(id_prestamo):
    prestamo_encontrado = None
    for p in prestamos:
        if p["id_prestamo"] == id_prestamo:
            prestamo_encontrado = p
            break
    if not prestamo_encontrado:
        mensaje_error = f"Error: El préstamo con ID {id_prestamo} no existe."
        print(mensaje_error)
        registrar_log(mensaje_error)
        return
    if prestamo_encontrado["estado"] == "devuelto":
        print("Este préstamo ya había sido devuelto anteriormente.")
        return
    print("\n¿En qué estado se devuelve la herramienta?")
    print("1. Buen estado y a tiempo")
    print("2. Dañada, incompleta o tarde (Penalizar usuario)")
    estado_dev = input("Opción (1-2): ")
    if estado_dev == "2":
        import usuarios
        usuario_castigado = usuarios.buscar_usuario(prestamo_encontrado["id_usuario"])
        if usuario_castigado:
            faltas_actuales = usuario_castigado.get("penalizaciones", 0)
            usuario_castigado["penalizaciones"] = faltas_actuales + 1
            usuarios.guardar_usuarios()
            print(f"Se ha añadido una penalización al usuario. (Faltas totales: {usuario_castigado['penalizaciones']})")
    prestamo_encontrado["estado"] = "devuelto"
    id_herra = prestamo_encontrado["id_herramienta"]
    cantidad_a_restaurar = prestamo_encontrado["cantidad"]
    for h in herramientas:
        if str(h["id"]) == str(id_herra):
            h["stock"] +=cantidad_a_restaurar
            guardar_prestamos()
            guardar_herramientas()
            mensaje_exito = f"Devolución exitosa: Se devolvió la herramienta {h['nombre']}. Stock restaurado: {h['stock']}"
            print(mensaje_exito)
            registrar_log(mensaje_exito)
            if h["stock"] > 0:
                h["estado"] = "activo"
            break

cargar_prestamos()