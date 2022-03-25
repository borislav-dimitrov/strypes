import sys
import Model.DataBase.my_db as db
import Model.Repositories.transaction_repo as trepo
import Model.Modules.sales.counterparty_mgmt as cptmgmt
from Model.Entities.counterparty import Counterparty
import json as js


# region CRUD
def create_transact(id_, type_, counterparty, assets: list[list], invoice=None, date="auto"):
    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.transactions)
    else:
        is_valid = db.validate_entity_id(id_, db.transactions)
        if not is_valid:
            return False, "Invalid Invoice id!"

    state, type_ = trepo.type_is_valid(type_)
    if not state:
        return False, type_

    if date != "auto":
        state, msg = trepo.validate_date(date)
        if not state:
            return False, msg
    else:
        date = trepo.get_date()

    if not isinstance(counterparty, Counterparty):
        return False, "Invalid counterparty!"

    price = 0

    for item in assets:
        if not isinstance(item[0], str) and not isinstance(item[1], int) and not isinstance(item[2], float):
            return False, "Invalid transaction assets!"
        price += item[1] * item[2]

    if not isinstance(invoice, int):
        return False, "Invalid invoice number"

    # endregion
    new_transact = trepo.create_transact(id_, type_, date, price, counterparty, assets, invoice)
    db.transactions.append(new_transact)
    return True, "Success", new_transact


def del_transact(id_):
    trepo.del_transact(id_, db.transactions)
    reload_transact()
    return True, "Success"


def edit_transact_type(id_, type_):
    state, type_ = trepo.type_is_valid(type_)
    if not state:
        return False, type_
    transaction = trepo.get_transact_by_id(id_, db.transactions)
    transaction.type = type_
    reload_transact()
    return True, "Success"


def edit_transact_counterparty(id_, counterparty):
    if not isinstance(counterparty, Counterparty):
        return False, "Invalid counterparty!"
    transaction = trepo.get_transact_by_id(id_, db.transactions)
    transaction.counterparty = counterparty
    reload_transact()
    return True, "Success"


def edit_transact_assets(id_, assets):
    price = 0

    for item in assets:
        if not isinstance(item[0], str) and not isinstance(item[1], int) and not isinstance(item[2], float):
            return False, "Invalid transaction assets!"
        price += item[1] * item[2]

    transaction = trepo.get_transact_by_id(id_, db.transactions)
    transaction.assets = assets
    transaction.price = price
    reload_transact()
    return True, "Success"


def edit_transact_invoice(id_, invoice=None):
    """

    :param id_: transaction id
    :param invoice: invoice number
    :return:
    """
    if invoice:
        state, msg, invoice = trepo.validate_inv_exist(invoice, db.invoices)
        if not state:
            return False, msg
    new_invoice = invoice
    transaction = trepo.get_transact_by_id(id_, db.transactions)
    transaction.invoice = new_invoice
    reload_transact()
    return True, "Success"


def edit_transact_date(id_, date="auto"):
    if date != "auto":
        state, msg = trepo.validate_date(date)
        if not state:
            return False, msg
    else:
        date = trepo.get_date()
    transaction = trepo.get_transact_by_id(id_, db.transactions)
    transaction.date = date
    reload_transact()
    return True, "Success"


# endregion


# region Save/Load/Reload
def save_transact():
    output_file = "./Model/DataBase/transactions.json"
    data = {"transactions": []}

    for transaction in db.transactions:
        invoice = None
        if transaction.invoice:
            invoice = transaction.invoice.invoice_number
        data["transactions"].append({
            "entity_id": transaction.entity_id,
            "type": transaction.type_,
            "date": transaction.date,
            "price": transaction.price,
            "counterparty": transaction.counterparty.entity_id,
            "assets": transaction.assets,
            "invoice": invoice
        })

    try:
        db.save_data_to_json(data, output_file)
    except Exception as ex:
        msg = "Error saving transactions!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def load_transact():
    try:
        with open("./Model/DataBase/transactions.json", "rt", encoding="utf-8") as file:
            data = js.load(file)
    except Exception as ex:
        msg = "Error reading transactions file!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)

    db.transactions.clear()

    try:
        for transaction in data["transactions"]:
            id_ = transaction["entity_id"]
            type_ = transaction["type"]
            date = transaction["date"]
            counterparty = cptmgmt.cptrepo.get_cprty_by_id(transaction["counterparty"], db.counterparties)
            assets = transaction["assets"]
            invoice = transaction["invoice"]

            state, msg, tr = create_transact(id_, type_, counterparty, assets, invoice, date=date)
            if not state:
                db.my_logger.log(__file__, "Error creating transaction", "ERROR", msg)
    except Exception as ex:
        msg = "Error Loading transactions!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def reload_transact():
    save_transact()
    load_transact()

# endregion
