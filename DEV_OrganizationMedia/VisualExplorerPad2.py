import os

import tkinter as tk

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from myFunctions import tkFunctions, sysFunctions
from tkinter import ttk

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, object_gui):
        super().__init__()
        self.object_gui = object_gui
        
    def on_deleted(self, event):
        if not self.object_gui.on_procesing:
            self.object_gui.display_folder(self.object_gui.folder_path)

    def on_modified(self, event):
        if not self.object_gui.on_procesing:
            self.object_gui.display_folder(self.object_gui.folder_path)
            if self.object_gui.button_pad_toggle.button_pad.bool_change_file_name.get() and self.object_gui.folder_path:
                self.object_gui.change_file_name_os(self.object_gui.folder_path)

class ScrollableCanvasHorizontal(tkFunctions, tk.Frame):
    def __init__(self, parent):
        tkFunctions.__init__(self)
        tk.Frame.__init__(self,parent)

        self.refresh_size = None
        self.max_rows = None

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.rowcolumn_configure(self, rows=2, columns=1, weights=3, specific_rows={2:0})
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrollbar.grid(row=1, column=0, sticky=tk.EW)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.bind('<Configure>', lambda e: self.update_scrollable())
        self.scrollable_frame.bind('<Configure>', lambda e: self.update_scrollable())

        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
        self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())
  
    def on_mousewheel(self, event): self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    def unbind_from_mousewheel(self): self.canvas.unbind_all("<MouseWheel>")
    def bind_to_mousewheel(self):
        if self.scrollbar.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        else: self.unbind_from_mousewheel()

    def update_scrollable(self):
        self.update()

        if self.scrollbar.state() == ('disabled',): self.scrollbar.grid_forget()
        else: self.scrollbar.grid(row=1, column=0, sticky=tk.EW)

        if self.refresh_size:
            self.max_rows = max(1, self.canvas.winfo_height() // self.refresh_size)
            if self.scrollable_frame.grid_size()[1] != self.max_rows:
                self.grid_widgets_list(self.scrollable_frame, self.scrollable_frame.winfo_children(), tk.VERTICAL, self.max_rows)

        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def put_widgets_on_scrollable_frame(self, widgets:list):
        if self.max_rows == None:
            self.grid_widgets_list(self.scrollable_frame, widgets, tk.VERTICAL, maximo=(int(len(widgets)**(1/2))))
            self.refresh_size = self.row_size(self.scrollable_frame,1)
        else:
            self.grid_widgets_list(self.scrollable_frame, widgets, tk.VERTICAL, maximo=self.max_rows)
            self.refresh_size = None
        self.update_scrollable()
        self.adjust_canvas_to_scrollable_frame()
        self.update_scrollable()

    def clean_widgets_on_scrollable_frame(self):
        self.destroy_widgets_on(self.scrollable_frame)
        self.update()
        self.update_scrollable()
    
    def adjust_canvas_to_scrollable_frame(self): self.canvas.configure(height=self.scrollable_frame.winfo_height())

class ScrollableCanvasVertical(tkFunctions, tk.Frame):
    def __init__(self, parent):
        tkFunctions.__init__(self)
        tk.Frame.__init__(self,parent)

        self.refresh_size = None
        self.max_columns = None

        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.rowcolumn_configure(self, rows=1, columns=2, weights=3, specific_columns={2:0})
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.bind('<Configure>', lambda e: self.update_scrollable())
        self.scrollable_frame.bind('<Configure>', lambda e: self.update_scrollable())

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
        self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())
  
    def on_mousewheel(self, event): self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def unbind_from_mousewheel(self): self.canvas.unbind_all("<MouseWheel>")
    def bind_to_mousewheel(self):
        if self.scrollbar.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        else: self.unbind_from_mousewheel()

    def update_scrollable(self):
        self.update()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

        if self.scrollbar.state() == ('disabled',): self.scrollbar.grid_forget()
        else: self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        if self.refresh_size:
            self.max_columns = max(1, self.canvas.winfo_width() // self.refresh_size)
            if self.scrollable_frame.grid_size()[0] != self.max_columns:
                self.grid_widgets_list(self.scrollable_frame, self.scrollable_frame.winfo_children(), tk.HORIZONTAL, self.max_columns)

        self.update()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def put_widgets_on_scrollable_frame(self, widgets:list, max_columns:int=None):
        if max_columns == None:
            self.max_columns = (int(len(widgets)**(1/2)))
            self.grid_widgets_list(self.scrollable_frame, widgets, tk.HORIZONTAL, maximo=self.max_columns)
            self.refresh_size = self.column_size(self.scrollable_frame,1)
        else:
            self.max_columns = max_columns
            self.grid_widgets_list(self.scrollable_frame, widgets, tk.HORIZONTAL, maximo=self.max_columns)
            self.refresh_size = None
        self.update_scrollable()
        self.adjust_canvas_to_scrollable_frame()
        self.update_scrollable()

    def clean_widgets_on_scrollable_frame(self):
        self.destroy_widgets_on(self.scrollable_frame)
        self.update()
        self.update_scrollable()
    
    def adjust_canvas_to_scrollable_frame(self): self.canvas.configure(height=self.canvas.winfo_height())

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

        self.rowcolumn_configure(self, rows=4, columns=2, weights=0)
        self.button_select_folder.grid(row=0, column=0, rowspan=2, ipadx=6, ipady=4, padx=15, pady=15)
        self.button_remove_container.grid(row=2, column=0, rowspan=2, ipadx=6, ipady=4, padx=15, pady=15)
        self.button_change_folder_name.grid(row=0, column=1, columnspan=2, ipadx=6, ipady=4)
        self.entry_folder_name.grid(row=1, column=1, columnspan=2, rowspan=2, padx=15, ipadx=30, ipady=5)
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
        
        self.rowcolumn_configure(self, rows=2, columns=1, weights=0)
        self.button_toggle_function.grid(row=0, column=0)
        self.button_pad.grid(row=1, column=0, sticky=tk.EW)

        self.button_pad.bind('<Configure>', lambda e: self.resize_button())
    
    def resize_button(self):
        if self.fixing_size:
            self.fixing_size = False
            self.button_toggle_function.grid_configure(ipadx=((self.button_pad.winfo_reqwidth()-self.button_toggle_function.winfo_reqwidth())//2))

    def click_button_toggle_pad(self):
        if self.button_pad.winfo_manager():
            self.button_pad.grid_forget()
            self.button_toggle_function.configure(text=self.text_show_panel)
        else:
            self.button_pad.grid(row=1, column=0, sticky=tk.EW)
            self.button_toggle_function.configure(text=self.text_hide_panel)

class VisualExplorerV2(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.reset_thumbnails_atributes()
        self.thumbnail_size = (80,80)
        self.function_on_proyection = lambda: None
        self.dinamic_canvas = False
        self.on_procesing = False

        self.thumbnail_drag_data = {"x": 0, "y": 0}
        self.thumbnail_projection_correction = {"x": 0, "y": 0}
        self.thumbnail_projection = None

        self.button_pad_toggle = ButtonPadToggle(self, ButtonPadV2)
        self.thumbnail_canvas = ScrollableCanvasHorizontal(self)

        self.thumbnail_canvas.max_rows = 1

        self.button_pad_toggle.button_pad.entry_folder_name['state'] = tk.DISABLED
        self.button_pad_toggle.button_pad.button_select_folder.configure(command=self.click_button_select_folder)
        self.button_pad_toggle.button_pad.button_change_folder_name.configure(command=self.click_button_change_folder_name)
        self.button_pad_toggle.button_pad.check_change_file_name.configure(command=self.detect_check_change_file_name)
        self.button_pad_toggle.button_pad.button_remove_container.configure(command=self.click_button_deselect_folder)

        self.rowcolumn_configure(self, rows=2, columns=1, weights=0, specific_columns={1:1})
        self.button_pad_toggle.grid(row=0, column=0)

        self.bind('<Configure>', lambda e: self.bind_function())

    def bind_function(self):
        #self.thumbnail_projection_correction["y"] = self.button_pad_toggle.button_pad.winfo_height()
        if self.folder_path: self.button_pad_toggle.text_show_panel = os.path.basename(self.folder_path)
        else: self.button_pad_toggle.text_show_panel = "Mostrar Panel"

        if self.dinamic_canvas and self.thumbnail_canvas.scrollable_frame.winfo_children() == []: self.thumbnail_canvas.pack_forget()
        else: self.thumbnail_canvas.grid(row=1, column=0, sticky=tk.EW)

    def observer_init(self):
        self.event_handler = ChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.folder_path, recursive=False)
        self.observer.start()

    def observer_stop(self):
        self.observer.stop()
        try: self.observer.join()
        except Exception: pass

    def click_button_change_folder_name(self):
        #self.observer_stop()
        if self.button_pad_toggle.button_pad.entry_folder_name['state'] == tk.DISABLED:
            self.button_pad_toggle.button_pad.entry_folder_name['state'] = tk.NORMAL
            self.button_pad_toggle.button_pad.button_change_folder_name.configure(text="Guardar cambio")
        else:
            self.button_pad_toggle.button_pad.entry_folder_name['state'] = tk.DISABLED
            self.button_pad_toggle.button_pad.button_change_folder_name.configure(text="Cambiar Nombre Carpeta")
            self.on_procesing = True
            new_path = self.change_folder_name_os(self.folder_path, self.button_pad_toggle.button_pad.str_folder_name.get())
            self.display_folder(new_path)
            self.update()
            if self.button_pad_toggle.button_pad.bool_change_file_name.get() and self.folder_path: self.detect_check_change_file_name()
            self.on_procesing = False
        #self.observer_init()

    def detect_check_change_file_name(self):
        #self.observer_stop()
        self.on_procesing = True
        if self.button_pad_toggle.button_pad.bool_change_file_name.get() and self.folder_path:
            self.change_file_name_os(self.folder_path)
        self.display_folder(self.folder_path)
        self.on_procesing = False
        #self.observer_init()

    def clear_container(self):
        self.clear_thumbnail_canvas()
        self.pack_forget()
        self.button_pad_toggle.button_pad.str_folder_name.set('')
        self.button_pad_toggle.button_pad.bool_change_file_name.set(tk.FALSE)
        self.thumbnail_canvas.update_scrollable()

    def click_button_select_folder(self):
        #try: self.observer_stop()
        #except Exception: pass
        self.on_procesing = True
        self.folder_path = self.select_folder_path()
        if self.folder_path:
            self.button_pad_toggle.button_pad.str_folder_name.set(os.path.basename(self.folder_path))
            self.pack(fill=tk.BOTH, expand=tk.TRUE)
            self.observer_init()
        
        self.display_folder(self.folder_path)
        self.bind_function()
        self.on_procesing = False

    def click_button_deselect_folder(self):
        self.thumbnail_canvas.clean_widgets_on_scrollable_frame()
        self.reset_thumbnails_atributes()
        self.bind_function()
        self.observer_stop()

    def reset_thumbnails_atributes(self):
        self.folder_path = None
        self.selected_file_path = None
        self.selected_label = None
        self.thumbnail_dict = {}
        self.thumbnail_label_dict = {}

    def display_folder(self, path:str=None):
        if path:
            self.folder_path = path
            self.selected_file_path = None
            self.selected_label = None

            self.thumbnail_dict = self.generate_thumbnail_dict(self.folder_path, self.thumbnail_size, self.thumbnail_dict)
            self.thumbnail_label_dict = self.generate_thumbnail_label_dict(self.thumbnail_canvas.scrollable_frame, self.thumbnail_dict, self.thumbnail_size[0], self.thumbnail_label_dict)
            self.thumbnail_canvas.put_widgets_on_scrollable_frame(list(self.thumbnail_label_dict.values()))
            for path, label in self.thumbnail_label_dict.items():
                label.bind("<Button-1>", lambda e, lbl=label, fp=path:self.select_label(e, lbl, fp))
                label.bind("<Double-1>", lambda e, fp=path: self.open_file(fp))
                label.bind("<B1-Motion>", lambda e: self.on_drag(e))
                label.bind("<ButtonRelease-1>", self.on_release)

    def select_label(self, event, label:tk.Widget, file_path):
        try:
            if self.selected_label: self.selected_label.config(borderwidth=0, relief=tk.FLAT)
            label.config(borderwidth=2, relief=tk.SOLID)
            self.selected_label = label
            self.selected_file_path = file_path

            self.thumbnail_drag_data["x"] = event.x
            self.thumbnail_drag_data["y"] = event.y
            self.thumbnail_projection = self.duplicate_label(self.selected_label)
        except Exception as e: print(f"Error seleccionar el archivo archivo {file_path}: {e}")

    def on_drag(self, event):
        if self.thumbnail_projection:            
            new_x = event.x_root - self.winfo_rootx() - self.thumbnail_drag_data["x"] + self.thumbnail_projection_correction["x"]
            new_y = event.y_root - self.winfo_rooty() - self.thumbnail_drag_data["y"] + self.thumbnail_projection_correction["y"]
            self.thumbnail_projection.place(x=new_x, y=new_y)

    def on_release(self, event):
        if self.thumbnail_projection:
            self.thumbnail_projection.destroy()
            self.update()
            target_widget = self.winfo_containing(event.x_root, event.y_root)
            if target_widget:
                print(f"Soltado sobre: {target_widget}")
                self.function_on_proyection()

    def clear_thumbnail_canvas(self):
        self.reset_thumbnails_atributes()
        self.button_pad_toggle.button_pad.str_folder_name.set('')
        self.button_pad_toggle.button_pad.bool_change_file_name.set(tk.FALSE)
        self.thumbnail_canvas.clean_widgets_on_scrollable_frame()

class VisualExplorerV3(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.remove_function = self.click_remove_container
        self.add_function = self.click_add_container
        
        self.container_list = []
        self.container = ScrollableCanvasVertical(self)    

    def click_add_container(self):
        temp_visual_explorer = VisualExplorerV2(self.container.scrollable_frame)
        temp_visual_explorer.button_pad_toggle.button_pad.button_remove_container.configure(command=lambda wdgt=temp_visual_explorer: self.remove_function(wdgt))
        temp_visual_explorer.dinamic_canvas = True
        temp_visual_explorer.bind('<Configure>', lambda e: self.container.update_scrollable())
        temp_visual_explorer.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.container_list.append(temp_visual_explorer)
        if not self.container.winfo_manager(): self.container.pack(fill=tk.Y, expand=tk.TRUE)

    def click_remove_container(self, widget):
        self.container_list.remove(widget)
        widget.destroy()
        if self.container_list == []:
            self.container.pack_forget()

class DemoVisualExplorer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        app = VisualExplorerV3(self)
        app.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

#DemoVisualExplorer()