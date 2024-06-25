import tkinter as tk

class MyApp(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        # Aquí puedes añadir más inicializaciones o widgets adicionales
        self.label = tk.Label(self, text="Hola, soy un widget!")
        self.label.pack()

root = tk.Tk()
app = MyApp(root)
app.pack(fill=tk.BOTH, expand=tk.TRUE)
root.mainloop()
