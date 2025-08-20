import tkinter as tk
from tkinter import ttk, messagebox
import decimal

class DictionaryGenerator(tk.Frame):
    def __init__(self, master, fields, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.fields = fields
        self.entries = {}
        self.allow_empty = "non"  # Opciones: "all", "visible", "non", "non-visible"

        # Crear un canvas con scrollbar
        self.canvas = tk.Canvas(self, highlightthickness=0, bg=self["bg"])  # Quitar bordes y fondo negro
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self["bg"])  # Asegurar fondo consistente

        # Asociar la scrollbar con el canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Empaquetar canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Crear los campos de entrada basados en la lista de campos
        for i, field in enumerate(self.fields):
            label = tk.Label(self.scrollable_frame, text=field["name"], bg=self["bg"])
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")

            entry = tk.Entry(self.scrollable_frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            # Guardar la referencia al campo, su tipo y sus widgets
            self.entries[field["name"]] = {
                "entry": entry,
                "label": label,
                "type": self.get_type_from_string(field["type"]),
                "visible": True,  # Por defecto, todos los campos son visibles
            }

        # Botón para guardar
        save_button = tk.Button(self.scrollable_frame, text="Guardar Cambios", command=self.save_changes)
        save_button.grid(row=len(self.fields), column=0, columnspan=2, pady=10)


    def get_type_from_string(self, type_str):
        if type_str == "<class 'int'>": return int
        elif type_str == "<class 'str'>": return str
        elif type_str == "<class 'float'>": return float
        elif type_str == "<class 'decimal.Decimal'>": return decimal.Decimal
        else: raise ValueError(f"Tipo no soportado: {type_str}")

    def save_changes(self):
        result = {}
        try:
            for field_name, field_info in self.entries.items():
                value = field_info["entry"].get()
                expected_type = field_info["type"]

                if not value.strip():
                    if self.allow_empty == "non" or (
                        self.allow_empty == "non-visible" and not field_info["visible"]
                    ) or (
                        self.allow_empty == "visible" and field_info["visible"]
                    ):
                        raise ValueError(f"El campo '{field_name}' no puede estar vacío.")

                if value.strip():
                    if expected_type == decimal.Decimal: value = decimal.Decimal(value)
                    else: value = expected_type(value)

                result[field_name] = value

            messagebox.showinfo("Éxito", f"Diccionario generado:\n{result}")

        except (ValueError, decimal.InvalidOperation) as e:
            messagebox.showerror("Error", f"Error en el campo '{field_name}': {str(e)}")

        return result

    def set_values_from_list(self, values):
        if len(values) != len(self.fields):
            raise ValueError(f"El número de valores ({len(values)}) no coincide con el número de campos ({len(self.fields)}).")

        for i, field in enumerate(self.fields):
            field_name = field["name"]
            self.entries[field_name]["entry"].delete(0, tk.END)
            self.entries[field_name]["entry"].insert(0, str(values[i]))

    def toggle_visible_fields(self, visible_fields):
        for field_name, field_info in self.entries.items():
            if field_name in visible_fields:
                field_info["label"].grid()
                field_info["entry"].grid()
                field_info["visible"] = True
            else:
                field_info["label"].grid_remove()
                field_info["entry"].grid_remove()
                field_info["visible"] = False