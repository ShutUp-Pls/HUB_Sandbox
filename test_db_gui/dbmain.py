import tkinter as tk
from tkinter import ttk, messagebox, Menu

class DatabaseManagerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de Base de Datos MariaDB")
        self.geometry("800x600")

        # Menú desplegable para seleccionar la base de datos
        self.database_select = ttk.Combobox(self, values=["Base de Datos 1", "Base de Datos 2"])
        self.database_select.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón para crear base de datos
        self.btn_create_db = tk.Button(self, text="Crear Base de Datos", command=self.create_database)
        self.btn_create_db.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Menú desplegable para seleccionar la tabla
        self.table_select = ttk.Combobox(self, values=["Tabla 1", "Tabla 2"])
        self.table_select.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón para crear tabla
        self.btn_create_table = tk.Button(self, text="Crear Tabla", command=self.create_table)
        self.btn_create_table.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Lista de columnas
        self.column_list = tk.Listbox(self)
        self.column_list.grid(row=2, column=0, padx=10, pady=10, sticky="ns")

        # Canvas para mostrar datos
        self.canvas_show_data = tk.Canvas(self, bg="white")
        self.canvas_show_data.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Configurar el peso de las columnas y filas para que el canvas se expanda
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def create_database(self):
        # Método para crear una nueva base de datos (placeholder)
        messagebox.showinfo("Crear Base de Datos", "Aquí se abriría un diálogo para crear una nueva base de datos.")

    def create_table(self):
        # Método para crear una nueva tabla (placeholder)
        messagebox.showinfo("Crear Tabla", "Aquí se abriría un diálogo para crear una nueva tabla.")

    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.mainloop()

app = DatabaseManagerGUI()
app.run()
