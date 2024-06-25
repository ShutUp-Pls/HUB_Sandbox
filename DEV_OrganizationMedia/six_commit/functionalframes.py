import os

import tkinter as tk

from myFunctions import tkFunctions, sysFunctions
from VisualExplorerPad1 import ThumbnailScrollableCanvasVertical, ThumbnailScrollableCanvasHorizontal
from buttonpads import ButtonPadV1, ButtonPadV2, ButtonPadToggle
from constants import *
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, function_reload, function_change_name=lambda:None):
        super().__init__()
        self.function_reload = function_reload
        self.function_change_name = function_change_name
        
    def on_deleted(self, event):
        self.function_reload(os.path.dirname(event.src_path))

    def on_modified(self, event):
        self.function_reload(os.path.dirname(event.src_path))
        self.function_change_name()

class FunctionalFrameV1(tkFunctions,sysFunctions,tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_pad = ButtonPadV1(self)
        self.button_pad.button_select_folder.configure(command=self.select_folder)

        self.canvas = ThumbnailScrollableCanvasVertical(self)

        self.button_pad.pack()
        self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)

    def select_folder(self):
        try: self.stop_observer()
        except Exception: pass
        self.canvas.display_folder(self.select_folder_path())
        if self.canvas.folder_path: self.init_observer()

    def init_observer(self):
        self.event_handler = ChangeHandler(self.canvas.display_folder)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.canvas.folder_path, recursive=False)
        self.observer.start()

    def stop_observer(self):
        try: self.observer.join()
        except Exception: pass

class FunctionalFrameV2(tkFunctions,sysFunctions,tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_pad = ButtonPadV2(self)
        self.button_pad.entry_folder_name['state'] = tk.DISABLED
        self.button_pad.button_select_folder.configure(command=self.select_folder)
        self.button_pad.button_change_folder_name.configure(command=self.change_folder_name)
        self.button_pad.check_change_file_name.configure(command=self.change_file_names)
        self.button_pad.button_remove_container.configure(command=self.clear_container)

        self.canvas = ThumbnailScrollableCanvasHorizontal(self)

        self.button_pad.pack()
    
    def select_folder(self):
        try: self.stop_observer()
        except Exception: pass
        self.canvas.display_folder(self.select_folder_path())
        if self.canvas.folder_path:
            self.button_pad.str_folder_name.set(os.path.basename(self.canvas.folder_path))
            self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)
            self.init_observer()

    def init_observer(self):
        self.event_handler = ChangeHandler(self.canvas.display_folder, self.change_file_names)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.canvas.folder_path, recursive=False)
        self.observer.start()

    def stop_observer(self):
        self.observer.stop()
        try: self.observer.join()
        except Exception: pass

    def change_folder_name(self):
        self.stop_observer()
        if self.button_pad.entry_folder_name['state'] == tk.DISABLED:
            self.button_pad.entry_folder_name['state'] = tk.NORMAL
            self.button_pad.button_change_folder_name.configure(text="Guardar cambio")
        else:
            self.button_pad.entry_folder_name['state'] = tk.DISABLED
            self.button_pad.button_change_folder_name.configure(text="Cambiar Nombre Carpeta")
            new_path = self.change_folder_name_os(self.canvas.folder_path, self.button_pad.str_folder_name.get())
            self.canvas.display_folder(new_path)
            if self.button_pad.bool_change_file_name.get() and self.canvas.folder_path: self.change_file_names()
        self.init_observer()

    def change_file_names(self):
        self.stop_observer()
        if self.button_pad.bool_change_file_name.get() and self.canvas.folder_path:
            self.change_file_name_os(self.canvas.folder_path)
        self.canvas.display_folder(self.canvas.folder_path)
        self.init_observer()

    def clear_container(self):
        self.canvas.clear_thumbnail_canvas()
        self.canvas.pack_forget()
        self.button_pad.str_folder_name.set('')
        self.button_pad.bool_change_file_name.set(tk.FALSE)
        self.canvas.thumbnail_canvas.update_scrollable()


