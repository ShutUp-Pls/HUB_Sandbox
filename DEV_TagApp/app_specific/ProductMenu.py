import tkinter as tk

from tkinter import ttk
from decimal import Decimal, InvalidOperation

from util.func_tools import  TkTools, JsonTools, DictTools

CONFIG_PATH = "app_specific\\config.json"
CONFIG = JsonTools.load_json(CONFIG_PATH)

import tkinter as tk
from decimal import Decimal

class CodeNamePriceMenu:
    def __init__(self, parent):
        self.parent = parent
        self.callback = None
        
        self.codigo_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        
        self.precio_var.trace_add("write", self._validate_price)

        self.labels = {
            "codigo": tk.Label(parent, text="Código:"),
            "nombre": tk.Label(parent, text="Nombre:"),
            "precio": tk.Label(parent, text="Precio:"),
        }
        self.entries = {
            "codigo": ttk.Entry(parent, textvariable=self.codigo_var),
            "nombre": ttk.Entry(parent, textvariable=self.nombre_var),
            "precio": ttk.Entry(parent, textvariable=self.precio_var),
        }
        self.entries["precio"].bind("<KeyRelease>", self._on_key)

    def _on_key(self, event):
        if self.callback: self.callback(self.precio_var.get())

    def _validate_price(self, *_):
        value = self.precio_var.get()
        if not all(c.isdigit() or c == '.' for c in value) or value.count('.') > 1:
            filtered_value = []
            dot_seen = False
            for c in value:
                if c.isdigit(): filtered_value.append(c)
                elif c == '.' and not dot_seen:
                    filtered_value.append(c)
                    dot_seen = True
            self.precio_var.set("".join(filtered_value))

    def grid_in(self):
        _, rows = self.parent.grid_size()
        for i, (key, label) in enumerate(self.labels.items(), start=rows):
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            self.entries[key].grid(row=i, column=1, sticky="we" if key != "precio" else "w", padx=5, pady=5)

    def grid_out(self):
        for label in self.labels.values(): label.grid_remove()
        for entry in self.entries.values(): entry.grid_remove()

    def return_info(self):
        if not all(var.get().strip() for var in [self.codigo_var, self.nombre_var, self.precio_var]): return None
        
        try:
            return {
                "codigo": str(self.codigo_var.get().strip()),
                "nombre": str(self.nombre_var.get().strip()),
                "precio_venta_boleta": Decimal(self.precio_var.get()),
            }
        
        except InvalidOperation: return None

    def set_values(self, data):
        if "codigo" in data: self.codigo_var.set(str(data["codigo"]))
        if "nombre" in data: self.nombre_var.set(str(data["nombre"]))
        if "precio_venta_boleta" in data:
            try: self.precio_var.set(str(Decimal(data["precio_venta_boleta"])))
            except InvalidOperation: self.precio_var.set("")

    def get_empty_entries_labels(self):
        empty_fields = []
        for key, var in zip(self.entries.keys(), [self.codigo_var, self.nombre_var, self.precio_var]):
            if not var.get().strip():
                label_text = self.labels[key].cget("text").rstrip(":")
                empty_fields.append(label_text)
        return empty_fields
    
    def reset(self):
        """Resetea los valores de las variables a su estado inicial."""
        self.codigo_var.set("")
        self.nombre_var.set("")
        self.precio_var.set("")

