import sys

import Model.DataBase.my_db as db
import Model.Repositories.products_repo as prepo
import json as js


# region Validations

def validate_id(id_):
    if id_ == "auto":
        uid = db.get_new_entity_id(db.products)
        return uid
    else:
        is_valid = db.validate_entity_id(id_, db.products)
        if not is_valid:
            return "ID already exist"
    return id_


def validate_type(type_):
    prod_type = "none"
    for item in db.allowed_types:
        if type_.lower() in item.lower():
            prod_type = item
    if prod_type == "none":
        print(f"Invalid product type {type_}!")
        return False
    return prod_type


def validate_price(price):
    if isinstance(price, float):
        return price
    if isinstance(price, int):
        return float(price)
    return False


def validate_assigned_wh(wh):
    for warehouse in db.warehouses:
        if warehouse.wh_name.lower() == wh.lower():
            return True
    return False


# endregion


# region CRUD
def create_new_product(id_, name: str, type_: str, bprice: float, sprice: float, quantity: int, assigned_wh):
    """
    Create new product
    :param id_: Id as int or "auto"
    :param name: Product name
    :param type_: Product type
    :param bprice: Product buy price
    :param sprice: Product sell price
    :param quantity: Product quantity
    :param assigned_wh: Product assigned to warehouse
    :return: True/False
    """
    pid = validate_id(id_)
    if isinstance(pid, str):
        return False

    ptype = validate_type(type_)
    if not ptype:
        print("Invalid type")
        return False

    b_price = validate_price(bprice)
    if not b_price:
        print("Invalid buy price!")
        return False

    s_price = validate_price(sprice)
    if not s_price:
        print("Invalid sell price!")
        return False

    if not isinstance(quantity, int):
        print("Invalid quantity!")
        return False

    if not validate_assigned_wh(assigned_wh):
        print("Invalid warehouse to assign!")
        return False

    # TODO assign wh id not object !!!!
    # TODO check if there is enough space in the assigned warehouse
    # TODO if not create with assigned none
    new_prod = prepo.create_product(pid, name, ptype, b_price, s_price, quantity, assigned_wh)
    db.products.append(new_prod)
    return True


def delete_product(id_):
    product = prepo.get_product_by_id(id_, db.products)
    db.products.pop()
    save_n_load_products()
    return True


def edit_product_name(id_, new_name):
    product = prepo.get_product_by_id(id_, db.products)
    product.product_name = new_name
    return True


def edit_product_type(id_, new_type):
    product = prepo.get_product_by_id(id_, db.products)
    ptype = validate_type(new_type)
    if not ptype:
        print("Invalid type")
        return False
    product.product_type = ptype
    return True


def edit_product_bprice(id_, new_price):
    product = prepo.get_product_by_id(id_, db.products)
    price = validate_price(new_price)
    if not price:
        print("Invalid buy price!")
        return False
    product.buy_price = price


def edit_product_sprice(id_, new_price):
    product = prepo.get_product_by_id(id_, db.products)
    price = validate_price(new_price)
    if not price:
        print("Invalid buy price!")
        return False
    product.sell_price = price


def edit_product_quantity(id_, new_quantity):
    product = prepo.get_product_by_id(id_, db.products)
    if not isinstance(new_quantity, int):
        print("Invalid quantity!")
        return False
    # TODO check if assigned_wh have space
    have_space = True
    if have_space:
        product.quantity = new_quantity
        return True
    else:
        print("Not enough room in assigned warehouse!")
        return False


def edit_product_assigned_warehouse(id_, new_wh):
    product = prepo.get_product_by_id(id_, db.products)
    if not validate_assigned_wh(new_wh):
        print("Invalid warehouse to assign!")
        return False
    product.assigned_wh = new_wh
    return True


# endregion


# region Save/Load/Reload
def save_products():
    output_file = "./Model/DataBase/products.json"
    data = {
        "products": []
    }

    for product in db.products:
        data["products"].append({
            "entity_id": product.entity_id,
            "product_name": product.product_name,
            "product_type": product.product_type,
            "buy_price": product.buy_price,
            "sell_price": product.sell_price,
            "quantity": product.quantity,
            "assigned_warehouse": "none"
        })

    db.save_data_to_json(data, output_file)


def load_products():
    try:
        with open("./Model/DataBase/products.json", "rt", encoding="utf-8") as file:
            data = js.load(file)
    except Exception as ex:
        msg = "Error loading products!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)

    db.products = []
    try:
        for prod in data["products"]:
            new_prod_id = prod["entity_id"]
            new_prod_name = prod["product_name"]
            new_prod_type = prod["product_type"]
            new_buy_price = prod["buy_price"]
            new_sell_price = prod["sell_price"]
            new_quantity = prod["quantity"]
            new_assigned_wh = prod["assigned_warehouse"]
            create_new_product(new_prod_id, new_prod_name, new_prod_type, new_buy_price,
                               new_sell_price, new_quantity, new_assigned_wh)
    except Exception as ex:
        msg = "Error loading products!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def save_n_load_products():
    save_products()
    load_products()
# endregion
