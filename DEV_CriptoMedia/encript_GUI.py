import threading
import traceback
import os
import sys

import tkinter as tk
import tkinter.ttk as ttk

from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

from Encriptacion.encript import CryptoUtil

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y almacena el path en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

CRYPTO = CryptoUtil()
ICON_PATH = resource_path('DEV_CriptoMedia\\Media\\logo.ico')

# Función para actualizar la entrada de texto con la carpeta seleccionada
def select_directory():
    folder_selected = filedialog.askdirectory()
    dire_input_entry.delete(0, tk.END)
    dire_input_entry.insert(0, folder_selected)
    print(folder_selected)

# Esta función deseleccionará cualquier entrada de texto al hacer clic en cualquier parte de la ventana que no sea una entrada.
def deselect_entry(event):
    widget = event.widget
    if not isinstance(widget, tk.Entry):
        root.focus()

# Actualizar Dirección
def update_dir(event=None, *args):
    CRYPTO.setdir(dir_var.get())

# Actualizar Codigo
def update_pass(event=None, *args):
    CRYPTO.setpass(pass_var.get())

# Actualizar Nombre
def update_name(event=None, *args):
    CRYPTO.setarchivo(name_var.get())

def on_init():
    # Deshabilitar botones
    encript_button.config(state=tk.DISABLED)
    desencript_button.config(state=tk.DISABLED)

def monitor_thread(thread):
    progress = CRYPTO.get_progress()
    progress_bar["value"] = progress
    if thread.is_alive():
        root.after(100, lambda: monitor_thread(thread))
    else:
        encript_button.config(state=tk.NORMAL)
        desencript_button.config(state=tk.NORMAL)
        CRYPTO.progreso_actual = 0
        progress_bar["value"] = CRYPTO.progreso_actual

def handle_exception_in_thread(e):
    # Imprimir el rastreo completo en la consola
    print(f"Excepción en el hilo: {e}")
    traceback.print_exc()

    # Mostrar solo el mensaje de error en el cuadro de diálogo
    messagebox.showerror("Error en el hilo", str(e))

def encript_thread_target():
    try:
        CRYPTO.encriptar_archivos()
        messagebox.showinfo("Finalizado", "¡Encriptación exitosa!")
    except Exception as e:
        # Pasar la excepción al hilo principal
        handle_exception_in_thread(e)

def desencript_thread_target():
    try:
        CRYPTO.desencriptar_archivos()
        messagebox.showinfo("Finalizado", "¡Desencriptación exitosa!")
    except Exception as e:
        # Pasar la excepción al hilo principal
        handle_exception_in_thread(e)

def encrypt_action():
    try:
        on_init()
        thread = threading.Thread(target=encript_thread_target,)
        thread.start()
        monitor_thread(thread)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt_action():
    try:
        on_init()
        thread = threading.Thread(target=desencript_thread_target,)
        thread.start()
        monitor_thread(thread)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Acciones para el menu
def actualizar_estado():
    CRYPTO.setencode_delete(str(encode_delete.get()))
    CRYPTO.setdecode_delete(str(decode_delete.get()))

# Creación de la ventana principal
root = tk.Tk()
root.title("Encriptar/Desencriptar GUI")
root.resizable(False, False)
root.iconbitmap(ICON_PATH)

# Configuración del grid
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)
root.bind('<Button-1>', deselect_entry)

#Frame para el paddle
frame = tk.Frame()
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=0)
frame.grid_columnconfigure(0, weight=0)
frame.grid(row=0, column=0, padx=10, pady=10)

# Crear variables para el menú
encode_delete = tk.BooleanVar(value=True)
decode_delete = tk.BooleanVar(value=True)
CRYPTO.setencode_delete(str(encode_delete.get()))
CRYPTO.setdecode_delete(str(decode_delete.get()))

# Crear menú
menu_principal = tk.Menu(root)
root.config(menu=menu_principal)

# Crear menú de opciones
menu_opciones = tk.Menu(menu_principal, tearoff=0)
menu_principal.add_cascade(label="Parametros", menu=menu_opciones)

