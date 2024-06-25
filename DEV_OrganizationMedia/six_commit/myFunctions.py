import os

import tkinter as tk

from tkinter import filedialog
from PIL import ImageTk, Image
from constants import *

class tkFunctions:
    def __init__(self): pass
    
    def grid_widgets_list(self, container:tk.Widget, widget_list:list, direction=tk.HORIZONTAL, maximo:int=None, **kwargs):
        if direction not in [tk.HORIZONTAL, tk.VERTICAL]: raise ValueError("La dirección debe ser tk.HORIZONTAL o tk.VERTICAL")
        fila, columna = 0, 0
        widgets_posicionados = []
        current_widgets = container.winfo_children()
        for index, widget in enumerate(widget_list):
            widget.grid_forget()
            widget.grid(row=fila, column=columna, **kwargs)
            widgets_posicionados.append(widget)
            if direction == tk.HORIZONTAL:
                columna += 1
                if maximo is not None and columna >= maximo:
                    columna = 0
                    fila += 1
            else:
                fila += 1
                if maximo is not None and fila >= maximo:
                    fila = 0
                    columna += 1
        for widget in current_widgets:
            if widget not in widgets_posicionados:
                widget.destroy()

    def rowcolumn_configure(self,container:tk.Widget, rows:int, columns:int, weights=1, specific_rows:dict=None, specific_columns:dict=None, **kwargs):
        for i in range(rows):
            temp_weight = specific_rows[i+1] if specific_rows and (i+1) in specific_rows else weights
            container.grid_rowconfigure(i, weight=temp_weight, **kwargs)
        for j in range(columns):
            temp_weight = specific_columns[j+1] if specific_columns and (j+1) in specific_columns else weights
            container.grid_columnconfigure(j, weight=temp_weight, **kwargs)

    def row_size(self, container:tk.Widget, row:int):
        container.update()
        bbox = container.grid_bbox(0, row-1)
        if bbox:
            _, _, _, height = bbox
            return height
        return None

    def column_size(self, container:tk.Widget, column:int):
        container.update()
        bbox = container.grid_bbox(column-1, 0)
        if bbox:
            _, _, width, _ = bbox
            return width
        return None
            
    def calculate_widget_size(self, widget:tk.Widget, side=tk.BOTH, package:str=GRID):
        if side == tk.HORIZONTAL:
            wid_width = widget.winfo_width()
            if package == GRID:
                pex_width = widget.grid_info()["padx"]
                pix_width = widget.grid_info()["ipadx"]
            elif package == PACK:
                pex_width = widget.pack_info()["padx"]
                pix_width = widget.pack_info()["ipadx"]
            elif package == PLACE:
                pex_width = widget.place_info()["padx"]
                pix_width = widget.place_info()["ipadx"]
            return wid_width + pex_width*2 + pix_width*2
        elif side == tk.VERTICAL:
            wid_height = widget.winfo_height()
            if package == GRID:
                pex_height = widget.grid_info()["pady"]
                pix_height = widget.grid_info()["ipady"]
            elif package == PACK:
                pex_height = widget.pack_info()["pady"]
                pix_height = widget.pack_info()["ipady"]
            elif package == PLACE:
                pex_height = widget.place_info()["pady"]
                pix_height = widget.place_info()["ipady"]
            return wid_height + pex_height*2 + pix_height*2
        elif side == tk.BOTH:
            width = self.calculate_widget_size(widget, tk.HORIZONTAL, package)
            height = self.calculate_widget_size(widget, tk.VERTICAL, package)
            return (width, height)

    def generate_thumbnail_label_dict(self, master:tk.Widget, thumbnail_dict:dict, thumbnail_size:int=50, existing_thumbnail_dict:dict=None):
        if existing_thumbnail_dict is None: existing_thumbnail_dict = {}
        updated_thumbnail_dict = {}

        for file_path, image in thumbnail_dict.items():
            if file_path in existing_thumbnail_dict: updated_thumbnail_dict[file_path] = existing_thumbnail_dict[file_path]
            else:
                try:
                    photo = ImageTk.PhotoImage(image)
                    label = tk.Label(master, image=photo, text=os.path.basename(file_path), compound=tk.TOP, wraplength=thumbnail_size)
                    label.image = photo  # Guardar referencia para evitar que la imagen sea recolectada por el garbage collector
                    updated_thumbnail_dict[file_path] = label
                except Exception as e: print(f"No se puede crear la etiqueta para {file_path}: {e}")

        for file_path in list(existing_thumbnail_dict.keys()):
            if file_path not in thumbnail_dict:
                existing_thumbnail_dict[file_path].destroy()

        return updated_thumbnail_dict
    
    def forget_widgets_on(self, widget:tk.Widget):
        for w in widget.winfo_children():
            widget_manager = w.winfo_manager()
            if widget_manager == GRID: w.grid_forget()
            elif widget_manager == PACK: w.pack_forget()
            elif widget_manager == PLACE: w.place_forget()

    def destroy_widgets_on(self, widget:tk.Widget):
        for w in widget.winfo_children(): w.destroy()

    def duplicate_label(self, label:tk.Widget):
        attributes = {
            'text': label['text'],
            'image': label['image'],
            'compound': label['compound'],
            'font': label['font'],
            'fg': label['fg'],
            'bg': label['bg'],
            'relief': label['relief'],
            'bd': label['bd'],
            'width': label['width'],
            'height': label['height'],
            'anchor': label['anchor'],
            'justify': label['justify'],
            'padx': label['padx'],
            'pady': label['pady'],
            'compound': label['compound'],
            'wraplength': label['wraplength']
        }
        new_label = tk.Label(label.winfo_toplevel(), **attributes)
        new_label.pack_forget()

        return new_label
    
    def childs_size_on_manager(self, widget:tk.Widget):
        width, height = 0, 0
        for child in widget.winfo_children():
            if child.winfo_manager():
                print(f"hijo:{child}\nmanager: {child.winfo_manager()}")
                width += child.winfo_width()
                height += child.winfo_height()
        return width, height

    def is_ancestor(self, ancestor, widget):
        current_widget = widget
        while current_widget is not None:
            if current_widget == ancestor:
                return True
            current_widget = current_widget.master
        return False
    
