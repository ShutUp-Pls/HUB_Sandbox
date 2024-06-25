import tkinter
import funciones
import sesion_admin
import sesion_venta

def abrir_login():
    global ventana_login
    ventana_login = tkinter.Tk()
    ventana_login.title("APP V1")
    ventana_login.geometry("400x100")
    ventana_login.resizable(True,False)
    funciones.configure_rowcolum(ventana_login,1,1)
    ventana_login.minsize(300,60)

    frame_main = tkinter.LabelFrame(ventana_login,text="Login")
    funciones.configure_rowcolum(frame_main,3,3)
    frame_main.columnconfigure(0,weight=0)
    frame_main.columnconfigure(1,weight=5)
    frame_main.columnconfigure(2,weight=0)
    frame_main.rowconfigure(0,weight=3)
    frame_main.rowconfigure(1,weight=3)
    frame_main.grid(row=0,column=0,sticky="nsew")

    label_usuario = tkinter.Label(frame_main,text="Usuario: ")
    label_usuario.grid(row=0,column=0,sticky="e")

    global var_usuario
    var_usuario = tkinter.StringVar()
    entry_usuario = tkinter.Entry(frame_main,textvariable=var_usuario)
    entry_usuario.grid(row=0,column=1,pady=4,sticky="nsew")

    label_contra = tkinter.Label(frame_main,text="Constraseña: ")
    label_contra.grid(row=1,column=0,sticky="e")

    global var_contra
    var_contra = tkinter.StringVar()
    entry_contra = tkinter.Entry(frame_main,textvariable=var_contra)
    entry_contra.grid(row=1,column=1,pady=4,sticky="nsew")

    global var_login_feedback
    var_login_feedback = tkinter.StringVar()
    var_login_feedback.set("Iniciar sesion")
    lbl_feedback= tkinter.Label(frame_main,textvariable=var_login_feedback)
    lbl_feedback.grid(row=2,column=1,sticky="we")

    btn_ingresar = tkinter.Button(frame_main,text="Ingresar",command=ingresar,width=15)
    btn_ingresar.grid(row=0,column=2,rowspan=2,sticky="nsew")

    ventana_login.mainloop()

def ingresar():
    res_tupla = funciones.user_autentication(var_usuario.get(),var_contra.get())
    if res_tupla[0]:
        var_login_feedback.set("Iniciando sesion")
        if res_tupla[1] == "admin":
            ventana_login.destroy()
            sesion_admin.iniciar_admin_sesion()
        elif res_tupla[1] == "venta":
            ventana_login.destroy()
            sesion_venta.iniciar_venta_sesion()
    else:
        if res_tupla[1] == "NE":
            var_login_feedback.set("Usuario no existe")
        else:
            var_login_feedback.set("Contraseña incorrecta")