# Añadir opciones al menú
menu_opciones.add_checkbutton(label="Borrar al codificar", onvalue=1, offvalue=0, variable=encode_delete, command=actualizar_estado)
menu_opciones.add_checkbutton(label="Borrar al decodificar", onvalue=1, offvalue=0, variable=decode_delete, command=actualizar_estado)

# Crear la barra de progreso
progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=200)
progress_bar.grid(row=3, column=0,sticky="ew")

################################################# DIR SECTION
# frame_dir labelFrame
frame_dir = tk.LabelFrame(frame, text="Directorio")
frame_dir.grid_rowconfigure(0, weight=0)
frame_dir.grid_columnconfigure(0, weight=2)
frame_dir.grid_columnconfigure(1, weight=0)
frame_dir.grid(row=0, column=0, sticky="ew")

dir_var = tk.StringVar() # Texto de la Direccion
dir_var.trace_add("write", update_dir)

# dir_selected entry
dire_input_entry = tk.Entry(frame_dir, width=40, textvariable=dir_var)
dire_input_entry.grid(row=0, column=0, sticky="ew")

# search_dir button
search_dir_button = tk.Button(frame_dir, text="search_dir", command=select_directory)
search_dir_button.grid(row=0, column=1, sticky="ew")

################################################# PARAMETERS SECTION
# frame_params frame
frame_params = tk.Frame(frame)
frame_params.grid_rowconfigure(0, weight=0)
frame_params.grid_columnconfigure(0, weight=0)
frame_params.grid_columnconfigure(1, weight=0)
frame_params.grid(row=1, column=0,sticky="nsew")

################################################# NAME SECTION
# pass_label labelframe
pass_frame = tk.LabelFrame(frame_params, text="Codigo de Encriptacion")
pass_frame.grid_rowconfigure(0, weight=0)
pass_frame.grid_columnconfigure(0, weight=0)
pass_frame.grid(row=0, column=0)

pass_var = tk.StringVar() # Texto de el Codigo
pass_var.trace_add("write", update_pass)

# pass_input entry
pass_input_entry = tk.Entry(pass_frame, width=40, textvariable=pass_var)
pass_input_entry.grid(row=0, column=0, sticky="ew")

################################################# NAME SECTION
# name_label labelframe
name_frame = tk.LabelFrame(frame_params, text="Nombre de Archivo Encriptado")
name_frame.grid_rowconfigure(0, weight=0)
name_frame.grid_columnconfigure(0, weight=0)
name_frame.grid(row=0, column=1)

name_var = tk.StringVar() # Texto de el Nombre de Archivo
name_var.trace_add("write", update_name)

# name_input entry
name_input_entry = tk.Entry(name_frame, width=40, textvariable=name_var)
name_input_entry.grid(row=0, column=0, sticky="ew")

################################################# BUTTONS SECTION
# frame_buttons frame
frame_buttons = tk.Frame(frame)
frame_buttons.grid(row=2, column=0, sticky="nsew")
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)

# Configurar columnas dentro de frame_buttons para centrar los botones y agregar espacio entre ellos
frame_buttons.grid_columnconfigure(0, weight=1)
frame_buttons.grid_columnconfigure(1, weight=1)
frame_buttons.grid_columnconfigure(2, weight=2)  # Esta es la columna del espacio
frame_buttons.grid_columnconfigure(3, weight=1)
frame_buttons.grid_columnconfigure(4, weight=1)

# encript_button
encript_button = tk.Button(frame_buttons, text="Encriptar", command=encrypt_action)
encript_button.grid(row=0, column=1, sticky="ew", pady=10)

# Espaciador: No es necesario agregar un widget, la columna vacía actúa como un espaciador

# desencript_button
desencript_button = tk.Button(frame_buttons, text="Desencriptar", command=decrypt_action)
desencript_button.grid(row=0, column=3, sticky="ew", pady=10)

# Ejecutar la ventana
root.mainloop()
