import tkinter as tk

from tkinter import ttk

from util.func_tools import TkTools

class OwnSearchBox(tk.Frame):
    PLACEHOLDER_SEARCH = "Buscar..."

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        TkTools.configure_grid(self, [1, 0], [0])
        
        self.callback_search = None

        self.search_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.search_var)
        self.entry.insert(0, self.PLACEHOLDER_SEARCH)

        self.search_button = ttk.Button(self, text="Buscar", command=self.__trigger_search)

        self.entry.grid(row=0, column=0, sticky=tk.EW)
        self.search_button.grid(row=0, column=1)

        self.entry.bind("<Return>", self.__on_enter_pressed)
        self.entry.bind("<FocusIn>", self.__on_focus_in)
        self.entry.bind("<FocusOut>", self.__on_focus_out)

        self.search_var.trace_add("write", self.__on_text_change)

    def get_entry_text(self):
        content = self.entry.get()
        return "" if content == self.PLACEHOLDER_SEARCH else content.strip()

    def set_entry_text(self, text):
        self.entry.delete(0, tk.END)
        if text.strip(): self.entry.insert(0, text.strip())
        else: self.entry.insert(0, self.PLACEHOLDER_SEARCH)

    def __on_enter_pressed(self, event):
        self.__trigger_search()

    def __on_focus_in(self, event):
        if self.entry.get() == self.PLACEHOLDER_SEARCH: self.entry.delete(0, tk.END)

    def __on_focus_out(self, event):
        if not self.entry.get().strip(): self.entry.insert(0, self.PLACEHOLDER_SEARCH)

    def __on_text_change(self, *args):
        if self.callback_search and self.entry.get() != self.PLACEHOLDER_SEARCH:
            query = self.search_var.get().lstrip()
            self.callback_search(query)

    def __trigger_search(self, *args):
        if self.callback_search:
            query = self.search_var.get().lstrip()
            self.callback_search(query)

import tkinter as tk
from tkinter import ttk

class OwnSearchBoxMenu(tk.Frame):
    PLACEHOLDER_SEARCH = "Buscar..."

    def __init__(self, parent, combobox_options=["-Vacío-"], **kwargs):
        super().__init__(parent, **kwargs)
        TkTools.configure_grid(self, [1, 0, 0], [0])
        
        self.callback_search = None

        self.combobox_var = tk.StringVar()
        self.combobox = ttk.Combobox(self, textvariable=self.combobox_var, state="readonly", values=combobox_options)
        self.combobox.grid(row=0, column=2)
        self.combobox.current(0)

        self.search_var = tk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.search_var)
        self.entry.insert(0, self.PLACEHOLDER_SEARCH)
        self.entry.grid(row=0, column=0, sticky=tk.EW)

        self.search_button = ttk.Button(self, text="Buscar en", command=self.__trigger_search)
        self.search_button.grid(row=0, column=1)

        self.entry.bind("<Return>", self.__on_enter_pressed)
        self.entry.bind("<FocusIn>", self.__on_focus_in)
        self.entry.bind("<FocusOut>", self.__on_focus_out)

        self.search_var.trace_add("write", self.__on_text_change)

    def get_entry_text(self):
        content = self.entry.get()
        return "" if content == self.PLACEHOLDER_SEARCH else content.strip()

    def set_entry_text(self, text):
        self.entry.delete(0, tk.END)
        if text.strip(): self.entry.insert(0, text.strip())
        else: self.entry.insert(0, self.PLACEHOLDER_SEARCH)

    def get_combobox_value(self):
        return self.combobox_var.get()

    def set_combobox_value(self, value):
        if value in self.combobox["values"]: self.combobox_var.set(value)

    def __on_enter_pressed(self, event):
        self.__trigger_search()

    def __on_focus_in(self, event):
        if self.entry.get() == self.PLACEHOLDER_SEARCH: self.entry.delete(0, tk.END)

    def __on_focus_out(self, event):
        if not self.entry.get().strip(): self.entry.insert(0, self.PLACEHOLDER_SEARCH)

    def __on_text_change(self, *args):
        if self.callback_search and self.entry.get() != self.PLACEHOLDER_SEARCH:
            query = self.search_var.get().lstrip()
            menu = self.combobox_var.get()
            self.callback_search(menu, query)

    def __trigger_search(self, *args):
        if self.callback_search:
            query = self.search_var.get().lstrip()
            menu = self.combobox_var.get()
            self.callback_search(menu, query)