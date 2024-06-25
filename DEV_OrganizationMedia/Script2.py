import os
import shutil
import cv2

from skimage.metrics import structural_similarity as ssim
from tkinter import filedialog

#CARPETA = "C:\\Users\\marqu\\OneDrive\\Pictures\\Jen\\dos_5"

class AutoOrderFile:
    def __init__(self):
        self.carpeta = filedialog.askdirectory()
        if self.carpeta:
            self.renombrar_archivos(self.carpeta)
            self.ordenar_en_carpetas(self.carpeta)
            self.renombrar_archivos(self.carpeta)
            self.renombrar_archivos_en_subcarpetas(self.carpeta)
            self.mover_archivos_a_carpeta_principal(self.carpeta)

    def obtener_carpetas(self, ruta):
        carpetas = []
        for elemento in os.listdir(ruta):
            elemento_ruta = os.path.join(ruta, elemento)
            if os.path.isdir(elemento_ruta):
                carpetas.append(elemento_ruta)
                carpetas.extend(self.obtener_carpetas(elemento_ruta))
        return carpetas
    
    def obtener_rutas_imagenes(self, carpeta):
        extensiones_imagenes = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        rutas_imagenes = []
        for ruta, _, archivos in os.walk(carpeta):
            for archivo in archivos:
                if any(archivo.lower().endswith(ext) for ext in extensiones_imagenes):
                    ruta_completa = os.path.join(ruta, archivo)
                    rutas_imagenes.append(ruta_completa)
        return rutas_imagenes

    def mover_archivos_a_carpeta(self, lista_rutas):
        if not lista_rutas: return print("La lista de rutas está vacía.")

        carpeta_destino = os.path.splitext(os.path.basename(lista_rutas[0]))[0]
        directorio_archivo = os.path.dirname(lista_rutas[0])
        carpeta_destino_path = os.path.join(directorio_archivo, carpeta_destino)

        if not os.path.exists(carpeta_destino_path): os.mkdir(carpeta_destino_path)

        for ruta in lista_rutas:
            nombre_archivo = os.path.basename(ruta)
            shutil.move(ruta, os.path.join(carpeta_destino_path, nombre_archivo))

    def mover_archivos_a_carpeta_principal(self, ruta_principal):
        if not os.path.isdir(ruta_principal): return print(f"La ruta {ruta_principal} no es válida.")

        for carpeta, subcarpetas, archivos in os.walk(ruta_principal):
            if carpeta == ruta_principal:continue
            
            for archivo in archivos:
                ruta_archivo = os.path.join(carpeta, archivo)
                destino = os.path.join(ruta_principal, archivo)
                print(f"Moviendo {ruta_archivo} a {destino}")
                shutil.move(ruta_archivo, destino)

            if not os.listdir(carpeta):
                print(f"Eliminando carpeta vacía {carpeta}")
                os.rmdir(carpeta)

    def comparar_imagenes(self, imagen1_ruta, imagen2_ruta):
        imagen1 = cv2.imread(imagen1_ruta)
        imagen2 = cv2.imread(imagen2_ruta)

        alto1, ancho1, _ = imagen1.shape
        alto2, ancho2, _ = imagen2.shape

        max_dimension = 512  # Ajustar según sea necesario
        imagen1 = self.reducir_resolucion(imagen1, max_dimension)
        imagen2 = self.reducir_resolucion(imagen2, max_dimension)

        if alto1 != alto2 or ancho1 != ancho2:
            ancho_nuevo, alto_nuevo = min(ancho1, ancho2), min(alto1, alto2)
            imagen1 = cv2.resize(imagen1, (ancho_nuevo, alto_nuevo))
            imagen2 = cv2.resize(imagen2, (ancho_nuevo, alto_nuevo))

        imagen1_gris = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
        imagen2_gris = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)

        indice_ssim_1, _ = ssim(imagen1_gris, imagen2_gris, full=True)
        imagen2_espejo = cv2.flip(imagen2_gris, 1)
        indice_ssim_2, _ = ssim(imagen1_gris, imagen2_espejo, full=True)

        indice_ssim_final = max(indice_ssim_1, indice_ssim_2)
        return indice_ssim_final
    
    def reducir_resolucion(self, imagen, max_dimension):
        alto, ancho = imagen.shape[:2]
        if max(alto, ancho) > max_dimension:
            factor = max_dimension / float(max(alto, ancho))
            nuevo_ancho = int(ancho * factor)
            nuevo_alto = int(alto * factor)
            imagen = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))
        return imagen

    def comparar_lista_imagenes(self, lista_rutas):
        imagen_referencia = lista_rutas[0]
        rutas_85 = [imagen_referencia]
        rutas_30 = []
        rutas_00 = []
        
        for ruta in lista_rutas[1:]:
            indice = self.comparar_imagenes(imagen_referencia, ruta)
            print(f"Indice entre {os.path.basename(lista_rutas[0])} y {os.path.basename(ruta)}: {indice}")
            if indice <= 1.0 and indice > 0.85: rutas_85.append(ruta)
            elif indice <= 0.85 and indice > 0.3: rutas_30.append(ruta)
            else: rutas_00.append(ruta)

        self.mover_archivos_a_carpeta(rutas_85)
        if rutas_30 != []: self.comparar_lista_imagenes(rutas_30)
        if rutas_00 != []: self.comparar_lista_imagenes(rutas_00)

    def renombrar_archivos(self, carpeta):
        if not os.path.isdir(carpeta):
            print(f"La ruta '{carpeta}' no es una carpeta válida.")
            return
        
        nombre_carpeta = os.path.basename(os.path.normpath(carpeta))
        archivos = os.listdir(carpeta)
        
        for i, archivo in enumerate(archivos):
            ruta_actual = os.path.join(carpeta, archivo)
            if os.path.isfile(ruta_actual) or os.path.isdir(ruta_actual):
                extension = os.path.splitext(archivo)[1]
                nuevo_nombre = f"{nombre_carpeta}_{i+1}{extension}"
                nueva_ruta = os.path.join(carpeta, nuevo_nombre)
                
                contador = 1
                while os.path.exists(nueva_ruta):
                    nuevo_nombre = f"{nombre_carpeta}_{i+1}_{contador}{extension}"
                    nueva_ruta = os.path.join(carpeta, nuevo_nombre)
                    contador += 1
                
                os.rename(ruta_actual, nueva_ruta)
                print(f"Renombrado: '{archivo}' a '{nuevo_nombre}'")

    def renombrar_archivos_en_subcarpetas(self, carpeta):
        subcarpetas = self.obtener_carpetas(carpeta)
        for carpeta in subcarpetas:
            self.renombrar_archivos(carpeta)

    def ordenar_en_carpetas(self, carpeta):
        lista_rutas = self.obtener_rutas_imagenes(carpeta)
        self.comparar_lista_imagenes(lista_rutas)

AutoOrderFile()