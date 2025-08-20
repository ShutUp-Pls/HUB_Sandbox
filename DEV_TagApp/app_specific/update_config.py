import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from own.OwnDbManagment import OwnDbManagmentMDB
from util.func_tools import JsonTools

CONFIG_PATH = "app_specific\\config.json"
CONFIG = JsonTools.load_json(CONFIG_PATH)

def build_family_dictionary(categories, subcategories):
    result = {}
    active_categories = [cat for cat in categories if cat[2] == "S"]

    for category in active_categories:
        category_id, category_name, _ = category
        active_subcategories = {
            str(sub[0]): sub[2]
            for sub in subcategories
            if sub[1] == category_id and sub[3] == "S"
        }

        result[str(category_id)] = {
            "familia": category_name,
            "sub_familia": active_subcategories if active_subcategories else ""
        }

    return result
    
db = OwnDbManagmentMDB(CONFIG["db_path"])
db_tables = db.get_db_tables()
_, product_columns = db.get_table_content(CONFIG["table_product"])
family_rows, _ = db.get_table_content(CONFIG["table_family"])
subfamily_rows, _ = db.get_table_content(CONFIG["table_subfamily"])
taxes_rows, _ = db.get_table_content(CONFIG["table_taxes"])

family_structure = build_family_dictionary(family_rows, subfamily_rows)
categories_structure = {str(key): value["familia"] for key, value in family_structure.items()}
subcategories_structure = {str(key): value["sub_familia"] for key, value in family_structure.items() if value["sub_familia"]}

taxes_structure = {item[0]: item[1] for item in taxes_rows}

info_update ={
    "db_tables":db_tables,
    "product_columns":product_columns,
    "family_structure":family_structure,
    "categories_structure":categories_structure,
    "subcategories_structure":subcategories_structure,
    "taxes_structure":taxes_structure
}

JsonTools.update_json(CONFIG_PATH, info_update)