class FamilyMenu:
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.parent = parent
        
        self.categories = CONFIG["categories_structure"]
        self.subcategories = CONFIG["subcategories_structure"]
        
        self.label_categories = tk.Label(parent, text="Familia:")
        self.combo_categories = ttk.Combobox(parent, values=list(self.categories.values()), state="readonly")
        self.combo_categories.bind("<<ComboboxSelected>>", self.update_subcategories)
        
        self.label_subcategories = tk.Label(parent, text="Subfamilia:")
        self.combo_subcategories = ttk.Combobox(parent, state="readonly")

        self.combo_categories.bind("<MouseWheel>", lambda event: "break")
        self.combo_categories.bind("<Button-4>", lambda event: "break")
        self.combo_categories.bind("<Button-5>", lambda event: "break")

        self.combo_subcategories.bind("<MouseWheel>", lambda event: "break")
        self.combo_subcategories.bind("<Button-4>", lambda event: "break")
        self.combo_subcategories.bind("<Button-5>", lambda event: "break")
        
        self.combo_categories.set(list(self.categories.values())[0])
        self.update_subcategories()

    def update_subcategories(self, event=None):
        selected_category = self.combo_categories.get()
        category_key = next((k for k, v in self.categories.items() if v == selected_category), None)
        
        if category_key and category_key in self.subcategories: subcategory_options = list(self.subcategories[category_key].values())
        else: subcategory_options = []
        
        self.combo_subcategories["values"] = subcategory_options
        if subcategory_options: self.combo_subcategories.set(subcategory_options[0])
        else: self.combo_subcategories.set('')

    def grid_in(self):
        _, rows = self.parent.grid_size()
        self.label_categories.grid(row=rows, column=0, padx=5, pady=5, sticky="e")
        self.combo_categories.grid(row=rows, column=1, padx=5, pady=5, sticky="w")
        self.label_subcategories.grid(row=rows + 1, column=0, padx=5, pady=5, sticky="e")
        self.combo_subcategories.grid(row=rows + 1, column=1, padx=5, pady=5, sticky="w")
    
    def grid_out(self):
        self.label_categories.grid_remove()
        self.combo_categories.grid_remove()
        self.label_subcategories.grid_remove()
        self.combo_subcategories.grid_remove()

    def set_values(self, data):
        family_id = str(data.get("familia", ""))
        subfamily_id = str(data.get("subfamilia", ""))
        
        if family_id in self.categories:
            self.combo_categories.set(self.categories[family_id])
            self.update_subcategories()
            
            if family_id in self.subcategories and subfamily_id in self.subcategories[family_id]:
                self.combo_subcategories.set(self.subcategories[family_id][subfamily_id])
            else:
                subcategory_options = list(self.subcategories.get(family_id, {}).values())
                if subcategory_options: self.combo_subcategories.set(subcategory_options[0])
        else:
            self.combo_categories.set(list(self.categories.values())[0])
            self.update_subcategories()

    def return_info(self):
        selected_category = self.combo_categories.get()
        selected_subcategory = self.combo_subcategories.get()
        
        category_id = next((k for k, v in self.categories.items() if v == selected_category), None)
        subcategory_id = next((k for k, v in self.subcategories.get(category_id, {}).items() if v == selected_subcategory), None)

        result = {"familia": category_id, "subfamilia": subcategory_id}
        return result
    
    def reset(self):
        self.combo_categories.set(list(self.categories.values())[0])
        self.update_subcategories()

class UnityMenu:
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.parent = parent
        self.unit_dict = CONFIG["unity_list"]

        self.label_units = tk.Label(parent, text="Unidades:")
        self.combo_units = ttk.Combobox(parent, values=list(self.unit_dict.keys()), state="readonly")

        self.combo_units.bind("<MouseWheel>", lambda event: "break")
        self.combo_units.bind("<Button-4>", lambda event: "break")
        self.combo_units.bind("<Button-5>", lambda event: "break")

        if self.unit_dict: self.combo_units.set(list(self.unit_dict.keys())[0])

    def grid_in(self):
        _, rows = self.parent.grid_size()
        self.label_units.grid(row=rows, column=0, padx=5, pady=5, sticky="e")
        self.combo_units.grid(row=rows, column=1, padx=5, pady=5, sticky="w")

    def grid_out(self):
        self.label_units.grid_remove()
        self.combo_units.grid_remove()

    def set_values(self, data):
        if "unidad" in data:
            for key, value in self.unit_dict.items():
                if value == data["unidad"]:
                    self.combo_units.set(key)
                    break

    def return_info(self):
        selected_unit = self.combo_units.get()
        unit_id = self.unit_dict.get(selected_unit, None)
        return {"unidad": unit_id}
    
    def reset(self):
        self.combo_units.set(list(self.unit_dict.keys())[0])


