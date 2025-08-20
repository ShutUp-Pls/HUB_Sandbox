import tkinter as tk

from tkinter import ttk

from util.func_tools import ListTools, TkTools, FormatTools, DictTools

class OwnTreeviewBase(ttk.Treeview):

    def __init__(self, parent, **kwargs):
        kwargs["show"] = "headings"
        kwargs["selectmode"] = "none"
        super().__init__(parent, **kwargs)

        self.order_dips_lst = ["def", "asc", "des"]
        self.callback_insert = None
        self.reset()

    def reset(self, keep_order=False):
        self.__loaded_rows = []
        self.__available_columns = []
        self.__available_rows = []
        self.__filtered_rows = []

        if not keep_order: self.__order_column = ""
        if not keep_order: self.__order_type = "def"
        if not keep_order: self.__order_last = {}

        self.loaded_columns = []
        self.available_columns = []
        self.visible_columns = []

        self.loaded_rows = []
        self.available_rows = []
        self.visible_rows = []

    def update_treeview(self):
        if self.state() == "normal": self.update()
        self.update_idletasks()

    @property
    def loaded_columns(self):
        return self["columns"]
    
    @loaded_columns.setter
    def loaded_columns(self, columns:list):
        self.visible_columns = []
        self["columns"] = columns
        
    @property
    def available_columns(self):
        return self.__available_columns
    
    @available_columns.setter
    def available_columns(self, columns:list):
        self.__available_columns = ListTools.common(columns, self.loaded_columns)
        self.visible_columns = []

    @property
    def visible_columns(self):
        return self["displaycolumns"]
    
    @visible_columns.setter
    def visible_columns(self, columns:list):
        self["displaycolumns"] = ListTools.common(columns, self.available_columns)
        for column in self["displaycolumns"]: self.heading(column=column, text=column)
        self.__adjust_to_stretch()

    @property
    def loaded_rows(self):
        return self.__loaded_rows
    
    @loaded_rows.setter
    def loaded_rows(self, rows:list):
        self.__loaded_rows = [tuple(str(element) for element in row) for row in rows]
        self.visible_rows = []

    @property
    def available_rows(self):
        return self.__available_rows
    
    @available_rows.setter
    def available_rows(self, rows:list):
        self.__available_rows = ListTools.common(rows, self.loaded_rows)
        self.visible_rows = []

    @property
    def visible_rows(self):
        iids = self.get_children()
        return {iid: self.item(iid, option="values") for iid in iids}
    
    @visible_rows.setter
    def visible_rows(self, rows:list):
        if rows:
            if self.__filtered_rows: rows = ListTools.common(rows, self.__filtered_rows)
            else: rows = ListTools.common(rows, self.__available_rows)
            self.delete(*self.get_children())

            total = len(rows)
            if self.callback_insert: 
                for idx, row in enumerate(rows):
                    self.callback_insert(idx, total, f"Insertando fila {idx} de {total}...")
                    self.insert("", tk.END, values=tuple(row))

            else:
                for row in rows: self.insert("", tk.END, values=tuple(row))
            self.__order_data()

        else: self.delete(*self.get_children())

    def visible_rows_yielded(self, rows:list):
        if rows:
            if self.__filtered_rows: rows = ListTools.common(rows, self.__filtered_rows)
            else: rows = ListTools.common(rows, self.__available_rows)
            self.delete(*self.get_children())

            total = len(rows)
            for idx, row in enumerate(rows):
                yield(total, f"Insertando fila {idx} de {total}...")
                self.insert("", tk.END, values=tuple(row))
            self.__order_data()

        else: self.delete(*self.get_children())

    @property
    def order_column(self):
        return self.__order_column
    
    @order_column.setter
    def order_column(self, column):
        if column in self.__available_columns:
            if column == self.__order_column: self.__order_type = ListTools.next_in(self.__order_type, self.order_dips_lst)
            else:
                self.__order_column = column
                self.__order_type = "asc"
                
        else: self.__order_column = ""

    @property
    def order_type(self):
        return self.__order_type
    
    @order_type.setter
    def order_type(self, order:str):
        if order in self.order_dips_lst and self.__order_column: self.__order_type = order
        else: self.__order_type = "def"

    def set_load_treeview(self, rows:list=None, columns:list=None, avaible_columns:list=None, avaible_rows:list=None, visible_columns:list=None, visible_rows:list=None):
        rows = rows if rows else self.loaded_rows
        columns = columns if columns else self.loaded_columns

        self.loaded_columns = columns
        self.available_columns = self.loaded_columns if avaible_columns is None else avaible_columns
        self.visible_columns = self.available_columns if visible_columns is None else visible_columns

        self.loaded_rows = rows
        self.available_rows = self.loaded_rows if avaible_rows is None else avaible_rows
        self.visible_rows = self.available_rows if visible_rows is None else visible_rows

    def set_load_treeview_yielded(self, rows:list=None, columns:list=None, avaible_columns:list=None, avaible_rows:list=None, visible_columns:list=None, visible_rows:list=None):
        STEP_COUNT = 1
        
        rows = rows if rows else self.loaded_rows
        columns = columns if columns else self.loaded_columns

        self.loaded_columns = columns
        self.available_columns = self.loaded_columns if avaible_columns is None else avaible_columns
        self.visible_columns = self.available_columns if visible_columns is None else visible_columns
        yield(STEP_COUNT, "Carga Columnas Completa")

        self.loaded_rows = rows
        self.available_rows = self.loaded_rows if avaible_rows is None else avaible_rows
        yield(STEP_COUNT, self.visible_rows_yielded(self.available_rows))

    def set_avaible_treeview(self, rows:list=None, columns:list=None, visible_columns:list=None, visible_rows:list=None):
        rows = rows if rows else self.available_rows
        columns = columns if columns else self.available_columns

        self.available_rows = rows
        self.visible_rows = self.available_rows if visible_rows is None else visible_rows

        self.available_columns = columns
        self.visible_columns = self.available_columns if visible_columns is None else visible_columns

    def set_columns_config(self, columns:list=[], **kwargs):
        common_list = ListTools.common(columns, self.available_columns)
        for col in common_list: self.column(column=col, **kwargs)

    def get_column_data(self, columns:list, from_tree="visible"):
        indices = [self.loaded_columns.index(column) for column in columns]

        if from_tree == "loaded": rows = self.loaded_rows
        elif from_tree == "available": rows = self.available_rows
        elif from_tree == "visible": rows = list(self.visible_rows.values())
        else: rows = list(self.visible_rows.values())

        return tuple([row[idx] for row in rows] for idx in indices)

    def filter_data(self, column, str_filter=""):
        if str_filter:
            filter_words = str(str_filter).lower().split()

            column_index = self.loaded_columns.index(column)
            rows = [row for row in self.available_rows if all(word in str(row[column_index]).lower() for word in filter_words)]

            self.__filtered_rows = rows
            self.visible_rows = self.__filtered_rows
        else:
            self.__filtered_rows = []
            self.visible_rows = self.available_rows

    def order_data(self, column:str=None, order:str=None):
        self.order_column = column if column else self.order_column
        self.order_type = order if order else self.order_type
        self.__order_data()
        return self.__order_column, self.__order_type
    
    def __adjust_to_stretch(self):
        self.update_treeview()
        column_numb = len(self.visible_columns)
        stretch_size = (self.winfo_width()//(column_numb if column_numb != 0 else 1))

        self.set_columns_config(self.visible_columns, width=stretch_size)

    def __order_data(self):
        if {self.__order_column:self.__order_type} == self.__order_last: return

        elif self.order_column == "" or self.order_type == "def":
            visible_rows = list(self.visible_rows.values())
            rows = ListTools.common(self.available_rows, visible_rows)
            self.delete(*self.get_children())
            for row in rows: self.insert("", tk.END, values=tuple(row))

        else:
            valid_data = []
            missing_data = []
            for item in self.visible_rows:
                value = FormatTools.safe_cast_value(self.set(item, self.order_column))
                if value is None: missing_data.append((value, item))
                else: valid_data.append((value, item))

            reverse = (self.order_type == "des")
            valid_data.sort(key=lambda entry: (isinstance(entry[0], str), entry[0]), reverse=reverse)
            sorted_data = valid_data + missing_data if reverse else missing_data + valid_data
            for index, (_, item) in enumerate(sorted_data): self.move(item, "", index)

        self.__order_last = {self.__order_column:self.__order_type}

class OwnTreeviewScroll(OwnTreeviewBase):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        TkTools.configure_grid(parent, [1, 0], [1, 0])

        self.__scrollv_visible = False
        self.__scrollh_visible = False

        self.__scrollbar_vertical = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
        self.__scrollbar_horizontal = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)

        self.grid(row=0, column=0, sticky=tk.NSEW)

        self.configure(yscrollcommand=self.__toggle_vertical_scroll, xscrollcommand=self.__toggle_horizontal_scroll)

    def __toggle_vertical_scroll(self, *args):
        self.__scrollbar_vertical.set(*args)
        visible = float(args[1]) - float(args[0]) < 1.0 and self.get_children()

        if visible and not self.__scrollv_visible:
            self.__scrollbar_vertical.grid(row=0, column=1, sticky=tk.NS)
            self.__scrollv_visible = True

        elif not visible and self.__scrollv_visible:
            self.__scrollbar_vertical.grid_remove()
            self.__scrollv_visible = False
    
    def __toggle_horizontal_scroll(self, *args):
        self.__scrollbar_horizontal.set(*args)
        visible = float(args[1]) - float(args[0]) < 1.0 and self.get_children()

        if visible and not self.__scrollh_visible:
            self.__scrollbar_horizontal.grid(row=1, column=0, sticky=tk.EW)
            self.__scrollh_visible = True

        elif not visible and self.__scrollh_visible:
            self.__scrollbar_horizontal.grid_remove()
            self.__scrollh_visible = False

    def get_vertical_scroll_position(self):
        return self.yview()

    def set_vertical_scroll_position(self, start, end=None):
        if end is None: self.yview_moveto(start)
        else: self.yview_scroll(start, end)

    def get_horizontal_scroll_position(self):
        return self.xview()

    def set_horizontal_scroll_position(self, start, end=None):
        if end is None: self.xview_moveto(start)
        else: self.xview_scroll(start, end)

