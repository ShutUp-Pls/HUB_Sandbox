import tkinter as tk

class MiGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)
        
        # Configurar el grid del contenedor
        self.configurar_grid(self.container, "column", (0, 3), (1, 0))
        self.configurar_grid(self.container, "row", (0, 0), (1, 3))

        # Crear widgets
        self.select_path_button = tk.Button(self.container, text="Seleccionar Ruta")
        self.scrollbar = tk.Scrollbar(self.container)
        self.canvas = tk.Canvas(self.container)
        
        # Configurar el grid de los widgets
        self.empaquetar_widgets(
            [self.select_path_button, (0, 0), {"columnspan": 2, "pady": 10}],
            [self.scrollbar, (1, 1), {"sticky": tk.NS}],
            [self.canvas, (1, 0), {"sticky": tk.NSEW}]
        )
        
    def configurar_grid(self, widget: tk.Widget, tipo: str, *configuraciones: tuple, **kwargs: dict) -> None:
        """
        Configura columnas o filas en un grid de Tkinter.

        Args:
            widget (tk.Widget): El widget sobre el cual se va a configurar el grid.
            tipo (str): "column" para configurar columnas o "row" para configurar filas.
            configuraciones (tuple): Tuplas indicando (número de fila/columna, peso).
            kwargs (dict): Otros parámetros adicionales para columnconfigure o rowconfigure.
        """
        if tipo == "column":
            for numero, peso in configuraciones:
                widget.columnconfigure(numero, weight=peso, **kwargs)
        elif tipo == "row":
            for numero, peso in configuraciones:
                widget.rowconfigure(numero, weight=peso, **kwargs)
        else:
            raise ValueError("El tipo debe ser 'column' o 'row'")
    
    def empaquetar_widgets(self, *widgets_config: list) -> None:
        """
        Empaqueta widgets usando el método grid de Tkinter.

        Args:
            widgets_config (list): Listas que contienen:
                - El widget a empaquetar (tk.Widget).
                - Una tupla (fila (int), columna (int)).
                - Diccionarios opcionales con parámetros adicionales para el método grid.
        """
        for config in widgets_config:
            widget = config[0]
            fila_columna = config[1]
            parametros = config[2] if len(config) > 2 else {}
            widget.grid(row=fila_columna[0], column=fila_columna[1], **parametros)

# Ejemplo de uso
if __name__ == "__main__":
    app = MiGUI()
    app.mainloop()