class IvaMenu:
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.parent = parent
        
        self.afecto_iva_var = tk.StringVar(value="SI")

        self.label_iva = tk.Label(parent, text="Afecto a IVA:")
        self.combo_iva = ttk.Combobox(parent, values=["SI", "NO"], state="readonly", textvariable=self.afecto_iva_var)

        self.combo_iva.bind("<MouseWheel>", lambda event: "break")
        self.combo_iva.bind("<Button-4>", lambda event: "break")
        self.combo_iva.bind("<Button-5>", lambda event: "break")
    
    def grid_in(self):
        _, rows = self.parent.grid_size()
        self.label_iva.grid(row=rows, column=0, padx=5, pady=5, sticky="e")
        self.combo_iva.grid(row=rows, column=1, padx=5, pady=5, sticky="w")

    def grid_out(self):
        self.label_iva.grid_remove()
        self.combo_iva.grid_remove()

    def return_info(self):
        selected_value = self.afecto_iva_var.get()
        result_str = "S" if selected_value == "SI" else "N"
        return {"afecto_iva": result_str}

    def set_values(self, data):
        if "afecto_iva" in data: self.afecto_iva_var.set("SI" if data["afecto_iva"] == "S" else "NO")

    def reset(self):
        self.afecto_iva_var.set("SI")
    
class TaxMenu:
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.parent = parent

        self.tax_data = DictTools.common_filter_list(CONFIG["taxes_show"],list(CONFIG["taxes_structure"].keys()))

        self.label_tax = tk.Label(parent, text="Impuesto adicional:")
        self.combo_tax = ttk.Combobox(parent, values=list(self.tax_data.values()), state="readonly")

        self.combo_tax.bind("<MouseWheel>", lambda event: "break")
        self.combo_tax.bind("<Button-4>", lambda event: "break")
        self.combo_tax.bind("<Button-5>", lambda event: "break")

        if self.tax_data: self.combo_tax.set(list(self.tax_data.values())[0])

    def grid_in(self):
        _, rows = self.parent.grid_size()
        self.label_tax.grid(row=rows, column=0, padx=5, pady=5, sticky="e")
        self.combo_tax.grid(row=rows, column=1, padx=5, pady=5, sticky="w")

    def grid_out(self):
        self.label_tax.grid_remove()
        self.combo_tax.grid_remove()

    def return_info(self):
        selected_tax = self.combo_tax.get()
        tax_id = next((k for k, v in self.tax_data.items() if v == selected_tax), None)
        result = {"id_impuestos": tax_id, "tiene_impuesto": "N" if tax_id == 0 else "S"}
        return result

    def set_values(self, data: dict):
        tax_id = data.get("id_impuestos", 0)
        if tax_id in self.tax_data: self.combo_tax.set(self.tax_data[tax_id])
        else: self.combo_tax.set(list(self.tax_data.values())[0])

        tiene_impuesto = "N" if tax_id == 0 else "S"
        assert tiene_impuesto == ("N" if tax_id == 0 else "S"), "Lógica interna corregida automáticamente."

    def reset(self):
        if self.tax_data:
            self.combo_tax.set(list(self.tax_data.values())[0])
    
