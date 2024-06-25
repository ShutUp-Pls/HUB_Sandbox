import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import subprocess

DEFAULT_THUMBNAIL_SIZE = 100

class FileExplorerApp:
    def __init__(self, root):
        self._root_ = root
        self._root_.title("Explorador de Archivos")

        # Variables de selección de archivo
        self.selected_label = None
        self.selected_file_path = None
        self.selected_folder_path = None
        self.selected_border_size = 2

        # Variables para mostrar miniaturas
        self.thumbnail_dict = {}
        self.thumbnail_size = tk.IntVar(value=DEFAULT_THUMBNAIL_SIZE)
        self.thumbnail_pad = 5
        self.thumbnail_columns = 0
        self.thumbnail_column_size = (self.thumbnail_size.get() + (self.thumbnail_pad*2) + self.selected_border_size)

        # Botón para seleccionar la ruta
        self.select_path_button = ttk.Button(self._root_, text="Seleccionar Ruta", command=self.select_path)
        # Frame contenedor del canvas y scrollbar
        self.container = tk.Frame(self._root_)
        # Canvas para mostrar las miniaturas
        self.canvas = tk.Canvas(self.container)
        # Frame interno que contiene las miniaturas
        self.thumbnail_frame = tk.Frame(self.canvas)
        # Scrollbar vertical
        self.scrollbar = tk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.canvas.yview)

        # Configuración de columnas
        self._root_.columnconfigure(0, weight=3)
        self._root_.columnconfigure(1, weight=3)
        self._root_.rowconfigure(0, weight=3)
        self._root_.rowconfigure(1, weight=3)

        # Empaquetado de Widgets
        self.select_path_button.grid(row=0, column=1, sticky=tk.EW, pady=10)
        self.container.grid(row=1, column=0, sticky=tk.NSEW, columnspan=2)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.FALSE)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)

        # Configuracion de Widgets
        self.canvas.create_window(0, 0, window=self.thumbnail_frame, anchor=tk.NW)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self._root_.bind('<Configure>', self.bind_root)
        self.canvas.bind('<Enter>', self.bind_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_from_mousewheel)

    def select_path(self):
        try:
            self.selected_folder_path = filedialog.askdirectory()
            self.generate_thumbnails()
            self.display_thumbnails()
        except Exception as e: print(f"Error al seleccionar carpeta: {e}")

    def bind_root(self, event):
        if self.selected_folder_path:
            self.thumbnail_size_slider['state'] = tk.NORMAL
            column_num = self.canvas.winfo_width()//self.thumbnail_column_size
            if self.thumbnail_columns != column_num:
                self.thumbnail_columns = column_num
                self.display_thumbnails()
        else:
            self.thumbnail_size_slider['state'] = tk.DISABLED

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    def unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def generate_thumbnails(self):
        for widget in self.thumbnail_frame.winfo_children():
            widget.destroy()
        self.thumbnail_dict.clear()
        self.selected_file_path = None
        self.selected_label = None

        files = os.listdir(self.selected_folder_path)
        for file in files:
            file_path = os.path.join(self.selected_folder_path, file)
            if os.path.isfile(file_path):
                try:
                    image = Image.open(file_path)
                    image.thumbnail((self.thumbnail_size.get(), self.thumbnail_size.get()))
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(self.thumbnail_frame, image=photo, text=file, compound=tk.TOP, wraplength=self.thumbnail_size.get())
                    label.image = photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                    self.thumbnail_dict[file_path]=label
                except Exception as e:
                    print(f"No se puede abrir el archivo {file_path}: {e}")

    def display_thumbnails(self):
        row, col = 0,0
        for file_path in self.thumbnail_dict:
            try:
                self.thumbnail_dict[file_path].grid(row=row, column=col, padx=self.thumbnail_pad, pady=self.thumbnail_pad)
                self.thumbnail_dict[file_path].bind("<Button-1>", lambda e, lbl=self.thumbnail_dict[file_path], fp=file_path: self.select_file(lbl, fp))
                self.thumbnail_dict[file_path].bind("<Double-1>", lambda e, fp=file_path: self.open_file(fp))
                col += 1
                if col >= self.thumbnail_columns:
                    col = 0
                    row += 1
            except Exception as e:
                print(f"No se puede gridear el label {self.thumbnail_dict[file_path]}: {e}")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()