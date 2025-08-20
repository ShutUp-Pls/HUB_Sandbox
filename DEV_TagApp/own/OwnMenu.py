import tkinter as tk

from tkinter import ttk

class OwnSimpleListMenu:
    def __init__(self, options_list:list):
        self.own_root = False
        if not tk._default_root:
            self.main_root = tk.Tk()
            self.main_root.withdraw()
            self.own_root = True

        else:  self.main_root = tk._default_root

        self.root = tk.Toplevel()
        self.root.title("Selecciona una opción")
        self.root.resizable(width=False, height=False)

        self.options = options_list
        self.selected_option = None
        self.var = tk.StringVar()

        dropdown = ttk.Combobox(self.root, textvariable=self.var, values=self.options, state="readonly")
        button = ttk.Button(self.root, text="Aceptar", command=self.__close_window)

        dropdown.pack(side=tk.LEFT, padx=(20, 20), pady=(20, 20))
        button.pack(side=tk.LEFT, padx=(20, 20), pady=(20, 20))

        self.var.set(self.options[0])

    def show(self):
        self.root.grab_set()
        self.root.wait_window()
        if self.own_root: self.main_root.destroy()
        return self.selected_option

    def __close_window(self):
        self.selected_option = self.var.get()
        self.root.destroy()

    @staticmethod
    def get_selection(option_list):
        menu = OwnSimpleListMenu(option_list)
        return menu.show()