class ValidityMenu:
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.parent = parent
        
        self.validity_var = tk.StringVar(value="SI")
        
        self.label_validity = tk.Label(parent, text="Vigente:")
        self.combo_validity = ttk.Combobox(parent, values=["SI", "NO"], state="readonly", textvariable=self.validity_var)

        self.combo_validity.bind("<MouseWheel>", lambda event: "break")
        self.combo_validity.bind("<Button-4>", lambda event: "break")
        self.combo_validity.bind("<Button-5>", lambda event: "break")
        
    def grid_in(self):
        _, rows = self.parent.grid_size()
        
        self.label_validity.grid(row=rows, column=0, padx=5, pady=5, sticky="e")
        self.combo_validity.grid(row=rows, column=1, padx=5, pady=5, sticky="w")
        
    def grid_out(self):
        self.label_validity.grid_remove()
        self.combo_validity.grid_remove()
        
    def return_info(self):
        selected_option = self.validity_var.get()
        result_str = "S" if selected_option == "SI" else "N" if selected_option == "NO" else ""
        return {"vigente": result_str}
    
    def set_values(self, data):
        if "vigente" in data:
            value = data["vigente"]
            if value == "S": self.validity_var.set("SI")
            elif value == "N": self.validity_var.set("NO")

    def reset(self):
        self.validity_var.set("SI")

class OptionalMenu:
    def __init__(self, parent: tk.Widget, *args, **kwargs):
        self.parent = parent
        self.callback = None

        self.cod_interno_var = tk.StringVar()
        self.precio_var = tk.StringVar()

        self.precio_var.trace_add("write", self._validate_price)

        self.labels = {
            "cod_interno": tk.Label(parent, text="Código Interno:"),
            "precio_venta": tk.Label(parent, text="Precio Factura:"),
        }
        self.entries = {
            "cod_interno": ttk.Entry(parent, textvariable=self.cod_interno_var),
            "precio_venta": ttk.Entry(parent, textvariable=self.precio_var),
        }

        self.entries["precio_venta"].bind("<KeyRelease>", self._on_key)

    def _on_key(self, event):
        if self.callback: self.callback(self.precio_var.get())

    def _validate_price(self, *_):
        value = self.precio_var.get()
        if not all(c.isdigit() or c == '.' for c in value) or value.count('.') > 1:
            filtered_value = []
            dot_seen = False
            for c in value:
                if c.isdigit():
                    filtered_value.append(c)
                elif c == '.' and not dot_seen:
                    filtered_value.append(c)
                    dot_seen = True
            self.precio_var.set("".join(filtered_value))

    def grid_in(self):
        _, rows = self.parent.grid_size()
        for i, (key, label) in enumerate(self.labels.items(), start=rows):
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            self.entries[key].grid(row=i, column=1, sticky="we" if key == "cod_interno" else "w", padx=5, pady=5)

    def grid_out(self):
        for label in self.labels.values(): label.grid_remove()
        for entry in self.entries.values(): entry.grid_remove()

    def set_values(self, data):
        if "cod_interno" in data:
            try: self.cod_interno_var.set(str(data["cod_interno"]))
            except (TypeError, ValueError): self.cod_interno_var.set("")

        if "precio_venta" in data:
            try: self.precio_var.set(str(Decimal(data["precio_venta"])))
            except (TypeError, ValueError, InvalidOperation): self.precio_var.set("")

    def return_info(self):
        return {"cod_interno": self.cod_interno_var.get().strip(), "precio_venta": Decimal(self.precio_var.get())}
    
    def reset(self):
        self.cod_interno_var.set("")
        self.precio_var.set("")