class FunctionalFrameV2Dinamic(tkFunctions,sysFunctions,tk.Frame):
    def __init__(self, master):
        tkFunctions.__init__(self)
        sysFunctions.__init__(self)
        tk.Frame.__init__(self, master)

        self.button_pad_toggle = ButtonPadToggle(self, ButtonPadV2)
        self.button_pad_toggle.button_pad.entry_folder_name['state'] = tk.DISABLED
        self.button_pad_toggle.button_pad.button_select_folder.configure(command=self.select_folder)
        self.button_pad_toggle.button_pad.button_change_folder_name.configure(command=self.change_folder_name)
        self.button_pad_toggle.button_pad.check_change_file_name.configure(command=self.change_file_names)
        self.button_pad_toggle.button_pad.button_remove_container.configure(command=self.clear_container)

        self.canvas = ThumbnailScrollableCanvasHorizontal(self)
        self.button_pad_toggle.pack()

        self.bind('<Configure>', lambda e: self.bind_self())

    def bind_self(self):
        self.canvas.thumbnail_projection_correction["y"] = self.button_pad_toggle.button_pad.winfo_height()
        if self.canvas.folder_path: self.button_pad_toggle.text_show_panel = os.path.basename(self.canvas.folder_path)
        else: self.button_pad_toggle.text_show_panel = "Mostrar Panel"
    
    def select_folder(self):
        try: self.stop_observer()
        except Exception: pass
        self.canvas.display_folder(self.select_folder_path())
        if self.canvas.folder_path:
            self.button_pad_toggle.button_pad.str_folder_name.set(os.path.basename(self.canvas.folder_path))
            self.canvas.pack(fill=tk.BOTH, expand=tk.TRUE)
            self.init_observer()

    def init_observer(self):
        self.event_handler = ChangeHandler(self.canvas.display_folder, self.change_file_names)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.canvas.folder_path, recursive=False)
        self.observer.start()

    def stop_observer(self):
        self.observer.stop()
        try: self.observer.join()
        except Exception: pass

    def change_folder_name(self):
        self.stop_observer()
        if self.button_pad_toggle.button_pad.entry_folder_name['state'] == tk.DISABLED:
            self.button_pad_toggle.button_pad.entry_folder_name['state'] = tk.NORMAL
            self.button_pad_toggle.button_pad.button_change_folder_name.configure(text="Guardar cambio")
        else:
            self.button_pad_toggle.button_pad.entry_folder_name['state'] = tk.DISABLED
            self.button_pad_toggle.button_pad.button_change_folder_name.configure(text="Cambiar Nombre Carpeta")
            new_path = self.change_folder_name_os(self.canvas.folder_path, self.button_pad_toggle.button_pad.str_folder_name.get())
            self.canvas.display_folder(new_path)
            if self.button_pad_toggle.button_pad.bool_change_file_name.get() and self.canvas.folder_path: self.change_file_names()
        self.init_observer()

    def change_file_names(self):
        self.stop_observer()
        if self.button_pad_toggle.button_pad.bool_change_file_name.get() and self.canvas.folder_path:
            self.change_file_name_os(self.canvas.folder_path)
        self.canvas.display_folder(self.canvas.folder_path)
        self.init_observer()

    def clear_container(self):
        self.canvas.clear_thumbnail_canvas()
        self.canvas.pack_forget()
        self.button_pad_toggle.button_pad.str_folder_name.set('')
        self.button_pad_toggle.button_pad.bool_change_file_name.set(tk.FALSE)
        self.canvas.thumbnail_canvas.update_scrollable()

class DemoFunctionalFrame(tk.Tk):
    def __init__(self):
        super().__init__()

        frame = FunctionalFrameV2Dinamic(self)
        frame.pack(fill=tk.BOTH, expand=tk.TRUE)

        self.mainloop()

#DemoFunctionalFrame()
