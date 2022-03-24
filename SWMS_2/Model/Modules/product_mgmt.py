import sys

import Model.DataBase.my_db as db
import Model.Repositories.products_repo as prepo
import Model.Modules.warehouse_mgmt as whmgmt
import json as js


# region CRUD
def create_new_product(id_, name: str, type_: str, b_price: float, s_price: float, quantity: int, assigned_wh):
    """
    Create new product
    :param id_: Id as int or "auto"
    :param name: Product name
    :param type_: Product type
    :param b_price: Product buy price
    :param s_price: Product sell price
    :param quantity: Product quantity
    :param assigned_wh: Product assigned to warehouse
    :return: True/False
    """

    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.products)
    else:
        is_valid = db.validate_entity_id(id_, db.products)
        if not is_valid:
            return False

    type_ = prepo.validate_type(type_, db.allowed_types)
    if not type_:
        print("Invalid type")
        return False

    b_price = prepo.validate_price(b_price)
    if not b_price:
        print("Invalid buy price!")
        return False

    s_price = prepo.validate_price(s_price)
    if not s_price:
        print("Invalid sell price!")
        return False

    if not isinstance(quantity, int):
        print("Invalid quantity!")
        return False

    if not prepo.validate_assigned_wh(assigned_wh, db.warehouses):
        print("Invalid warehouse to assign!")
        return False
    # endregion

    exists, product = prepo.check_product_exist(name, type_, b_price, s_price, quantity, assigned_wh, db.products)
    # If product already exist
    if exists:
        wh = whmgmt.get_wh_by_name(assigned_wh)
        total, free = whmgmt.wh_capacity_info(wh)
        # Increase quantity if possible
        if free >= quantity:
            product.quantity += quantity
        # Else create as new product with new id and assigned to virtual warehouse
        else:
            new_prod = prepo.create_product(db.get_new_entity_id(db.products), name,
                                            type_, b_price, s_price, quantity, "Virtual01")
            db.products.append(new_prod)
    # Else create new product
    else:
        wh = whmgmt.get_wh_by_name(assigned_wh)
        total, free = whmgmt.wh_capacity_info(wh)
        # If no space in assigned warehouse
        if free >= quantity:
            new_prod = prepo.create_product(id_, name, type_, b_price, s_price, quantity, assigned_wh)
        # Create in virtual warehouse
        else:
            new_prod = prepo.create_product(id_, name, type_, b_price, s_price, quantity, "Virtual01")
        db.products.append(new_prod)
        whmgmt.hook_products_to_warehouse()
        return True, "Success"


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
    ptype = prepo.validate_type(new_type, db.allowed_types)
    if not ptype:
        print("Invalid type")
        return False
    product.product_type = ptype
    return True


def edit_product_bprice(id_, new_price):
    product = prepo.get_product_by_id(id_, db.products)
    price = prepo.validate_price(new_price)
    if not price:
        print("Invalid buy price!")
        return False
    product.buy_price = price


def edit_product_sprice(id_, new_price):
    product = prepo.get_product_by_id(id_, db.products)
    price = prepo.validate_price(new_price)
    if not price:
        print("Invalid buy price!")
        return False
    product.sell_price = price


def edit_product_quantity(id_, new_quantity):
    product = prepo.get_product_by_id(id_, db.products)
    if not isinstance(new_quantity, int):
        print("Invalid quantity!")
        return False
    wh = whmgmt.get_wh_by_name(product.assigned_wh)
    total, free = whmgmt.wh_capacity_info(wh)
    if free >= (new_quantity - product.quantity):
        product.quantity = new_quantity
        return True
    else:
        create_new_product("auto", product.product_name, product.product_type,
                           product.buy_price, product.sell_price, new_quantity - product.quantity, "Virtual01")
        whmgmt.hook_products_to_warehouse()
        return True


def edit_product_assigned_warehouse(id_, new_wh_name):
    product = prepo.get_product_by_id(id_, db.products)
    if not prepo.validate_assigned_wh(new_wh_name, db.warehouses):
        print("Invalid warehouse to assign!")
        return False
    product.assigned_wh = new_wh_name
    whmgmt.hook_products_to_warehouse()
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
