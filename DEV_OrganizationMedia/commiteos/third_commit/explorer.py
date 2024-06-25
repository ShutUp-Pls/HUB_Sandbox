import os
import tkinter as tk
import third_commit.sys_functions as sf
import third_commit.tk_functions as tf

from tkinter import ttk
from PIL import ImageTk
from third_commit.cons import *

class ScrollableCanvas(sf.SysFunctions,tf.TkFunctions):
    def __init__(self, parent):
        super().__init__()
        self.columnrows_configure(parent,COLUMN,(0,3),(1,0))
        self.columnrows_configure(parent,ROW,(0,3))
        self.canvas = tk.Canvas(parent,background="red")
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, background="purple")
        
        self.grid_widgets(
            [self.scrollbar,(0,1),{"sticky":tk.NS}],
            [self.canvas,(0,0),{"sticky":tk.NSEW}]
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        parent.bind('<Configure>', lambda e: self.resize_scrollable_frame())
        self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
        self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())

    def on_mousewheel(self, event): self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def bind_to_mousewheel(self): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
    def unbind_from_mousewheel(self): self.canvas.unbind_all("<MouseWheel>")

    def update_scrollbar(self):
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def resize_scrollable_frame(self):
        self.scrollable_frame.configure(width=self.canvas.winfo_width(), height=self.canvas.winfo_height())

class VisualExplorer(sf.SysFunctions, tf.TkFunctions):
    def __init__(self, parent):
        self.folder_path = self.select_folder_path(empty=True)
        self.thumbnail_dict = self.generate_thumbnail_dict(empty=True)
        self.label_dict = self.generate_label_dict(empty=True)

        self.label_size = 1
        self.max_columns = 0
        self.selected_label = None

        self.container = tk.Frame(parent, background="blue")
        self.columnrows_configure(self.container,COLUMN,(0,3))
        self.columnrows_configure(self.container,ROW,(0,0),(1,3))

        self.button_select_path = ttk.Button(self.container, text="Seleccionar Ruta", command=self.click_button_select_path)
        self.frame_canvas = tk.Frame(self.container)
        self.canvas = ScrollableCanvas(self.frame_canvas)
        self.canvas.canvas.bind('<Configure>', self.bind_canvas)

        self.container.pack(fill=tk.BOTH,expand=True)
        self.grid_widgets(
            [self.button_select_path, (0, 0), {"pady": 10}],
            [self.frame_canvas, (1, 0), {"sticky": tk.NSEW}]
        )

    def generate_label_dict(self, thumbnail_dict:dict=None, empty:bool=False):
        label_dict = {}
        if not empty:
            for file_path, image in thumbnail_dict.items():
                try:
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(self.canvas.scrollable_frame, image=photo, text=os.path.basename(file_path), compound=tk.TOP, wraplength=THUMBNAIL_SIZE)
                    label.image = photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                    label_dict[file_path] = label
                except Exception as e:
                    print(f"No se puede crear la etiqueta para {file_path}: {e}")
        return label_dict.copy()

    def display_thumbnails(self, new:bool=False):
        row, col = 0,0
        for file_path in self.label_dict:
            try:
                self.label_dict[file_path].grid(row=row, column=col, padx=5, pady=5)
                self.label_dict[file_path].bind("<Button-1>", lambda e, lbl=self.label_dict[file_path], fp=file_path: self.select_file(lbl, fp))
                self.label_dict[file_path].bind("<Double-1>", lambda e, fp=file_path: self.open_file(fp))
                if new:
                    self.canvas.scrollable_frame.update()
                    self.label_size = self.calculate_widget_size(list(self.label_dict.values())[0], tk.X, GRID)
                    self.max_columns = self.canvas.canvas.winfo_width()//self.label_size
                    new = False
                col += 1
                if col >= self.max_columns:
                    col = 0
                    row += 1
            except Exception as e: print(f"No se puede gridear el label {self.label_dict[file_path]}: {e}")
        self.canvas.update_scrollbar()

    def select_file(self, label, file_path):
        try:
            if self.selected_label: self.selected_label.config(borderwidth=0, relief=tk.FLAT)
            label.config(borderwidth=2, relief=tk.SOLID)
            self.selected_label = label
            self.selected_file_path = file_path
        except Exception as e: print(f"Error seleccionar el archivo archivo {file_path}: {e}")

    def bind_canvas(self, event):
        var_max_column = self.canvas.canvas.winfo_width()//self.label_size
        if self.max_columns != var_max_column:
            self.max_columns = var_max_column
            self.display_thumbnails()

    def click_button_select_path(self):
        selected_folder = self.select_folder_path()
        if selected_folder and selected_folder != self.folder_path:
            self.folder_path = selected_folder
            for widget in self.canvas.scrollable_frame.winfo_children(): widget.destroy()
            self.thumbnail_dict.clear()
            self.thumbnail_dict = self.generate_thumbnail_dict(path=self.folder_path,size=TUPLE_THUMBNAIL_SIZE)
            self.label_dict.clear()
            self.label_dict = self.generate_label_dict(self.thumbnail_dict)
            self.display_thumbnails(True)

