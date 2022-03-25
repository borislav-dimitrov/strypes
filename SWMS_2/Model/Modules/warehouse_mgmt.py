import sys

import Model.Repositories.warehouses_repo as whrep
import Model.DataBase.my_db as db
import json as js


# region CHECKS
def wh_capacity_info(warehouse):
    total = 0
    for product in warehouse.wh_products:
        total += product.quantity
    free = warehouse.wh_capacity - total
    return warehouse.wh_capacity, free


# endregion


# region CRUD
def create_new_wh(id_, name, type_, capacity, products: list, status):
    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.warehouses)
    else:
        is_valid = db.validate_entity_id(id_, db.warehouses)
        if not is_valid:
            print("ID already exist")
            return
    is_valid, msg = whrep.validate_name(name, db.warehouses)
    if not is_valid:
        print(msg)
        return

    is_valid = whrep.validate_type(type_, db.allowed_types)
    if is_valid == -1:
        print("Invalid warehouse type!")
        return

    if not isinstance(capacity, int):
        print("Invalid capacity!")
        return

    status = whrep.validate_status(status)
    if status == -1:
        print("Invalid status")
        return
    # endregion

    new_wh = whrep.create_warehouse(id_, name, type_, capacity, products, status)

    # add to db warehouses
    db.warehouses.append(new_wh)
    return True


def delete_wh(id_: int):
    status, msg = whrep.delete_warehouse(id_, db.warehouses)
    if status:
        db.my_logger.log(__file__, msg, "INFO")
        print(status, msg)
    if not status:
        db.my_logger.log(__file__, msg, "WARNING")
        print(status, msg)


def edit_wh_name(id_, new_name):
    warehouse = whrep.get_wh_by_id(id_, db.warehouses)
    is_valid, msg = whrep.validate_name(new_name, db.warehouses)
    if not is_valid:
        return msg
    warehouse.wh_name = new_name
    reload_whs()
    return True, "Success"


def edit_wh_type(id_, new_type):
    warehouse = whrep.get_wh_by_id(id_, db.warehouses)
    is_valid = whrep.validate_type(new_type, db.allowed_types)
    if is_valid == -1:
        return False, "Invalid warehouse type!"
    warehouse.wh_type = new_type
    reload_whs()
    return True, "Success"


def edit_wh_capacity(id_, new_capacity):
    warehouse = whrep.get_wh_by_id(id_, db.warehouses)
    if not isinstance(new_capacity, int):
        return False, "Invalid capacity!"
    warehouse.wh_capacity = new_capacity
    reload_whs()
    return True, "Success"


def edit_wh_stored_products(id_, new_products: list):
    warehouse = whrep.get_wh_by_id(id_, db.warehouses)
    warehouse.wh_products = new_products
    reload_whs()
    return True, "Success"


def add_product_to_wh(id_, new_product):
    warehouse = whrep.get_wh_by_id(id_, db.warehouses)
    warehouse.wh_products.append(new_product)
    reload_whs()
    return True, "Success"


def edit_wh_status(id_, new_status):
    warehouse = whrep.get_wh_by_id(id_, db.warehouses)
    new_status = whrep.validate_status(new_status)
    if new_status == -1:
        return False, "Invalid status"
    warehouse.wh_status = new_status
    reload_whs()
    return True, "Success"


# endregion


# region Save/Load/Reload
def save_whs():
    output_file = "./Model/DataBase/warehouses.json"
    data = {
        "warehouses": []
    }

    for warehouse in db.warehouses:
        data["warehouses"].append({
            "entity_id": warehouse.entity_id,
            "warehouse_name": warehouse.wh_name,
            "warehouse_type": warehouse.wh_type,
            "warehouse_capacity": warehouse.wh_capacity,
            "warehouse_products": [f"{p.product_name} x {p.quantity}" for p in warehouse.wh_products],
            "warehouse_status": warehouse.wh_status
        })

    try:
        db.save_data_to_json(data, output_file)
        return "Warehouses saved successfully!"
    except Exception as ex:
        msg = "Error saving warehouses!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def load_whs():
    try:
        with open("./Model/DataBase/warehouses.json", "rt", encoding="utf-8") as file:
            data = js.load(file)
    except Exception as ex:
        msg = "Error reading warehouses file!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)

    db.warehouses = []
    try:
        for warehouse in data["warehouses"]:
            new_wh_id = warehouse["entity_id"]
            new_wh_name = warehouse["warehouse_name"]
            new_wh_type = warehouse["warehouse_type"]
            new_wh_capacity = warehouse["warehouse_capacity"]
            new_wh_products = []
            new_wh_status = warehouse["warehouse_status"]

            create_new_wh(new_wh_id, new_wh_name, new_wh_type, new_wh_capacity,
                          new_wh_products, new_wh_status)
        return "Warehouses loaded successfully!"
    except Exception as ex:
        msg = "Error Loading warehouses!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def reload_whs():
    save_whs()
    load_whs()


# endregion


# region OTHER
def hook_products_to_warehouse():
    for warehouse in db.warehouses:
        warehouse.wh_products = []

        for product in db.products:
            if product.assigned_wh.lower() == warehouse.wh_name.lower():
                warehouse.wh_products.append(product)


def get_wh_by_name(name):
    return whrep.get_wh_by_name(name, db.warehouses)


def get_wh_by_id(id_):
    return whrep.get_wh_by_id(id_, db.warehouses)
# endregion
