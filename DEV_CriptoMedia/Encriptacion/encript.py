from cryptography.fernet import Fernet
import hashlib
import os
import base64

class FernetFail(Exception):
    def __init__(self):
        super().__init__("Codigo para desencriptar no coindice.")

class CarpetaVaciaFail(Exception):
    def __init__(self):
        super().__init__("Carpeta de encriptación vacía.")

class CodigoInvalidoFail(Exception):
    def __init__(self):
        super().__init__("Codigo de encriptación invalido.")

class DireccionInvalidaFail(Exception):
    def __init__(self):
        super().__init__("Direccion de Carpeta invalido.")

class ArchivoFail(Exception):
    def __init__(self):
        super().__init__("Direccion de Archivo invalido.")

class ArchivorRepetidoFail(Exception):
    def __init__(self):
        super().__init__("No se puede encriptar el archivo resultado.\nArchivo a encriptar tiene el nombre del resultado.")

class CryptoUtil:

    def __init__(self):
        # Atributos de la app
        self.sesion_pass = None
        self.sesion_fernet = None

        self.sesion_carpeta = None
        self.sesion_carpeta_archivos = None

        self.sesion_archivo_nombre = None
        self.sesion_archivo_ruta = None

        self.encode_delete = False # Borrar archivos despues de codificar
        self.decode_delete = False # Borrar archivo despues de decodificar

        self.progreso_actual = 0

    # Función para generar una clave Fernet a partir del hash de la contraseña dada
    def generar_clave_fernet(self, *args):
        # Generar clave a partir del hash almacenado
        hash_bytes = hashlib.sha256(self.sesion_pass.strip().encode()).digest()
        clave_fernet = base64.urlsafe_b64encode(hash_bytes[:32])
        self.sesion_fernet = clave_fernet
        # return clave_fernet

    def getinfo(self, callback, *args):
        self.refresh_info()
        # Definir los callbacks en una lista
        callbacks = [
            lambda: callback(f"- Codigos de Encriptacion...\nHash: {self.sesion_pass}\nFernet: {self.sesion_fernet}"),
            lambda: callback(f"- Carpeta a Encriptar...\nDirección apuntada: {self.sesion_carpeta}\nArchivos apuntados: {('\n'+'\n'.join(self.sesion_carpeta_archivos)) if self.sesion_carpeta_archivos else 'None'}"),
            lambda: callback(f"- Archivo de Salida...\nNombre del archivo: {self.sesion_archivo_nombre}\nRuta del Archivo: {self.sesion_archivo_ruta}"),
            lambda: callback(f"- Encode/Decode Delete...\nBorrar archivos despues de codificar: {self.encode_delete}\nBorrar archivo despues de decodificar: {self.decode_delete}")
        ]

        # Ejecutar el callback específico si se proporciona un número en args
        if args:
            for arg in args:
                if 0 <= arg < len(callbacks):
                    callbacks[arg]()
                else:
                    for cb in callbacks: cb()
        else:
            # Si no se proporciona ningún número, ejecutar todos los callbacks
            for cb in callbacks: cb()

    def refresh_info(self, callback=None, *args):
        self.setdir(self.sesion_carpeta, callback)
        self.setarchivo(self.sesion_archivo_nombre, callback)

    def get_progress(self):
        # Devuelve el progreso actual como un porcentaje
        return self.progreso_actual

    # Setters
    def setpass(self, passwd, callback=None, *args):
        if passwd != None:
            hash_objeto = hashlib.sha256(passwd.encode())
            self.sesion_pass = hash_objeto.hexdigest()
            self.generar_clave_fernet()
        else:
            self.sesion_pass = None
            self.sesion_fernet = None
        if callback: self.getinfo(callback, 0)

    def setdir(self, direccion, callback=None, *args):
        if direccion != None:
            self.sesion_carpeta = direccion
            try:
                self.sesion_carpeta_archivos = [os.path.join(direccion, archivo) for archivo in os.listdir(direccion)]
            except Exception as e:
                if callback: callback(f"Direccion invalida: {e}")
        else:
            self.sesion_carpeta = None
            self.sesion_carpeta_archivos = None
        if callback: self.getinfo(callback, 1)

    def setarchivo(self, nombre_archivo, callback=None, *args):
        if nombre_archivo != None:
            self.sesion_archivo_nombre = nombre_archivo
            self.sesion_archivo_ruta = self.sesion_carpeta + '\\' + self.sesion_archivo_nombre
        else:
            self.sesion_archivo_nombre = None
            self.sesion_archivo_ruta = None
        if callback: self.getinfo(callback, 2)

    def setencode_delete(self, bool_delete, callback=None, *args):
        if bool_delete.lower() == "true": self.encode_delete = True
        elif bool_delete.lower() == "false": self.encode_delete = False
        if callback: self.getinfo(callback, 3)

    def setdecode_delete(self, bool_delete, callback=None, *args):
        if bool_delete.lower() == "true": self.decode_delete = True
        elif bool_delete.lower() == "false": self.decode_delete = False
        if callback: self.getinfo(callback, 3)

    # Función para encriptar archivos
    def encriptar_archivos(self, callback=None, *args):
        self.progreso_actual = 0
        self.refresh_info()
        contenido_total = b''

        try:
            fernet = Fernet(self.sesion_fernet)
            self.progreso_actual = 3
        except Exception:
            self.progreso_actual = 0
            raise CodigoInvalidoFail
        try:
            cantidad_de_archivos = len(self.sesion_carpeta_archivos)
            self.progreso_actual = 6
        except:
            self.progreso_actual = 0
            raise DireccionInvalidaFail
        try:
            aumento_de_progreso = 60/cantidad_de_archivos
            self.progreso_actual = 10
        except:
            self.progreso_actual = 0
            raise CarpetaVaciaFail

        for ruta in self.sesion_carpeta_archivos:
            if ruta == self.sesion_archivo_ruta:
                self.progreso_actual = 0
                raise ArchivorRepetidoFail
            if callback: callback(f"Encriptando: {ruta}")
            with open(ruta, 'rb') as archivo:
                contenido = archivo.read()
                nombre_archivo = os.path.basename(ruta).encode()
                contenido_total += nombre_archivo + b'\n' + contenido + b'\n---DELIMITADOR---\n'
            self.progreso_actual += aumento_de_progreso

        contenido_encriptado = fernet.encrypt(contenido_total)
        self.progreso_actual = 75
        try:
            with open(self.sesion_archivo_ruta, 'wb') as archivo_salida:
                archivo_salida.write(contenido_encriptado)
            self.progreso_actual = 80
        except:
            self.progreso_actual = 0
            raise ArchivoFail
        

        if self.encode_delete:
            for ruta in self.sesion_carpeta_archivos:
                os.remove(ruta)
                self.progreso_actual += self.progreso_actual + (20/len(self.sesion_carpeta_archivos))
            if callback: callback(f"Removiendo: {ruta}")

        if callback: callback(f"Encriptacion exitosa!")
        self.progreso_actual = 100
        self.refresh_info()

    # Función para desencriptar archivos
    def desencriptar_archivos(self, callback=None, *args):
        self.progreso_actual = 0
        self.refresh_info()

        try: fernet = Fernet(self.sesion_fernet)
        except Exception:
            self.progreso_actual = 0
            raise CodigoInvalidoFail
        self.progreso_actual = 5

        with open(self.sesion_archivo_ruta, 'rb') as archivo:
            contenido_encriptado = archivo.read()
        self.progreso_actual = 15

        try:
            contenido_desencriptado = fernet.decrypt(contenido_encriptado)
            self.progreso_actual = 20
        except Exception:
            self.progreso_actual = 0
            raise FernetFail
        archivos_separados = contenido_desencriptado.split(b'\n---DELIMITADOR---\n')
        self.progreso_actual = 25

        cantidad_de_archivos = len(archivos_separados)
        aumento_de_progreso = 65/cantidad_de_archivos
        for contenido_archivo in archivos_separados:
            if contenido_archivo:
                nombre_archivo, contenido = contenido_archivo.split(b'\n', 1)
                ruta = os.path.join(self.sesion_carpeta, nombre_archivo.decode())
                if callback: callback(f"Desencriptando: {ruta}")

                with open(ruta, 'wb') as archivo:
                    archivo.write(contenido)
            self.progreso_actual += aumento_de_progreso

        if self.decode_delete:
            os.remove(self.sesion_archivo_ruta)
            if callback: callback(f"Removiendo: {self.sesion_archivo_ruta}")

        if callback: callback(f"Desencriptacion exitosa!")
        self.progreso_actual = 100
        self.refresh_info()