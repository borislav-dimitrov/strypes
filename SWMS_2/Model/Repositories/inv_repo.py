import sys

import xlsxwriter as xl
from Model.Entities.invoices import Invoice
from datetime import datetime as dt


# region Validations
def valid_inv_status(status):
    if not isinstance(status, str):
        return False, "Invalid Status!"
    valid_statuses = ["NEW", "PENDING", "PAID", "OVERDUE"]
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
    date = now.strftime("%d-%m-%Y %H:%M:%S")
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
            return False, "Invoice date too old!"
        return True, "Valid"
    except Exception as ex:
        return False, "Date is invalid format!"


def get_total_price(items):
    total = 0
    for item in items:
        qty = item[1]
        unit_price = item[2]
        total += int(qty) * int(unit_price)
    return total


# endregion

# region INVOICING
def generate_xls(invoice, logger, path="./Resources/invoices/default_inv.xlsx"):
    workbook = xl.Workbook(path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({"bold": True})
    align_r = workbook.add_format({
        "align": "right",
        "valign": "vright"
    })
    title_merge = workbook.add_format({
        "bold": 1,
        "align": "center",
        "valign": "vcenter",
        "font_size": 24
    })
    status = False
    try:
        xls_bill_to(invoice.to_info, worksheet, bold, align_r)
        xls_invoice_date(invoice.invoice_date, worksheet)
        xls_invoice_title(invoice.invoice_number, worksheet, title_merge)
        xls_items_title(worksheet, bold)
        for index, item in enumerate(invoice.items):
            xls_items_info(item, index, worksheet)
        current_row = 14 + len(invoice.items)
        xls_invoice_total(current_row + 1, invoice.total_price, worksheet, bold)
        current_row = current_row + 5
        xls_from(current_row, invoice.from_info, worksheet, align_r)
        xls_set_col_width(worksheet)
        status = True
    except Exception as ex:
        msg = "Error occurred while writing to xlsx file!"
        tb = sys.exc_info()[2].tb_frame
        logger.log(__file__, msg, "ERROR", type(ex), tb)
    finally:
        try:
            workbook.close()
        except Exception as ex:
            msg = "Error occurred while writing to xlsx file!"
            tb = sys.exc_info()[2].tb_frame
            logger.log(__file__, msg, "ERROR", type(ex), tb)
        return status


def xls_bill_to(info, sheet, bold, align):
    # [company_name, address1, address2, city, state / province, zip / postal, phone]
    sheet.write("A1", "Bill To:", bold)
    sheet.write("A2", "Company Name:")
    sheet.write("A3", "Payment nr:")
    sheet.write("A4", "DDS:")
    sheet.write("A5", "City")
    sheet.write("A6", "State/Province")
    sheet.write("A7", "zip/postal")
    sheet.write("A8", "Phone")

    sheet.write("B2", info[0], align)
    sheet.write("B3", info[1], align)
    sheet.write("B4", info[2], align)
    sheet.write("B5", info[3], align)
    sheet.write("B6", info[4], align)
    sheet.write("B7", int(info[5]), align)
    sheet.write("B8", int(info[6]), align)


def xls_invoice_date(info, sheet):
    sheet.write("K3", "Invoice Date:")
    sheet.write("L3", info.split(" ")[0])


def xls_invoice_title(info, sheet, format_):
    sheet.merge_range("D11:I11", f"INVOICE # {info.split('-')[1]}", format_)


def xls_items_title(sheet, bold):
    sheet.merge_range("A14:D14", "Item", bold)
    sheet.write("E14", "Qty", bold)
    sheet.write("G14", "Unit Price", bold)
    sheet.write("I14", "Subtotal", bold)


def xls_items_info(item, item_num, sheet):
    row = 14 + item_num
    sheet.merge_range(row, 0, row, 3, item[0])
    sheet.write(row, 4, item[1])
    sheet.write(row, 6, item[2])
    sheet.write(row, 8, item[1] * item[2])


def xls_invoice_total(row, info, sheet, bold):
    sheet.write(row, 8, f"TOTAL: {info}лв", bold)


def xls_from(row, info, sheet, align):
    # [company_name, address1, address2, city, state / province, zip / postal, phone]
    sheet.write(row, 0, "Company Name:")
    sheet.write(row + 1, 0, "Address1:")
    sheet.write(row + 2, 0, "Payment nr:")
    sheet.write(row + 3, 0, "City:")
    sheet.write(row, 3, "State/Province:")
    sheet.write(row + 1, 3, "zip/postal:")
    sheet.write(row + 2, 3, "Phone:")

    sheet.write(row, 1, info[0], align)
    sheet.write(row + 1, 1, info[1], align)
    sheet.write(row + 2, 1, info[2], align)
    sheet.write(row + 3, 1, info[3], align)
    sheet.write(row, 4, info[4], align)
    sheet.write(row + 1, 4, int(info[5]), align)
    sheet.write(row + 2, 4, int(info[6]), align)


def xls_set_col_width(sheet):
    for col in range(0, 12):
        sheet.set_column(0, col, 15)
# endregion
