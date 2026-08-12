import datetime
import os
DIRECTORIO_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_LOGS = os.path.join(DIRECTORIO_BASE, "registro_eventos.txt")
def registrar_log(mensaje):
    try:
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(RUTA_LOGS, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{fecha_hora}] {mensaje}\n")
    except Exception as e:
        print(f"Error al escribir en el registro de eventos: {e}")