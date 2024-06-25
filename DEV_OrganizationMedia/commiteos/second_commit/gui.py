import os
import tkinter as tk
import tkinter_def as td
import subprocess

from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class FileExplorerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Explorador de Archivos")
        self.canvas_list = []
        self.configure(background="blue")

        # Configuración de red para ventana root
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=3)

        # Frames que contiene al main canvas
        self.left_side_frame = tk.Frame(self,background="green")
        self.left_side_frame.columnconfigure(0, weight=3)
        self.left_side_frame.rowconfigure(0, weight=0)
        self.left_side_frame.rowconfigure(1, weight=3)

        # Frame que contiene los demas canvas
        self.right_side_frame = tk.Frame(self,background="purple")
        self.right_side_frame.columnconfigure(0, weight=3)

        # Botón para seleccionar la ruta
        self.add_container_button = ttk.Button(self.left_side_frame, text="Añadir contenedor", command=lambda:self.add_canvas(td.FolderCanvas(self.right_side_frame,False,len(self.canvas_list)-1)))

        # Añade canvas main
        self.add_canvas(td.FolderCanvas(self.left_side_frame))

        # Empaquetado de widgets
        self.left_side_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
        self.right_side_frame.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
        self.add_container_button.grid(row=0, column=0, sticky=tk.NSEW)

        # Configuracion de widgets
        self.bind('<Configure>', self.bind_root)

    # Ajusta los elementos del canvas según cambie la ventana root
    def bind_root(self, event):
        try:
            for canvas in self.canvas_list:
                canvas.bind_root()
        except Exception as e: print(e)

    def add_canvas(self, canvas):
        canvas.del_canvas = self.del_canvas
        self.canvas_list.append(canvas)
        if not canvas.is_main: self.right_side_frame.rowconfigure(self.canvas_list.index(canvas)-1, weight=3)
        print(self.canvas_list)

    def del_canvas(self, canvas):
        self.container.destroy()
        self.canvas_list.remove(canvas)


if __name__ == "__main__":
    app = FileExplorerApp()
    app.mainloop()