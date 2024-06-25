import tkinter
import os
import json

KEY_USER = "users"

NAME_DATA_FOLDER = "data"
DIR_DATA_FOLDER = os.path.join(os.getcwd(),NAME_DATA_FOLDER)

NAME_SYSTEM_JSON = "system.json"
DIR_SYSTEM_JSON = os.path.join(DIR_DATA_FOLDER,NAME_SYSTEM_JSON)

##[ INTERACCIONES JSON ]##
def json_to_py(dir):
    with open(dir) as json_file:
        pydir = json.load(json_file)
    return pydir

def user_autentication(user_name,user_pass):
    users_dicc = json_to_py(DIR_SYSTEM_JSON)[KEY_USER]
    for user_id in users_dicc:
        if users_dicc[user_id]["nombre"]==user_name:
            if users_dicc[user_id]["pass"]==user_pass:
                return (True, users_dicc[user_id]["tipo"])
            else:
                return (False, "IN")
    return (False, "NE")

##[ INTERACCIONES TKINTER ]##
def configure_rowcolum(wdgt,fila,columna):
    for r in range(0,fila):
        wdgt.rowconfigure(r, weight=1)
    for c in range(0,columna):
        wdgt.columnconfigure(c, weight=1)