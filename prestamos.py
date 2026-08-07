from logs import registrar_log
from mock_data import usuarios, prestamos
from Herramientas_p import herramientas
import datetime

def solicitar_prestamo(id_usuario, id_herramienta, cantidad_solicitada):
    herramienta_encontrada = None
    for h in herramientas:
        if h["id"] == id_herramienta:
            herramienta_encontrada = h
            break
    if not herramienta_encontrada:
        print("Error: La herramienta no existe.")
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
        if h["id"] == id_herramienta:
            herramienta_encontrada = h
            break
    if herramienta_encontrada["stock"] < cantidad_solicitada:
        mensaje_error = f"Error al aprobar {id_prestamo}: Stock insuficiente de {herramienta_encontrada['nombre']}."
        print(mensaje_error)
        registrar_log(mensaje_error)
        prestamo_encontrado["estado"] = "rechazado"
        return
    herramienta_encontrada["stock"] -= cantidad_solicitada
    prestamo_encontrado["estado"] = "activo"
    prestamo_encontrado["observaciones"] = "Aprobado y entregado en buenas condiciones"

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
    prestamo_encontrado["estado"] = "devuelto"
    id_herra = prestamo_encontrado["id_herramienta"]
    cantidad_a_restaurar = prestamo_encontrado["cantidad"]
    for h in herramientas:
        if h["id"] == id_herra:
            h["stock"] +=cantidad_a_restaurar
            mensaje_exito = f"Devolución exitosa: Se devolvió la herramienta {h['nombre']}. Stock restaurado: {h['stock']}"
            print(mensaje_exito)
            registrar_log(mensaje_exito)
            break