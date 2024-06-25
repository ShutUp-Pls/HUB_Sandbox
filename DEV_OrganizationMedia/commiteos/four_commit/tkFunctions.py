import os

import tkinter as tk

from constants import *
from PIL import ImageTk

class tkFunctions:
    def __init__(self): pass

    def grid_widgets(self, *widgets_config:list):
        for config in widgets_config:
            widget = config[0]
            fila_columna = config[1]
            parametros = config[2] if len(config) > 2 else {}
            widget.grid(row=fila_columna[0], column=fila_columna[1], **parametros)

    def grid_widgets_list(self, master:tk.Frame, widgets:list, grid_side:str=tk.HORIZONTAL, maximo:int=None):
        # Configurar filas y columnas
        if not maximo or not grid_side:
            maximo = int(len(widgets)**(1/2))
            grid_side = tk.HORIZONTAL
        if grid_side == tk.VERTICAL:
            for i, widget in enumerate(widgets):
                fila = i % maximo
                columna = i // maximo
                master.rowconfigure(fila, weight=1)
                master.columnconfigure(columna, weight=1)
                widget.grid(row=fila, column=columna, sticky=tk.NSEW)
        elif grid_side == tk.HORIZONTAL:
            for i, widget in enumerate(widgets):
                fila = i // maximo
                columna = i % maximo
                master.rowconfigure(fila, weight=1)
                master.columnconfigure(columna, weight=1)
                widget.grid(row=fila, column=columna, sticky=tk.NSEW)

    def columnrows_configure(self, widget:tk.Widget, *configuraciones:list):
        for tipo, *configuracion in configuraciones:
            if tipo == ROW:
                for numero, peso in configuracion: 
                    widget.rowconfigure(numero, weight=peso)
            elif tipo == COLUMN:
                for numero, peso in configuracion:
                    widget.columnconfigure(numero, weight=peso)
            else:
                raise ValueError("El tipo debe ser 'column' o 'row'")
            
    def calculate_widget_size(self, widget:tk.Widget, side=tk.BOTH, package:str=GRID):
        if side == tk.HORIZONTAL:
            wid_width = widget.winfo_width()
            if package == GRID:
                pex_width = widget.grid_info()["padx"]
                pix_width = widget.grid_info()["ipadx"]
            elif package == PACK:
                pex_width = widget.pack_info()["padx"]
                pix_width = widget.pack_info()["ipadx"]
            elif package == PLACE:
                pex_width = widget.place_info()["padx"]
                pix_width = widget.place_info()["ipadx"]
            return wid_width + pex_width*2 + pix_width*2
        elif side == tk.VERTICAL:
            wid_height = widget.winfo_height()
            if package == GRID:
                pex_height = widget.grid_info()["pady"]
                pix_height = widget.grid_info()["ipady"]
            elif package == PACK:
                pex_height = widget.pack_info()["pady"]
                pix_height = widget.pack_info()["ipady"]
            elif package == PLACE:
                pex_height = widget.place_info()["pady"]
                pix_height = widget.place_info()["ipady"]
            return wid_height + pex_height*2 + pix_height*2
        elif side == tk.BOTH:
            width = self.calculate_widget_size(widget, tk.HORIZONTAL, package)
            height = self.calculate_widget_size(widget, tk.VERTICAL, package)
            return (width, height)
        
    def generate_thumbnail_label_dict(self, master, thumbnail_dict, thumbnail_size):
        label_dict = {}
        for file_path, image in thumbnail_dict.items():
            try:
                photo = ImageTk.PhotoImage(image)
                label = tk.Label(master, image=photo, text=os.path.basename(file_path), compound=tk.TOP, wraplength=thumbnail_size)
                label.image = photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                label_dict[file_path] = label
            except Exception as e:
                print(f"No se puede crear la etiqueta para {file_path}: {e}")
        return label_dict
    
    def forget_widgets_on(self, widget:tk.Widget):
        for w in widget.winfo_children():
            widget_manager = w.winfo_manager()
            if widget_manager == GRID: w.grid_forget()
            elif widget_manager == PACK: w.pack_forget()
            elif widget_manager == PLACE: w.place_forget()

    def destroy_widgets_on(self, widget:tk.Widget):
        for w in widget.winfo_children():
            if w.winfo_manager():
                w.destroy()

    def duplicate_label(self, label):
        # Obtén los atributos del label original
        attributes = {
            'text': label['text'],
            'image': label['image'],
            'compound': label['compound'],
            'font': label['font'],
            'fg': label['fg'],
            'bg': label['bg'],
            'relief': label['relief'],
            'bd': label['bd'],
            'width': label['width'],
            'height': label['height'],
            'anchor': label['anchor'],
            'justify': label['justify'],
            'padx': label['padx'],
            'pady': label['pady'],
            'compound': label['compound'],
            'wraplength': label['wraplength']
        }

        # Crea un nuevo label con los mismos atributos
        new_label = tk.Label(label.master, **attributes)
        new_label.grid()

        return new_label