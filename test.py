import pyodbc

def describe_mdb(file_path):
    try:
        # Conectar a la base de datos .mdb
        conn = pyodbc.connect(
            f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={file_path};"
        )
        cursor = conn.cursor()

        # Obtener todas las tablas en la base de datos
        tables = [row.table_name for row in cursor.tables(tableType='TABLE')]

        if not tables:
            print("No se encontraron tablas en la base de datos.")
            return

        # Describir cada tabla y sus columnas
        for table in tables:
            print(f"Tabla: {table}")
            columns = cursor.columns(table=table)
            for column in columns:
                print(f"  - Columna: {column.column_name}, Tipo: {column.type_name}")
            print()

        # Cerrar la conexión
        conn.close()
    except Exception as e:
        print(f"Error al conectar o describir la base de datos: {e}")

# Ruta al archivo .mdb
mdb_file_path = r"C:\Users\marqu\Desktop\rjc_prod_f1578.mdb"

# Llamar a la función para describir la base de datos
describe_mdb(mdb_file_path)