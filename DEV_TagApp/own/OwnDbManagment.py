import pyodbc

from own.OwnExceptions import VerboseExceptionHandler

class OwnDbManagmentMDB:
    CONNECTION_COMMAND = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={};"
    SELECT_TABLE_COMMAND = "SELECT * FROM {table}"
    CHECK_IN_COLUMN_COMMAND = "SELECT 1 FROM {table} WHERE {column} = ?"
    INSERT_ROW_COMMAND = "INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    SEARCH_ON_COLUMN_COMMAND = "SELECT * FROM {table} WHERE {column} = ?"
    DELETE_ON_COLUMN_COMMAND = "DELETE FROM {table} WHERE {where_clause}"
    UPDATE_ON_COLUMN_COMMAND = "UPDATE {table} SET {set_clause} WHERE {key_column} = ?"

    def __init__(self, db_path):
        self.connection = db_path

    @property
    def connection(self):
        try:
            self.__connection.cursor().execute("SELECT 1")
            return self.__connection
        
        except:
            print(f"No se validó la conexión.")
            return None

    @connection.setter
    def connection(self, path:str):
        try: self.__connection = pyodbc.connect(self.CONNECTION_COMMAND.format(path))
        except:
            print(f"No se pudo establecer conexión con:\n{path}\n")
            self.__connection = None

    @VerboseExceptionHandler
    def value_exists_in_column(self, value:any, column:str, table:str):
        def except_action(*args, **kwargs):  return False
        self.insert_row.set_except(except_action)

        con = self.connection
        if con:
            cursor = con.cursor()
            query = self.CHECK_IN_COLUMN_COMMAND.format(table=table, column=column)
            cursor.execute(query, value)
            return cursor.fetchone() is not None
        
        else: return False

    @VerboseExceptionHandler
    def get_db_tables(self):
        def except_action(*args, **kwargs):  return []
        self.insert_row.set_except(except_action)

        con = self.connection
        if con:
            cursor = con.cursor()
            return [row.table_name for row in cursor.tables(tableType="TABLE")]
        
        else: return []

    @VerboseExceptionHandler
    def get_table_content(self, table:str):
        def except_action(*args, **kwargs):  return [], []
        self.insert_row.set_except(except_action)

        con = self.connection
        if con:
            cursor = con.cursor()
            cursor.execute(self.SELECT_TABLE_COMMAND.format(table=table))

            table_columns = [column[0] for column in cursor.description]
            table_rows = cursor.fetchall()
            return table_rows, table_columns

        else: [], []

    @VerboseExceptionHandler
    def get_row_by_column_value(self, value:any, column:str, table:str):
        def except_action(*args, **kwargs):  return None
        self.insert_row.set_except(except_action)

        con = self.connection
        if con:
            cursor = con.cursor()
            query = self.SEARCH_ON_COLUMN_COMMAND.format(table=table, column=column)
            cursor.execute(query, value)
            row = cursor.fetchone()
            return row
        
        else: return None

    @VerboseExceptionHandler
    def get_next_column_int_value(self, column: str, table:str=None):
        def except_action(*args, **kwargs): return None
        self.get_next_column_int_value.set_except(except_action)

        con = self.connection
        if con:
            rows, columns = self.get_table_content(table)
            column_idx = columns.index(column)

            values = {row[column_idx] for row in rows if isinstance(row[column_idx], (int, float))}

            if values: next_value = min(set(range(1, max(values) + 2)) - values)
            else: next_value = 1
            return next_value
        
        else: None

    @VerboseExceptionHandler
    def update_record(self, updates: dict, key_column:str, table:str=None):
        def except_action(*args, **kwargs): return False
        self.update_record.set_except(except_action)

        con = self.connection
        if con:
            where_value = updates.pop(key_column)
            set_clause = ", ".join(f"{column} = ?" for column in updates.keys())
            values = list(updates.values()) + [where_value]

            cursor = con.cursor()
            query = self.UPDATE_ON_COLUMN_COMMAND.format(table=table, set_clause=set_clause, key_column=key_column)
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                con.commit()
                return True
            return False
        
        else: return False

    @VerboseExceptionHandler
    def insert_row(self, row_data:dict, table:str=None):
        def except_action(*args, **kwargs):  return False
        self.insert_row.set_except(except_action)

        con = self.connection
        if con:
            columns = ", ".join(row_data.keys())
            placeholders = ", ".join(["?"] * len(row_data))
            values = list(row_data.values())

            cursor = con.cursor()
            query = self.INSERT_ROW_COMMAND.format(table=table, columns=columns, placeholders=placeholders)
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                con.commit()
                return True
            return False
        
        else: False

    @VerboseExceptionHandler
    def delete_row(self, conditions:dict, table:str):
        def except_action(*args, **kwargs): return False
        self.delete_row.set_except(except_action)

        con = self.connection
        if con:
            where_clause = " AND ".join([f"{col} = ?" for col in conditions.keys()])
            values = list(conditions.values())

            cursor = con.cursor()
            query = self.DELETE_ON_COLUMN_COMMAND.format(table=table, where_clause=where_clause)
            cursor.execute(query, values)
            if cursor.rowcount > 0:
                con.commit()
                return True
            return False
        
        else: return False
        