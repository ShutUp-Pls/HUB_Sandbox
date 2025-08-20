import traceback
import threading

import tkinter as tk

from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import Text
from tkinter import messagebox
from tkinter import filedialog

from util.func_tools import TextTools, TkTools

class VerboseExceptionHandler:
    local_thread = threading.local()

    def __init__(self, func):
        self.__try__ = func
        self.__except__ = None

    def __call__(self, *args, **kwargs):        
        if not hasattr(self.local_thread, 'decorator_stack'): self.local_thread.decorator_stack = []
        self.local_thread.decorator_stack.append(self.__try__.__name__)

        result = None
        try: result = self.__try__(*args, **kwargs)

        except Exception as error:
            tb_str = traceback.format_exc()
            log_description = f"[ERROR] Se produjo una excepción al ejecutar la función '{self.__try__.__name__}'\n\n[TRACEBACK DESCRIPTION]\n{tb_str}"

            if self.__except__: result = self.__except__(*args, **kwargs)
            if len(self.local_thread.decorator_stack) > 1: raise

            VerboseException.show_error(min_log=str(error), ext_log=log_description)

        finally: self.local_thread.decorator_stack.pop()

        return result
    
    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs): return self.__call__(instance, *args, **kwargs)
        if instance is None: return self
        
        wrapper.set_except = self.set_except
        
        return wrapper

    def set_except(self, except_func):
        if callable(except_func): self.__except__ = except_func

class VerboseException(tk.Toplevel):
    def __init__(self, master=None, title=None, min_log=None, ext_log=None, type_dialog="error"):
        if not master and not tk._default_root:
            self.main_root = tk.Tk()
            self.main_root.withdraw()
            self.own_root = True
        else:
            self.main_root = master if master else tk._default_root
            self.own_root = False

        super().__init__(self.main_root)
        self.protocol("WM_DELETE_WINDOW", self.__close_window)

        # ===========================================================
        # CONFIGURACIONES PREVIAS
        # ===========================================================

        if type_dialog == "error":
            icon_path = "src\\error_icon.png"
            if not title: self.title_str = "Error:"

        elif type_dialog == "info":
            icon_path = "src\\info_icon.png"
            if not title: self.title_str = "Información:"

        else: icon_path = "src\\info_icon.png"

        self.iconphoto(False, tk.PhotoImage(file=icon_path))

        if min_log: self.min_log = min_log
        else: self.min_log = "Desconocido."

        if ext_log: self.ext_log = ext_log
        else: self.ext_log = "No hay más información."

        self.title(self.title_str)
        self.resizable(width=False, height=False)

        self.is_extended = False
        wrapped_text = TextTools.wrap_text_width(self.min_log, 60)

        # ===========================================================
        # CONSTRUIR TOP FRAME
        # ===========================================================

        self.top_frame = tk.Frame(self, bg="white")
        self.icon_label = tk.Label(self.top_frame, bg="white")
        try:
            image = Image.open(icon_path)
            image = image.resize((32, 32), Image.Resampling.LANCZOS)
            self.icon_image_tk = ImageTk.PhotoImage(image)
            self.icon_label.config(image=self.icon_image_tk)
        except: pass
        self.min_log_label = ttk.Label(self.top_frame, text=wrapped_text, justify=tk.LEFT, background="white")

        self.top_frame.pack(fill=tk.X, expand=True)
        self.icon_label.grid(row=0, column=0, padx=(20,5), pady=10)
        self.min_log_label.grid(row=0, column=1, padx=(5,20), pady=10)

        # ===========================================================
        # CONSTRUIR MIDDLE FRAME
        # ===========================================================

        self.middle_frame = tk.Frame(self)
        self.accept_button = ttk.Button(self.middle_frame, text="Aceptar", command=self.__close_window)
        self.more_button = ttk.Button(self.middle_frame, text="Ver detalles", command=self.__toggle_details)

        self.middle_frame.pack()
        self.accept_button.pack(padx=5, pady=5, side=tk.RIGHT)
        self.more_button.pack(padx=5, pady=5, side=tk.RIGHT)

        # ===========================================================
        # CONSTRUIR BOTTOM FRAME
        # ===========================================================

        self.update_idletasks()

        self.bottom_frame = tk.Frame(self)
        self.details_text = Text(self.bottom_frame, wrap=tk.WORD, state=tk.DISABLED)
        size = TkTools.calculate_text_width(self.details_text, self.top_frame.winfo_reqwidth())
        self.details_text.configure(height=int((size*10)/80), width=size)
        self.save_button = ttk.Button(self.bottom_frame,text="Guardar como...", command=self.__save_log)

        self.bottom_frame.pack()
        self.details_text.pack()
        self.save_button.pack(padx=10, pady=(0,10), side=tk.RIGHT)

        # ===========================================================
        # CONFIGURACIONES ADICIONALES
        # ===========================================================

        self.update()
        self.update_idletasks()

        # Dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Dimensiones de la ventana
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Cálculo de la posición centrada
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2

        # Ajusta la geometría para centrar la ventana
        self.open_geometry = f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}"
        self.close_geometry = f"{self.winfo_reqwidth()}x{self.top_frame.winfo_reqheight()+self.middle_frame.winfo_reqheight()}"
        self.geometry(f"{self.close_geometry}+{position_x}+{position_y}")
        self.attributes("-topmost", True)

    def __toggle_details(self):
        if self.is_extended:
            self.more_button.config(text="Ver detalles")
            self.geometry(self.close_geometry)
        else:
            self.details_text.config(state=tk.NORMAL)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert("1.0", self.ext_log)
            self.details_text.config(state=tk.DISABLED)
            self.more_button.config(text="Ocultar detalles")
            self.geometry(self.open_geometry)

        self.is_extended = not self.is_extended

    def __save_log(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"), ("All files", "*.*")],title="Guardar como...",parent=self)

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file: file.write(self.ext_log)
                messagebox.showinfo("Exito", f"Log guardado exitosamente en:\n{file_path}")

            except Exception as error: messagebox.showerror("Error", f"No se pudo guardar el log:\n{error}")

    def __show(self, grab_set=None, wait_window=None):
        if grab_set:
            try: self.grab_set()
            except: pass
        if wait_window: self.wait_window()

    def __close_window(self):
        self.grab_release()
        if self.own_root: self.main_root.destroy()
        self.destroy()

    @staticmethod
    def show_error(min_log=None, ext_log=None, title=None, master=None, grab_set=None, wait_window=None):
        window = VerboseException(master=master, title=title, min_log=min_log, ext_log=ext_log, type_dialog="error")
        window.__show(grab_set=grab_set)

    @staticmethod
    def show_info(min_log=None, ext_log=None, title=None, master=None, grab_set=None, wait_window=None):
        window = VerboseException(master=master, title=title, min_log=min_log, ext_log=ext_log, type_dialog="info")
        window.__show(grab_set=grab_set)