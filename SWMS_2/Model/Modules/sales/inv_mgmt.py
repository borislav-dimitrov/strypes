import os
import sys

import Model.DataBase.my_db as db
import Model.Repositories.inv_repo as invrepo
import Model.Modules.sales.transaction_mgmt as trmgmt
from Model.Entities.counterparty import Counterparty
import Model.Modules.sales.counterparty_mgmt as ctrpmgmt
import json as js


# region CRUD
def create_new_inv(id_, num, from_, to_, date, due_to, items: list[str, int, float], descr, terms, status):
    """

    :param id_: "auto" or int
    :param num: "auto" or int
    :param from_:
    :param to_:
    :param date: "auto" or date
    :param due_to: "auto" or date
    :param items:
    :param descr:
    :param terms:
    :param status:
    :return:
    """
    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.invoices)
    else:
        is_valid = db.validate_entity_id(id_, db.invoices)
        if not is_valid:
            return False, "Invalid Invoice id!"

    if num == "auto":
        num = invrepo.get_new_inv_number(db.invoices)
    elif num != "auto":
        if not isinstance(num, int):
            return False, f"'{num}' is not a valid number!"
        stat, msg = invrepo.valid_new_inv_num(num, db.invoices)
        if not stat:
            return False, msg

    if not isinstance(from_, Counterparty):
        return False, "Invalid invoicer counterparty!"

    if not isinstance(to_, Counterparty):
        return False, "Invalid invoice bill to counterparty!"

    if date == "auto":
        date = invrepo.get_inv_date()
    else:
        is_valid, msg = invrepo.validate_date(date)
        if not is_valid:
            return False, msg

    if due_to == "auto":
        due_to = invrepo.get_inv_date()
    else:
        is_valid, msg = invrepo.validate_date(due_to)
        if not is_valid:
            return False, msg

    price = 0

    for item in items:
        if not isinstance(item[0], str) and not isinstance(item[1], int) and not isinstance(item[2], float):
            return False, "Invalid transaction assets!"
        price += item[1] * item[2]

    state, status = invrepo.valid_inv_status(status)
    if not state:
        return False, status
    # endregion

    new_inv = invrepo.create_invoice(id_, num, from_, to_, date, due_to, items, price, descr, terms, status)
    db.invoices.append(new_inv)
    hook_invoices_to_transactions()
    return True, "Success", new_inv


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
    invoice.invoice_number = number
    reload_inv()
    return True, "Success"


def edit_inv_from(id_, from_):
    if not isinstance(from_, Counterparty):
        return False, "Invalid invoicer counterparty!"
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.to_info = from_
    reload_inv()
    return True, "Success"


def edit_inv_to(id_, to_):
    if not isinstance(to_, Counterparty):
        return False, "Invalid invoicer counterparty!"
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.to_info = to_
    reload_inv()
    return True, "Success"


def edit_inv_date(id_, date):
    if date == "auto":
        date = invrepo.get_inv_date()
    else:
        is_valid, msg = invrepo.validate_date(date)
        if not is_valid:
            return False, msg
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.invoice_date = date
    reload_inv()
    return True, "Success"


def edit_inv_items(id_, items):
    if not isinstance(items, list) or not items:
        return False, "Invalid Invoice item list!"
    for item in items:
        if len(item) < 3:
            return False, f"Invalid item - {item}"
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.items = items
    reload_inv()
    return True, "Success"


def edit_inv_status(id_, status):
    state, status = invrepo.valid_inv_status(status)
    if not state:
        return False, status
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    invoice.status = status
    reload_inv()
    return True, "Success"


# endregion


# region Save/Load/Reload
def hook_invoices_to_transactions():
    for transaction in db.transactions:
        for invoice in db.invoices:
            if invoice.invoice_number == transaction.invoice:
                transaction.invoice = invoice


def save_inv():
    output_file = "./Model/DataBase/invoices.json"
    data = {"invoices": []}

    for invoice in db.invoices:
        data["invoices"].append({
            "entity_id": invoice.entity_id,
            "invoice_number": invoice.invoice_number,
            "invoice_from": invoice.from_info.entity_id,
            "invoice_to": invoice.to_info.entity_id,
            "invoice_date": invoice.invoice_date,
            "due_to": invoice.due_to,
            "invoice_items": invoice.items,
            "invoice_total_price": invoice.total_price,
            "invoice_description": invoice.description,
            "invoice_terms": invoice.terms_conditions,
            "invoice_status": invoice.status
        })

    try:
        db.save_data_to_json(data, output_file)
    except Exception as ex:
        msg = "Error saving invoices!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def load_inv():
    try:
        with open("./Model/DataBase/invoices.json", "rt", encoding="utf-8") as file:
            data = js.load(file)
    except Exception as ex:
        msg = "Error reading users file!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)

    db.invoices.clear()

    try:
        for invoice in data["invoices"]:
            new_inv_id = invoice["entity_id"]
            new_inv_number = invoice["invoice_number"]
            new_inv_from = ctrpmgmt.cptrepo.get_cprty_by_id(invoice["invoice_from"], db.counterparties)
            new_inv_to = ctrpmgmt.cptrepo.get_cprty_by_id(invoice["invoice_to"], db.counterparties)
            new_inv_date = invoice["invoice_date"]
            new_inv_due_to = invoice["due_to"]
            new_inv_items = invoice["invoice_items"]
            new_inv_description = invoice["invoice_description"]
            new_inv_terms = invoice["invoice_terms"]
            new_inv_status = invoice["invoice_status"]

            create_new_inv(new_inv_id, new_inv_number, new_inv_from, new_inv_to, new_inv_date,
                           new_inv_due_to, new_inv_items, new_inv_description,
                           new_inv_terms, new_inv_status)
        hook_invoices_to_transactions()
        trmgmt.save_transact()
    except Exception as ex:
        msg = "Error Loading invoices!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def reload_inv():
    save_inv()
    load_inv()


# endregion


def generate_invoice(id_):
    invoice = invrepo.get_inv_by_id(id_, db.invoices)
    curr_dir = os.getcwd()
    path = os.path.join(curr_dir, f"Resources\\invoices\\{invoice.invoice_number}.pdf")
    status = invrepo.generate_pdf(invoice, db.my_logger, path=path)

    if status:
        os.startfile(path)
        pass
    else:
        return False, "Failed to generate invoice!"
