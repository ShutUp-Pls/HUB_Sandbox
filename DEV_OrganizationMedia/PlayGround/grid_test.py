import tkinter as tk
import time
from tkinter.constants import HORIZONTAL, VERTICAL

# Primera implementación
def empaquetar_widgets_v1(widget_list, container, direccion=HORIZONTAL, maximo=None, **kwargs):
    if direccion not in [HORIZONTAL, VERTICAL]:
        raise ValueError("La dirección debe ser tk.HORIZONTAL o tk.VERTICAL")
    
    fila, columna = 0, 0
    widgets_posicionados = set()
    
    # Obtener widgets actuales en el contenedor
    current_widgets = container.winfo_children()
    
    for index, widget in enumerate(widget_list):
        widget.grid_forget()
        widget.grid(row=fila, column=columna, **kwargs)
        widgets_posicionados.add(widget)

        if direccion == HORIZONTAL:
            columna += 1
            if maximo is not None and columna >= maximo:
                columna = 0
                fila += 1
        elif direccion == VERTICAL:
            fila += 1
            if maximo is not None and fila >= maximo:
                fila = 0
                columna += 1
    
    # Remover widgets que ya no están en la lista
    for widget in current_widgets:
        if widget not in widgets_posicionados:
            widget.grid_forget()

# Segunda implementación (la de tu compañero)
def empaquetar_widgets_v2(widget_list, container, direccion=HORIZONTAL, maximo=None, **kwargs):
    if direccion not in [HORIZONTAL, VERTICAL]:
        raise ValueError("La dirección debe ser tk.HORIZONTAL o tk.VERTICAL")
    
    fila, columna = 0, 0
    widgets_posicionados = set()
    
    # Obtener widgets actuales en el contenedor
    current_widgets = container.winfo_children()
    
    for index, widget in enumerate(widget_list):
        current_info = widget.grid_info()
        new_info = {'row': fila, 'column': columna, **kwargs}
        
        # Verificar si el widget necesita ser reempaquetado
        if not current_info or any(current_info.get(k) != v for k, v in new_info.items()):
            widget.grid_forget()
            widget.grid(**new_info)

        widgets_posicionados.add(widget)
            
        if direccion == HORIZONTAL:
            columna += 1
            if maximo is not None and columna >= maximo:
                columna = 0
                fila += 1
        elif direccion == VERTICAL:
            fila += 1
            if maximo is not None and fila >= maximo:
                fila = 0
                columna += 1
    
    # Remover widgets que ya no están en la lista
    for widget in current_widgets:
        if widget not in widgets_posicionados:
            widget.grid_forget()


# Función para medir el tiempo de ejecución
def medir_tiempo(func, widget_list, container, direccion, maximo, **kwargs):
    start_time = time.time()
    func(widget_list, container, direccion, maximo, **kwargs)
    end_time = time.time()
    return end_time - start_time

# Ejemplo de uso
root = tk.Tk()

# Crear una lista de widgets
widgets = [tk.Label(root, text=f"Label_widgets {i}") for i in range(2000)]
widgots = [tk.Label(root, text=f"Label_widgots {i}") for i in range(2000)]

# Medir el tiempo de empaquetación la primera implementación
tiempo_v1_1 = medir_tiempo(empaquetar_widgets_v1, widgets, root, HORIZONTAL, 5, padx=5, pady=5)
root.update()
# Medir el tiempo de reempaquetación la primera implementación
tiempo_v1_2 = medir_tiempo(empaquetar_widgets_v1, widgots, root, VERTICAL, 5, padx=5, pady=5)
root.update()

root.mainloop()
root = tk.Tk()

widgets = [tk.Label(root, text=f"Label_widgets {i}") for i in range(2000)]
widgots = [tk.Label(root, text=f"Label_widgots {i}") for i in range(2000)]

# Medir el tiempo de la segunda implementación
tiempo_v2_1 = medir_tiempo(empaquetar_widgets_v2, widgets, root, HORIZONTAL, 5, padx=5, pady=5)
root.update()
# Medir el tiempo de reempaquetación la primera implementación
tiempo_v2_2 = medir_tiempo(empaquetar_widgets_v2, widgots, root, VERTICAL, 5, padx=5, pady=5)
root.update()


root.mainloop()

# Mostrar los resultados
print(f"Tiempo de empaquetamiento v1: {tiempo_v1_1:.6f} segundos")
print(f"Tiempo de reempaquetamiento v1: {tiempo_v1_2:.6f} segundos")
print(f"===========================================================")
print(f"Tiempo de empaquetamiento v2: {tiempo_v2_1:.6f} segundos")
print(f"Tiempo de reempaquetamiento v2: {tiempo_v2_2:.6f} segundos")

# Mantener la ventana abierta para observar los resultados
