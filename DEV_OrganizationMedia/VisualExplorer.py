import tkinter as tk

from myFunctions import tkFunctions
from VisualExplorerPad1 import VisualExplorerV1
from VisualExplorerPad2 import VisualExplorerV3

class MainApp(tkFunctions, tk.Tk):
    def __init__(self):
        tkFunctions.__init__(self)
        tk.Tk.__init__(self)

        self.left_side = VisualExplorerV1(self)
        self.right_side = VisualExplorerV3(self)

        self.left_side.function_on_proyection = self.function_proyection
        self.left_side.button_pad.button_add_container.configure(command=self.click_add_container)
        self.right_side.remove_function = self.click_remove_container

        self.rowcolumn_configure(self, rows=1, columns=2, weights=1, specific_columns={2:0})
        self.left_side.grid(row=0, column=0, sticky=tk.NSEW)
        self.right_side.grid(row=0, column=1, sticky=tk.NSEW)

        self.mainloop()

    def click_add_container(self):
        self.right_side.click_add_container()
        if self.right_side.container_list != []: self.right_side.grid(row=0, column=1, sticky=tk.NSEW)


    def click_remove_container(self, widget):
        self.right_side.click_remove_container(widget)
        if self.right_side.container_list == []: self.right_side.grid_forget()

    def function_proyection(self, widget:tk.Widget): print(f"Soltado en: {widget}")


MainApp()