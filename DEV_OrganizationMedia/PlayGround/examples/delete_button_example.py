import tkinter as tk

class ButtonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Button Manager")

        # Crear los frames
        self.left_frame = tk.Frame(root, width=200, height=400)
        self.right_frame = tk.Frame(root, width=200, height=400)
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Asegurar que ambos frames tengan el mismo peso
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # Botón en el frame izquierdo
        self.add_button = tk.Button(self.left_frame, text="Añadir Botón", command=self.add_button_to_right_frame)
        self.add_button.pack(padx=10, pady=10)

        # Lista para almacenar referencias a los botones
        self.buttons = []

    def add_button_to_right_frame(self):
        # Crear un nuevo botón
        button = tk.Button(self.right_frame, text="Borrar", command=lambda: self.remove_button(button))
        button.pack(padx=10, pady=10)
        # Añadir el botón a la lista
        self.buttons.append(button)

    def remove_button(self, button):
        # Eliminar el botón del frame
        button.destroy()
        # Remover el botón de la lista
        self.buttons.remove(button)

if __name__ == "__main__":
    root = tk.Tk()
    app = ButtonApp(root)
    root.mainloop()
