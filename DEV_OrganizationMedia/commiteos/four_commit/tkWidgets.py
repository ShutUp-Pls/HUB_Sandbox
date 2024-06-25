import os

import tkinter as tk
import tkFunctions as tf
import sysFunctions as sf

from tkinter import ttk
from constants import *


class ScrollableCanvas(tf.tkFunctions, tk.Frame):
    def __init__(self, parent, scrolltype:str=tk.VERTICAL):
        tf.tkFunctions.__init__(self)
        tk.Frame.__init__(self,parent,background="gray")
        self.scrolltype = scrolltype
        self.resizable = True
        self.scrollbar_v = None
        self.scrollbar_h = None
        self.widget_size = None
        self.max_columns = None
        self.max_rows = None
        self.pin_up_columns = None
        self.pin_up_rows = None

        self.canvas = tk.Canvas(self,background="red")
        self.scrollable_frame = tk.Frame(self.canvas, background="purple")

        if self.scrolltype == tk.VERTICAL:
            self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.columnrows_configure(self,[ROW,(0,3)],[COLUMN,(0,3),(1,0)])
            self.grid_widgets(
            [self.scrollbar_v,(0,1),{"sticky":tk.NS}],
            [self.canvas,(0,0),{"sticky":tk.NSEW}]
            )
        elif self.scrolltype == tk.HORIZONTAL:
            self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.columnrows_configure(self,[ROW,(0,3),(1,0)],[COLUMN,(0,3)])
            self.grid_widgets(
            [self.scrollbar_h,(1,0),{"sticky":tk.EW}],
            [self.canvas,(0,0),{"sticky":tk.NSEW}]
            )
        elif self.scrolltype == tk.BOTH:
            self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.grid_widgets(
            [self.scrollbar_v,(0,1),{"sticky":tk.NS}],
            [self.scrollbar_h,(1,0),{"sticky":tk.EW}],
            [self.canvas,(0,0),{"sticky":tk.NSEW}]
            )
        else:
            raise ValueError("El scrolltype debe ser 'tk.VERTICAL'-'tk.HORIZONTAL'-'tk.BOTH'")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.bind('<Configure>', lambda e: self.update_widget())
        self.scrollable_frame.bind('<Configure>', lambda e: self.update_widget())

        if self.scrolltype == tk.VERTICAL:
            self.canvas.configure(yscrollcommand=self.scrollbar_v.set)
            self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
            self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())
        elif self.scrolltype == tk.HORIZONTAL:
            self.canvas.configure(xscrollcommand=self.scrollbar_h.set)
            self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
            self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())
        elif self.scrolltype == tk.BOTH:
            self.canvas.configure(yscrollcommand=self.scrollbar_v.set)
            self.canvas.configure(xscrollcommand=self.scrollbar_h.set)

    def on_mousewheel(self, event):
        if self.scrolltype == tk.VERTICAL: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif self.scrolltype == tk.HORIZONTAL: self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def bind_to_mousewheel(self):
        if self.scrollbar_v:
            if self.scrollbar_v.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
            else: self.unbind_from_mousewheel()
        elif self.scrollbar_h:
            if self.scrollbar_h.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
            else: self.unbind_from_mousewheel()

    def unbind_from_mousewheel(self): self.canvas.unbind_all("<MouseWheel>")

    def update_widget(self):
        self.resize_scrollable_frame()
        self.update_scrollbar()

    def update_scrollbar(self):
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def resize_scrollable_frame(self):
        if self.resizable: self.adjust_scrollable_frame_to_canvas()
        else: self.adjust_canvas_to_scrollable_frame()

    def adjust_canvas_to_scrollable_frame(self):
        if self.max_columns: self.canvas.configure(width=self.widget_size*self.max_columns)
        elif self.max_rows: self.canvas.configure(height=self.widget_size*self.max_rows)
    
    def adjust_scrollable_frame_to_canvas(self):
        if self.max_columns:
            var_max = max(1, self.canvas.winfo_width() // self.widget_size)
            if self.max_columns != var_max:
                self.max_columns = var_max
                self.grid_widgets_list(self.scrollable_frame,self.scrollable_frame.winfo_children(),tk.HORIZONTAL,self.max_columns)
        elif self.max_rows:
            var_max = max(1, self.canvas.winfo_height() // self.widget_size)
            if self.max_rows != var_max:
                self.max_rows = var_max
                self.grid_widgets_list(self.scrollable_frame,self.scrollable_frame.winfo_children(),tk.VERTICAL,self.max_rows)

    def put_widgets_on_scrollable_frame(self, widgets:list, add=False):
        if add: self.forget_widgets_on(self.scrollable_frame)
        else: self.destroy_widgets_on(self.scrollable_frame)

        if self.scrolltype == tk.VERTICAL:
            self.grid_widgets_list(self.scrollable_frame,widgets,tk.HORIZONTAL,1)
            self.scrollable_frame.update()

            self.widget_size = self.calculate_widget_size(widgets[0], tk.HORIZONTAL, GRID)
            self.max_columns = 1
        elif self.scrolltype == tk.HORIZONTAL:
            self.grid_widgets_list(self.scrollable_frame,widgets,tk.VERTICAL,1)
            self.scrollable_frame.update()

            self.widget_size = self.calculate_widget_size(widgets[0], tk.VERTICAL, GRID)
            self.max_rows = 1
        else: 
            self.grid_widgets_list(self.scrollable_frame,widgets)
            self.scrollable_frame.update()
        self.update_widget()

class DemoScrollableCanvas(tk.Tk):
    def __init__(self, scrolltype, label_range):
        super().__init__()
        scroll = ScrollableCanvas(self, scrolltype)
        label_list = []
        for i in range(label_range):
            label = tk.Label(scroll.scrollable_frame, text=f"label_{i}")
            label_list.append(label)
        scroll.put_widgets_on_scrollable_frame(label_list)
        scroll.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

# DemoScrollableCanvas(tk.VERTICAL, 2000)

class VisualExplorer(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master, scrolltype):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master, background="green")
        self.columnrows_configure(self,[ROW,(0,0),(1,3)],[COLUMN,(0,3)])

        self.thumbnail_size = TUPLE_THUMBNAIL_SIZE

        self.folder_path = None
        self.selected_label = None
        self.selected_file_path = None
        self.thumbnail_dict = {}
        self.thumbnail_label_dict = {}
        self.thumbnail_drag_data = {"x": 0, "y": 0}
        self.thumbnail_projection = None

        self.button_select_path = ttk.Button(self, text="Seleccionar Ruta", command=self.click_button_select_path)

        self.thumbnail_canvas = ScrollableCanvas(self, scrolltype)
        self.thumbnail_canvas_package = [self.thumbnail_canvas,(1,0),{"sticky":tk.NSEW}]
        self.thumbnail_canvas_dinamic = False
        
        self.grid_widgets([self.button_select_path,(0,0),{"sticky":tk.NSEW}],
                          self.thumbnail_canvas_package
                          )
        
        self.thumbnail_canvas.scrollable_frame.bind('<Configure>', lambda e: self.bind_scrollable_frame())

    def bind_scrollable_frame(self):
        if self.thumbnail_canvas_dinamic:
            if self.thumbnail_canvas.scrollable_frame.winfo_children(): self.grid_widgets(self.thumbnail_canvas_package)
            else: self.thumbnail_canvas.grid_forget()
        else:
            if not self.thumbnail_canvas.winfo_manager(): self.grid_widgets(self.thumbnail_canvas_package)

    def click_button_select_path(self):
        folder_path = self.select_folder_path()
        if folder_path and self.folder_path != folder_path:
            self.folder_path = folder_path
            self.selected_label = None
            self.selected_file_path = None
            self.thumbnail_dict = {}
            self.thumbnail_label_dict = {}

            self.thumbnail_dict = self.generate_thumbnail_dict(self.folder_path,self.thumbnail_size)
            self.thumbnail_label_dict = self.generate_thumbnail_label_dict(self.thumbnail_canvas.scrollable_frame, self.thumbnail_dict, self.thumbnail_size[0])
            self.add_bind_label_dict()
            self.thumbnail_canvas.put_widgets_on_scrollable_frame(list(self.thumbnail_label_dict.values()))

    def click_label_select_label(self, event, label, file_path):
        try:
            if self.selected_label:
                self.selected_label.config(borderwidth=0, relief=tk.FLAT)
            label.config(borderwidth=2, relief=tk.SOLID)
            self.selected_label = label
            self.selected_file_path = file_path
            self.thumbnail_drag_data["x"] = event.x
            self.thumbnail_drag_data["y"] = event.y
            self.thumbnail_projection = self.duplicate_label(self.selected_label)
            self.thumbnail_projection.place(x=self.winfo_x(), y=self.winfo_y())
            self.thumbnail_projection.lift()
            x = label.winfo_x() - self.thumbnail_drag_data["x"] + event.x
            y = label.winfo_y() - self.thumbnail_drag_data["y"] + event.y
            self.thumbnail_projection.place(x=x, y=y)
        except Exception as e: print(f"Error seleccionar el archivo archivo {file_path}: {e}")

    def add_bind_label_dict(self):
        for path, label in self.thumbnail_label_dict.items():
                label.bind("<Button-1>", lambda e, lbl=label, fp=path:self.click_label_select_label(e, lbl, fp))
                label.bind("<Double-1>", lambda e, fp=path: self.open_file(fp))
                label.bind('<B1-Motion>', lambda e, lbl=label: self.on_drag(e, lbl))
                label.bind('<ButtonRelease-1>', self.on_release)

    def on_drag(self, event, label):
        if self.thumbnail_projection:
            print(f"({label.winfo_x()},{self.thumbnail_drag_data["x"]},{event.x})")
            x = label.winfo_x() - self.thumbnail_drag_data["x"] + event.x
            y = label.winfo_y() - self.thumbnail_drag_data["y"] + event.y
            self.thumbnail_projection.place(x=x, y=y)
            #self.check_frame(x, y)

    def on_release(self, event):
        print("SOLTADO")
        if self.thumbnail_projection:
            self.thumbnail_projection.destroy()

class DemoVisualExplorer(tk.Tk):
    def __init__(self, scrolltype):
        super().__init__()
        scroll = VisualExplorer(self, scrolltype)
        scroll.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

# DemoVisualExplorer(tk.VERTICAL)

class VisualExplorerAdd(VisualExplorer):
    def __init__(self, master, scrolltype):
        VisualExplorer.__init__(self, master, scrolltype)
        self.columnrows_configure(self,[ROW,(0,0),(1,3)],[COLUMN,(0,3),(1,3)])
        self.function_add_container = None
        self.thumbnail_canvas_package = [self.thumbnail_canvas,(1,0),{"sticky":tk.NSEW, "columnspan":2}]

        self.button_add_container = ttk.Button(self, text="Añadir contenedor", command=self.click_button_add_container)

        self.forget_widgets_on(self)

        self.grid_widgets(
            [self.button_select_path,(0,0)],
            [self.button_add_container,(0,1)],
            self.thumbnail_canvas_package
        )

    def click_button_add_container(self, **kwargs): self.function_add_container(**kwargs)

class VisualExplorerRemove(VisualExplorer):
    def __init__(self, master, scrolltype):
        VisualExplorer.__init__(self, master, scrolltype)
        self.columnrows_configure(self,[ROW,(0,0),(1,3)],[COLUMN,(0,3),(1,3)])
        self.function_remove_container = None
        self.thumbnail_canvas.resizable = False
        self.thumbnail_canvas_package = [self.thumbnail_canvas,(1,0),{"sticky":tk.NSEW, "columnspan":2}]
        self.thumbnail_canvas_dinamic = True

        self.button_remove_container = ttk.Button(self, text="Remover contenedor", command=lambda:self.click_button_remove_container(self))

        self.forget_widgets_on(self)

        self.grid_widgets(
            [self.button_select_path,(0,0)],
            [self.button_remove_container,(0,1)]
        )

    def click_button_remove_container(self, container): self.function_remove_container(container)

class MultiVisualExplorer(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self,master,background="yellow")
        self.columnrows_configure(self,[ROW,(0,3)],[COLUMN,(0,3),(1,0)])

        self.remove_container_list = []

        self.visual_explorer_add = VisualExplorerAdd(self, tk.VERTICAL)
        self.visual_explorer_add.function_add_container = self.add_container

        self.container_explorer = ScrollableCanvas(self, tk.VERTICAL)
        self.container_explorer.resizable = False

        self.grid_widgets([self.visual_explorer_add, (0,0), {"sticky":tk.NSEW}])

    def bind_explorer_remove(self, width):
        if self.container_explorer.widget_size != width:
            self.container_explorer.widget_size = width
            self.container_explorer.update_widget()

    def add_container(self):
        visual_explorer_remove = VisualExplorerRemove(self.container_explorer.scrollable_frame, tk.HORIZONTAL)
        visual_explorer_remove.function_remove_container = self.remove_container
        visual_explorer_remove.bind('<Configure>', lambda e: self.bind_explorer_remove(e.width))
        self.remove_container_list.append(visual_explorer_remove)
        self.container_explorer.put_widgets_on_scrollable_frame(self.remove_container_list,add=True)
        if self.container_explorer.winfo_manager:
            self.grid_widgets([self.container_explorer, (0,1), {"sticky":tk.NSEW}])

    def remove_container(self, container):
        if container in self.remove_container_list:
            self.remove_container_list.remove(container)
            container.destroy()
        if self.remove_container_list == []:
            self.container_explorer.grid_forget()

main = tk.Tk()
app = MultiVisualExplorer(main)
app.pack(fill=tk.BOTH, expand=tk.TRUE)
main.mainloop()