import tkinter as tk

from tkinter import ttk

from util.func_tools import JsonTools, TkTools

CONFIG_PATH = "app_specific\\config.json"
CONFIG = JsonTools.load_json(CONFIG_PATH)

import json
import os

class TagMenu(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        TkTools.configure_grid(self, [1, 1], [1, 1])

        self.callback_print = None
        self.callback_search = None

        self.design_combobox_value = tk.StringVar()
        self.paper_size_combobox_value = tk.StringVar()
        self.printer_combobox_value = tk.StringVar()
        self.printer_options_combobox_value = tk.StringVar()

        self.design_frame = ttk.LabelFrame(self, text="Diseño Etiqueta")
        self.design_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.design_combobox = ttk.Combobox(self.design_frame, textvariable=self.design_combobox_value, state="readonly")
        self.design_combobox.pack(fill="x", padx=5, pady=5)

        self.paper_size_frame = ttk.LabelFrame(self, text="Tamaño Papel")
        self.paper_size_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.paper_size_combobox = ttk.Combobox(self.paper_size_frame, textvariable=self.paper_size_combobox_value, state="readonly")
        self.paper_size_combobox.pack(fill="x", padx=5, pady=5)

        self.printer_frame = ttk.LabelFrame(self, text="Impresora")
        TkTools.configure_grid(self.printer_frame, [1], [1, 1])
        self.printer_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        self.search_printers_button = ttk.Button(self.printer_frame, text="Buscar Impresoras", command=self.search_printers_action)
        self.search_printers_button.grid(row=0, column=0, sticky=tk.EW)

        self.printer_combobox = ttk.Combobox(self.printer_frame, textvariable=self.printer_combobox_value, state="readonly")
        self.printer_combobox.grid(row=1, column=0, sticky=tk.EW)

        self.print_label_button = ttk.Button(self, text="Imprimir etiqueta", command=self.print_label_action)
        self.print_label_button.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.__load_design_options()
        self.__load_paper_size_options()

    def __load_design_options(self):
        self.templates = {}
        options = []

        for path in CONFIG.get("config_tags", []):
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as file:
                    data = JsonTools.load_json(path)
                    name = data.get("name", None)
                    if name:
                        options.append(name)
                        self.templates[name] = path

        self.design_combobox["values"] = options
        if options: 
            self.design_combobox.current(0)

    def __load_paper_size_options(self):
        options = list(CONFIG["config_papers"].keys())
        self.paper_size_combobox["values"] = options
        if options:
            self.paper_size_combobox.current(0)

    def search_printers_action(self):
        print("Search")
        if self.callback_search: 
            self.callback_search()

    def print_label_action(self):
        selected_design_name = self.design_combobox_value.get()
        selected_design_path = self.templates.get(selected_design_name)

        selected_paper_size = self.paper_size_combobox_value.get()
        paper_size_values = CONFIG["config_papers"].get(selected_paper_size)

        if selected_design_path and paper_size_values:
            print(f"Design: {selected_design_name} -> {selected_design_path}")
            print(f"Paper Size: {selected_paper_size} -> {paper_size_values}")
            if self.callback_print: 
                self.callback_print(selected_design_path, paper_size_values)
        else:
            print("Falta seleccionar una plantilla o un tamaño de papel válido.")
