import queue
import traceback
import threading
import time

import tkinter as tk

from tkinter import ttk
from types import GeneratorType

from own.OwnExceptions import VerboseException

class OwnLoadingBar:
    local_thread = threading.local()

    def __init__(self, func):
        self.__try__ = func
        self.__except__ = None
        self.__callback__ = None

    def __call__(self, *args, icon_path=None, title="Progreso", optional="Procesando...",**kwargs):    
        self.progress_screen = ProgressScreen.show(icon_path=icon_path, title=title, optional=optional)

        def process_yield(iterator, local_current=0, local_step=1, global_total=1):
            for idx, (total_, optional) in enumerate(iterator):
                actual_step = local_step/total_
                actual_current = round(local_current + (actual_step * idx), 7)
                if isinstance(optional, str): self.progress_screen.progress_queue.put((actual_current, global_total, optional))
                elif isinstance(optional, GeneratorType): process_yield(optional, actual_current, actual_step, global_total)
                else: self.progress_screen.progress_queue.put((actual_current, global_total, None))

        def run_func():
            if not hasattr(self.local_thread, "decorator_stack"): self.local_thread.decorator_stack = []
            self.local_thread.decorator_stack.append(self.__try__.__name__)

            try: process_yield(self.__try__(*args, **kwargs))

            except Exception as error:
                tb_str = traceback.format_exc()
                log_description = f"[ERROR] Se produjo una excepción al ejecutar la función '{self.__try__.__name__}'\n\n[TRACEBACK DESCRIPTION]\n{tb_str}"

                if self.__except__: self.__except__(*args, **kwargs)
                if len(self.local_thread.decorator_stack) > 1: raise

                self.progress_screen.do_check = False
                VerboseException.show_error(min_log=str(error), ext_log=log_description, wait_window=True)

            finally:
                if self.local_thread.decorator_stack: self.local_thread.decorator_stack.pop()
                if len(self.local_thread.decorator_stack) == 0:
                    if self.__callback__: self.__callback__()

        active_thread = threading.Thread(target=run_func)

        if not hasattr(self.local_thread, "thread_stack"): self.local_thread.thread_stack = []
        self.local_thread.thread_stack.append(active_thread)

        active_thread.start()
        self.progress_screen.check_queue()

    def __del__(self): pass
    
    def __get__(self, instance, owner):
        def wrapper(*args, **kwargs): return self.__call__(instance, *args, **kwargs)
        if instance is None: return self
        
        wrapper.set_except = self.set_except
        wrapper.set_callback = self.set_callback_end
        wrapper.force_close = self.force_close
        
        return wrapper

    def set_except(self, except_func):
        if callable(except_func): self.__except__ = except_func

    def set_callback_end(self, callback_func):
        if callable(callback_func): self.__callback_end__ = callback_func

    def force_close(self):
        if hasattr(self.local_thread, "thread_stack"):
            while self.local_thread.thread_stack:
                thread = self.local_thread.thread_stack.pop()
                if thread.is_alive():
                    try: thread.join(timeout=1)
                    except RuntimeError: pass

        if hasattr(self.local_thread, "decorator_stack"): self.local_thread.decorator_stack.clear()

        if hasattr(self, 'progress_screen') and self.progress_screen:
            self.progress_screen.do_check = False
            self.progress_screen.float_var.set(100)

class ProgressScreen(tk.Toplevel):
    def __init__(self, master=None, title=None, optional=None, icon_app=None):
        self.optional_placeholder = optional

        if not master and not tk._default_root:
            self.main_root = tk.Tk()
            self.main_root.withdraw()
            self.own_root = True
        else:
            self.main_root = master if master else tk._default_root
            self.own_root = False

        super().__init__(self.main_root)

        self.title(title)
        self.geometry("400x150")
        if icon_app: self.iconphoto(False, tk.PhotoImage(file=icon_app))
        self.resizable(False, False)

        self.do_check = True

        self.label = ttk.Label(self, text=self.optional_placeholder)
        self.label.pack(pady=10)

        self.float_var = tk.DoubleVar(value=0.0)
        self.float_var.trace_add("write", self.update_progress)

        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

        self.progress_label = ttk.Label(self, text="0 de 0 elementos procesados")
        self.progress_label.pack(pady=10)

        self.progress_queue = queue.Queue()

    def check_queue(self):
        try:
            current, total, optional = self.progress_queue.get_nowait()
            progress_value = (current/total) * 100 if total > 0 else 0

            self.optional = optional
            self.current = current
            self.total = total
            self.float_var.set(progress_value)
        except queue.Empty: pass

        if self.do_check: self.after(1, self.check_queue)

    def update_progress(self, *args):
        if hasattr(self, "progress_bar") and self.progress_bar.winfo_exists(): self.progress_bar["value"] = self.float_var.get()

        if hasattr(self, "progress_label") and self.progress_label.winfo_exists():
            if self.optional is None: self.progress_label.config(text=f"{self.current} de {self.total} elementos procesados")
            else: self.progress_label.config(text=f"{self.optional}")

        self.update_idletasks()

        if self.float_var.get() == 100: self.close()

    def close(self):
        self.do_check = False
        self.grab_release()
        if self.own_root: self.main_root.destroy()
        self.destroy()

    @staticmethod
    def show(title=None, optional=None, master=None, icon_path=None):
        window = ProgressScreen(master=master, title=title, optional=optional, icon_app=icon_path)
        try: window.grab_set()
        except: pass
        window.update()
        window.update_idletasks()
        window.attributes("-topmost", True)
        return window
