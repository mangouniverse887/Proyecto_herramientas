import datetime
def registrar_log(mensaje):
    with open("registro_eventos.txt", "a") as archivo:
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{fecha_hora}] {mensaje}\n")