from fpdf import FPDF

from model.entities.counterparty import Counterparty


class PdfMaker:
    def gen_pdf(self, invoice, path="./resources/invoices/default_invoice.pdf"):
        pdf = FPDF("P", "mm", (210, 297))
        pdf.add_page()

        x = 20.0
        y = 30.0
        self.inv_logo(x, 10, pdf)

        y = self.inv_bill_to(x, y, pdf, invoice.to)
        self.inv_date(x + 120, y - 15, pdf, invoice.date, invoice.due_to)

        y += 6
        pdf.line(10, y - 1, 200, y)
        self.inv_title(x, y, pdf, invoice.number)

        y += 21
        pdf.line(10, y - 1, 200, y)

        y = self.inv_items(x, y, pdf, invoice.assets, invoice.price)
        pdf.line(10, y - 1, 200, y)
        self.inv_from(x, y, pdf, invoice.from_)
        pdf.output(path, "F")
        return True

    @staticmethod
    def add_txt_to_pdf(x, y, pdf, txt="", font_family='Arial', font_style='', font_size=11, alignment='L',
                       fill=False, link='', border=0, new_line=1, cell_width=0,  # 0 takes the whole line
                       cell_height=10):
        if pdf:
            pdf.set_xy(x, y)
            pdf.set_font(font_family, font_style, font_size)
            pdf.cell(cell_width, cell_height, txt, border, new_line, alignment, fill, link)
        else:
            raise Exception("Failed creating pdf!")

    def inv_logo(self, x, y, pdf):
        self.add_txt_to_pdf(x, y, pdf, "SWMS", cell_width=20, font_style="B", font_size=24)

    def inv_bill_to(self, x, y, pdf, counterparty: Counterparty):
        self.add_txt_to_pdf(x, y, pdf, "Bill To:", cell_width=20, font_style="B")

        y += 5
        self.add_txt_to_pdf(x, y, pdf, "Company Name:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, counterparty.name, cell_width=20)

        y += 5
        self.add_txt_to_pdf(x, y, pdf, "Phone:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, counterparty.phone, cell_width=20)

        y += 5
        self.add_txt_to_pdf(x, y, pdf, "Payment nr:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, counterparty.payment_nr, cell_width=20)

        y += 5
        return y

    def inv_date(self, x, y, pdf, date, due_to):
        self.add_txt_to_pdf(x - 20, y, pdf, "Invoice Date:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, date.split(" ")[0], cell_width=20)

        self.add_txt_to_pdf(x - 20, y + 5, pdf, "Invoice Due to Date:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y + 5, pdf, due_to.split(" ")[0], cell_width=20)

    def inv_title(self, x, y, pdf, number):
        self.add_txt_to_pdf(x + 60, y + 5, pdf, f"INVOICE # {number}", font_style="B", font_size=20)

    def inv_items(self, x, y, pdf, items, total):
        self.add_txt_to_pdf(x, y, pdf, "Item", font_style="BU")
        self.add_txt_to_pdf(x + 70, y, pdf, "Qty", font_style="BU")
        self.add_txt_to_pdf(x + 100, y, pdf, "Unit Price", font_style="BU")
        self.add_txt_to_pdf(x + 140, y, pdf, "Subtotal", font_style="BU")

        for item in items:
            y += 5
            self.add_txt_to_pdf(x, y, pdf, str(item.name))
            self.add_txt_to_pdf(x + 70, y, pdf, str(item.quantity))
            self.add_txt_to_pdf(x + 100, y, pdf, str(item.price) + " BGN")
            self.add_txt_to_pdf(x + 140, y, pdf, str(float(item.quantity) * int(item.price)) + " BGN")
        y += 15
        self.add_txt_to_pdf(x + 140, y, pdf, f"TOTAL: {total:2n} BGN", font_style="B")
        y += 5
        self.add_txt_to_pdf(x + 140, y, pdf, f"DDS: {total * 0.2:2n} BGN", font_style="B")
        y += 5
        self.add_txt_to_pdf(x + 140, y, pdf, f"FINAL: {total + (total * 0.2):2n} BGN", font_style="BU")
        return y + 10

    def inv_from(self, x, y, pdf, info):
        self.add_txt_to_pdf(x, y, pdf, "Company Name:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, info.name, cell_width=20)

        y += 5
        self.add_txt_to_pdf(x, y, pdf, "Phone:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, info.phone, cell_width=20)

        y += 5
        self.add_txt_to_pdf(x, y, pdf, "Payment nr:", cell_width=20, font_style="B")
        self.add_txt_to_pdf(x + 40, y, pdf, info.payment_nr, cell_width=20)
