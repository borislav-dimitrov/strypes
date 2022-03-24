from Model.Entities.invoices import Invoice
from datetime import datetime as dt


# region Validations
def valid_inv_status(status):
    valid_statuses = ["PENDING", "PAID", "OVERDUE"]
    for st in valid_statuses:
        if st.lower() == status.lower():
            return True, st
    return False, "Invalid Status!"


def valid_new_inv_num(num, all_inv):
    for invoice in all_inv:
        if int(invoice.invoice_number.split("-")[1]) == num:
            return False, f"Invoice number INV-{num} already exists!"
    return True, f"Invoice number INV-{num} is free!"



# endregion

# region CRUD
def create_invoice(id_, num, from_, to_, date, items, price, descr, terms, status):
    new_inv = Invoice(id_, num, from_, to_, date, items, price, descr, terms, status)
    return new_inv


def del_invoice(id_, all_inv):
    for invoice in all_inv:
        if invoice.entity_id == id_:
            inv_num = invoice.invoice_number
            index = get_inv_index(id_, all_inv)
            all_inv.pop(index)
            return True, f"Invoice with number {inv_num} successfully deleted!"
    return False, f"Invoice with id {id_} not found!"


# endregion


# region GET OBJECTS
def get_inv_by_id(id_, all_inv):
    for invoice in all_inv:
        if invoice.entity_id == id_:
            return invoice
    return None


def get_inv_index(id_, all_inv):
    for invoice in all_inv:
        if invoice.entity_id == id_:
            return all_inv.index(invoice)
    return None


def get_new_inv_number(all_inv):
    highest = 0
    if len(all_inv) == 0:
        return f"INV-{1}"
    else:
        for invoice in all_inv:
            if int(invoice.invoice_number.split("-")[1]) > highest:
                highest = int(invoice.invoice_number.split("-")[1])
        return f"INV-{highest + 1}"


def get_inv_date():
    now = dt.now()
    date = now.strftime("%d-%m-%y %H:%M:%S")
    return date


def validate_date(full_date):
    try:
        date = full_date.split(" ")[0]
        year = int(date.split("-")[2])
        time = full_date.split(" ")[1]
        now = get_inv_date()
        now_date = now.split(" ")[0]
        year_now = int(now_date.split("-")[2])

        if year < year_now - 1:
            return False, "Cannot create Invoices more than a year behind!"
        return True, "Valid"
    except Exception as ex:
        return False, "Date is invalid format!"
# endregion
