import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import subprocess

DEFAULT_THUMBNAIL_SIZE = 100

class FolderCanvas:
    # Los parametros por defecto son los de la ventana main
    def __init__(self, parent, is_main=True, row = 1):
        self.is_main = is_main
        self.grid_row = row

        # Variables de selección de archivo
        self.selected_label = None
        self.selected_file_path = None
        self.selected_folder_path = None
        self.selected_border_size = 2

        # Diccionario de imagenes y labels
        self.image_dict = {}
        self.label_dict = {}

        # Variables para mostrar miniaturas
        self.thumbnail_pad = 5
        self.thumbnail_columns = 0
        self.thumbnail_rows = 0
        self.thumbnail_column_size = (DEFAULT_THUMBNAIL_SIZE + (self.thumbnail_pad*2) + self.selected_border_size)
        self.thumbnail_row_size = (DEFAULT_THUMBNAIL_SIZE + (self.thumbnail_pad*2) + self.selected_border_size)

        # Frame contenedor del canvas y scrollbar
        self.container = tk.Frame(parent)

        self.container.columnconfigure(0, weight=3)
        self.container.columnconfigure(1, weight=0)
        self.container.rowconfigure(0, weight=0)
        self.container.rowconfigure(1, weight=3)
        if not is_main: self.container.rowconfigure(2, weight=0)

        # Botón para seleccionar la ruta
        self.select_path_button = ttk.Button(self.container, text="Seleccionar Ruta", command=self.select_path)

        # Botón para eliminar el contenedor
        if not is_main: self.delete_container_button = ttk.Button(self.container, text="Eliminar Contenedor", command=self.del_canvas)

        # Canvas para mostrar las miniaturas
        self.canvas = tk.Canvas(self.container)

        # Frame interno que contiene las miniaturas
        self.thumbnail_frame = tk.Frame(self.canvas)

        # Scrollbar
        if is_main: self.scrollbar = tk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.canvas.yview)
        else: self.scrollbar = tk.Scrollbar(self.container, orient=tk.HORIZONTAL, command=self.canvas.xview)

        # Empaquetado de Widgets
        self.container.grid(row=self.grid_row, column=0, sticky=tk.NSEW)
        if is_main:
            self.select_path_button.grid(row=0, column=0, sticky=tk.NSEW, pady=10, columnspan=2)
            self.scrollbar.grid(row=1, column=1, sticky=tk.NS)
            self.canvas.grid(row=1, column=0, sticky=tk.NSEW)
        else:
            self.select_path_button.grid(row=0, column=0, sticky=tk.NSEW, pady=10)
            self.delete_container_button.grid(row=0, column=1, sticky=tk.NSEW, pady=10)
            self.scrollbar.grid(row=2, column=0, sticky=tk.EW, columnspan=2)
            self.canvas.grid(row=1, column=0, sticky=tk.NSEW, columnspan=2)

        # Configuracion de Widgets
        self.canvas.create_window(0, 0, window=self.thumbnail_frame, anchor=tk.NW)
        self.canvas.bind('<Enter>', self.bind_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_from_mousewheel)
        if is_main: self.canvas.configure(yscrollcommand=self.scrollbar.set)
        else: self.canvas.configure(xscrollcommand=self.scrollbar.set)

    def select_path(self):
        try:
            self.selected_folder_path = filedialog.askdirectory()
            self.generate_thumbnails()
            self.display_thumbnails()
        except Exception as e: print(f"Error al seleccionar carpeta: {e}")

    def on_mousewheel(self, event):
        if self.is_main: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        else: self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    def bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    def unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def generate_thumbnails(self):
        for widget in self.thumbnail_frame.winfo_children(): widget.destroy()
        self.image_dict.clear()
        self.label_dict.clear()
        self.selected_file_path = None
        self.selected_label = None

        files = os.listdir(self.selected_folder_path)
        for file in files:
            file_path = os.path.join(self.selected_folder_path, file)
            if os.path.isfile(file_path):
                try:
                    self.label_dict[file_path] = Image.open(file_path)
                    image = self.label_dict[file_path].copy()
                    image.thumbnail((DEFAULT_THUMBNAIL_SIZE,DEFAULT_THUMBNAIL_SIZE))
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(self.thumbnail_frame, image=photo, text=file, compound=tk.TOP, wraplength=DEFAULT_THUMBNAIL_SIZE)
                    label.image = photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                    self.label_dict[file_path] = label
                except Exception as e:
                    print(f"No se puede abrir el archivo {file_path}: {e}")

    def display_thumbnails(self):
        row, col = 0,0
        for file_path in self.label_dict:
            try:
                self.label_dict[file_path].grid(row=row, column=col, padx=self.thumbnail_pad, pady=self.thumbnail_pad)
                self.label_dict[file_path].bind("<Button-1>", lambda e, lbl=self.label_dict[file_path], fp=file_path: self.select_file(lbl, fp))
                self.label_dict[file_path].bind("<Double-1>", lambda e, fp=file_path: self.open_file(fp))
                if self.is_main:
                    col += 1
                    if col >= self.thumbnail_columns:
                        col = 0
                        row += 1
                else:
                    row += 1
                    if row >= self.thumbnail_rows:
                        row = 0
                        col += 1 
            except Exception as e:
                print(f"No se puede gridear el label {self.label_dict[file_path]}: {e}")

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def select_file(self, label, file_path):
        try:
            # Si hay un label seleccionado, lo deselecciona
            if self.selected_label:
                self.selected_label.config(borderwidth=0, relief=tk.FLAT)
            
            label.config(borderwidth=self.selected_border_size, relief=tk.SOLID)
            self.selected_label = label
            self.selected_file_path = file_path
        except Exception as e:
            print(f"Error seleccionar el archivo archivo {file_path}: {e}")

    def open_file(self, file_path):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.run(['open', file_path], check=True) if sys.platform == 'darwin' else subprocess.run(['xdg-open', file_path], check=True)
        except Exception as e:
            print(f"Error al abrir el archivo {file_path}: {e}")

    def del_canvas(self): pass

    def bind_root(self):
        if self.selected_folder_path:
            if self.is_main:
                    column_num = self.canvas.winfo_width()//self.thumbnail_column_size
                    if self.thumbnail_columns != column_num:
                        self.thumbnail_columns = column_num
                        self.display_thumbnails()
            else:
                    row_num = self.canvas.winfo_width()//self.thumbnail_row_size
                    if self.thumbnail_rows != row_num:
                        self.thumbnail_rows = row_num
                        self.display_thumbnails()