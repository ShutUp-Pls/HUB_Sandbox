import tkinter as tk

from functionalframes import FunctionalFrameV1, FunctionalFrameV2, FunctionalFrameV2Dinamic
from buttonpads import ButtonPadToggle
from VisualExplorerPad1 import ScrollableCanvasVertical
from myFunctions import tkFunctions

class MainApp(tkFunctions, tk.Tk):
    def __init__(self):
        tkFunctions.__init__(self)
        tk.Tk.__init__(self)

        self.folders_list = []

        self.main_frame = FunctionalFrameV1(self)
        self.container_frame = ScrollableCanvasVertical(self)

        self.rowcolumn_configure(self, rows=1, columns=2, weights=1, specific_columns={2:0})
        self.main_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.main_frame.button_pad.button_add_container.configure(command=self.add_container)
        #self.container_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=tk.TRUE)

        self.update()
        self.minsize(self.main_frame.winfo_width(), self.main_frame.winfo_height())

        self.mainloop()

    def add_container(self):
        temp_button_pad = FunctionalFrameV2Dinamic(self.container_frame.scrollable_frame)
        temp_button_pad.index = len(self.folders_list)
        self.folders_list.append(temp_button_pad)
        self.container_frame.put_widgets_on_scrollable_frame(self.folders_list, 1)
        if not self.container_frame.winfo_manager():
            self.rowcolumn_configure(self, rows=1, columns=2, weights=1, specific_columns={1:0})
            self.container_frame.grid(row=0, column=1, sticky=tk.NSEW)
            self.update()
            self.minsize(self.main_frame.canvas.winfo_width()+temp_button_pad.winfo_width()+32, self.main_frame.winfo_height())
        self.rowcolumn_configure(self, rows=1, columns=2, weights=1, specific_columns={2:0})

MainApp()