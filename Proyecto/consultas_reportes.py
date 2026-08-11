from prestamos import prestamos
from Herramientas_p import herramientas
import datetime
import usuarios

AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CELESTE = "\033[36m"
MORADO = "\033[35m"
RESET = "\033[0m"

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
    usuario = usuarios.buscar_usuario(id_usuario)
    if usuario:
        faltas = usuario.get("penalizaciones", 0)
        if faltas > 0:
            print(f"{ROJO}ATENCIÓN: Este usuario tiene {faltas} penalización(es) por mal comportamiento{RESET}")
        else:
            print(f"{VERDE}Usuario con historial limpio (0 penalizaciones){RESET}")
    else:
        print("Usuario no encontrado en la base de datos.")
    encontrados = False
    for p in prestamos:
        if str(p["id_usuario"]) == str(id_usuario):
            print(f"- Préstamo {p['id_prestamo']} | Herramienta ID: {p['id_herramienta']} | Cantidad: {p['cantidad']} | Estado: {p['estado']} | Fecha: {p['fecha_inicio']}")
            encontrados = True

    if not encontrados:
        print("Este usuario no ha realizado ninguna solicitud.")

def resporte_lista_negra():
    print(f"\n{ROJO}--- LISTA NEGRA DE USUARIOS (Penalizaciones) ---{RESET}")
    lista_usuarios = usuarios.listar_usuarios()
    usuarios_penalizados = [u for u in lista_usuarios if u.get("penalizaciones", 0) > 0]
    usuarios_penalizados.sort(key=lambda x: x.get("penalizaciones", 0), reverse=True)
    if len(usuarios_penalizados) == 0:
        print(f"{VERDE}Todos los usuarios tienen un historial limpio.")
        return
    for u in usuarios_penalizados:
        faltas = u.get("penalizaciones", 0)
        print(f"ID: {u['id']} | Nombre: {u['nombres']} {u['apellidos']} |{AMARILLO} Faltas: {faltas}{RESET}")
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