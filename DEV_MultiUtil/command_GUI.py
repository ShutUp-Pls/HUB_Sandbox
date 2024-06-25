import tkinter as tk
from key_creator import crear_hash
from encript import generar_clave_fernet, encriptar_archivos, desencriptar_archivos
import os
import datetime

class NoValidFolder(Exception):
    def __init__(self):
        super().__init__("Ruta de carpeta inválido...")

class Consola_GUI:
    def __init__(self):
        # Atributos de la app
        self.sesion_pass = None
        self.sesion_fernet = None

        self.encode_delete = False # Borrar archivos despues de codificar
        self.decode_delete = False # Borrar archivo despues de decodificar

        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("kithub v1.0")
        self.root.resizable(False, False)

        # Crear el contenedor para el área de texto y la barra de desplazamiento
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        # Crear el área de texto donde se mostrarán los mensajes
        self.text_area = tk.Text(self.text_frame, height=20, width=120, state=tk.DISABLED)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear y configurar la barra de desplazamiento
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configurar el área de texto para usar la barra de desplazamiento
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        # Crear un frame para la caja de texto y el botón
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(fill=tk.X)

        # Crear la caja de texto para ingresar los comandos
        self.entry = tk.Entry(self.entry_frame, width=73)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.execute_command)

        # Crear el botón para ejecutar comandos
        self.execute_button = tk.Button(self.entry_frame, text="Ejecutar", command=self.execute_command)
        self.execute_button.pack(side=tk.RIGHT)

    #Metodo que define los comandos de la consola
    def execute_command(self, event=None):
        argumento = self.entry.get().split() if self.entry.get() else " "
        self.text_area.configure(state=tk.NORMAL)  # Habilitar el área de texto para modificarla
        command_functions = {
            "setpass": self.comando_setpass,
            "setencode": self.comando_setencode,
            "setdecode": self.comando_setdecode,
            "encode": self.comando_encode,
            "decode": self.comando_decode,
            "getpass": self.comando_getpass,
            "getfernet": self.comando_getfernet,
            "getencode": self.comando_getencode,
            "getdecode": self.comando_getdecode
        }
        try:
            function = command_functions.get(argumento[0], self.comando_desconocido)
            function(argumento)
        except Exception as e: self.message_feedback(f"FAIL: {e}")
        finally:
            self.text_area.see(tk.END)
            self.text_area.configure(state=tk.DISABLED)
            self.entry.delete(0, tk.END)

    def comando_desconocido(self, argumento):
        self.message_feedback(f"Comando \'{argumento[0]}\' desconocido.")

    def comando_setpass(self, argumento):
        self.sesion_pass = crear_hash(argumento[1])
        self.sesion_fernet = generar_clave_fernet(self.sesion_pass)
        self.message_feedback("Hash de contraseña generado con éxito!")

    def comando_setencode(self, argumento):
        if argumento[1] == "delete":
            if argumento[2].lower() == "true": self.encode_delete = True
            elif argumento[2].lower() == "false": self.encode_delete = False
            else: self.message_feedback(f"Argumento \'{argumento[2]}\' desconocido.")
        else:
            self.message_feedback(f"Argumento \'{argumento[1]}\' desconocido.")

    def comando_setdecode(self, argumento):
        if argumento[1] == "delete":
            if argumento[2].lower() == "true": self.decode_delete = True
            elif argumento[2].lower() == "false": self.decode_delete = False
            else: self.message_feedback(f"Argumento \'{argumento[2]}\' desconocido.")
        else:
            self.message_feedback(f"Argumento \'{argumento[1]}\' desconocido.")

    def comando_encode(self, argumento):
        self.message_feedback(f"Encriptando contenido de {argumento[1]}")
        sesion_archv = [os.path.join(argumento[1], archivo) for archivo in os.listdir(argumento[1])]
        encriptar_archivos(self.sesion_fernet,
                           sesion_archv,
                           argumento[2],
                           callback=self.message_feedback)
        if self.encode_delete:
           for archv in sesion_archv:
               os.remove(archv)
        self.message_feedback(f"Encriptado correctamente! {argumento[1]}")
        
    def comando_decode(self, argumento):
        self.message_feedback(f"Desencriptando contenido de {argumento[1]}")
        sesion_folder = argumento[2]
        desencriptar_archivos(self.sesion_fernet,
                                sesion_folder,
                                argumento[1],
                                callback=self.message_feedback)
        if self.decode_delete: os.remove(argumento[1])
        self.message_feedback(f"Desencriptado correctamente! {argumento[1]}")
        
    def comando_getpass(self, argumento):
        self.message_feedback(f"Hash actual:\n<{self.sesion_pass}>")

    def comando_getfernet(self, argumento):
        self.message_feedback(f"Fernet actual:\n<{self.sesion_fernet}>")

    def comando_getencode(self, argumento):
        if argumento[1] == "delete":
            self.message_feedback(f"Borrar despues de codificar:\n<{self.encode_delete}>")
        else:
            self.message_feedback(f"Argumento \'{argumento[1]}\' desconocido.")

    def comando_getdecode(self, argumento):
        if argumento[1] == "delete":
            self.message_feedback(f"Borrar despues de decodificar:\n<{self.decode_delete}>")
        else:
            self.message_feedback(f"Argumento \'{argumento[1]}\' desconocido.")

    def message_feedback(self, mensaje):
        # Obtener la hora actual
        hora_actual = datetime.datetime.now()
        self.text_area.insert(tk.END, f"{hora_actual.strftime("[%H:%M:%S]:")} {mensaje}\n")

    def launch_app(self): self.root.mainloop()

app = Consola_GUI()
app.launch_app()
