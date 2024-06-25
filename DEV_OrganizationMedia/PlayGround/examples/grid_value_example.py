import tkinter as tk

# Crear una ventana
root = tk.Tk()

# Crear widgets y ubicarlos en la cuadrícula
label1 = tk.Label(root, text="Columna 1 plus", background="green")
label1.grid(row=0, column=0)
label2 = tk.Label(root, text="Columna 2 pero mas larga", background="red")
label2.grid(row=0, column=1)

# Necesitamos iniciar el mainloop para que el grid se configure correctamente
root.update()

# Obtener y mostrar el ancho de la columna 0
ancho_columna_0 = label1.grid_bbox()
print(f"El ancho de la columna 0 es: {ancho_columna_0} píxeles")

# Obtener y mostrar el ancho de la columna 1
ancho_columna_1 = label2.winfo_width()
print(f"El ancho de la columna 1 es: {ancho_columna_1} píxeles")

# Iniciar el bucle principal de la aplicación
root.mainloop()
