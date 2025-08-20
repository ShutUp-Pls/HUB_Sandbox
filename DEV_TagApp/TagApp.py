import requests

import tkinter as tk

from datetime import datetime
from tkinter import ttk

from util.func_tools import ListTools, TkTools, OsTools, JsonTools, DictTools
from app_specific.tag_generator import generate_tags_yielded

from app_specific.ProductMenu import ProductMenu
from app_specific.TagMenu import TagMenu

from own.OwnTreeview import OwnTreeview
from own.OwnSearchBox import OwnSearchBoxMenu
from own.OwnDbManagment import OwnDbManagmentMDB
from own.OwnExceptions import VerboseException
from own.OwnLoadingBar import OwnLoadingBar

CONFIG = JsonTools.load_json("app_specific\\config.json")

class TagApp(tk.Tk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_app(icon_path=CONFIG["icon_loading"], title="Iniciando Aplicación")
        self.mainloop()

    @OwnLoadingBar
    def build_app(self):
        STEP_COUNT = 4
        self.withdraw()

        yield(STEP_COUNT,"Configuraciones iniciales...")
        self.title("Demo APP V1")
        self.iconphoto(False, tk.PhotoImage(file=CONFIG["icon_app"]))
        self.protocol("WM_DELETE_WINDOW", self.__on_close)

        geometry_width = int(self.winfo_screenwidth()*0.5)
        geometry_height = int(self.winfo_screenheight()*0.5)
        self.geometry(f"{geometry_width}x{geometry_height}")
        self.minsize(geometry_width, geometry_height)

        self.option_add("*Font", ("TkDefaultFont", 10))
        style = ttk.Style()
        style.configure(".", font=("TkDefaultFont", 10))

        TkTools.configure_grid(self, [1,1], [1])

        yield(STEP_COUNT,"Conectando Base de Datos Local...")
        self.db = OwnDbManagmentMDB(CONFIG["db_path"])

        # ===========================================================
        # FRAME IZQUIERDO: VISUALIZACIÓN BASE DATOS TOTAL
        # ===========================================================

        yield(STEP_COUNT,"Construyendo aplicacion...")
        left_frame = tk.Frame(self)
        TkTools.configure_grid(left_frame, [1], [0,1])

        self.search_box = OwnSearchBoxMenu(left_frame, ListTools.common(CONFIG["product_search_columns"], CONFIG["product_columns"]))
        self.search_box.callback_search = self.__callback_search

        self.db_view = OwnTreeview(left_frame)
        self.db_view.treeview.callback_pivot = self.__callback_pivot
        self.db_view.grid_propagate(False)
        self.db_tag_state = self.__save_db_view_state()
        self.db_prod_state = self.__save_db_view_state()

        left_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.search_box.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.db_view.grid(row=1, column=0, sticky=tk.NSEW)

        # ===========================================================
        # FRAME DERECHO: NOTEBOOK Y APLICACIONES
        # ===========================================================

        right_frame = tk.Frame(self)
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.bind("<<NotebookTabChanged>>", self.__on_tab_change)

        edit_product = tk.Frame(self.notebook)
        TkTools.configure_grid(edit_product, [1], [1])

        tag_generator = tk.Frame(self.notebook)
        TkTools.configure_grid(tag_generator, [1], [1,0])

        self.notebook.add(edit_product, text="Añadir/Editar Producto")
        self.notebook.add(tag_generator, text="Generar Etiquetas")

        right_frame.grid(row=0, column=1, sticky=tk.NSEW)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # ===========================================================
        # APLICACIÓN: IMPRESION DE ETIQUETAS
        # ===========================================================

        self.tag_view = OwnTreeview(tag_generator)
        self.tag_view.grid_propagate(False)
        self.tag_view.treeview.selected_mode = "extended"

        self.tag_menu = TagMenu(tag_generator)
        self.tag_menu.callback_print = self.__callback_print
        # self.tag_menu.callback_search

        self.tag_view.grid(row=0, column=0, sticky=tk.NSEW)
        self.tag_menu.grid(row=1, column=0, sticky=tk.NSEW)

        # ===========================================================
        # APLICACIÓN: MANUPULACIÓN DE PRODUCTOS
        # ===========================================================

        self.prod_view = ProductMenu(edit_product)
        self.prod_view.callback_action = lambda icon_path=CONFIG["icon_loading"], title="": self.__callback_action(icon_path=icon_path, title=title)
        self.prod_view.grid_propagate(False)
        self.prod_view.grid(row=0, column=0, sticky=tk.NSEW)
        self.bind("<Return>", self.__enter_key)

        yield(STEP_COUNT,"Cargando Información a Visualización...")
        self.__load_db_views()
        self.update_idletasks()
        yield(STEP_COUNT,"Carga Completada")
        self.deiconify()
        self.build_app.force_close()

    def toggle_views_rows(self, selected_db_rows=[], selected_tag_rows=[]):
        actual_frame_name = self.notebook.tab(self.notebook.index("current"), option="text")
        if actual_frame_name == "Generar Etiquetas":
            in_tag_view_rows = list(self.tag_view.treeview.visible_rows.values())
            
            tag_view_rows = ListTools.difference(selected_db_rows + in_tag_view_rows, selected_tag_rows)
            db_view_rows = ListTools.difference(self.db_view.treeview.loaded_rows, tag_view_rows)

            self.tag_view.treeview.visible_rows = tag_view_rows
            self.db_view.treeview.set_avaible_treeview(db_view_rows)

    def __on_close(self):
        self.destroy()

    def __load_db_views(self):
        rows, columns = self.db.get_table_content(CONFIG["table_product"])

        self.db_view.treeview.set_load_treeview(rows, columns, avaible_columns=CONFIG["product_show_columns"])
        self.tag_view.treeview.set_load_treeview(rows, columns, avaible_columns=CONFIG["product_show_columns"], visible_rows=[])

    def __load_db_views_yielded(self):
        STEP_COUNT = 1

        self.db_view.treeview.reset(keep_order=True)
        self.tag_view.treeview.reset(keep_order=True)

        rows, columns = self.db.get_table_content(CONFIG["table_product"])

        yield(STEP_COUNT,self.db_view.treeview.set_load_treeview_yielded(rows, columns, avaible_columns=CONFIG["product_show_columns"]))
        self.tag_view.treeview.set_load_treeview(rows, columns, avaible_columns=CONFIG["product_show_columns"], visible_rows=[])
        yield(STEP_COUNT,"Carga Completada")

    def __enter_key(self, event):
        self.toggle_views_rows(selected_db_rows=list(self.db_view.treeview.selected_rows.values()), selected_tag_rows=list(self.tag_view.treeview.selected_rows.values()))

    def __tab_state_reload(self, tab=None):
        if tab is None: return
        state = self.__save_db_view_state()
        self.search_box.set_entry_text("")
        state["selected_rows"] = None

        if tab == "Generar Etiquetas":
            self.db_tag_state = state
            self.db_view.treeview.selected_mode = "multiply"
        elif tab == "Añadir/Editar Producto":
            self.db_prod_state = state
            self.db_view.treeview.selected_mode = "simple"

        self.__put_db_view_state(state)

    def __tab_state_change(self, tab=None):
        if tab is None: return
        self.search_box.set_entry_text("")

        if tab == "Generar Etiquetas":
            self.db_prod_state = self.__save_db_view_state()
            self.db_view.treeview.selected_mode = "multiply"
            self.__put_db_view_state(self.db_tag_state)
            
        elif tab == "Añadir/Editar Producto":
            self.db_tag_state = self.__save_db_view_state()
            self.db_view.treeview.selected_mode = "simple"
            self.__put_db_view_state(self.db_prod_state)

    def __on_tab_change(self, event):
        actual_frame_name = self.notebook.tab(self.notebook.index("current"), option="text")
        if actual_frame_name == "Generar Etiquetas": self.__tab_state_change("Generar Etiquetas")
        elif actual_frame_name == "Añadir/Editar Producto": self.__tab_state_change("Añadir/Editar Producto")
                    
    def __save_db_view_state(self):
        temp_dict = {"position":self.db_view.treeview.get_vertical_scroll_position() or None,
                     "avaible_rows":self.db_view.treeview.available_rows or None,
                     "selected_rows":list(self.db_view.treeview.selected_rows.values()) or None,
                     "order_column":(self.db_view.treeview.order_column, self.db_view.treeview.order_type) or None,
                     "search_str":self.search_box.get_entry_text() or None,
                     "search_menu":self.search_box.get_combobox_value() or None}

        return temp_dict
    
    def __put_db_view_state(self, state):
        if state["avaible_rows"]: self.db_view.treeview.set_avaible_treeview(state["avaible_rows"])
        if state["search_menu"]: self.search_box.set_combobox_value(state["search_menu"])
        if state["search_str"]: self.search_box.set_entry_text(state["search_str"])
        if state["position"]: self.db_view.treeview.set_vertical_scroll_position(state["position"][0])
        if state["order_column"]: self.db_view.treeview.order_data(state["order_column"])
        if state["selected_rows"]:
            reversed_visible_rows = {value: key for key, value in self.db_view.treeview.visible_rows.items()}
            self.db_view.treeview.selected_rows = [reversed_visible_rows[row] for row in state["selected_rows"]]

    def __merge_http_dict(self, attr_db:dict):
        attr_http_post = {
            "txtporcentaje_iva": "19",
            "txtid": "",
            "txtcodigo": attr_db.get("codigo", ""),
            "txtcod_interno": attr_db.get("cod_interno", ""),
            "txtnombre": attr_db.get("nombre", ""),
            "txtfamilia_producto": str(attr_db.get("familia", "")),
            "txtsubfamilia_producto": str(attr_db.get("subfamilia", "")),
            "txtunidad": attr_db.get("unidad", ""),
            "txtiva": "S" if attr_db.get("afecto_iva", "S") == "S" else "N",
            "txtid_impuestos1": str(attr_db.get("id_impuestos", "")),
            "txtprecio_venta": str(attr_db.get("precio_venta", 0.00)).replace(".", ","),
            "txtprecio_venta_boleta": str(attr_db.get("precio_venta_boleta", 0.00)).replace(".", ","),
            "txtstock_critico": str(attr_db.get("stock_critico", 0)),
            "txtdias_reposion": str(attr_db.get("dias_reposion", 0)),
            "txtvigente": attr_db.get("vigente", "S"),
            "txtfactor_compra": str(attr_db.get("factor_compra", 0)).replace(".", ","),
            "txtid_producto": attr_db.get("id_producto", ""),
            "txtfecha_creacion": self.__merge_date(attr_db.get("fecha_creacion", datetime.now().strftime('%Y-%m-%d')))
        }
        return attr_http_post
    
    def __merge_db_dict(self, input_dict):
        merged_dict ={
            "id_producto":"",
            "codigo":"",
            "nombre":"",
            "unidad":"",
            "factor_compra":0,
            "precio_venta":0.00,
            "fecha_creacion":datetime.now().strftime('%Y-%m-%d'),
            "vigente":"S",
            "id_usuario_creacion":1,
            "fecha_modificacion":datetime.now().strftime('%Y-%m-%d'),
            "id_usuario_modificacion":1,
            "stock_critico":6,
            "dias_reposion":0,
            "id_impuestos":0,
            "afecto_iva":"S",
            "tiene_impuesto":"N",
            "precio_venta_boleta":0.00,
            "familia":1,
            "subfamilia":1,
            "cod_interno":"",
            "vendidos":0
        }
        merged_dict.update(input_dict)
        return merged_dict
    
    def __merge_date(self, fecha_str):
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha.strftime('%Y-%m-%dT%H:%M:%S-04:00')
        except ValueError: return fecha_str

    def __description_product_row(self, info):
        des = ""
        info_dict = info if isinstance(info, dict) else DictTools.build_dict(CONFIG["product_columns"], info)
        for key, value in info_dict.items(): des += f"[{key} = {value}]\n"
        return des
    
    def __callback_search(self, value, query):
        if value in self.db_view.treeview.available_columns: self.db_view.treeview.filter_data(value, query)

    def __callback_pivot(self, click_info:dict):
        actual_frame_name = self.notebook.tab(self.notebook.index("current"), option="text")
        if actual_frame_name == "Añadir/Editar Producto":
            if click_info:
                _, content_pivot = next(iter(click_info.items()))
                dict_values = DictTools.build_dict(CONFIG["product_columns"], content_pivot)
                self.prod_view.set_values(dict_values)

            else: self.prod_view.reset()

    @OwnLoadingBar
    def __callback_action(self):
        STEP_COUNT = 7

        is_id = ("id_producto" in self.prod_view.input_dict)

        yield(STEP_COUNT,"Verificando campos...")
        dict_required = self.prod_view.codenameprice_menu.return_info()
        if dict_required is None:
            VerboseException.show_error("No pueden haber campos criticos vacíos.", f"Los siguientes campos están vacios:\n{self.prod_view.codenameprice_menu.get_empty_entries_labels()}\n\nLos campos criticos son:\n-Codigo.\n-Nombre.\n-Precio.", grab_set=True)
            return

        yield(STEP_COUNT,"Verificando codigo único...")
        row_code = self.db.get_row_by_column_value(dict_required["codigo"], "codigo", CONFIG["table_product"])
        if (row_code and is_id and self.prod_view.input_dict["id_producto"] != str(row_code[0])) or (row_code and not is_id):
            VerboseException.show_error("Codigo de producto ya existe.", f"No se puede agregar un producto con un codigo de barras existente.\n\nProducto Existente:\n{self.__description_product_row(row_code)}", grab_set=True)
            return
        
        yield(STEP_COUNT,"Verificando id del producto...")
        if is_id: dict_id = {}
        else: 
            last_id = self.db.get_next_column_int_value("id_producto",CONFIG["table_product"])
            if last_id is None:
                VerboseException.show_error("No se pudo obtener un ID valido para la inserción del producto.", grab_set=True)
                return
            else: dict_id = {"id_producto":last_id}

        insertion_dict = self.__merge_db_dict({**dict_required, **dict_id, **self.prod_view.input_dict, **self.prod_view.get_info(partial=True)})
        post_dict = self.__merge_http_dict(insertion_dict)

        yield(STEP_COUNT,"Enviando solicitud a Base de Datos Online...")
        if is_id:
            with requests.Session() as session:
                response = session.post(CONFIG["url_edit"], headers=CONFIG["headers_edit"], data=post_dict)
                if response.status_code == 200:
                    is_edited = self.db.update_record(insertion_dict, "id_producto", CONFIG["table_product"])

                    yield (STEP_COUNT, "Enviando solicitud a Base de Datos Local...")
                    if is_edited: VerboseException.show_info("Producto Editado Correctamente",f"Producto Editado:\n{self.__description_product_row(insertion_dict)}",grab_set=True)
                    else: VerboseException.show_info("ERROR PARCIAL:\nBase de Datos Central = CORRECTO\nBase de Datos Local = ERROR","No se pudo editar el producto en la base de datos local, sin embargo, la respuesta del servidor fue positiva.\n\nSe sugiere reiniciar aplicación RJC y verificar los cambios.",grab_set=True)
                else:
                    try: extended_info = response.json()
                    except ValueError: extended_info = response.text
                    VerboseException.show_error(f"Error de conexión: {response.status_code}",f"{extended_info}",grab_set=True)
                response.close()
        else:
            with requests.Session() as session:
                response = session.post(CONFIG["url_add"], headers=CONFIG["headers_add"], data=post_dict)
                if response.status_code == 200:
                    is_insert = self.db.insert_row(insertion_dict, CONFIG["table_product"])

                    yield (STEP_COUNT, "Enviando solicitud a Base de Datos Local...")
                    if is_insert: VerboseException.show_info("Producto Agregado Correctamente",f"Producto Agregado:\n{self.__description_product_row(insertion_dict)}",grab_set=True)
                    else: VerboseException.show_info("ERROR PARCIAL:\nBase de Datos Central -> CORRECTO\nBase de Datos Local -> ERROR","No se pudo editar el producto en la base de datos local, sin embargo, la respuesta del servidor fue positiva.\n\nSe sugiere reiniciar aplicación RJC y verificar los cambios.",grab_set=True)
                else:
                    try: extended_info = response.json()
                    except ValueError: extended_info = response.text
                    VerboseException.show_error(f"Error de conexión: {response.status_code}",f"{extended_info}",grab_set=True)
                response.close()

        self.withdraw()
        self.prod_view.reset()
        yield(STEP_COUNT,"Actualizando información para aplicación...")

        yield(STEP_COUNT, self.__load_db_views_yielded())
        self.__tab_state_reload(tab="Añadir/Editar Producto")

        yield(STEP_COUNT, "Proceso Completado")
        self.__callback_action.force_close()
        self.deiconify()

    @OwnLoadingBar
    def __callback_print(self, tag_config, paper_size):
        STEP_COUNT = 4
        tag_folder = CONFIG["tags_folder"]

        yield(STEP_COUNT, "Obteniendo datos...")
        name_list, price_list = self.tag_view.treeview.get_column_data(["nombre", "precio_venta_boleta"])

        yield(STEP_COUNT, "Limpiando directorio de Etiquetas...")
        OsTools.clean_dir(tag_folder)

        yield(STEP_COUNT, generate_tags_yielded(name_list, price_list, paper_size, 40, tag_config, tag_folder))

        self.withdraw()
        self.prod_view.reset()
        yield(STEP_COUNT,"Actualizando información para aplicación...")

        self.__tab_state_reload("Generar Etiquetas")
        self.update_idletasks()
        self.toggle_views_rows(selected_tag_rows=list(self.tag_view.treeview.visible_rows.values()))
        yield(STEP_COUNT, "Proceso Completado")
        self.__callback_action.force_close()
        self.deiconify()

TagApp()