import tkinter as tk
from tkinter import ttk

# Asumimos que VisualExplorer ya está definida.
class VisualExplorer:
    def __init__(self, parent):
        self.container = tk.Frame(parent)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.select_path_button = ttk.Button(self.container, text="Seleccionar Ruta")
        self.scrollbar = ttk.Scrollbar(self.container)
        self.canvas = tk.Canvas(self.container)

    def columnrows_configure(self, widget, mode, *args):
        # Configuración de columnas/filas según el modo
        for i, weight in args:
            if mode == "COLUMN":
                widget.columnconfigure(i, weight=weight)
            elif mode == "ROW":
                widget.rowconfigure(i, weight=weight)

    def grid_widgets(self, *args):
        # Colocar los widgets en una cuadrícula
        for widget, position, options in args:
            widget.grid(row=position[0], column=position[1], **options)

    def click_button(self, id):
        # Acción del botón (para ser sobreescrita en subclases)
        pass

class VisualExplorerSub(VisualExplorer):
    def __init__(self, parent, remove_callback):
        super().__init__(parent)
        self.remove_callback = remove_callback
        self.columnrows_configure(self.container, "COLUMN", (0, 3), (1, 3), (2, 0))
        self.columnrows_configure(self.container, "ROW", (0, 0), (1, 3))

        self.id_button_del_container = 2
        self.del_container_button = ttk.Button(self.container, text="Borrar Contenedor", command=lambda: self.click_button(self.id_button_del_container))

        self.grid_widgets(
            [self.select_path_button, (0, 0), {"columnspan": 1, "pady": 10}],
            [self.del_container_button, (0, 1), {"columnspan": 1, "pady": 10}],
            [self.scrollbar, (1, 2), {"columnspan": 1, "sticky": tk.NS}],
            [self.canvas, (1, 0), {"columnspan": 2, "sticky": tk.NSEW}]
        )

    def click_button(self, id: int):
        if id == self.id_button_del_container:
            for widget in self.container.winfo_children():
                widget.destroy()
            self.container.destroy()
            self.remove_callback(self)
        else:
            super().click_button(id)

class ButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Manager")

        # Crear los frames
        self.left_frame = tk.Frame(root, width=200, height=400)
        self.right_frame = tk.Frame(root, width=200, height=400)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Asegurar que ambos frames tengan el mismo peso
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Botón en el frame izquierdo
        self.add_button = tk.Button(self.left_frame, text="Añadir Contenedor", command=self.add_visual_explorer_sub)
        self.add_button.pack(padx=10, pady=10)

        # Canvas y Scrollbar en el frame derecho5
        self.canvas = tk.Canvas(self.right_frame)
        self.scrollbar = tk.Scrollbar(self.right_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Lista para almacenar referencias a los contenedores
        self.containers = []

    def add_visual_explorer_sub(self):
        # Crear un nuevo VisualExplorerSub
        container = VisualExplorerSub(self.scrollable_frame, self.remove_container)
        # Añadir el contenedor a la lista
        self.containers.append(container)

    def remove_container(self, container):
        # Eliminar el contenedor de la lista
        if container in self.containers:
            self.containers.remove(container)

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()