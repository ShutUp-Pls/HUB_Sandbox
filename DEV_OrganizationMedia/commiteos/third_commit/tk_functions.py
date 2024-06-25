import tkinter as tk

from third_commit.cons import *

class TkFunctions:
    def __init__(self): pass

    def grid_widgets(self, *widgets_config:list):
        """
        Función para empaquetar widgets usando el método grid de Tkinter.

        :param widgets_config: Listas que contienen:
                               - El widget a empaquetar.
                               - Una tupla (fila, columna).
                               - Diccionarios opcionales con parámetros adicionales para el método grid.
        """
        for config in widgets_config:
            widget = config[0]
            fila_columna = config[1]
            parametros = config[2] if len(config) > 2 else {}
            widget.grid(row=fila_columna[0], column=fila_columna[1], **parametros)

    def columnrows_configure(self, widget:tk.Widget, tipo:str, *configuraciones:tuple, **kwargs:dict):
        """
        Función para configurar columnas o filas en un grid de Tkinter.

        :param widget: Widget sobre el cual se va a configurar el grid.
        :param tipo: "column" para configurar columnas o "row" para configurar filas.
        :param configuraciones: Tuplas indicando (número de fila/columna, peso).
        :param kwargs: Otros parámetros adicionales para columnconfigure o rowconfigure.
        """
        if tipo == "column":
            for numero, peso in configuraciones:
                widget.columnconfigure(numero, weight=peso, **kwargs)
        elif tipo == "row":
            for numero, peso in configuraciones:
                widget.rowconfigure(numero, weight=peso, **kwargs)
        else:
            raise ValueError("El tipo debe ser 'column' o 'row'")

    def calculate_widget_size(self, widget:tk.Widget, side=tk.BOTH, package:str=GRID):
        if side == tk.X:
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
        elif side == tk.Y:
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
            width = self.calculate_widget_size(widget, tk.X, package)
            height = self.calculate_widget_size(widget, tk.Y, package)
            return (width, height)