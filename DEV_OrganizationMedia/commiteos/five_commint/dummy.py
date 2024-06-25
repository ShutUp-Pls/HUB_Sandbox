import tkinter as tk

def mostrar_estado():
    estado = var.get()
    if estado:
        label.config(text="Checkbox seleccionada")
    else:
        label.config(text="Checkbox deseleccionada")

# Crear la ventana principal
root = tk.Tk()
root.title("Demo de Checkbutton en Tkinter")

# Variable para almacenar el estado de la checkbox
var = tk.BooleanVar()

# Crear la checkbox
checkbox = tk.Checkbutton(root, text="Selecciona esta opción", variable=var, command=mostrar_estado)
checkbox.pack(pady=10)

# Crear una etiqueta para mostrar el estado de la checkbox
label = tk.Label(root, text="Checkbox deseleccionada")
label.pack(pady=10)

# Iniciar el bucle principal
root.mainloop()
