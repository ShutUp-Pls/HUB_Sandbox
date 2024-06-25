import tkinter as tk

from myFunctions import tkFunctions, sysFunctions
from tkinter import ttk

from constants import *

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
        self.put_widgets_on_scrollable_frame([tk.Label(self.scrollable_frame)])
        self.update()
        self.update_scrollable()
    
    def adjust_canvas_to_scrollable_frame(self): self.canvas.configure(width=self.scrollable_frame.winfo_width())

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
        if self.scrollbar.state() == ('disabled',): self.scrollbar.grid_forget()
        else: self.scrollbar.grid(row=1, column=0, sticky=tk.EW)

        if self.refresh_size:
            self.max_rows = max(1, self.canvas.winfo_height() // self.refresh_size)
            if self.scrollable_frame.grid_size()[1] != self.max_rows:
                self.grid_widgets_list(self.scrollable_frame, self.scrollable_frame.winfo_children(), tk.VERTICAL, self.max_rows)

        self.canvas.update()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def put_widgets_on_scrollable_frame(self, widgets:list, max_rows:int=None):
        if max_rows == None:
            self.max_rows = (int(len(widgets)**(1/2)))
            self.grid_widgets_list(self.scrollable_frame, widgets, tk.VERTICAL, maximo=self.max_rows)
            self.refresh_size = self.row_size(self.scrollable_frame,1)
        else:
            self.max_rows = max_rows
            self.grid_widgets_list(self.scrollable_frame, widgets, tk.VERTICAL, maximo=self.max_rows)
            self.refresh_size = None
        self.update_scrollable()
        self.adjust_canvas_to_scrollable_frame()

    def clean_widgets_on_scrollable_frame(self):
        self.destroy_widgets_on(self.scrollable_frame)
        self.put_widgets_on_scrollable_frame([tk.Label(self.scrollable_frame)])
        self.update()
        self.update_scrollable()

    def adjust_canvas_to_scrollable_frame(self): self.canvas.configure(height=self.scrollable_frame.winfo_height())

class ScrollableCanvasFrame(tkFunctions, tk.Frame):
    def __init__(self, parent):
        tkFunctions.__init__(self)
        tk.Frame.__init__(self,parent)

        self.canvas = tk.Canvas(self)
        self.scrollbar_v = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_h = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.rowcolumn_configure(self, rows=2, columns=1, weights=3, specific_rows={2:0}, specific_columns={2:0})
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)
        self.scrollbar_v.grid(row=0, column=1, sticky=tk.NS)
        self.scrollbar_h.grid(row=1, column=0, sticky=tk.EW)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.canvas.bind('<Configure>', lambda e: self.update_scrollable())
        self.scrollable_frame.bind('<Configure>', lambda e: self.update_scrollable())

        self.canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        self.canvas.bind('<Enter>', lambda e: self.bind_to_mousewheel())
        self.canvas.bind('<Leave>', lambda e: self.unbind_from_mousewheel())
  
    def on_mousewheel_y(self, event): self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    def on_mousewheel_x(self, event): self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
    def unbind_from_mousewheel(self): self.canvas.unbind_all("<MouseWheel>")

    def bind_to_mousewheel(self):
        if (self.scrollbar_v.winfo_manager() and not self.scrollbar_h.winfo_manager()) or (not self.scrollbar_v.winfo_manager() and self.scrollbar_h.winfo_manager()):
            if self.scrollbar_v.winfo_manager() and self.scrollbar_v.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_y)
            elif self.scrollbar_h.winfo_manager() and self.scrollbar_h.state() != ('disabled',): self.canvas.bind_all("<MouseWheel>", self.on_mousewheel_x)
            else: self.unbind_from_mousewheel()
        else: self.unbind_from_mousewheel()

    def update_scrollable(self):
        if self.scrollbar_v.state() == ('disabled',): self.scrollbar_v.grid_forget()
        else: self.scrollbar_v.grid(row=0, column=1, sticky=tk.NS)
        if self.scrollbar_h.state() == ('disabled',): self.scrollbar_h.grid_forget()
        else: self.scrollbar_h.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))

    def put_widgets_on_scrollable_frame(self, widgets:list):
        self.grid_widgets_list(self.scrollable_frame, widgets, tk.HORIZONTAL, maximo=(int(len(widgets)**(1/2))))
        self.update()
        self.update_scrollable()

    def clean_widgets_on_scrollable_frame(self):
        self.destroy_widgets_on(self.scrollable_frame)
        self.put_widgets_on_scrollable_frame([tk.Label(self.scrollable_frame)])
        self.update()
        self.update_scrollable()

    def adjust_canvas_to_scrollable_frame(self): self.canvas.configure(height=self.scrollable_frame.winfo_height())

