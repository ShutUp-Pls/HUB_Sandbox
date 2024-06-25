import os

import tkinter as tk
import tkFunctions as tf
import sysFunctions as sf

from tkinter import ttk
from constants import *

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, function):
        super().__init__()
        self.function = function
        
    def on_created(self, event):
        print(f"Se ha creado el archivo: {event.src_path}")
        self.app.on_change()

    def on_deleted(self, event):
        print(f"Se ha eliminado el archivo: {event.src_path}")
        self.app.on_change()

    def on_modified(self, event):
        print(f"Se ha modificado el archivo: {event.src_path}")
        self.app.on_change()

    def on_moved(self, event):
        print(f"Se ha movido el archivo: {event.src_path}")
        self.app.on_change()

class ScrollableCanvas(tf.tkFunctions, tk.Frame):
    def __init__(self, parent, scrolltype:str=tk.BOTH):
        tf.tkFunctions.__init__(self)
        tk.Frame.__init__(self,parent)
        self.scrolltype = scrolltype
        self.resizable = (True, 0)

        self.widget_size = 1

        self.scrollbar_v, self.scrollbar_h = None, None
        scrollbar_v_package, scrollbar_h_package = [], []

        self.canvas = tk.Canvas(self)
        self.scrollable_frame = tk.Frame(self.canvas)
        
        scroll_v, scroll_h, scroll_b = (scrolltype==tk.VERTICAL), (scrolltype==tk.HORIZONTAL), (scrolltype==tk.BOTH)
        if (not scroll_v) and (not scroll_h) and (not scroll_b): raise ValueError("Scrolltype invalido...")

        if (scroll_v and not scroll_b) or (not scroll_v and scroll_b):
            self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.scrollbar_v.set)
            scrollbar_v_package  = [self.scrollbar_v,(0,1),{"sticky":tk.NS}]
            if not scroll_b: row_config, column_config = [ROW,(0,3)], [COLUMN,(0,3),(1,0)]

        if (scroll_h and not scroll_b) or (not scroll_h and scroll_b):
            self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
            self.canvas.configure(xscrollcommand=self.scrollbar_h.set)
            scrollbar_h_package = [self.scrollbar_h,(1,0),{"sticky":tk.EW}]
            if not scroll_b: row_config, column_config = [ROW,(0,3),(1,0)], [COLUMN,(0,3)]

        if scroll_b: row_config, column_config = [ROW,(0,3),(1,0)], [COLUMN,(0,3),(1,0)]

        if scroll_v or scroll_h:
            self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
            self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())

        canvas_package = [self.canvas,(0,0),{"sticky":tk.NSEW}]

        self.columnrows_configure(self, row_config, column_config)
        self.grid_widgets(canvas_package, scrollbar_v_package, scrollbar_h_package)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.bind('<Configure>', lambda e: self.update_widget())
        self.scrollable_frame.bind('<Configure>', lambda e: self.update_widget())                     

    def on_mousewheel(self, event):
        if self.scrolltype == tk.VERTICAL: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        elif self.scrolltype == tk.HORIZONTAL: self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")

    def unbind_from_mousewheel(self): self.canvas.unbind_all("<MouseWheel>")

    def bind_to_mousewheel(self):
        if self.scrollbar_v and self.scrollbar_v.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        elif self.scrollbar_h and self.scrollbar_h.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        else: self.unbind_from_mousewheel()

    def update_widget(self):
        if self.scrollable_frame.winfo_children():
            self.resize_scrollable_frame()
            self.canvas.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def resize_scrollable_frame(self):
        if self.resizable[0]: self.adjust_scrollable_frame_to_canvas()
        else:
            if self.scrolltype == tk.VERTICAL:
                self.grid_widgets_list(self.scrollable_frame, self.scrollable_frame.winfo_children(),tk.HORIZONTAL,self.resizable[1])
                self.canvas.configure(width=self.scrollable_frame.winfo_width())
            elif self.scrolltype == tk.HORIZONTAL:
                self.grid_widgets_list(self.scrollable_frame, self.scrollable_frame.winfo_children(),tk.VERTICAL,self.resizable[1])
                self.canvas.configure(height=self.scrollable_frame.winfo_height())
    
    def adjust_scrollable_frame_to_canvas(self):
        if self.scrolltype == tk.VERTICAL:
            var_max = max(1, self.canvas.winfo_width() // self.widget_size)
            if self.scrollable_frame.grid_size()[0] != var_max:
                self.grid_widgets_list(self.scrollable_frame,self.scrollable_frame.winfo_children(),tk.HORIZONTAL,var_max)
        elif self.scrolltype == tk.HORIZONTAL:
            var_max = max(1, self.canvas.winfo_height() // self.widget_size)
            if self.scrollable_frame.grid_size()[1] != var_max:
                self.grid_widgets_list(self.scrollable_frame,self.scrollable_frame.winfo_children(),tk.VERTICAL,var_max)

    def put_widgets_on_scrollable_frame(self, widgets:list, add:bool=False):
        if add: self.forget_widgets_on(self.scrollable_frame)
        else: self.destroy_widgets_on(self.scrollable_frame)
        
        self.grid_widgets_list(self.scrollable_frame,widgets)
        self.scrollable_frame.update()

        if self.scrolltype == tk.VERTICAL: self.widget_size = self.calculate_widget_size(widgets[0], tk.HORIZONTAL, GRID)
        elif self.scrolltype == tk.HORIZONTAL: self.widget_size = self.calculate_widget_size(widgets[0], tk.VERTICAL, GRID)

        self.resize_scrollable_frame()

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

#DemoScrollableCanvas(tk.BOTH, 2000)

class VisualFolderExplorer(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master, scrolltype):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.thumbnail_size = TUPLE_THUMBNAIL_SIZE
        self.reset_select_path()

        self.thumbnail_drag_data = {"x": 0, "y": 0}
        self.thumbnail_projection = None

        self.thumbnail_canvas = ScrollableCanvas(self, scrolltype)
        self.thumbnail_canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

    def reset_select_path(self):
        try: self.stop()
        except Exception: pass
        self.folder_path = None
        self.selected_label = None
        self.selected_file_path = None
        self.thumbnail_dict = {}
        self.thumbnail_label_dict = {}

    def display_folder(self, path:str=None):
        if path and self.folder_path != path:
            self.reset_select_path()
            self.folder_path = path

            self.thumbnail_dict = self.generate_thumbnail_dict(self.folder_path,self.thumbnail_size)
            self.thumbnail_label_dict = self.generate_thumbnail_label_dict(self.thumbnail_canvas.scrollable_frame, self.thumbnail_dict, self.thumbnail_size[0])
            self.thumbnail_canvas.put_widgets_on_scrollable_frame(list(self.thumbnail_label_dict.values()))
            self.add_bind_label_dict()

    def add_bind_label_dict(self):
        for path, label in self.thumbnail_label_dict.items():
                label.bind("<Button-1>", lambda e, lbl=label, fp=path:self.select_label(e, lbl, fp))
                label.bind("<Double-1>", lambda e, fp=path: self.open_file(fp))
                label.bind("<B1-Motion>", lambda e, lbl=label: self.on_drag(e, lbl))
                label.bind("<ButtonRelease-1>", self.on_release)

    def select_label(self, event, label, file_path):
        try:
            if self.selected_label: self.selected_label.config(borderwidth=0, relief=tk.FLAT)
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

    def refresh_display(self):
        temp_path = self.folder_path
        self.reset_select_path()
        self.display_folder(temp_path)

class DemoFolderExplorer(tk.Tk):
    def __init__(self, scrolltype):
        super().__init__()
        scroll = VisualFolderExplorer(self, scrolltype)
        scroll.display_folder(EXAMPLE_FOLDER_PATH)
        scroll.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

#DemoFolderExplorer(tk.VERTICAL)

class ButtonPadMainFolder(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_select_folder = ttk.Button(self, text="Seleccionar Carpeta", command=self.click_button_select_folder)
        self.button_select_folder_function = print
        button_select_folder_package = [self.button_select_folder, (0,0), {"ipady":4, "ipadx":6, "padx":15, "pady":15}]

        self.button_add_container = ttk.Button(self, text="Añadir Contenedor", command=self.click_button_add_container)  
        self.button_add_container_function = print 
        button_add_container_package = [self.button_add_container, (0,1), {"ipady":4, "ipadx":6, "padx":15, "pady":15}]

        self.columnrows_configure(self,[ROW,(0,3)],[COLUMN,(0,3),(1,3)])
        self.grid_widgets(button_select_folder_package, button_add_container_package)

        self.after(100, lambda: self.configure(width=self.winfo_width(), height=self.winfo_height()))

    def click_button_select_folder(self): self.button_select_folder_function()
    def click_button_add_container(self): self.button_add_container_function()

class DemoButtonPadMainFolder(tk.Tk):
    def __init__(self):
        super().__init__()
        scroll = ButtonPadMainFolder(self)
        scroll.pack()
        self.mainloop()

#DemoButtonPadMainFolder()

class ButtonPadOtherFolder(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.bool_change_file_name = tk.BooleanVar()
        self.str_folder_name = tk.StringVar()

        self.button_select_folder = ttk.Button(self, text="Seleccionar Carpeta", command=self.click_button_select_folder)
        self.button_select_folder_function = print
        button_select_folder_package = [self.button_select_folder, (1,0), {"ipady":4, "ipadx":6, "padx":15, "pady":15, "rowspan":2}]

        self.button_change_folder_name = ttk.Button(self, text="Cambiar Nombre Carpeta", command=self.click_button_change_folder_name)
        self.button_change_folder_name_function = print
        button_change_folder_name_package = [self.button_change_folder_name, (1,1), {"ipady":4, "ipadx":6, "columnspan":2}]

        self.entry_folder_name = tk.Entry(self, textvariable=self.str_folder_name)
        entry_folder_name_package = [self.entry_folder_name, (2,1), {"ipady":6, "ipadx":30, "pady":15, "padx":30, "columnspan":2, "rowspan":2}]

        self.check_change_file_name = tk.Checkbutton(self, text="Renombrar Archivos", variable=self.bool_change_file_name, command=self.click_check_change_file_name)
        self.check_change_file_name_function = print
        check_change_file_name_package = [self.check_change_file_name, (4,1), {"ipadx":6, "columnspan":2}]

        self.button_remove_container = ttk.Button(self, text="Eliminar Contenedor", command=self.click_button_remove_container)  
        self.button_remove_container_function = print 
        button_remove_container_package = [self.button_remove_container, (3,0), {"ipady":4, "ipadx":6, "padx":15, "pady":15, "rowspan":2}]

        self.columnrows_configure(self,[ROW,(0,3),(1,3),(2,3),(3,3),(4,3)],[COLUMN,(0,3),(1,3),(2,3)])
        self.grid_widgets(button_select_folder_package,
                          entry_folder_name_package,
                          button_remove_container_package,
                          check_change_file_name_package,
                          button_change_folder_name_package,  
                          )

    def click_button_change_folder_name(self): self.button_change_folder_name_function()
    def click_check_change_file_name(self): self.check_change_file_name_function()
    def click_button_select_folder(self): self.button_select_folder_function()
    def click_button_remove_container(self): self.button_remove_container_function()

class DemoButtonPadOtherFolder(tk.Tk):
    def __init__(self):
        super().__init__()
        scroll = ButtonPadOtherFolder(self)
        scroll.pack()
        self.mainloop()

#DemoButtonPadOtherFolder()

class ToggleButtonPad(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master, buttonpad:tk.Widget):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.is_showing = True
        self.variable_button_text = tk.StringVar()

        self.button_toggle_pad = ttk.Button(self, textvariable=self.variable_button_text, command=self.click_button_toggle_pad)
        button_toggle_pad_package = [self.button_toggle_pad,(0,0),{"sticky":tk.NSEW}]

        self.buttonpad = buttonpad
        self.buttonpad_package = [self.buttonpad,(1,0)]
        
        self.columnrows_configure(self,[ROW,(0,0),(1,3)],[COLUMN,(0,3)])
        self.grid_widgets(button_toggle_pad_package, self.buttonpad_package)

        self.click_button_toggle_pad()

    def click_button_toggle_pad(self):
        if self.is_showing:
            self.is_showing = False
            self.variable_button_text.set("Mostrar Panel")
            self.buttonpad.grid_forget()
            self.button_toggle_pad.configure(width=80)
        else:
            self.is_showing = True
            self.variable_button_text.set("Ocultar Panel")
            self.grid_widgets(self.buttonpad_package)
            self.button_toggle_pad.configure(width=80)
            

class DemoToggleButtonPad(tk.Tk):
    def __init__(self):
        super().__init__()
        pad = ButtonPadOtherFolder(self)
        toggle = ToggleButtonPad(self, pad)
        toggle.grid(row=0, column=0, sticky=tk.NSEW)
        self.mainloop()

DemoToggleButtonPad()

class VisualButtonExplorer(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_pad = ButtonPadMainFolder(self)
        self.visual_explorer_main = VisualFolderExplorer(self, tk.VERTICAL)

        self.button_pad.button_select_folder_function = self.select_folder

        self.button_pad.pack()
        self.visual_explorer_main.pack(fill=tk.BOTH, expand=tk.TRUE)

    def select_folder(self):
        self.visual_explorer_main.display_folder(self.select_folder_path())
        self.visual_explorer_main.thumbnail_canvas.update_widget()

class DemoVisualButtonExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        vs_explorer = VisualButtonExplorer(self)
        vs_explorer.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()
 
#DemoVisualButtonExplorer()

class VisualButtonExplorerPanel(tf.tkFunctions,sf.sysFunctions,tk.Frame):
    def __init__(self, master):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_pad = ButtonPadOtherFolder(self)
        self.toggle_button_pad = ToggleButtonPad(self, self.button_pad)
        toggle_button_pad_package = [self.toggle_button_pad, (0,0)]

        self.visual_explorer_main = VisualFolderExplorer(self, tk.HORIZONTAL)
        self.visual_explorer_main.thumbnail_canvas.resizable = (False,1)
        canvas_main_páckage = [self.visual_explorer_main, (2,0), {"sticky":tk.NSEW}]

        self.button_pad.entry_folder_name['state'] = tk.DISABLED
        self.button_pad.button_select_folder_function = self.select_folder
        self.button_pad.button_change_folder_name_function = self.change_folder_name
        self.button_pad.check_change_file_name_function = self.change_file_names

        self.columnrows_configure(self, [ROW, (0,0),(1,0),(2,3)], [COLUMN, (0,3)])
        self.grid_widgets(toggle_button_pad_package, canvas_main_páckage)

    def select_folder(self):
        self.visual_explorer_main.display_folder(self.select_folder_path())
        print(self.visual_explorer_main.folder_path)
        self.button_pad.str_folder_name.set(os.path.basename(self.visual_explorer_main.folder_path))
        self.visual_explorer_main.thumbnail_canvas.update_widget()
    
    def change_folder_name(self):
        if self.button_pad.entry_folder_name['state'] == tk.DISABLED:
            self.button_pad.entry_folder_name['state'] = tk.NORMAL
            self.button_pad.button_change_folder_name.configure(text="Guardar cambio")
        else:
            self.button_pad.entry_folder_name['state'] = tk.DISABLED
            self.button_pad.button_change_folder_name.configure(text="Cambiar Nombre Carpeta")
            new_path = self.change_folder_name_os(self.visual_explorer_main.folder_path, self.button_pad.str_folder_name.get())
            self.visual_explorer_main.display_folder(new_path)

    def change_file_names(self):
        if self.button_pad.bool_change_file_name.get() and self.visual_explorer_main.folder_path:
            self.change_file_name_os(self.visual_explorer_main.folder_path)
            self.visual_explorer_main.refresh_display()

class DemoVisualButtonExplorerPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        vs_explorer = VisualButtonExplorerPanel(self)
        vs_explorer.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

#DemoVisualButtonExplorerPanel()

class MainApp(tf.tkFunctions, sf.sysFunctions, tk.Tk):
    def __init__(self):
        tf.tkFunctions.__init__(self)
        sf.sysFunctions.__init__(self)
        tk.Tk.__init__(self)
        self.title("APP V1")
        
        self.aux_container_list = []

        self.main_container = VisualButtonExplorer(self)
        self.main_container.button_pad.button_add_container_function = self.add_aux_containers
        self.main_container_package = [self.main_container, (0,0), {"sticky":tk.NSEW}]

        self.aux_container = ScrollableCanvas(self, tk.VERTICAL)
        self.aux_container.resizable = (False,1)
        self.aux_container_package = [self.aux_container, (0,1)]

        self.columnrows_configure(self, [ROW, (0,3)], [COLUMN, (0,3), (1,0)])
        self.grid_widgets(self.main_container_package)

    def add_aux_containers(self):
        temp_widget = VisualButtonExplorerPanel(self.aux_container)
        temp_widget.button_pad.button_remove_container_function = self.remove_aux_containers
        self.aux_container_list.append(temp_widget)
        self.aux_container.put_widgets_on_scrollable_frame(self.aux_container_list, add=True)
        self.aux_container.update_widget()
        if not self.aux_container.winfo_manager():
            self.grid_widgets(self.aux_container_package)
    
    def remove_aux_containers(self): print("REMOVER")

#app = MainApp()
#app.mainloop()