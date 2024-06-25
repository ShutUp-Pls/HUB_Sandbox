import tkinter

root = tkinter.Tk()
root.title("Ventana padre")
# Creamos una ventana hija de root
otra_ventana = tkinter.Toplevel(root)
otra_ventana.title("Ventana hija")
# Este es solo para decoracion
etiqueta = tkinter.Label(otra_ventana, text='Este es un ejemplo de transient')
etiqueta.pack()
# Posicionamos las dos ventanas para que sea mas claro el ejemplo
root.geometry("400x400+100+100")
otra_ventana.geometry("200x200+150+150")
# Y ahora si llamamos a este metodo
otra_ventana.transient(root)
root.mainloop()