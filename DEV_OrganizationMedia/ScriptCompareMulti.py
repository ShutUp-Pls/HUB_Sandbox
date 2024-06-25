import os
import shutil
import cv2

import numpy as np
import cupy as cp

from multiprocessing import Pool, cpu_count
from skimage.metrics import structural_similarity as ssim
from tkinter import filedialog


def obtener_carpetas(ruta):
    carpetas = []
    for elemento in os.listdir(ruta):
        elemento_ruta = os.path.join(ruta, elemento)
        if os.path.isdir(elemento_ruta):
            carpetas.append(elemento_ruta)
            carpetas.extend(obtener_carpetas(elemento_ruta))
    return carpetas

def obtener_rutas_imagenes(carpeta):
    extensiones_imagenes = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    rutas_imagenes = []
    for ruta, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            if any(archivo.lower().endswith(ext) for ext in extensiones_imagenes):
                ruta_completa = os.path.join(ruta, archivo)
                rutas_imagenes.append(ruta_completa)
    return rutas_imagenes

def mover_archivos_a_carpeta(lista_rutas):
    if not lista_rutas: return print("La lista de rutas está vacía.")

    carpeta_destino = os.path.splitext(os.path.basename(lista_rutas[0]))[0]
    directorio_archivo = os.path.dirname(lista_rutas[0])
    carpeta_destino_path = os.path.join(directorio_archivo, carpeta_destino)

    if not os.path.exists(carpeta_destino_path): os.mkdir(carpeta_destino_path)

    for ruta in lista_rutas:
        nombre_archivo = os.path.basename(ruta)
        shutil.move(ruta, os.path.join(carpeta_destino_path, nombre_archivo))

def mover_archivos_a_carpeta_principal(ruta_principal):
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

def comparar_imagenes(par):
    imagen1_ruta, imagen2_ruta = par
    imagen1 = cv2.imread(imagen1_ruta)
    imagen2 = cv2.imread(imagen2_ruta)

    alto1, ancho1, _ = imagen1.shape
    alto2, ancho2, _ = imagen2.shape

    max_dimension = 512  # Ajustar según sea necesario
    imagen1 = reducir_resolucion(imagen1, max_dimension)
    imagen2 = reducir_resolucion(imagen2, max_dimension)

    if alto1 != alto2 or ancho1 != ancho2:
        ancho_nuevo, alto_nuevo = min(ancho1, ancho2), min(alto1, alto2)
        imagen1 = cv2.resize(imagen1, (ancho_nuevo, alto_nuevo))
        imagen2 = cv2.resize(imagen2, (ancho_nuevo, alto_nuevo))

    imagen1_gris = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
    imagen2_gris = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)

    imagen1_gris_cp = cp.array(imagen1_gris)
    imagen2_gris_cp = cp.array(imagen2_gris)
    
    indice_ssim_1, _ = ssim(imagen1_gris_cp, imagen2_gris_cp, full=True)

    imagen2_espejo = cv2.flip(imagen2_gris, 1)
    imagen2_espejo_cp = cp.array(imagen2_espejo)

    indice_ssim_2, _ = ssim(imagen1_gris_cp, imagen2_espejo_cp, full=True)

    indice_ssim_final = max(indice_ssim_1, indice_ssim_2)
    return indice_ssim_final

def reducir_resolucion(imagen, max_dimension):
    alto, ancho = imagen.shape[:2]
    if max(alto, ancho) > max_dimension:
        factor = max_dimension / float(max(alto, ancho))
        nuevo_ancho = int(ancho * factor)
        nuevo_alto = int(alto * factor)
        imagen = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))
    return imagen

def procesar_lote(pares_imagenes, num_procesos):
    with Pool(num_procesos) as pool:
        resultados = pool.map(comparar_imagenes, pares_imagenes)
    return resultados

def comparar_lista_imagenes(lista_rutas):
    pares_imagenes = generar_pares(lista_rutas)
    imagen_referencia = lista_rutas[0]
    nuevas_rutas = [imagen_referencia]

    total_pares = len(pares_imagenes)
    
    for i in range(0, total_pares, 10):
        lote = pares_imagenes[i:i+10]
        resultados = procesar_lote(pares_imagenes, max(1, int(cpu_count() // 1.2)))
    
    for resultado in resultados:
        if resultado[2] is not None:
            print(f"Comparación entre {resultado[0]} y {resultado[1]}: Índice SSIM final: {resultado[2]}")
            if resultado[2] > 0.8:
                nuevas_rutas.append(resultado[1])
        else:
            print(f"Error al leer las imágenes {resultado[0]} y {resultado[1]}")

    for ruta in nuevas_rutas:
        lista_rutas.remove(ruta)

    return nuevas_rutas

def generar_pares(rutas_imagenes):
    primera_imagen = rutas_imagenes[0]
    pares = [(primera_imagen, ruta) for ruta in rutas_imagenes[1:]]
    return pares

def renombrar_archivos(carpeta):
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

def renombrar_archivos_en_subcarpetas( carpeta):
    subcarpetas = obtener_carpetas(carpeta)
    for carpeta in subcarpetas:
        renombrar_archivos(carpeta)

def ordenar_en_carpetas(carpeta):
    lista_rutas = obtener_rutas_imagenes(carpeta)
    iteraciones = len(lista_rutas)
    for i in range(iteraciones):
        if len(lista_rutas) != 0:
            nuevas_rutas = comparar_lista_imagenes(lista_rutas)
            mover_archivos_a_carpeta(nuevas_rutas)

if __name__ == "__main__":
    carpeta = filedialog.askdirectory()
    if carpeta:
        renombrar_archivos(carpeta)
        ordenar_en_carpetas(carpeta)
        renombrar_archivos(carpeta)
        renombrar_archivos_en_subcarpetas(carpeta)
        mover_archivos_a_carpeta_principal(carpeta)