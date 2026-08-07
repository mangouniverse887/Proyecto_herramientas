from mock_data import prestamos
from Herramientas_p import herramientas
import datetime

def reporte_stock_bajo():
    print("\n--- HERRAMIENTAS CON STOCK BAJO (menos de 3) ---")
    encontradas = False
    for h in herramientas:
        if h["stock"] < 3:
            print(f"- {h['nombre']} (ID: {h['id']}): Quedan {h['stock']} unidades.")
            encontradas = True
    if not encontradas:
        print("Todo el stock está en orden (3 o más unidades).")

def reporte_prestamos_activos():
    print("\n--- PRÉSTAMOS ACTIVOS ---")
    activos = [p for p in prestamos if p["estado"] == "activo"]
    if len(activos) == 0:
        print("No hay préstamos activos en este momento.")
    else:
        for p in activos:
            print(f"Préstamo {p['id_prestamo']}: Usuario {p['id_usuario']} tiene {p['cantidad']} de la herramienta {p['id_herramienta']}.")

def reporte_prestamos_vencidos():
    print("\n--- PRÉSTAMOS VENCIDOS ---")
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
    encontrados = False
    for p in prestamos:
        if p["estado"] == "activo" and p.get("fecha_estimada_devolucion", "Pendiente") != "Pendiente":
            if p["fecha_estimada_devolucion"] < fecha_actual:
                print(f"Alerta: El préstamo {p['id_prestamo']} del usuario {p['id_usuario']} está vencido. (Debió entregarse el {p['fecha_estimada_devolucion']})")
                encontrados = True
    if not encontrados:
        print("No hay préstamos vencidos en este momento.")

def historial_usuario(id_usuario):
    print(f"\n--- HISTORIAL DE PRÉSTAMOS (Usuario: {id_usuario}) ---")
    encontrados = False
    for p in prestamos:
        if str(p["id_usuario"]) == str(id_usuario):
            print(f"- Préstamo {p['id_prestamo']} | Herramienta ID: {p['id_herramienta']} | Cantidad: {p['cantidad']} | Estado: {p['estado']}")
            encontrados = True

    if not encontrados:
        print("Este usuario no ha realizado ninguna solicitud.")

def herramientas_mas_solicitadas():
    print("\n--- HERRAMIENTAS MÁS SOLICITADAS ---")
    conteo = {}
    for p in prestamos:
        id_herra = str(p["id_herramienta"])
        conteo[id_herra] = conteo.get(id_herra, 0) + p["cantidad"]
    if not conteo:
        print("No hay registros de préstamos aún.")
        return
    herramientas_ordenadas = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    for id_herra, total in herramientas_ordenadas:
        nombre_herramienta = "Desconocida"
        for h in herramientas:
            if str(h["id"]) == id_herra:
                nombre_herramienta = h["nombre"]
                break
        print(f"- {nombre_herramienta} (ID {id_herra}): {total} unidades solicitadas en total.")

def usuarios_mas_activos():
    print("\n--- USUARIOS CON MÁS PRÉSTAMOS ---")
    conteo = {}
    for p in prestamos:
        id_usu = str(p["id_usuario"])
        conteo[id_usu] = conteo.get(id_usu, 0) + p["cantidad"]
    if not conteo:
        print("No hay registros de préstamos aún.")
        return
    usuarios_ordenados = sorted(conteo.items(), key=lambda x: x[1], reverse=True)
    for id_usu, total in usuarios_ordenados:
        print(f"- Usuario ID {id_usu}: {total} herramientas solicitadas en total.")