class OwnTreeviewEvents(OwnTreeviewScroll):
    def __init__(self, parent, selection_mode="extended", **kwargs):
        super().__init__(parent, **kwargs)

        self.callback_pivot = None

        self.__key_set = set()

        self.__update_click_info()

        self.__selection_mode = selection_mode
        self.__selected_pivot = ""

        self.bind("<Button-1>", self.__left_click_action)
        self.bind("<KeyPress>", self.__key_click_on)
        self.bind("<KeyRelease>", self.__key_click_off)

    @property
    def selected_rows(self):
        iids = self.selection()
        return {iid: self.item(iid, option="values") for iid in iids}

    @selected_rows.setter
    def selected_rows(self, rows_ids:list):
        rows_ids = ListTools.common(rows_ids, list(self.visible_rows.keys()))
        self.selection_set(rows_ids)

    @property
    def selected_pivot(self):
        return self.__selected_pivot
    
    @selected_pivot.setter
    def selected_pivot(self, row_id:str):
        row_id = row_id if row_id in list(self.visible_rows.keys()) else ""
        self.__selected_pivot = row_id

        if self.callback_pivot:
            if row_id: self.callback_pivot({row_id:self.item(row_id, option="values")})
            else: self.callback_pivot({})

    @property
    def selected_mode(self):
        return self.__selection_mode
    
    @selected_mode.setter
    def selected_mode(self, mode:str):
        self.__selection_mode = mode
        self.selected_rows = []

    def __key_click_on(self, event):
        self.__key_set.add(event.keysym)

        if event.keysym in ("Up", "Down") and self.selected_pivot:
            all_items = list(self.visible_rows.keys())
            current_index = all_items.index(self.selected_pivot)
            
            if event.keysym == "Up" and current_index > 0: new_index = current_index - 1
            elif event.keysym == "Down" and current_index < len(all_items) - 1: new_index = current_index + 1
            else: return

            self.selected_pivot = all_items[new_index]
            self.selected_rows = [all_items[new_index]]

    def __key_click_off(self, event):
        self.__key_set.discard(event.keysym)

    def __left_click_action(self, event):
        self.__update_click_info(event.x, event.y)

        if self.__click["region"] == "heading": self.order_data(column=self.__click["column_name"])
        self.__select_item()

        self.__update_click_info()

    def __update_click_info(self, coord_x=-1, coord_y=-1):
        region = self.identify("region", coord_x, coord_y) or ""
        column_id = self.identify_column(coord_x) or ""
        column_idx = int(column_id.replace("#", "")) - 1 if column_id else ""
        column_name = self.visible_columns[column_idx] if column_id and self.visible_columns else ""
        item_id = self.identify_row(coord_y) or ""
        item_row = self.item(item_id, option="values") if item_id else ""
        item_name = item_row[self.loaded_columns.index(column_name)] if item_id and column_name else ""

        self.__click = {"region":region, "column_id":column_id, "column_idx":column_idx, "column_name":column_name,
                            "item_id":item_id, "item_row":item_row, "item_name":item_name}

        if region == "cell" and item_id:
            item_in_selected_rows = item_id in list(self.selected_rows.keys())
            shift_pressed = "Shift_L" in self.__key_set
            
            if shift_pressed and self.selected_pivot: pass
            elif not shift_pressed and item_in_selected_rows: self.selected_pivot = ""
            else: self.selected_pivot = item_id

    def __select_item(self):
        if not self.__click["item_id"]: return

        item_id = self.__click["item_id"]
        selected_rows = list(self.selected_rows.keys())
        all_items = list(self.visible_rows.keys())

        if self.__selection_mode == "simple": self.selected_rows = [] if item_id in selected_rows else [item_id]

        if self.__selection_mode == "extended":
            if "Control_L" in self.__key_set: self.selected_rows = ListTools.toggle_item(item_id, selected_rows)
            
            elif "Shift_L" in self.__key_set and self.selected_pivot:
                    idx_ini = all_items.index(self.selected_pivot)
                    idx_fin = all_items.index(item_id)
                    self.selected_rows = all_items[min(idx_ini, idx_fin): max(idx_ini, idx_fin) + 1]

            else: self.selected_rows = [] if item_id in selected_rows else [item_id]

        if self.__selection_mode == "multiply":                
            if "Shift_L" in self.__key_set and self.selected_pivot:
                idx_ini = all_items.index(self.selected_pivot)
                idx_fin = all_items.index(item_id)
                new_selection = all_items[min(idx_ini, idx_fin): max(idx_ini, idx_fin) + 1]
                self.selected_rows = list(set(selected_rows + new_selection))

            else: self.selected_rows = ListTools.toggle_item(item_id, selected_rows)

class OwnTreeview(tk.Frame):
    def __init__(self, parent, type=None, selection_mode="extended", **kwargs):
        super().__init__(parent, **kwargs)

        if type == "base": self.treeview = OwnTreeviewBase(self)
        elif type == "scroll": self.treeview = OwnTreeviewScroll(self)
        elif type == "event": self.treeview = OwnTreeviewEvents(self, selection_mode=selection_mode)
        else: self.treeview = OwnTreeviewEvents(self, selection_mode=selection_mode)