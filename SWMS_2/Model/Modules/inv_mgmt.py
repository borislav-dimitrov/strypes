import sys

import Model.DataBase.my_db as db
import Model.Repositories.inv_repo as invrepo
import json as js


# region CRUD
def create_new_inv(id_, from_, to_, date, items, price, descr, terms, status):
    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.invoices)
    else:
        is_valid = db.validate_entity_id(id_, db.invoices)
        if not is_valid:
            return False, "Invalid Invoice id!"

    num = invrepo.get_new_inv_number(db.invoices)

    if not isinstance(to_, list) or len(from_) != 7:
        return False, "Invalid Invoice issuer(from) parameters!"

    if not isinstance(to_, list) or len(to_) != 7:
        return False, "Invalid Invoice issuer(to) parameters!"

    if date == "auto":
        date = invrepo.get_inv_date()
    else:
        is_valid, msg = invrepo.validate_date(date)
        if not is_valid:
            return False, msg

    if not items:
        return False, "Invoice items can't be empty!"

    if not isinstance(price, int) or price <= 0 or not price:
        return False, "Invalid Invoice price!"

    state, status = invrepo.valid_inv_status(status)
    if not state:
        return False, status
    # endregion

    new_inv = invrepo.create_invoice(id_, num, from_, to_, date, items, price, descr, terms, status)
    db.invoices.append(new_inv)
    return True, "Success"


def delete_inv(id_):
    state, msg = invrepo.del_invoice(id_, db.invoices)
    return state, msg


def edit_inv_num(id_, number):
    if not isinstance(number, int):
        return False, f"'{number}' is not a valid number!"
    status, msg = invrepo.valid_new_inv_num(number, db.invoices)
    if not status:
        return False, msg
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.invoice_number = f"INV-{number}"
    return True, "Success"


def edit_inv_from(id_, from_):
    if not isinstance(from_, list) or len(from_) != 7:
        return False, "Invalid Invoice issuer(to) parameters!"
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.to_info = from_
    return True, "Success"

def edit_inv_to(id_, to_):
    if not isinstance(to_, list) or len(to_) != 7:
        return False, "Invalid Invoice issuer(to) parameters!"
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.to_info = to_
    return True, "Success"
# endregion


# region Save/Load/Reload

def save_inv():
    pass


def load_inv():
    pass


def save_n_load_inv():
    save_inv()
    load_inv()

# endregion
