from Model.Entities.transaction import Transaction
from datetime import datetime as dt


# region Validations
def status_is_valid(status):
    allowed = ("ENABLED", "DISABLED")
    for stat in allowed:
        if stat.lower() == status.lower():
            return True, stat
    return False, "Invalid status!"


def type_is_valid(type_):
    allowed = ("SALE", "PURCHASE")
    for typ in allowed:
        if typ.lower() == type_.lower():
            return True, typ
    return False, "Invalid type!"


def validate_date(full_date):
    valid_format = "%d-%m-%Y %H:%M:%S"
    try:
        return bool(dt.strptime(full_date, valid_format)), "Success"
    except ValueError:
        return False, "Invalid date format"
    except Exception as ex:
        return False, f"Something went wrong! Err:{ex}\nErrType:{type(ex)}"


def validate_inv_exist(inv_number, all_inv):
    for invoice in all_inv:
        if invoice.invoice_number == inv_number:
            return True, invoice
    return False, "Invoice not found!"


# endregion

# region CRUD
def create_transact(id_, type_, date, price, counterparty, assets, invoice):
    new_transact = Transaction(id_, type_, date, price, counterparty, assets, invoice)
    return new_transact


def del_transact(id_, all_tr):
    for transaction in all_tr:
        if transaction.entity_id == id_:
            tr_id = transaction.entity_id
            index = get_transact_index(id_, all_tr)
            all_tr.pop(index)
            return True, f"Transaction {tr_id} successfully deleted!"
        return False, f"Transaction with id {id_} not found!"


# endregion

# region GET OBJECTS
def get_transact_by_id(id_, all_tr):
    for transaction in all_tr:
        if transaction.entity_id == id_:
            return transaction
    return None


def get_transact_index(id_, all_tr):
    for transaction in all_tr:
        if transaction.entity_id == id_:
            return all_tr.index(transaction)


def get_date():
    now = dt.now()
    date = now.strftime("%d-%m-%Y %H:%M:%S")
    return date
# endregion
