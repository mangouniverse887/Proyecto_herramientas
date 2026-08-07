PERMISOS = {
    "administrador": [
        "registrar_usuario",
        "actualizar_usuario",
        "eliminar_usuario",
        "gestionar_herramientas",
        "consultar_herramientas",
        "aprobar_solicitud"
    ],

    "residente": [
        "consultar_herramientas",
        "crear_solicitud"
    ]
}


def tiene_permiso(usuario, accion):
    if usuario is None:
        return False

    tipo_usuario = usuario.get("tipo_usuario", "").lower()

    if tipo_usuario not in PERMISOS:
        return False

    return accion in PERMISOS[tipo_usuario]


def puede_registrar_usuarios(usuario):
    return tiene_permiso(usuario, "registrar_usuario")


def puede_gestionar_herramientas(usuario):
    return tiene_permiso(usuario, "gestionar_herramientas")


def puede_consultar_herramientas(usuario):
    return tiene_permiso(usuario, "consultar_herramientas")


def puede_crear_solicitud(usuario):
    return tiene_permiso(usuario, "crear_solicitud")


def puede_aprobar_solicitud(usuario):
    return tiene_permiso(usuario, "aprobar_solicitud")
