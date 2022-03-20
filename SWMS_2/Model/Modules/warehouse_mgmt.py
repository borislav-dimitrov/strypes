import sys

import Model.Repositories.warehouses_repo as whrep
import Model.DataBase.my_db as db
import json as js


# region CRUD
def create_new_wh(id_, name, type_, capacity, products: list[int], status):
    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.users)
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

    valid_products, msg = whrep.validate_products(products)
    if not valid_products:
        print(msg)
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


def delete_wh():
    pass


def edit_wh_name():
    pass


def edit_wh_type():
    pass


def edit_wh_capacity():
    pass


def edit_wh_stored_products():
    pass


def edit_wh_status():
    pass


# endregion


# region Save/Load/Reload
def load_whs():
    pass


def save_whs():
    pass


def reload_whs():
    pass
# endregion