class ProductMenu(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        TkTools.configure_grid(self, [1], [1,0])

        self.input_dict = {}
        self.callback_action = None

        self.top_frame = tk.Frame(self)
        TkTools.configure_grid(self.top_frame, [1,0], [1])

        self.canvas = tk.Canvas(self.top_frame, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.top_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas)
        TkTools.configure_grid(self.inner_frame, [0,1,1], [])
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw",)

        self.codenameprice_menu = CodeNamePriceMenu(self.inner_frame)
        self.codenameprice_menu.grid_in()

        self.family_menu = FamilyMenu(self.inner_frame)
        self.family_menu.grid_in()

        self.unity_menu = UnityMenu(self.inner_frame)
        self.unity_menu.grid_in()

        self.iva_menu = IvaMenu(self.inner_frame)
        self.tax_menu = TaxMenu(self.inner_frame)
        self.validity_menu = ValidityMenu(self.inner_frame)
        self.optional_menu = OptionalMenu(self.inner_frame)

        self.codenameprice_menu.callback = self._set_price_bill_iva
        self.optional_menu.callback = self._set_price_sale_iva

        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        self.bottom_frame = tk.Frame(self)
        TkTools.configure_grid(self.bottom_frame, [1,1], [0,0])

        self.button_show_more = ttk.Button(self.bottom_frame, text="Mostrar Opciones Avanzadas", command=self.__toggle_advanced_options)
        self.button_show_more.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.button_action = ttk.Button(self.bottom_frame, text="Crear Producto", command=self.__action_product)
        self.button_action.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)

        self.top_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.bottom_frame.grid(row=1, column=0, sticky=tk.NSEW)

    @property
    def hiden_info(self):
        return 

    def _set_price_sale_iva(self, value):
        if value: value = Decimal(Decimal(value)*Decimal(1.19)).quantize(Decimal('1.00'))
        else: value = ""
        self.codenameprice_menu.set_values({"precio_venta_boleta":value})

    def _set_price_bill_iva(self, value):
        if value: value = Decimal(Decimal(value)/Decimal(1.19)).quantize(Decimal('1.00'))
        else: value = ""
        self.optional_menu.set_values({"precio_venta":value})

    def __toggle_advanced_options(self):
        _, columns = self.inner_frame.grid_size()
        if columns <= 6:
            self._grid_in_advanced_options()
            self.button_show_more.configure(text="Ocultar Opciones Avanzadas")
        else:
            self._grid_out_advanced_options()
            self.button_show_more.configure(text="Mostrar Opciones Avanzadas")

    def _grid_in_advanced_options(self):
        self.iva_menu.grid_in()
        self.tax_menu.grid_in()
        self.validity_menu.grid_in()
        self.optional_menu.grid_in()

    def _grid_out_advanced_options(self):
        self.iva_menu.grid_out()
        self.tax_menu.grid_out()
        self.validity_menu.grid_out()
        self.optional_menu.grid_out()

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.config(width=self.inner_frame.winfo_reqwidth())

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.inner_frame_id, width=canvas_width)

    def _on_mousewheel(self, event):
        if event.delta != 0: direction = -1 if event.delta > 0 else 1
        else: direction = -1 if event.num == 4 else 1

        top, bottom = self.canvas.yview()
        if (top <= 0.0 and direction < 0) or (bottom >= 1.0 and direction > 0): return

        self.canvas.yview_scroll(direction, "units")

    def set_values(self, values):
        self.codenameprice_menu.set_values(values)
        self.family_menu.set_values(values)
        self.unity_menu.set_values(values)
        self.iva_menu.set_values(values)
        self.tax_menu.set_values(values)
        self.validity_menu.set_values(values)
        self.optional_menu.set_values(values)

        self.input_dict = {k: v for k, v in values.items() if k not in self.get_info()}

        if "id_producto" in self.input_dict: self.button_action.configure(text="Editar Producto")
        else: self.button_action.configure(text="Crear Producto")

    def get_info(self, partial=False):
        if partial: dict0 = {}
        else: dict0 = self.codenameprice_menu.return_info()
        dict1 = self.family_menu.return_info()
        dict2 = self.unity_menu.return_info()
        dict3 = self.iva_menu.return_info()
        dict4 = self.tax_menu.return_info()
        dict5 = self.validity_menu.return_info()
        dict6 = self.optional_menu.return_info()

        return {**dict0, **dict1, **dict2, **dict3, **dict4, **dict5, **dict6}
    
    def reset(self):
        self.input_dict = {}
        self.codenameprice_menu.reset()
        self.family_menu.reset()
        self.unity_menu.reset()
        self.iva_menu.reset()
        self.tax_menu.reset()
        self.validity_menu.reset()
        self.optional_menu.reset()

        self.button_action.configure(text="Crear Producto")

    def __action_product(self):
        if self.callback_action: self.callback_action()
        else: print("Presionado el botón")