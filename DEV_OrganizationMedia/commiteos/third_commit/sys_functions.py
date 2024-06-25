import os

from tkinter import filedialog
from PIL import Image

class SysFunctions:
    '''
    Clase de funciones con el objetivo de ser heredada.

    :method -generate_thumbnail_dict-: Genera un diccionario de miniaturas.
    :method -select_folder_path-: Abre una ventana de dialogo para seleccionar una carpeta.
    :method -open_file: Abre un archivo a tráves del metodo del sistema operativo.
    '''
    def __init__(self): pass

    def generate_thumbnail_dict(self, path:os.PathLike=None, empty:bool=False, size:tuple=(50,50)):
        """
        Genera un diccionario de miniaturas a partir de un 'os.PathLike'.

        :param -path-: Dirección de la carpeta sobre la que generar las miniaturas.
        :param -empty-:
        - True: Genera un diccionario diccionario vacío.
        - False: Genera un diccionario de miniaturas a partir del path indicado.

        :param -size-: Tamaño de las miniaturas en formato tupla (x_size, y_size).
        
        :return 'dict': Devuelve un diccionario de la forma { path : thumbnail }.
        """
        thumbnail_dict = {}
        if not empty:
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
        return thumbnail_dict.copy()
    
    def select_folder_path(self, empty:bool=False):
        """
        Abre una ventana de dialogo para seleccionar una carpeta.
        
        :param -empty-:
        - True: Asigna 'NONE' como dirección de carpeta.
        - False: Abre la ventana de dialogo para seleccionar una carpeta y guarda su ruta.

        :return 'str': Devuelve una cadena de texto en formato 'os.PathLike'.
        """
        folder_path = None
        if not empty:
            try: folder_path = filedialog.askdirectory()
            except Exception as e: print(f"Error al seleccionar carpeta: {e}")
        return folder_path
    
    def open_file(self, file_path:os.PathLike=None):
        """
        Abre un archivo a tráves del metodo del sistema operativo.
        
        :param -file_path-: Ruta del archivo para abrir.
        """
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS, Linux
                subprocess.run(['open', file_path], check=True) if sys.platform == 'darwin' else subprocess.run(['xdg-open', file_path], check=True)
        except Exception as e:
            print(f"Error al abrir el archivo {file_path}: {e}")