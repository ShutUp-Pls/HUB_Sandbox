import os
import tkinter as tk
import third_commit.sys_functions as sf
import third_commit.tk_functions as tf

from tkinter import ttk
from PIL import ImageTk
from third_commit.cons import *

class VisualExplorer(tk.Tk, sf.SysFunctions, tf.TkFunctions):
    def __init__(self):
        super().__init__()
        self.title("Explorador de Archivos")
        self.columnrows_configure(self, COLUMN, (0,3))
        self.columnrows_configure(self, ROW, (0,3))

        self.folder_path = self.select_folder_path(empty=True)
        self.thumbnail_dict = self.generate_thumbnail_dict(empty=True)
        self.label_dict = self.generate_label_dict(empty=True)

        self.label_size = 1
        self.max_columns = 0
        self.selected_label = None

        # Frame contenedor del canvas y scrollbar
        self.container = tk.Frame(self, background="red")
        self.columnrows_configure(self.container,COLUMN,(0,3),(1,0))
        self.columnrows_configure(self.container,ROW,(0,0),(1,3))

        # Botón para seleccionar la ruta
        self.select_path_button = ttk.Button(self.container, text="Seleccionar Ruta", command=lambda:self.click_button(1))
        # Canvas para mostrar las miniaturas
        self.canvas = tk.Canvas(self.container, background="blue")
        # Scrollbar vertical para navegar por el Canvas
        self.scrollbar = tk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.canvas.yview)
        # Frame interno que contiene las miniaturas
        self.thumbnail_frame = tk.Frame(self.canvas, background="green")

        # Empaquetado de Widgets
        self.container.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.grid_widgets(
            [self.select_path_button, (0, 0), {"columnspan": 2, "pady": 10}],
            [self.scrollbar, (1, 1), {"sticky": tk.NS}],
            [self.canvas, (1, 0), {"sticky": tk.NSEW}]
        )

        # Configuracion de Widgets
        self.canvas.create_window(0, 0, window=self.thumbnail_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', self.bind_root)
        self.canvas.bind('<Enter>', self.bind_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_from_mousewheel)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    def unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    ### =========================== ###
    ### === METODOS ESPECIFICOS === ###
    ### =========================== ###

    def display_thumbnails(self, new:bool=False):
        row, col = 0,0
        for file_path in self.label_dict:
            try:
                self.label_dict[file_path].grid(row=row, column=col, padx=5, pady=5)
                self.label_dict[file_path].bind("<Button-1>", lambda e, lbl=self.label_dict[file_path], fp=file_path: self.select_file(lbl, fp))
                self.label_dict[file_path].bind("<Double-1>", lambda e, fp=file_path: self.open_file(fp))
                if new:
                    self.thumbnail_frame.update()
                    self.label_size = self.calculate_widget_size(list(self.label_dict.values())[0], tk.X, GRID)
                    self.max_columns = self.container.winfo_width()//self.label_size
                    new = False
                col += 1
                if col >= self.max_columns:
                    col = 0
                    row += 1
            except Exception as e: print(f"No se puede gridear el label {self.label_dict[file_path]}: {e}")
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def generate_label_dict(self, thumbnail_dict:dict=None, empty:bool=False):
        """
        Genera un diccionario de 'tk.Label'. El metodo requiere de tener 'tk.Tk' iniciado.

        :param -thumbnail_dict-: Diccionario con las rutas y miniaturas sobre el que se generan los 'tk.Label'.
        :param -empty-:
        - True: Genera un diccionario diccionario vacío.
        - False: Genera un diccionario de la forma a partir del 'thumbnail_dict'.

        :return 'dict': Devuelve un diccionario de la forma { key : tk.Label } manteniendo las llaves del 'thumbnail_dict'.
        """
        label_dict = {}
        if not empty:
            for file_path, image in thumbnail_dict.items():
                try:
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(self.thumbnail_frame, image=photo, text=os.path.basename(file_path), compound=tk.TOP, wraplength=THUMBNAIL_SIZE)
                    label.image = photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                    label_dict[file_path] = label
                except Exception as e:
                    print(f"No se puede crear la etiqueta para {file_path}: {e}")
        return label_dict.copy()

    def select_file(self, label, file_path):
        try:
            # Si hay un label seleccionado, lo deselecciona
            if self.selected_label:
                self.selected_label.config(borderwidth=0, relief=tk.FLAT)
            label.config(borderwidth=2, relief=tk.SOLID)
            self.selected_label = label
            self.selected_file_path = file_path
        except Exception as e: print(f"Error seleccionar el archivo archivo {file_path}: {e}")

    ### ======================== ###
    ### === METODOS OVERRIDE === ###
    ### ======================== ###

    def click_button(self, id:int):
        if id == 1:
            selected_folder = self.select_folder_path()
            if selected_folder and selected_folder != self.folder_path:
                self.folder_path = selected_folder
                for widget in self.thumbnail_frame.winfo_children(): widget.destroy()
                self.thumbnail_dict.clear()
                self.thumbnail_dict = self.generate_thumbnail_dict(path=self.folder_path,size=TUPLE_THUMBNAIL_SIZE)
                self.label_dict.clear()
                self.label_dict = self.generate_label_dict(self.thumbnail_dict)
                self.display_thumbnails(True)

    def bind_root(self, event):
        var_max_column = self.container.winfo_width()//self.label_size
        if self.max_columns != var_max_column:
            self.max_columns = var_max_column
            self.display_thumbnails()

class VisualExplorerSub(VisualExplorer):
    def __init__(self):
        super().__init__()
        self.columnrows_configure(self.container,COLUMN,(0,3),(1,3),(2,0))
        self.columnrows_configure(self.container,ROW,(0,0),(1,3))

        self.del_container_button = ttk.Button(self.container, text="Borrar Contenedor", command=lambda:self.click_button(2))

        self.grid_widgets(
            [self.select_path_button, (0, 0), {"columnspan": 1, "pady": 10}],
            [self.del_container_button, (0, 1), {"columnspan": 1, "pady": 10}],
            [self.scrollbar, (1, 2), {"columnspan": 1, "sticky": tk.NS}],
            [self.canvas, (1, 0), {"columnspan": 2, "sticky": tk.NSEW}]
        )

    def click_button(self, id:int):
        if id == 2:
            for widget in self.container.winfo_children():
                widget.destroy()
            self.container.destroy()
            print("Contenedor eliminado")
        else:
            super().click_button(id)

class VisualExplorerMain(VisualExplorer):
    def __init__(self):
        super().__init__()
        self.container.pack_forget()
        self.frame_left = tk.Frame(self)
        self.frame_right = tk.Frame(self)
        self.container.pack()
        self.columnrows_configure(self.frame_left,COLUMN,(0,3))
        self.columnrows_configure(self.frame_left,ROW,(0,3))
        self.columnrows_configure(self.frame_right,COLUMN,(1,0))

        self.columnrows_configure(self.container,COLUMN,(0,3),(1,3),(2,0))
        self.columnrows_configure(self.container,ROW,(0,0),(1,3))

        self.add_container_button = ttk.Button(self.container, text="Añadir contenedor", command=lambda:self.click_button(3))

        self.grid_widgets(
            [self.frame_left, (0, 0), {"columnspan": 1, "sticky": tk.NSEW, "pady": 10}],
            [self.frame_right, (0, 1), {"columnspan": 1, "sticky": tk.NSEW, "pady": 10}],
            [self.select_path_button, (0, 0), {"columnspan": 1, "pady": 10}],
            [self.add_container_button, (0, 1), {"columnspan": 1, "pady": 10}],
            [self.scrollbar, (1, 2), {"columnspan": 1, "sticky": tk.NS}],
            [self.canvas, (1, 0), {"columnspan": 2, "sticky": tk.NSEW}]
        )

    def click_button(self, id:int):
        if id == 3:
            for widget in self.container.winfo_children():
                widget.destroy()
            self.container.destroy()
        else:
            super().click_button(id)

app = VisualExplorer()
app.mainloop()