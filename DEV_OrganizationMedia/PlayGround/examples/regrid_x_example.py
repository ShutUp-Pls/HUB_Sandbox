import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def cargar_imagenes(carpeta):
    global imagenes, etiquetas, carpeta_seleccionada
    carpeta_seleccionada = carpeta
    for widget in frame_imagenes.winfo_children():
        widget.destroy()

    archivos_imagen = [archivo for archivo in os.listdir(carpeta) if archivo.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
    
    imagenes = []
    etiquetas = []
    
    for archivo in archivos_imagen:
        imagen_path = os.path.join(carpeta, archivo)
        imagen = Image.open(imagen_path)
        imagen.thumbnail((100, 100))  # Ajustar el tamaño de la miniatura
        img_tk = ImageTk.PhotoImage(imagen)
        imagenes.append(img_tk)

    actualizar_grid()

def actualizar_grid(*args):
    for widget in frame_imagenes.winfo_children():
        widget.destroy()

    num_columnas = slider_columnas.get()
    num_imagenes = len(imagenes)
    num_filas = int(np.ceil(num_imagenes / num_columnas))

    for idx, img_tk in enumerate(imagenes):
        fila = idx // num_columnas
        columna = idx % num_columnas
        label = tk.Label(frame_imagenes, image=img_tk)
        label.image = img_tk  # Guardar una referencia para evitar el garbage collection
        label.grid(row=fila, column=columna, padx=5, pady=5)
        etiquetas.append(label)

    frame_imagenes.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        cargar_imagenes(carpeta)

root = tk.Tk()
root.title("Visor de Imágenes")

carpeta_seleccionada = ""
imagenes = []
etiquetas = []

frame_principal = tk.Frame(root)
frame_principal.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_principal)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas = tk.Canvas(frame_principal, yscrollcommand=scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=canvas.yview)

frame_imagenes = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_imagenes, anchor="nw")

frame_imagenes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

boton_cargar = tk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_cargar.pack(pady=10)

slider_columnas = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, label="Número de Columnas", command=actualizar_grid)
slider_columnas.set(4)  # Valor inicial
slider_columnas.pack(pady=10)

root.mainloop()
