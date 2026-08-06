from mock_data import herramientas, prestamos

def reporte_stock_bajo():
    print("\n--- HERRAMIENTAS CON STOCK BAJO (menos de 3) ---")
    encontradas = False
    for h in herramientas:
        if h["cantidad_disponible"] < 3:
            print(f"- {h['nombre']} (ID: {h['id']}): Quedan {h['cantidad_disponible']} unideades.")
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
            