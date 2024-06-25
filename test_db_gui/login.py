import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self):
        # Crear la ventana principal
        self.root = tk.Tk()
        self.root.title("Ingreso de Usuario")

        # Crear campos de texto y etiquetas para el nombre de usuario y la contraseña
        label_user = tk.Label(self.root, text="Usuario:")
        label_user.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.entry_user = tk.Entry(self.root)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        label_password = tk.Label(self.root, text="Contraseña:")
        label_password.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.entry_password = tk.Entry(self.root, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Crear botón de ingreso
        button_login = tk.Button(self.root, text="Ingresar", command=self.on_login_clicked)
        button_login.grid(row=2, column=0, columnspan=2, pady=5)

        # Configurar el evento de cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_login_clicked(self):
        # En un caso real, aquí verificarías las credenciales.
        user = self.entry_user.get()
        password = self.entry_password.get()
        messagebox.showinfo("Login", f"Usuario: {user}\nContraseña: {password}")
        # Limpiar los campos
        self.entry_user.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def on_close(self):
        # Acciones al cerrar la ventana, si es necesario realizar alguna limpieza o guardado
        if messagebox.askokcancel("Salir", "¿Deseas salir de la aplicación?"):
            self.root.destroy()

    def run(self):
        # Iniciar el bucle principal de la interfaz
        self.root.mainloop()
