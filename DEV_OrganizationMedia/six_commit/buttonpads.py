import tkinter as tk

from myFunctions import tkFunctions, sysFunctions
from tkinter import ttk
from constants import *

class ButtonPadV1(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_select_folder = ttk.Button(self, text="Seleccionar Carpeta")
        self.button_add_container = ttk.Button(self, text="Añadir Contenedor")  

        self.rowcolumn_configure(self, rows=1, columns=2, weights=3)
        self.button_select_folder.grid(row=0, column=0, ipady=4, ipadx=6, padx=15, pady=15)
        self.button_add_container.grid(row=0, column=1, ipady=4, ipadx=6, padx=15, pady=15)

class ButtonPadV2(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.bool_change_file_name = tk.BooleanVar()
        self.str_folder_name = tk.StringVar()

        self.button_select_folder = ttk.Button(self, text="Seleccionar Carpeta")
        self.button_remove_container = ttk.Button(self, text="Eliminar Contenedor")
        self.button_change_folder_name = ttk.Button(self, text="Cambiar Nombre Carpeta")
        self.entry_folder_name = tk.Entry(self, textvariable=self.str_folder_name)
        self.check_change_file_name = tk.Checkbutton(self, text="Renombrar Archivos", variable=self.bool_change_file_name)

        self.rowcolumn_configure(self, rows=4, columns=3, weights=3)
        self.button_select_folder.grid(row=0, column=0, rowspan=2, ipadx=6, ipady=4, padx=15, pady=15)
        self.button_remove_container.grid(row=2, column=0, rowspan=2, ipadx=6, ipady=4, padx=15, pady=15)
        self.button_change_folder_name.grid(row=0, column=1, columnspan=2, ipadx=6, ipady=4)
        self.entry_folder_name.grid(row=1, column=1, columnspan=2, rowspan=2, padx=30, ipadx=30, ipady=5)
        self.check_change_file_name.grid(row=3, column=1, columnspan=2, ipadx=6, ipady=6)

class ButtonPadToggle(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master, button_pad:tk.Widget, init_show=True):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.fixing_size = True

        self.text_show_panel = "Mostrar Panel"
        self.text_hide_panel = "Ocultar Panel"

        self.button_toggle_function = ttk.Button(self, text=self.text_hide_panel, command=self.click_button_toggle_pad)
        self.button_pad = button_pad(self)
        
        self.rowcolumn_configure(self, rows=2, columns=1, weights=3, specific_rows={1: 0})
        self.button_toggle_function.grid(row=0, column=0)
        self.button_pad.grid(row=1, column=0, sticky=tk.EW)

        self.button_pad.bind('<Configure>', lambda e: self.resize_button())
    
    def resize_button(self):
        if self.fixing_size:
            self.fixing_size = False
            self.button_toggle_function.grid_configure(ipadx=((self.button_pad.winfo_width()-self.button_toggle_function.winfo_width())//2))

    def click_button_toggle_pad(self):
        if self.button_pad.winfo_manager():
            self.button_pad.grid_forget()
            self.button_toggle_function.configure(text=self.text_show_panel)
        else:
            self.button_pad.grid(row=1, column=0, sticky=tk.EW)
            self.button_toggle_function.configure(text=self.text_hide_panel)

class DemoButtonPad(tk.Tk):
    def __init__(self):
        super().__init__()
        button_pad = ButtonPadV1(self)
        button_pad.pack()
        
        self.mainloop()

class DemoButtonPadToggle(tk.Tk):
    def __init__(self):
        super().__init__()

        button_pad = ButtonPadToggle(self, ButtonPadV2)
        button_pad.pack(fill=tk.BOTH, expand=True)

        self.mainloop()

#DemoButtonPadToggle()