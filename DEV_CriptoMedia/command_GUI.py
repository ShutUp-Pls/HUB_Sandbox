import tkinter as tk
from Encriptacion.encript import CryptoUtil
import datetime
import threading

class ComandoDesconocido(Exception):
    """ Excepción personalizada para comandos desconocidos. """
    def __init__(self):
        super().__init__("[] ERROR: Comando desconocido")

class Consola_GUI:
    """ Clase principal para la interfaz gráfica de la consola. """

    def __init__(self):
        self.cryptoU = CryptoUtil()
        self._setup_main_window()
        self._setup_text_area()
        self._setup_entry_and_button()

    def _setup_main_window(self):
        """ Configura la ventana principal. """
        self.root = tk.Tk()
        self.root.title("kithub v1.0")
        self.root.resizable(False, False)

    def _setup_text_area(self):
        """ Configura el área de texto y la barra de desplazamiento. """
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.text_frame, height=20, width=120, state=tk.DISABLED)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

    def _setup_entry_and_button(self):
        """ Configura la entrada de texto y el botón. """
        self.entry_frame = tk.Frame(self.root)
        self.entry_frame.pack(fill=tk.X)

        self.entry = tk.Entry(self.entry_frame, width=73)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.execute_command)

        self.execute_button = tk.Button(self.entry_frame, text="Ejecutar", command=self.execute_command)
        self.execute_button.pack(side=tk.RIGHT)

    def execute_command(self, event=None):
        """ Ejecuta un comando ingresado en la consola. """
        argumento = self.entry.get().split() if self.entry.get() else " "
        self._process_command(argumento)
        self.entry.delete(0, tk.END)

    def _process_command(self, argumento):
        """ Procesa el comando ingresado. """
        # Formateo y visualización del comando
        argumento_str = ' '.join(map(str, argumento))
        hora_actual = f"{datetime.datetime.now().strftime('[%H:%M:%S]:')}"
        mensaje_comando = f"{hora_actual} {argumento_str}"
        linea = "=" * len(mensaje_comando)

        self.message_feedback(linea)
        self.message_feedback(mensaje_comando)

        # Habilitar el área de texto para modificarla
        self.text_area.configure(state=tk.NORMAL)

        # Diccionario de funciones de comando
        command_functions = {
            "cryptoinfo": self.cryptoU.getinfo,
            "cryptopass": self.cryptoU.setpass,
            "cryptodir": self.cryptoU.setdir,
            "cryptoname": self.cryptoU.setarchivo,
            "cryptoencode": self.cryptoU.encriptar_archivos,
            "cryptodecode": self.cryptoU.desencriptar_archivos,
            "encode_delete": self.cryptoU.setencode_delete,
            "decode_delete": self.cryptoU.setdecode_delete
        }
        
        def _do_function():
            # Ejecución de funciones basada en el comando
            try: # ... (procesamiento de comandos)
                function = command_functions.get(argumento[0])
                if function:
                    n_param = function.__code__.co_argcount
                    if n_param == 2:
                        function(self.message_feedback)
                    elif n_param == 3:
                        try: function(argumento[1], self.message_feedback)
                        except IndexError as e: self.message_feedback(f"Faltan paramentros: {e}")
                        except Exception as e: self.message_feedback(f"Error al llamar funcion \"{argumento[0]}\": {e}")
                else: self.message_feedback(f"Comando \"{argumento[0]}\" desconocido.")
            except Exception as e: # ... (manejo de excepciones)
                self.message_feedback(f"Una Excepcion ha ocurrido:")
                self.message_feedback(f"{e}")
            finally:
                self.text_area.see(tk.END)
                self.text_area.configure(state=tk.DISABLED)
        thread = threading.Thread(target=_do_function)
        thread.start()

    def message_feedback(self, mensaje):
        """ Actualiza el área de texto con un nuevo mensaje de forma segura para hilos. """
        def _safe_update():
            self.text_area.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, f"{mensaje}\n")
            self.text_area.see(tk.END)
            self.text_area.config(state=tk.DISABLED)
            self.root.update()
        self.root.after(0, _safe_update)

    def launch_app(self):
        """ Inicia la aplicación. """
        self.root.mainloop()

# Creación y ejecución de la aplicación
app = Consola_GUI()
app.launch_app()