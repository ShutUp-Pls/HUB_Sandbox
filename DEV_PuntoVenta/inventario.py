from importlib import invalidate_caches
import tkinter

inv_abierto = False

def abrir_inventario(ventana_ancla,es_admin):
    global ventana_inventario
    ventana_inventario = tkinter.Toplevel(ventana_ancla)
    ventana_inventario.protocol("WM_DELETE_WINDOW", cerrar_inventario)
    ventana_inventario.geometry("500x500")
    ventana_inventario.title("Inventario")

    

def cerrar_inventario(es_admin):
    global inv_abierto
    inv_abierto = False
    ventana_inventario.destroy()

def front_inventario(es_admin):
    ventana_inventario.lift()
    ventana_inventario.attributes('-topmost',True)
    ventana_inventario.after_idle(ventana_inventario.attributes,'-topmost',False)