from logs import registrar_log
from mock_data import herramientas, usuarios, prestamos
import datetime

def registrar_prestamo(id_usuario, id_herramienta, cantidad_solicitada):
    herramienta_encontrada = None
    for h in herramientas:
        if j["id"] == id_herramienta:
            herramienta_encontrada = h
            break
    if not herramienta_encontrada:
        print("Error: La herramienta no existe.")
        return
    if herramienta_encontrada["canditad_disponible"] < cantidad_solicitada:
        mensaje_error = f"intento fallido: No hay suficiente stock de {herramienta_encontrada['nombre']}. Solicitado: {cantidad_solicitada}, Disponible: {herramienta_encontrada['cantidad_disponible']}"
        print(mensaje_error)
        registrar_log(mensaje_error)
        return
    herramienta_encontrada["cantidad_disponible"] -= cantidad_solicitada

    nuevo_id_prestamo = f"P{len(prestamos) + 1}"
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")

    nuevo_prestamo = {
        "id_prestamo": nuevo_id_prestamo,
        "id_usuario": id_usuario,
        "id_herramienta": id_herramienta,
        "cantidad": cantidad_solicitada,
        "fecha_inicio": fecha_hoy,
        "fecha_estimada_devolución": "Pendiente",
        "estado": "activo",
        "observaciones": "Entregado en buenas condiciones"
    }
    prestamos.append(nuevo_prestamo)
    print(f"\nPréstamo {nuevo_id_prestamo} registrado exitosamente.")
    print(f"Nuevo stock de {herramienta_encontrada['nombre']}: {herramienta_encontrada['cantidad_disponible']}")
