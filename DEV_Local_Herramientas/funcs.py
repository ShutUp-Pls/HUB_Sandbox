import pyodbc, csv, json
from PIL import Image, ImageDraw, ImageFont

def number_format(number_raw):
    try: number_float = float(number_raw)
    except ValueError:
        print("Entrada no es un número")
        return None

    if number_float.is_integer():
        number_int = int(number_float)
        return f"{number_int:,}".replace(",", ".")
    
    else: return f"{number_float:,.0f}".replace(",", ".")

def str_convert(str_value):
    if isinstance(str_value, str):
        try: return int(str_value)
        except:
            try: return float(str_value)
            except: return str_value

    else: return str_value

def load_json(path):
    with open(path, 'r', encoding='utf-8') as archivo: datos = json.load(archivo)

    return datos

def load_json_convert(path):
    with open(path, 'r', encoding='utf-8') as archivo: datos = json.load(archivo)

    datos_convertidos = {clave: str_convert(valor) for clave, valor in datos.items()}

    return datos_convertidos

def export_to_csv(db_path, table_name, columns, output_csv_path):
    # Conexión a la base de datos Access
    conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={db_path}"
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Crear la query dinámica con las columnas
    query = f"SELECT {', '.join(columns)} FROM {table_name}"
    cursor.execute(query)
    
    # Obtener los resultados
    rows = cursor.fetchall()
    
    # Guardar en CSV
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)
    
    cursor.close()
    conn.close()

def putprice(text_name, text_price, path_config, path_output):
    def put_text_by_char(draw, text, text_font, text_color, text_space, pos_x, pos_y):
        for i, char in enumerate(reversed(text)):
            bbox_char = draw.textbbox((0, 0), char, font=text_font)
            char_ancho = bbox_char[2] - bbox_char[0]
            draw.text((pos_x, pos_y), char, fill=text_color, font=text_font)

            if ((i+1)%3) == 0: pos_x -= char_ancho - 2*text_space
            else: pos_x -= char_ancho - text_space
                    
    config = load_json(path_config)

    imagen = Image.open(config["path"])
    draw = ImageDraw.Draw(imagen)

    for tag in ["price", "name"]:
        font = ImageFont.truetype(config[f"{tag}_font"], config[f"{tag}_size"])
        x_pos = config[f"{tag}_x_pos"]
        y_pos = config[f"{tag}_y_pos"]
        space = config[f"{tag}_space"]
        color = config[f"{tag}_color"]

        if tag == "price": put_text_by_char(draw, text_price, font, color, space, x_pos, y_pos)
        else: put_text_by_char(draw, text_name, font, color, space, x_pos, y_pos)

    imagen.save(path_output)
    print(f"Etiqueta generada y guardada en {path_output}")

# Ejemplo de uso
if __name__ == "__main__":
    # config = load_json(r"etiquetas\plantilla_1.json")
    # ruta_input = r"C:\Users\marqu\Desktop\rjc_prod_f1578.mdb"
    # ruta_output = "datos.csv"
    # tabla = "producto"
    # columnas = ["nombre", "precio_venta_boleta"]

    # export_to_csv(ruta_input,tabla,columnas,ruta_output)

    # ruta_entrada = "etiquetas\\plantilla_1.png"
    # precio = "27.990"

    putprice("Producto", "17.000", path_config="etiquetas\\plantilla_1.json", path_output="etiqueta_ejemplo.png")
    # print(type(load_json(r"C:\Users\marqu\Documents\GitHub\DEV_Local_Herramientas\etiquetas\plantilla_1.json")["color_name"]))