import json
import os
import shutil

import tkinter as tk

from tkinter import font
from PIL import ImageDraw, ImageFont
from itertools import zip_longest

class OsTools:

    @staticmethod
    def is_path(path):
        return os.path.exists(path)
    
    @staticmethod
    def is_dir(path):
        return os.path.isdir(path)

    @staticmethod
    def clean_dir(path):
        if not os.path.exists(path): raise FileNotFoundError(f"La ruta '{path}' no existe.")
        if not os.path.isdir(path): raise NotADirectoryError(f"La ruta '{path}' no es un directorio.")

        try:
            shutil.rmtree(path)
            os.makedirs(path)
        except:
            list_dir = os.listdir(path)
            for file in list_dir:
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path) or os.path.islink(file_path): os.unlink(file_path)
                elif os.path.isdir(file_path): shutil.rmtree(file_path)
        
    @staticmethod
    def len_files(path):
        if not os.path.exists(path): raise FileNotFoundError(f"La ruta '{path}' no existe.")
        if not os.path.isdir(path): raise NotADirectoryError(f"La ruta '{path}' no es un directorio.")

        list_dir = os.listdir(path)
        files = [f for f in list_dir if os.path.isfile(os.path.join(path, f))]
        return len(files)

    @staticmethod   
    def put_directory(path):
        if not os.path.exists(path): os.makedirs(path)
        elif not os.path.isdir(path): raise NotADirectoryError(f"La ruta '{path}' existe pero no es un directorio.")

class TextTools:

    @staticmethod
    def wrap_text_width(text:str, max_width:int):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            if len(current_line) + len(word) + 1 <= max_width: current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line: lines.append(current_line.strip())

        return "\n".join(lines)

class ListTools:
    
    @staticmethod
    def difference(source_list:list, filter_list:list):
        filter_set = set(filter_list)
        return [item for item in source_list if not(item in filter_set)]

    @staticmethod
    def common(source_list:list, filter_list:list):
        filter_set = set(filter_list)
        return [item for item in source_list if item in filter_set]
    
    @staticmethod
    def toggle_item(item, toggle_list:list):
        if item in toggle_list: toggle_list.remove(item)
        else: toggle_list.append(item)
        return toggle_list
    
    @staticmethod
    def next_in(value, lst):
        if value in lst: return lst[(lst.index(value) + 1) % len(lst)]
        else: raise ValueError(f"El valor '{value}' no se encuentra en la lista proporcionada.")

    @staticmethod
    def get_next_available_int_value(self, column:str, rows:list, columns:list[str]):
        column_idx = columns.index(column)

        values = {row[column_idx] for row in rows if isinstance(row[column_idx], (int, float))}

        if values: next_value = min(set(range(1, max(values) + 2)) - values)
        else: next_value = 1

        return next_value
    
class TkTools:
    class GrabManager:
        def __init__(self):
            self.current_grab = None

        def set_grab(self, widget:tk.Widget, force:bool=True):
            if self.current_grab and force:
                try: self.current_grab.grab_release()
                except: pass
            try:
                widget.grab_set()
                self.current_grab = widget
            except: pass

    @staticmethod
    def configure_grid(widget:tk.Widget, column_weights:list, row_weights:list):
        for col_index, weight in enumerate(column_weights):
            if weight: widget.grid_columnconfigure(col_index, weight=weight)
        
        for row_index, weight in enumerate(row_weights):
            if weight: widget.grid_rowconfigure(row_index, weight=weight)

    @staticmethod
    def calculate_text_width(widget:tk.Widget, container_width:int):
        widget_font = font.Font(font=widget['font'])
        avg_char_width = widget_font.measure("M")
        return container_width // avg_char_width
        
    
class FormatTools:

    @staticmethod
    def safe_cast_value(value):
        try: return float(value) if value not in (None, "") else None
        except ValueError: return str(value)

    @staticmethod
    def number_to_str(number_raw):
        try: number_float = float(number_raw)
        except ValueError: return None

        if number_float.is_integer():
            number_int = int(number_float)
            return f"{number_int:,}".replace(",", ".")
        
        else: return f"{number_float:,.0f}".replace(",", ".")

    @staticmethod
    def str_to_number(str_value):
        if isinstance(str_value, str):
            try: return int(str_value)
            except:
                try: return float(str_value)
                except: return str_value

        else: return str_value

class JsonTools:

    @staticmethod
    def load_json(path):
        with open(path, 'r', encoding='utf-8') as archivo: datos = json.load(archivo)
        return datos if datos else None
    
    @staticmethod
    def save_as_json(diccionario, ruta):  
        with open(ruta, 'w', encoding='utf-8') as archivo:
            json.dump(diccionario, archivo, indent=4, ensure_ascii=False)

    @staticmethod
    def update_json(path, new_data_dict):
        data = JsonTools.load_json(path) or {}
        data.update(new_data_dict)
        JsonTools.save_as_json(data, path)
    
class PillowTools:

    @staticmethod
    def put_text_by_char(draw:ImageDraw, text:str, text_font:ImageFont, text_color:str, text_space:int, pos_x:int, pos_y:int, direction:str='rtl', point_space:bool=True, point_steps:int=3):
        if direction == 'rtl':
            chars = reversed(text)
            step_sign = -1
        else:
            chars = text
            step_sign = 1

        for i, char in enumerate(chars):
            bbox_char = draw.textbbox((0, 0), char, font=text_font)
            char_ancho = bbox_char[2] - bbox_char[0]
            draw.text((pos_x, pos_y), char, fill=text_color, font=text_font)

            if point_space and ((i + 1) % point_steps) == 0: pos_x += step_sign * (char_ancho - 2 * text_space)
            else: pos_x += step_sign * (char_ancho - text_space)

class DictTools:

    @staticmethod
    def merge_dicts_absent(target_dict, source_dict):
        for key, value in source_dict.items():
            if key not in target_dict: target_dict[key] = value
        return target_dict
    
    @staticmethod
    def safe_dict_assign(target_dict, key, value, default=None):
        target_dict[key] = value if value else default

    @staticmethod
    def build_dict(keys, values, fill_keys=False, fill_values=False, default_key="default_key", default_value=None):
        max_length = max(len(keys), len(values))
        
        if fill_keys: keys = (keys + [f"{default_key}_{i}" for i in range(len(keys), max_length)]) if len(keys) < max_length else keys
        if fill_values: values = (values + [default_value] * (max_length - len(values))) if len(values) < max_length else values

        return dict(zip_longest(keys, values, fillvalue=default_value))
    
    @staticmethod
    def common_filter_list(source_dict: dict, filter_list: list):
        filter_set = set(filter_list)
        return {key: value for key, value in source_dict.items() if key in filter_set}