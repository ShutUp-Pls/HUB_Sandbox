import os

from tkinter import filedialog
from PIL import Image

class sysFunctions:
    def __init__(self): pass

    def generate_thumbnail_dict(self, path:os.PathLike=None, size:tuple=(50,50)):
        thumbnail_dict = {}
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                try:
                    image = Image.open(file_path)
                    image.thumbnail(size)
                    thumbnail_dict[file_path] = image
                except Exception as e:
                    print(f"No se puede abrir el archivo {file_path}: {e}")
        return thumbnail_dict
    
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