class VisualExplorerDel(VisualExplorer):
    def __init__(self, parent, remove_container):
        super().__init__(parent)
        self.columnrows_configure(self.container,COLUMN,(0,3),(1,3),(2,3))
        self.columnrows_configure(self.container,ROW,(0,0),(1,3))

        self.dummy_frame = tk.Frame(self.canvas.canvas,width=30,height=300,background="purple")

        self.remove_container = remove_container
        self.button_remove_container = ttk.Button(self.container, text="Borrar Contenedor", command=self.click_button_remove_container)

        self.dummy_frame.pack(side=tk.RIGHT,expand=False)
        self.grid_widgets(
            [self.button_select_path, (0, 0), {"pady": 10}],
            [self.button_remove_container, (0, 1), {"pady": 10}],
            [self.frame_canvas, (1, 0), {"columnspan": 2}]
        )

    def click_button_remove_container(self):
        for widget in self.container.winfo_children(): widget.destroy()
        self.container.destroy()
        self.remove_container(self)

class VisualExplorerAdd(VisualExplorer):
    def __init__(self, parent, add_container):
        super().__init__(parent)
        self.columnrows_configure(self.container,COLUMN,(0,3),(1,3))
        self.columnrows_configure(self.container,ROW,(0,0),(1,3))

        self.add_containter = add_container
        self.button_add_container = ttk.Button(self.container, text="Añadir Contenedor", command=self.click_button_add_container)

        self.grid_widgets(
            [self.button_select_path, (0, 0), {"pady": 10}],
            [self.button_add_container, (0, 1), {"pady": 10}],
            [self.frame_canvas, (1, 0), {"columnspan": 2}]
        )

    def click_button_add_container(self):
        self.add_containter(VisualExplorerDel)

class MainVisualExplorer(tk.Tk, sf.SysFunctions, tf.TkFunctions):
    def __init__(self):
        super().__init__()
        self.columnrows_configure(self,COLUMN,(0,3),(1,1))
        self.columnrows_configure(self,ROW,(0,3))

        self.container_list = []

        self.frame_left = tk.Frame(self, background="purple")
        self.frame_right = tk.Frame(self)

        self.main_explorer = VisualExplorerAdd(self.frame_left, self.add_container)

        self.canvas_container = ScrollableCanvas(self.frame_right)

        self.grid_widgets(
            [self.frame_left, (0,0),{"sticky":tk.NSEW}],
            [self.frame_right, (0,1),{"sticky":tk.NSEW}]
        )

    def remove_container(self, container):
        if container in self.container_list: self.container_list.remove(container)
        self.canvas_container.update_scrollbar()

    def add_container(self, container):
        self.container_list.append(container(self.canvas_container.scrollable_frame, self.remove_container))
        self.canvas_container.update_scrollbar()

ventana = tk.Tk()
app = VisualExplorer(ventana)
ventana.mainloop()