class sysFunctions:
    def __init__(self): pass

    def generate_thumbnail_dict(self, path:os.PathLike, size:tuple = (50, 50), existing_image_dict:dict = None):
        if existing_image_dict is None: existing_image_dict = {}
        updated_image_dict = {}

        try: files = os.listdir(path)
        except Exception as e:
            print(f"No se puede listar los archivos en el directorio {path}: {e}")
            return updated_image_dict
        
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if file_path in existing_image_dict: updated_image_dict[file_path] = existing_image_dict[file_path]
                else:
                    try:
                        image = Image.open(file_path)
                        image.thumbnail(size)
                        updated_image_dict[file_path] = image
                    except Exception as e: print(f"No se puede abrir el archivo {file_path}: {e}")
        for file_path in list(existing_image_dict.keys()):
            if file_path not in updated_image_dict:
                existing_image_dict.pop(file_path, None)

        return updated_image_dict
    
    def select_folder_path(self):
        try: folder_path = filedialog.askdirectory()
        except Exception as e: print(f"Error al seleccionar carpeta: {e}")
        return folder_path
    
    def open_file(self, file_path:os.PathLike=None):
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.run(['open', file_path], check=True) if sys.platform == 'darwin' else subprocess.run(['xdg-open', file_path], check=True)
        except Exception as e:
            print(f"Error al abrir el archivo {file_path}: {e}")

    def change_folder_name_os(self, ruta_original, nuevo_nombre):
        directorio_padre = os.path.dirname(ruta_original)
        nueva_ruta = os.path.join(directorio_padre, nuevo_nombre)
        os.rename(ruta_original, nueva_ruta)
        return nueva_ruta

    def change_file_name_os(self, folder_path):
        if not os.path.isdir(folder_path):
            print("La ruta proporcionada no es una carpeta válida.")
            return

        # Obtener el nombre de la carpeta
        nombre_carpeta = os.path.basename(folder_path.rstrip(os.sep))
        
        # Listar todos los archivos en la carpeta
        archivos = os.listdir(folder_path)

        for archivo in archivos:
            ruta_actual = os.path.join(folder_path, archivo)
            
            # Verificar si es un archivo
            if os.path.isfile(ruta_actual):
                # Obtener la extensión del archivo
                nombre, extension = os.path.splitext(archivo)

                # Verificar si el archivo ya cumple con el formato
                if nombre.startswith(nombre_carpeta + "_") and nombre[len(nombre_carpeta) + 1:].isdigit():
                    continue
                
                # Encontrar un nuevo nombre que no entre en conflicto
                indice = 0
                nuevo_nombre = f"{nombre_carpeta}_{indice}{extension}"
                nueva_ruta = os.path.join(folder_path, nuevo_nombre)
                
                while os.path.exists(nueva_ruta):
                    indice += 1
                    nuevo_nombre = f"{nombre_carpeta}_{indice}{extension}"
                    nueva_ruta = os.path.join(folder_path, nuevo_nombre)
                
                # Renombrar el archivo
                os.rename(ruta_actual, nueva_ruta)
                print(f"Renombrado: {archivo} a {nuevo_nombre}")