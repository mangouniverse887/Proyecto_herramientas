import consultas_reportes
import usuarios
import Herramientas_p
import prestamos
import usuarios

AZUL = "\033[34m"
VERDE = "\033[32m"
ROJO = "\033[31m"
AMARILLO = "\033[33m"
CELESTE = "\033[36m"
MORADO = "\033[35m"
RESET = "\033[0m"

def menu_reportes():
    while True:
        print(f"\n{MORADO}--- MENÚ DE REPORTES ---{RESET}")
        print("1. Herramientas con stock bajo")
        print("2. Préstamos activos")
        print("3. Préstamos vencidos")
        print("4. Historial de un usuario")
        print("5. Herramientas más solicitadas")
        print("6. Usuarioas con más préstamos")
        print(f"{AMARILLO}7. Lista negra de usuarios (Penalizaciones){RESET}")
        print(f"{ROJO}8. Volver al menú principal{RESET}")
        opcion = input("\nElige un reporte(1-8): ")
        if opcion == "1":
            consultas_reportes.reporte_stock_bajo()
        elif opcion == "2":
            consultas_reportes.reporte_prestamos_activos()
        elif opcion == "3":
            consultas_reportes.reporte_prestamos_vencidos()
        elif opcion == "4":
            id_usu = input("Ingrese el ID del usuario: ")
            consultas_reportes.historial_usuario(id_usu)
        elif opcion == "5":
            consultas_reportes.herramientas_mas_solicitadas()
        elif opcion == "6":
            consultas_reportes.usuarios_mas_activos()
        elif opcion == "7":
            consultas_reportes.resporte_lista_negra()
        elif opcion == "8":
            break
        else:
            print("Opción inválida. Intente de nuevo.")

def gestionar_usuarios():
    while True:
        print(f"{AZUL}1. Crear | 2. Listar | 3. Actualizar | 4. Eliminar {RESET}|{ROJO} 5. Volver al menú{RESET}")
        sub_op = input("Elige acción: ")
        if sub_op == "1":
            id_u = input("ID: ")
            nom = input("Nombres: ")
            ape = input("Apellidos: ")
            tel = input("Teléfono: ")
            dire = input("Dirección: ")
            t_usu = input("Tipo (residente/administrador): ")
            if usuarios.crear_usuario(id_u, nom, ape, tel, dire, t_usu):
                print(f"{VERDE}Usuario creado con éxito.{RESET}")
            else:
                print(f"{ROJO}Error: Datos inválidos o el usuario ya existe.{RESET}")
        elif sub_op == "2":
            lista = usuarios.listar_usuarios()
            for u in lista:
                print(f"- ID {u['id']}: {u['nombres']} {u['apellidos']} (Rol: {u['tipo_usuario']})")
        elif sub_op == "3":
            id_u = input("ID a actualizar: ")
            print("Deje el campo vacío y presione Enter si NO desea modificarlo: ")
            nuevo_nom = input("Nuevo nombre: ")
            nuevo_ape = input("Nuevo Apellido: ")
            nuevo_tel = input("Nuevo teléfono: ")
            nuevo_dir = input("Nueva Dirección: ")
            nuevo_tipo = input("Nuevo tipo (residente/admin): ")
            usuarios.actualizar_usuario(
                id_u,
                nombres=nuevo_nom if nuevo_nom != "" else None,
                apellidos=nuevo_ape if nuevo_ape != "" else None,
                telefono=nuevo_tel if nuevo_tel != "" else None,
                direccion=nuevo_dir if nuevo_dir != "" else None,
                tipo_usuario=nuevo_tipo if nuevo_tipo != "" else None
            )
            print(f"{VERDE}Proceso de actualización finalizado.{RESET}")
        elif sub_op == "4":
            id_u = input("ID a Eliminar: ")
            if usuarios.eliminar_usuario(id_u):
                print("Usuario eliminado del sistema.")
            else:
                print(f"{ROJO}Error al eliminar (Usuario no encontrado){RESET}")
        elif sub_op == "5":
            break

def gestionar_herramientas():
    while True:
        print(f"\n{VERDE}1. Crear | 2. Listar | 3. Buscar | 4. Actualizar | 5. Inactivar {RESET} | 6. Enviar a Reparación | 7. Retornar de Reparación |{ROJO} 8. Volver al menú{RESET}")
        sub_op = input("Elige una acción: ")
        if sub_op == "1":
            Herramientas_p.crear_herramienta()
        elif sub_op == "2":
            Herramientas_p.listar_herramientas()
        elif sub_op == "3":
            Herramientas_p.consultar_herramienta()
        elif sub_op == "4":
             Herramientas_p.actualizar_herramienta()
        elif sub_op == "5":
            Herramientas_p.inactivar_herramienta()
        elif sub_op == "6":
            Herramientas_p.enviar_reparacion()
        elif sub_op == "7":
            Herramientas_p.retornar_reparacion()
        elif sub_op == "8":
            break

def prestamos_aprobar_devolver():
    while True:
        print(f"\n{AMARILLO}1. Aprobar Solicitud de Préstamo | 2. Registrar Devolución | 3. Préstamos Pendientes {RESET}|{ROJO} 4. Volver al menú{RESET}")
        sub_op = input("Elige acción: ")
        if sub_op == "1":
            id_p = input("Ingrese el ID de la solicitud (ej. P1): ")
            prestamos.aprobar_prestamo(id_p)
        elif sub_op == "2":
            id_p = input("Ingrese el ID del préstamo a deolver (ej. P1): ")
            prestamos.registrar_devolucion(id_p)
        elif sub_op == "3":
            print("\n---SOLICITUDES DE PRÉSTAMO PENDIENTES ---")
            pendientes = [p for p in prestamos.prestamos if p["estado"] == "pendiente"]
            if len(pendientes) == 0:
                print("No hay solicitudes pendientes de aprobación en este momento.")
                return
            for p in pendientes:
                datos_usuario = usuarios.buscar_usuario(p["id_usuario"])
                nombre_usuario = f"{datos_usuario['nombres']} {datos_usuario['apellidos']}" if datos_usuario else "Usuario desconocido"
                print(f"-"*40)
                print(f"ID Solicitud: {p['id_prestamo']}")
                print(f"Usuario: {nombre_usuario} (ID: {p['id_usuario']})")
                print(f"ID Herramienta Solicitada: {p['id_herramienta']}")
                print(f"Cantidad: {p['cantidad']}")
                print(f"Fecha de solicitud: {p['fecha_inicio']}")
        elif sub_op == "4":
            break