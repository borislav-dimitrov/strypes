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
    # region FORMATS
    border = workbook.add_format({"border": 1})
    border_align_l = workbook.add_format({
        "border": 1,
        "align": "left",
        "valign": "vcenter"
    })
    border_align_r = workbook.add_format({
        "border": 1,
        "align": "right",
        "valign": "vcenter"
    })
    bold = workbook.add_format({"bold": True})
    bold_align_l = workbook.add_format({
        "bold": True,
        "align": "left",
        "valign": "vcenter"
    })
    bold_border = workbook.add_format({"bold": True, "border": 1})
    bold_border_align_l = workbook.add_format({"bold": True,
                                               "border": 1,
                                               "align": "right",
                                               "valign": "vright"})
    bold_border_align_r = workbook.add_format({"bold": True,
                                               "border": 1,
                                               "align": "right",
                                               "valign": "vright"})
    bold_border_align_c = workbook.add_format({"bold": True,
                                               "border": 1,
                                               "align": "center",
                                               "valign": "vcenter"})
    align_l = workbook.add_format({
        "align": "left",
        "valign": "vcenter"
    })
    align_r = workbook.add_format({
        "align": "right",
        "valign": "vcenter"
    })
    title_merge = workbook.add_format({
        "bold": 1,
        "align": "center",
        "valign": "vcenter",
        "font_size": 24
    })
    # endregion
    status = False
    try:
        xls_bill_to(invoice.to_info, worksheet, bold_border, bold_align_l, align_r)
        xls_invoice_date(invoice.invoice_date, worksheet, bold_align_l, align_r)
        xls_invoice_title(invoice.invoice_number, worksheet, title_merge)
        xls_items_title(worksheet, bold_border_align_c)
        for index, item in enumerate(invoice.items):
            xls_items_info(item, index, worksheet, border)
        current_row = 14 + len(invoice.items)
        xls_invoice_total(current_row, invoice.total_price, worksheet, bold_border_align_r)
        current_row = current_row + 5
        xls_from(current_row, invoice.from_info, worksheet, bold_align_l, align_r)

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


def xls_bill_to(info, sheet, bold, align_l, align_r):
    # [company_name, address1, address2, city, state / province, zip / postal, phone]
    sheet.write("A1", "Bill To:", bold)
    sheet.write("A2", "Company Name:", align_l)
    sheet.write("A3", "Payment nr:", align_l)
    sheet.write("A4", "DDS:", align_l)
    sheet.write("A5", "City", align_l)
    sheet.write("A6", "State/Province", align_l)
    sheet.write("A7", "zip/postal", align_l)
    sheet.write("A8", "Phone", align_l)

    sheet.write("B2", info[0], align_r)
    sheet.write("B3", info[1], align_r)
    sheet.write("B4", info[2], align_r)
    sheet.write("B5", info[3], align_r)
    sheet.write("B6", info[4], align_r)
    sheet.write("B7", int(info[5]), align_r)
    sheet.write("B8", int(info[6]), align_r)


def xls_invoice_date(info, sheet, align_l, align_r):
    sheet.write("H5", "Invoice Date:", align_l)
    sheet.write("I5", info.split(" ")[0], align_r)


def xls_invoice_title(info, sheet, format_):
    sheet.merge_range("B11:H11", f"INVOICE # {info.split('-')[1]}", format_)


def xls_items_title(sheet, format_):
    sheet.merge_range("A14:D14", "Item", format_)
    sheet.merge_range("E14:F14", "Qty", format_)
    sheet.merge_range("G14:H14", "Unit Price", format_)
    sheet.write("I14", "Subtotal", format_)


def xls_items_info(item, item_num, sheet, format_):
    row = 14 + item_num
    sheet.merge_range(row, 0, row, 3, item[0], format_)
    sheet.merge_range(row, 4, row, 5, item[1], format_)
    sheet.merge_range(row, 6, row, 7, item[2], format_)
    sheet.write(row, 8, item[1] * item[2], format_)


def xls_invoice_total(row, info, sheet, format_):
    sheet.write(row, 8, f"TOTAL: {info}лв", format_)


def xls_from(row, info, sheet, align_l, align_r):
    # [company_name, address1, address2, city, state / province, zip / postal, phone]
    sheet.write(row, 0, "Company Name:", align_l)
    sheet.write(row + 1, 0, "Address1:", align_l)
    sheet.write(row + 2, 0, "Payment nr:", align_l)
    sheet.write(row + 3, 0, "City:", align_l)
    sheet.write(row, 4, "State/Province:", align_l)
    sheet.write(row + 1, 4, "zip/postal:", align_l)
    sheet.write(row + 2, 4, "Phone:", align_l)

    sheet.write(row, 1, info[0], align_r)
    sheet.write(row + 1, 1, info[1], align_r)
    sheet.write(row + 2, 1, info[2], align_r)
    sheet.write(row + 3, 1, info[3], align_r)
    sheet.write(row, 5, info[4], align_r)
    sheet.write(row + 1, 5, int(info[5]), align_r)
    sheet.write(row + 2, 5, int(info[6]), align_r)


def xls_set_col_width(sheet):
    for col in range(0, 9):
        sheet.set_column(0, col, 15)
# endregion