class DemoScrollableCanvas(tk.Tk):
    def __init__(self, label_range):
        super().__init__()
        self.geometry("300x300")
        scroll = ScrollableCanvasHorizontal(self)
        #scroll = ScrollableCanvasVertical(self)
        label_list = []
        for i in range(label_range):
            label = tk.Label(scroll.scrollable_frame, text=f"label_{i}", background="green")
            label_list.append(label)
        scroll.put_widgets_on_scrollable_frame(label_list)
        scroll.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

#DemoScrollableCanvas(100)

class DemoScrollableCanvasFrame(tk.Tk):
    def __init__(self, label_range):
        super().__init__()
        self.geometry("300x300")
        scroll = ScrollableCanvasFrame(self)
        label_list = []
        for i in range(label_range):
            label = tk.Label(scroll.scrollable_frame, text=f"label_{i}", background="green")
            label_list.append(label)
        scroll.put_widgets_on_scrollable_frame(label_list)
        scroll.pack(fill=tk.BOTH, expand=tk.TRUE)
        self.mainloop()

#DemoScrollableCanvasFrame(2000)

class ThumbnailScrollableCanvasVertical(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.thumbnail_size = TUPLE_THUMBNAIL_SIZE
        self.function_on_proyection = lambda: None
        self.reset_thumbnails_atributes()

        self.thumbnail_canvas = ScrollableCanvasVertical(self)
        self.thumbnail_canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.thumbnail_drag_data = {"x": 0, "y": 0}
        self.thumbnail_projection_correction = {"x": 0, "y": 0}
        self.thumbnail_projection = None

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
            self.add_bind_label_dict()

    def add_bind_label_dict(self):
        for path, label in self.thumbnail_label_dict.items():
                label.bind("<Button-1>", lambda e, lbl=label, fp=path:self.select_label(e, lbl, fp))
                label.bind("<Double-1>", lambda e, fp=path: self.open_file(fp))
                label.bind("<B1-Motion>", lambda e, : self.on_drag(e))
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
        print("SOLTADO")
        if self.thumbnail_projection:
            self.thumbnail_projection.destroy()
            self.update()
            target_widget = self.winfo_containing(event.x_root, event.y_root)
            if target_widget:
                self.function_on_proyection()

    def clear_thumbnail_canvas(self):
        self.reset_thumbnails_atributes()
        self.thumbnail_canvas.clean_widgets_on_scrollable_frame()

class DemoThumbnailScrollableCanvasVertical(tk.Tk):
    def __init__(self):
        super().__init__()
        
        explorer = ThumbnailScrollableCanvasVertical(self)
        explorer.pack(fill=tk.BOTH, expand=tk.TRUE)
        explorer.display_folder(EXAMPLE_FOLDER_PATH)

        self.mainloop()

#DemoThumbnailScrollableCanvasVertical()

class ThumbnailScrollableCanvasHorizontal(tkFunctions, sysFunctions, tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.thumbnail_size = TUPLE_THUMBNAIL_SIZE
        self.function_on_proyection = lambda: None
        self.reset_thumbnails_atributes()
        
        self.thumbnail_canvas = ScrollableCanvasHorizontal(self)
        self.thumbnail_canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.thumbnail_drag_data = {"x": 0, "y": 0}
        self.thumbnail_projection_correction = {"x": 0, "y": 0}
        self.thumbnail_projection = None

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
            self.thumbnail_canvas.put_widgets_on_scrollable_frame(list(self.thumbnail_label_dict.values()), 1)
            self.add_bind_label_dict()

    def add_bind_label_dict(self):
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
        print("SOLTADO")
        if self.thumbnail_projection:
            self.thumbnail_projection.destroy()
            self.update()
            target_widget = self.winfo_containing(event.x_root, event.y_root)
            if target_widget:
                self.function_on_proyection()

    def clear_thumbnail_canvas(self):
        self.reset_thumbnails_atributes()
        self.thumbnail_canvas.clean_widgets_on_scrollable_frame()

class DemoThumbnailScrollableCanvasHorizontal(tk.Tk):
    def __init__(self):
        super().__init__()
        
        explorer = ThumbnailScrollableCanvasHorizontal(self)
        explorer.display_folder(EXAMPLE_FOLDER_PATH)
        explorer.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.mainloop()

#DemoThumbnailScrollableCanvasHorizontal()