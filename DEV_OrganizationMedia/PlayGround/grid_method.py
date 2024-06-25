import tkinter as tk
from tkinter.constants import HORIZONTAL, VERTICAL

def empaquetar_widgets(widget_list, container:tk.Widget, direccion=tk.HORIZONTAL, maximo=None, **kwargs):
    if direccion not in [tk.HORIZONTAL, tk.VERTICAL]: raise ValueError("La dirección debe ser tk.HORIZONTAL o tk.VERTICAL")
    fila, columna = 0, 0
    widgets_posicionados = set()
    current_widgets = container.winfo_children()
    for index, widget in enumerate(widget_list):
        widget.grid_forget()
        widget.grid(row=fila, column=columna, **kwargs)
        widgets_posicionados.add(widget)
        if direccion == tk.HORIZONTAL:
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
            widget.grid_forget()

def configurar_grid(container, num_filas, num_columnas, peso=1, pesos_filas=None, pesos_columnas=None, **kwargs):
    # Configurar pesos por defecto para filas
    for i in range(num_filas):
        # Ajustar índice para pesos_filas (1 basado)
        peso_fila = pesos_filas[i + 1] if pesos_filas and (i + 1) in pesos_filas else peso
        container.grid_rowconfigure(i, weight=peso_fila, **kwargs)
    
    # Configurar pesos por defecto para columnas
    for j in range(num_columnas):
        # Ajustar índice para pesos_columnas (1 basado)
        peso_columna = pesos_columnas[j + 1] if pesos_columnas and (j + 1) in pesos_columnas else peso
        container.grid_columnconfigure(j, weight=peso_columna, **kwargs)

def obtener_tamaño_fila(container:tk.Widget, fila:int):
    container.update()
    bbox = container.grid_bbox(0, fila-1)
    if bbox:
        _, _, _, height = bbox
        return height
    return None

def obtener_tamaño_columna(container:tk.Widget, columna:int):
    container.update()
    bbox = container.grid_bbox(columna-1, 0)
    if bbox:
        _, _, width, _ = bbox
        return width
    return None

# Ejemplo de uso
root = tk.Tk()

# Configurar una cuadrícula de 5 filas y 5 columnas
configurar_grid(root, num_filas=5, num_columnas=5, peso=1)

# Crear y empaquetar widgets para visualizar el efecto
widgets = [tk.Label(root, text=f"Label {i}") for i in range(20)]
empaquetar_widgets(widgets, root, direccion=HORIZONTAL, maximo=5, padx=5, pady=5)

# Obtener el tamaño de la fila 1 y la columna 1
tamaño_fila_1 = obtener_tamaño_fila(root, 1)
tamaño_columna_1 = obtener_tamaño_columna(root, 1)

print(f"Tamaño de la fila 1: {tamaño_fila_1}")
print(f"Tamaño de la columna 1: {tamaño_columna_1}")

# Añadir un nuevo widget a la lista y volver a empaquetar
widgets.append(tk.Label(root, text="New Label"))
empaquetar_widgets(widgets, root, direccion=HORIZONTAL, maximo=3, padx=20, pady=5)

# Obtener el tamaño de la fila 1 y la columna 1
tamaño_fila_1 = obtener_tamaño_fila(root, 1)
tamaño_columna_1 = obtener_tamaño_columna(root, 1)

# Crear y empaquetar widgets para visualizar el efecto
widgots = [tk.Label(root, text=f"Label {i}") for i in range(20)]
empaquetar_widgets(widgots, root, direccion=VERTICAL, maximo=2, padx=5, pady=5)

print(f"Tamaño de la fila 1: {tamaño_fila_1}")
print(f"Tamaño de la columna 1: {tamaño_columna_1}")

print(widgots[0].master)

root.mainloop()