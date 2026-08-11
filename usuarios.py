import json
from pathlib import Path


ARCHIVO = Path(__file__).with_name("usuarios.json")
TIPOS_USUARIO = ("residente", "administrador")
usuarios = []


def cargar_usuarios():
    """Carga los usuarios guardados; si no hay archivo, inicia una lista vacía."""
    global usuarios

    if not ARCHIVO.exists():
        usuarios = []
        return

    try:
        with ARCHIVO.open("r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        usuarios = datos if isinstance(datos, list) else []
    except (OSError, json.JSONDecodeError):
        print("Aviso: no fue posible leer usuarios.json.")
        usuarios = []


def guardar_usuarios():
    """Guarda todos los usuarios en formato JSON."""
    try:
        with ARCHIVO.open("w", encoding="utf-8") as archivo:
            json.dump(usuarios, archivo, indent=4, ensure_ascii=False)
        return True
    except OSError:
        print("Error: no fue posible guardar los usuarios.")
        return False


def leer_id(mensaje="ID: ", permitir_vacio=False):
    while True:
        entrada = input(mensaje).strip()
        if permitir_vacio and entrada == "":
            return None
        if entrada.isdigit() and int(entrada) > 0:
            return int(entrada)
        print("El ID debe ser un número entero mayor que cero.")


def leer_texto(mensaje, permitir_vacio=False):
    while True:
        texto = input(mensaje).strip()
        if texto or permitir_vacio:
            return texto
        print("Este campo no puede quedar vacío.")


def leer_telefono(mensaje="Teléfono: ", permitir_vacio=False):
    while True:
        telefono = input(mensaje).strip()
        if permitir_vacio and telefono == "":
            return ""

        telefono_limpio = telefono.replace(" ", "").replace("-", "")
        if telefono_limpio.isdigit() and 7 <= len(telefono_limpio) <= 15:
            return telefono
        print("Ingrese un teléfono válido de 7 a 15 dígitos.")


def leer_tipo_usuario(permitir_vacio=False):
    while True:
        print("Tipos: 1. Residente | 2. Administrador")
        opcion = input("Seleccione el tipo de usuario: ").strip()

        if permitir_vacio and opcion == "":
            return None
        if opcion == "1":
            return "residente"
        if opcion == "2":
            return "administrador"
        print("Opción inválida.")


def buscar_usuario(id_usuario):
    for usuario in usuarios:
        if str(usuario["id"]) == str(id_usuario):
            return usuario
    return None


def crear_usuario(id_usuario, nombres, apellidos, telefono, direccion,
                  tipo_usuario):
    """Crea un usuario desde otro módulo y devuelve True si tuvo éxito."""
    if buscar_usuario(id_usuario) is not None:
        return False

    nombres = str(nombres).strip()
    apellidos = str(apellidos).strip()
    telefono = str(telefono).strip()
    direccion = str(direccion).strip()
    tipo_usuario = str(tipo_usuario).strip().lower()

    if not nombres or not apellidos or not telefono or not direccion:
        return False
    if tipo_usuario not in TIPOS_USUARIO:
        return False

    nuevo_usuario = {
        "id": id_usuario,
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "direccion": direccion,
        "tipo_usuario": tipo_usuario,
    }

    usuarios.append(nuevo_usuario)
    if guardar_usuarios():
        return True

    usuarios.remove(nuevo_usuario)
    return False


def listar_usuarios():
    """Devuelve una copia para evitar cambios accidentales desde otros módulos."""
    return usuarios.copy()


def actualizar_usuario(id_usuario, nombres=None, apellidos=None,
                       telefono=None, direccion=None, tipo_usuario=None):
    usuario = buscar_usuario(id_usuario)
    if usuario is None:
        return False

    cambios = {}
    valores = {
        "nombres": nombres,
        "apellidos": apellidos,
        "telefono": telefono,
        "direccion": direccion,
    }

    for campo, valor in valores.items():
        if valor is not None:
            valor = str(valor).strip()
            if not valor:
                return False
            cambios[campo] = valor

    if tipo_usuario is not None:
        tipo_usuario = str(tipo_usuario).strip().lower()
        if tipo_usuario not in TIPOS_USUARIO:
            return False
        cambios["tipo_usuario"] = tipo_usuario

    usuario.update(cambios)
    return guardar_usuarios()


def eliminar_usuario(id_usuario):
    usuario = buscar_usuario(id_usuario)
    if usuario is None:
        return False

    usuarios.remove(usuario)
    if guardar_usuarios():
        return True

    usuarios.append(usuario)
    return False


def mostrar_usuario(usuario):
    print("-" * 42)
    print(f'ID: {usuario["id"]}')
    print(f'Nombre: {usuario["nombres"]} {usuario["apellidos"]}')
    print(f'Teléfono: {usuario["telefono"]}')
    print(f'Dirección: {usuario["direccion"]}')
    print(f'Tipo de usuario: {usuario["tipo_usuario"]}')


def registrar_usuario_menu():
    print("\n--- REGISTRAR USUARIO ---")
    id_usuario = leer_id()

    if buscar_usuario(id_usuario) is not None:
        print("Ya existe un usuario con ese ID.")
        return

    nombres = leer_texto("Nombres: ")
    apellidos = leer_texto("Apellidos: ")
    telefono = leer_telefono()
    direccion = leer_texto("Dirección: ")
    tipo_usuario = leer_tipo_usuario()

    if crear_usuario(
        id_usuario, nombres, apellidos, telefono, direccion, tipo_usuario
    ):
        print("Usuario registrado correctamente.")
    else:
        print("No fue posible registrar el usuario.")


def listar_usuarios_menu():
    print("\n--- LISTA DE USUARIOS ---")
    if not usuarios:
        print("No hay usuarios registrados.")
        return

    for usuario in usuarios:
        mostrar_usuario(usuario)


def buscar_usuario_menu():
    print("\n--- BUSCAR USUARIO ---")
    usuario = buscar_usuario(leer_id("Ingrese el ID: "))

    if usuario is None:
        print("No se encontró el usuario.")
        return
    mostrar_usuario(usuario)


def actualizar_usuario_menu():
    print("\n--- ACTUALIZAR USUARIO ---")
    id_usuario = leer_id("Ingrese el ID: ")
    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        print("No se encontró el usuario.")
        return

    print("Presione Enter para conservar el valor actual.")
    nombres = leer_texto(
        f'Nombres [{usuario["nombres"]}]: ', permitir_vacio=True
    )
    apellidos = leer_texto(
        f'Apellidos [{usuario["apellidos"]}]: ', permitir_vacio=True
    )
    telefono = leer_telefono(
        f'Teléfono [{usuario["telefono"]}]: ', permitir_vacio=True
    )
    direccion = leer_texto(
        f'Dirección [{usuario["direccion"]}]: ', permitir_vacio=True
    )
    tipo_usuario = leer_tipo_usuario(permitir_vacio=True)

    resultado = actualizar_usuario(
        id_usuario,
        nombres=nombres or None,
        apellidos=apellidos or None,
        telefono=telefono or None,
        direccion=direccion or None,
        tipo_usuario=tipo_usuario,
    )
    print("Usuario actualizado correctamente." if resultado
          else "No fue posible actualizar el usuario.")


def eliminar_usuario_menu():
    print("\n--- ELIMINAR USUARIO ---")
    id_usuario = leer_id("Ingrese el ID: ")
    usuario = buscar_usuario(id_usuario)

    if usuario is None:
        print("No se encontró el usuario.")
        return

    mostrar_usuario(usuario)
    confirmar = input("¿Confirma la eliminación? (s/n): ").strip().lower()
    if confirmar != "s":
        print("Operación cancelada.")
        return

    if eliminar_usuario(id_usuario):
        print("Usuario eliminado correctamente.")
    else:
        print("No fue posible eliminar el usuario.")


def menu_usuarios():
    cargar_usuarios()

    while True:
        print("\n=== GESTIÓN DE USUARIOS ===")
        print("1. Registrar usuario")
        print("2. Listar usuarios")
        print("3. Buscar usuario")
        print("4. Actualizar usuario")
        print("5. Eliminar usuario")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_usuario_menu()
        elif opcion == "2":
            listar_usuarios_menu()
        elif opcion == "3":
            buscar_usuario_menu()
        elif opcion == "4":
            actualizar_usuario_menu()
        elif opcion == "5":
            eliminar_usuario_menu()
        elif opcion == "0":
            print("Programa finalizado.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu_usuarios()
