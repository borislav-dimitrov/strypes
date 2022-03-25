import sys

from fpdf import FPDF
from Model.Entities.invoices import Invoice
from datetime import datetime as dt


# region Validations
def valid_inv_status(status):
    if not isinstance(status, str):
        return False, "Invalid Status!"
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
def generate_pdf(invoice, logger, path="./Resources/invoices/default_inv.pdf"):
    pdf = FPDF("P", "mm", (210, 297))
    pdf.add_page()
    # Set cursor position
    x = 20.0
    y = 30.0
    inv_logo(x, 10, pdf)
    y = inv_bill_to(x, y, pdf, invoice.to_info)
    inv_date(x + 120, y - 15, pdf, invoice.invoice_date)
    y += 6
    pdf.line(10, y - 1, 200, y)
    inv_title(x, y, pdf, invoice.invoice_number)
    y += 21
    pdf.line(10, y - 1, 200, y)
    y = inv_items(x, y, pdf, invoice.items, invoice.total_price)
    pdf.line(10, y - 1, 200, y)
    inv_from(x, y, pdf, invoice.from_info)
    pdf.output(path, "F")
    return True


def add_txt_to_pdf(x, y, pdf, txt="", font_family='Arial', font_style='', font_size=11, alignment='L',
                   fill=False, link='', border=0, new_line=1, cell_width=0,  # 0 takes the whole line
                   cell_height=10):
    if pdf:
        pdf.set_xy(x, y)
        pdf.set_font(font_family, font_style, font_size)
        pdf.cell(cell_width, cell_height, txt, border, new_line, alignment, fill, link)
    else:
        print("Invalid pdf!")


def inv_logo(x, y, pdf):
    add_txt_to_pdf(x, y, pdf, "SWMS", cell_width=20, font_style="B", font_size=24)


def inv_bill_to(x, y, pdf, info):
    add_txt_to_pdf(x, y, pdf, "Bill To:", cell_width=20, font_style="B")
    y += 5
    add_txt_to_pdf(x, y, pdf, "Company Name:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[0], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "Address:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[1], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "Payment nr:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[2], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "City:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[3], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "State/Province:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[4], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "ZIP/Postal:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[5], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "Phone:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[6], cell_width=20)
    y += 5
    return y


def inv_date(x, y, pdf, info):
    add_txt_to_pdf(x, y, pdf, "Invoice Date:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 30, y, pdf, info.split(" ")[0], cell_width=20)


def inv_title(x, y, pdf, info):
    add_txt_to_pdf(x + 60, y + 5, pdf, f"INVOICE # {info.split('-')[1]}", font_style="B", font_size=20)


def inv_items(x, y, pdf, items, total):
    add_txt_to_pdf(x, y, pdf, "Item", font_style="BU")
    add_txt_to_pdf(x + 70, y, pdf, "Qty", font_style="BU")
    add_txt_to_pdf(x + 100, y, pdf, "Unit Price", font_style="BU")
    add_txt_to_pdf(x + 140, y, pdf, "Subtotal", font_style="BU")

    for item in items:
        y += 5
        add_txt_to_pdf(x, y, pdf, item[0])
        add_txt_to_pdf(x + 70, y, pdf, str(item[1]))
        add_txt_to_pdf(x + 100, y, pdf, str(item[2]))
        add_txt_to_pdf(x + 140, y, pdf, str(float(item[1]) * int(item[2])))
    y += 10
    add_txt_to_pdf(x + 140, y, pdf, f"TOTAL: {total} BGN", font_style="BU")
    return y + 10


def inv_from(x, y, pdf, info):
    add_txt_to_pdf(x, y, pdf, "Company Name:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[0], cell_width=20)
    add_txt_to_pdf(x + 100, y, pdf, "City:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 140, y, pdf, info[3], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "Address:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[1], cell_width=20)
    add_txt_to_pdf(x + 100, y, pdf, "State/Province:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 140, y, pdf, info[4], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "Payment nr:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[2], cell_width=20)
    add_txt_to_pdf(x + 100, y, pdf, "ZIP/Postal:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 140, y, pdf, info[5], cell_width=20)
    y += 5
    add_txt_to_pdf(x, y, pdf, "Phone:", cell_width=20, font_style="B")
    add_txt_to_pdf(x + 40, y, pdf, info[6], cell_width=20)
# endregion
