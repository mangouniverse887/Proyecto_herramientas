# Manual de Usuario: Sistema Comunitario de Préstamo de Herramientas

## 1. Introducción al Sistema
El Sistema Comunitario de Préstamo de Herramientas es una plataforma de consola diseñada para organizar el inventario compartido de una comunidad y facilitar el control de usuarios, solicitudes, préstamos, devoluciones y reportes. Toda la información gestionada (usuarios, préstamos y herramientas) se guarda de forma segura y persistente mediante archivos '.json' locales.
> **⚠️ IMPORTANTE - PRIMER INGRESO:** Para acceder al sistema por primera vez, utilice el usuario base con permisos de administrador ingresando el ID **123456789**. Por motivos de seguridad, se recomienda enfáticamente crear sus propios usuarios administradores en el sistema y, posteriormente, **eliminar este usuario base**.

---

## 2. Acceso y Autenticación
* Para iniciar el programa, el sistema solicitará el ingreso mediante un número de ID (cédula).
* Dependiendo del rol asignado en la base de datos, el sistema dirigirá automáticamente al usuario al **Menú de Administrador** o al **Menú de Residente**.
* Si se ingresa un ID que no figura en los registros, el acceso será denegado y se sugerirá contactar a un administrador.

---

## 3. Guía para el Administrador
El perfil de Administrador cuenta con permisos globales para gestionar la operatividad del sistema a través de cuatro módulos principales.

### A. Gestión de Usuarios
- **Crear:** Permite registrar nuevos miembros solicitando ID, nombres, apellidos, teléfono, dirección y rol (administrador o residente).
- **Listar:** Muestra en pantalla a todos los usuarios registrados con su respectivo rol.
- **Actualizar:** Permite modificar datos específicos de un usuario; los campos que se dejen en blanco conservarán su información original.
- **Eliminar:** Borra permanentemente a un usuario del sistema mediante su ID.

### B. Gestión de Herramientas
- **Inventario Básico:** El sistema permite registrar nuevas herramientas, actualizar sus características, buscarlas por ID o listarlas en su totalidad para visualizar su stock, estado y valor estimado.
- **Inactivar:** Cambia el estado de una herramienta a "fuera de servicio" sin eliminarla del registro.
- **Sistema de Reparaciones:** Se pueden enviar unidades específicas al taller (descontándolas del stock disponible) y retornarlas posteriormente para que regresen al estado "activa". Si el stock de una herramienta llega a cero, su estado cambiará automáticamente a "agotado".

### C. Control de Préstamos
- **Préstamos Pendientes:** Lista todas las solicitudes de los residentes que están a la espera de aprobación.
- **Aprobar Solicitud:** Confirma el préstamo de una herramienta, verificando que haya stock suficiente, y actualiza el estado a "activo".
- **Registrar Devolución:** Finaliza un préstamo y restaura el stock de la herramienta. Durante este proceso, el administrador debe evaluar las condiciones de entrega; si la herramienta se devuelve dañada, incompleta o tarde, el sistema añadirá automáticamente una penalización al perfil del usuario.

### D. Reportes del Sistema
- **Stock e Inventario:** Genera alertas de herramientas con menos de 3 unidades disponibles o identifica las herramientas más solicitadas por la comunidad.
- **Estado de Préstamos:** Permite visualizar todos los préstamos actualmente activos y resalta aquellos que se encuentran vencidos comparando la fecha de devolución con la fecha actual.
- **Auditoría de Usuarios:** Incluye la visualización del historial completo de un residente, la lista de los usuarios con más actividad de préstamos, y una **Lista Negra** que expone a los residentes ordenados por su cantidad de penalizaciones acumuladas.

---

## 4. Guía para el Residente
El perfil de Residente está enfocado en la consulta y el autoservicio, limitando las acciones para proteger la integridad de los datos.

### A. Consultar Catálogo de Herramientas
- **Listar todas:** Muestra el catálogo completo de la comunidad indicando claramente cuántas unidades de cada herramienta están disponibles para uso inmediato.
- **Buscar específica:** Permite ingresar el ID de una herramienta puntual para conocer sus detalles y disponibilidad sin tener que leer todo el catálogo.

### B. Solicitar un Préstamo
- El residente debe ingresar el ID de la herramienta que necesita y la cantidad de unidades requeridas (en números enteros).
- El sistema validará en tiempo real si la herramienta existe, si se encuentra en estado "activa", y si hay stock suficiente para cubrir la cantidad pedida. 
- Si la validación es exitosa, la solicitud quedará en estado "pendiente" hasta que un administrador la apruebe.

### C. Ver Historial
- Muestra un reporte personalizado donde el residente puede auditar todos los préstamos que ha solicitado y el estado actual de cada uno.
- En la cabecera de este historial, el sistema alertará de manera visible si el usuario tiene un historial limpio o si cuenta con penalizaciones acumuladas por entregas defectuosas.
