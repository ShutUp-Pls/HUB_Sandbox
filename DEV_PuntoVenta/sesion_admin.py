import tkinter
import inventario
import funciones

def iniciar_admin_sesion():
    global ventana_admin_sesion
    ventana_admin_sesion = tkinter.Tk()
    ventana_admin_sesion.geometry("500x100")
    ventana_admin_sesion.title("Modo Sesion: Admin")
    funciones.configure_rowcolum(ventana_admin_sesion,1,1)

    btn_inventario = tkinter.Button(ventana_admin_sesion,text="Inventario",command=abrir_inv)
    btn_inventario.grid(row=0,column=0,sticky="nsew")

    ventana_admin_sesion.mainloop()

def abrir_inv():
    if inventario.inv_abierto:
        inventario.front_inventario()
        print("Inventario abierto actualmente...")
    else:
        inventario.inv_abierto = True
        inventario.abrir_inventario(ventana_admin_sesion,True)