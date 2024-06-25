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

    def change_folder_name_os(self, ruta_original, nuevo_nombre):
        # Obtener el directorio que contiene la carpeta
        directorio_padre = os.path.dirname(ruta_original)
        
        # Construir la nueva ruta con el nuevo nombre
        nueva_ruta = os.path.join(directorio_padre, nuevo_nombre)
        
        # Cambiar el nombre de la carpeta
        os.rename(ruta_original, nueva_ruta)
        return nueva_ruta

    def change_file_name_os(self, ruta_carpeta):
        # Verificar si la ruta es una carpeta válida
        if not os.path.isdir(ruta_carpeta):
            print(f"La ruta {ruta_carpeta} no es una carpeta válida.")
            return

        # Obtener el nombre de la carpeta
        nombre_carpeta = os.path.basename(ruta_carpeta)

        # Listar todos los archivos en la carpeta
        archivos = [f for f in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, f))]
        
        # Renombrar los archivos secuencialmente
        for i, archivo in enumerate(archivos, start=1):
            # Obtener la extensión del archivo
            extension = os.path.splitext(archivo)[1]
            # Crear el nuevo nombre
            nuevo_nombre = f"{nombre_carpeta}_{i}{extension}"
            # Obtener la ruta completa de los archivos
            ruta_vieja = os.path.join(ruta_carpeta, archivo)
            ruta_nueva = os.path.join(ruta_carpeta, nuevo_nombre)
            # Renombrar el archivo
            os.rename(ruta_vieja, ruta_nueva)

    def obtener_archivos_nuevos(ruta_carpeta, estado_anterior):
        archivos_nuevos = []

        with os.scandir(ruta_carpeta) as entradas:
            for entrada in entradas:
                if entrada.is_file() and entrada.name not in estado_anterior:
                    archivos_nuevos.append(entrada.name)

        return archivos_nuevos