from cryptography.fernet import Fernet
import hashlib
import os
import base64

class FernetFail(Exception):
    def __init__(self):
        super().__init__("Fernet key no coincide")

# Función para generar una clave Fernet a partir del hash de la contraseña correcta
def generar_clave_fernet(seed:str):
    # Generar clave a partir del hash almacenado
    hash_bytes = hashlib.sha256(seed.strip().encode()).digest()
    clave_fernet = base64.urlsafe_b64encode(hash_bytes[:32])
    return clave_fernet

# Función para encriptar archivos
def encriptar_archivos(clave_fernet, rutas_archivos, archivo_salida, callback=None):
    fernet = Fernet(clave_fernet)

    contenido_total = b''
    for ruta in rutas_archivos:
        if callback:
            callback(f"Encriptando archivo:{ruta}")
        with open(ruta, 'rb') as archivo:
            contenido = archivo.read()
            nombre_archivo = os.path.basename(ruta).encode()
            contenido_total += nombre_archivo + b'\n' + contenido + b'\n---DELIMITADOR---\n'

    contenido_encriptado = fernet.encrypt(contenido_total)
    
    with open(archivo_salida, 'wb') as archivo_salida:
        archivo_salida.write(contenido_encriptado)

# Función para desencriptar archivos
def desencriptar_archivos(clave_fernet, ruta_carpeta, archivo_entrada, callback=None):
    fernet = Fernet(clave_fernet)

    with open(archivo_entrada, 'rb') as archivo:
        contenido_encriptado = archivo.read()
    
    try: contenido_desencriptado = fernet.decrypt(contenido_encriptado)
    except Exception: raise FernetFail
    archivos_separados = contenido_desencriptado.split(b'\n---DELIMITADOR---\n')

    for contenido_archivo in archivos_separados:
        if contenido_archivo:
            nombre_archivo, contenido = contenido_archivo.split(b'\n', 1)
            ruta = os.path.join(ruta_carpeta, nombre_archivo.decode())
            if callback:
                callback(f"Desencriptando archivo:{ruta}")
            with open(ruta, 'wb') as archivo:
                archivo.write(contenido)