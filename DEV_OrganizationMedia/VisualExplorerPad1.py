import tkinter as tk

from myFunctions import tkFunctions, sysFunctions
from tkinter import ttk

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

        if self.scrollbar.state() == ('disabled',): self.scrollbar.grid_forget()
        else: self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        if self.refresh_size:
            self.max_columns = max(1, self.canvas.winfo_width() // self.refresh_size)
            if self.scrollable_frame.grid_size()[0] != self.max_columns:
                self.grid_widgets_list(self.scrollable_frame, self.scrollable_frame.winfo_children(), tk.HORIZONTAL, self.max_columns)

        self.canvas.update()
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
    
    def adjust_canvas_to_scrollable_frame(self): self.configure(width=self.scrollable_frame.winfo_width())

class ButtonPadV1(tkFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_deselect_folder = ttk.Button(self, text="Cerrar Carpeta")
        self.button_select_folder = ttk.Button(self, text="Seleccionar Carpeta")
        self.button_add_container = ttk.Button(self, text="Añadir Contenedor")  

        self.rowcolumn_configure(self, rows=1, columns=3, weights=0)
        self.button_deselect_folder.grid(row=0, column=0, ipady=4, ipadx=6, padx=15, pady=15)
        self.button_select_folder.grid(row=0, column=1, ipady=4, ipadx=6, padx=15, pady=15)
        self.button_add_container.grid(row=0, column=2, ipady=4, ipadx=6, padx=15, pady=15)

class VisualExplorerV1(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.reset_thumbnails_atributes()
        self.thumbnail_size = (80,80)
        self.function_on_proyection = lambda: None
        self.dinamic_canvas = False

        self.thumbnail_drag_data = {"x": 0, "y": 0}
        self.thumbnail_projection_correction = {"x": 0, "y": 0}
        self.thumbnail_projection = None

        self.button_pad = ButtonPadV1(self)
        self.thumbnail_canvas = ScrollableCanvasVertical(self)

        self.button_pad.button_select_folder.configure(command=self.click_button_select_folder)
        self.button_pad.button_deselect_folder.configure(command=self.click_button_deselect_folder)

        self.button_pad.pack()

        self.bind('<Configure>', lambda e: self.bind_function())

    def bind_function(self):
        if self.dinamic_canvas and self.thumbnail_canvas.scrollable_frame.winfo_children() == []: self.thumbnail_canvas.pack_forget()
        else: self.thumbnail_canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

    def click_button_select_folder(self):
        self.folder_path = self.select_folder_path()
        self.display_folder(self.folder_path)
        self.bind_function()

    def click_button_deselect_folder(self):
        self.thumbnail_canvas.clean_widgets_on_scrollable_frame()
        self.reset_thumbnails_atributes()
        self.bind_function()

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
                self.function_on_proyection(target_widget)

    def clear_thumbnail_canvas(self):
        self.reset_thumbnails_atributes()
        self.thumbnail_canvas.clean_widgets_on_scrollable_frame()

class DemoVisualExplorer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        app = VisualExplorerV1(self)
        app.dinamic_canvas = True
        app.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

#DemoVisualExplorer()
