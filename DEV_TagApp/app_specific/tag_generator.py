import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PIL import Image, ImageDraw, ImageFont
from util.func_tools import FormatTools, JsonTools, PillowTools, OsTools

def fit_count(paper_width, paper_height, image_width, image_height, image_padding):
    def count_images(fit_width, fit_height, img_width, img_height, padding):
        cols = fit_width // (img_width + padding)
        rows = fit_height // (img_height + padding)
        return cols * rows
    
    original_count = count_images(paper_width, paper_height, image_width, image_height, image_padding)
    rotated_count = count_images(paper_width, paper_height, image_height, image_width, image_padding)

    return original_count, rotated_count

def generate_tags_yielded(name_list, price_list, paper_size, padding, path_config, path_output):
    config = JsonTools.load_json(path_config)
    imagen = Image.open(config["path"])

    paper_width, paper_height = paper_size
    image_width, image_height = imagen.size
    og_fit, rt_fit = fit_count(paper_width=paper_width, paper_height=paper_height, image_width=image_width, image_height=image_height, image_padding=padding)
    rotate = rt_fit > og_fit

    print(f"rt: {rt_fit}\nog: {og_fit}")

    imagenes = []
    total = len(name_list)
    for idx in range(len(name_list)):
        yield (total, f"Generando etiqueta {idx+1} de {total}...")
        price_list[idx] = FormatTools.number_to_str(price_list[idx])[:config["price_max_ch"]]
        name_list[idx] = name_list[idx][:config["name_max_ch"]]

        imagen = Image.open(config["path"])
        draw = ImageDraw.Draw(imagen)

        for tag in ["price", "name"]:
            font = ImageFont.truetype(config[f"{tag}_font"], config[f"{tag}_size"])
            x_pos = config[f"{tag}_x_pos"]
            y_pos = config[f"{tag}_y_pos"]
            space = config[f"{tag}_space"]
            color = config[f"{tag}_color"]

            if tag == "price": PillowTools.put_text_by_char(draw, price_list[idx], font, color, space, x_pos, y_pos, direction='rtl', point_space=True)
            else: PillowTools.put_text_by_char(draw, name_list[idx], font, color, space, x_pos, y_pos, direction='ltr', point_space=False)

        if rotate:
            imagen = imagen.rotate(90, expand=True)
        imagenes.append(imagen)

    paginas = []
    pagina_actual = Image.new("RGB", paper_size, "white")

    x_offset = padding
    y_offset = padding
    max_row_height = 0

    for idx, img in enumerate(imagenes):
        img_width, img_height = img.size

        if x_offset + img_width > paper_width:
            x_offset = padding
            y_offset += max_row_height + padding
            max_row_height = 0

        if y_offset + img_height > paper_height:
            paginas.append(pagina_actual)
            pagina_actual = Image.new("RGB", paper_size, "white")
            x_offset = padding
            y_offset = padding
            max_row_height = 0

        pagina_actual.paste(img, (x_offset, y_offset))
        x_offset += img_width + padding
        max_row_height = max(max_row_height, img_height)
        
    paginas.append(pagina_actual)
    

    for idx,pagina in enumerate(paginas): pagina.save(os.path.join(path_output, f"page_{OsTools.len_files(path_output)}.png"))