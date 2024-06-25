import tkinter as tk

def duplicate_label(label):
    # Obtén los atributos del label original
    attributes = {
        'text': label['text'],
        'image': label['image'],
        'compound': label['compound'],
        'font': label['font'],
        'fg': label['fg'],
        'bg': label['bg'],
        'relief': label['relief'],
        'bd': label['bd'],
        'width': label['width'],
        'height': label['height'],
        'anchor': label['anchor'],
        'justify': label['justify'],
        'padx': label['padx'],
        'pady': label['pady']
    }

    # Crea un nuevo label con los mismos atributos
    new_label = tk.Label(label.master, **attributes)
    new_label.pack()  # Ajusta el empaquetado según tus necesidades

    return new_label

# Crear la ventana principal
root = tk.Tk()

# Crear el label original con atributos específicos
original_label = tk.Label(root, text="Hola, mundo!", font=("Helvetica", 16), fg="blue", bg="yellow", width=20, height=2)
original_label.pack()

# Duplicar el label
duplicated_label = duplicate_label(original_label)

# Ejecutar el bucle principal
root.mainloop()
