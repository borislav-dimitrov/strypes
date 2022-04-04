from utils.data_utils import to_json_helper


class Invoice:
    """Class, keeping the information about the invoices"""

    def __init__(self, invoice_number: int, invoicer, invoice_to,
                 invoice_date: str, due_to: str, items: list, total_price: float, description: str, terms: str,
                 status: str, id_: int = None):
        """
        Initialize invoice object.
        :param invoice_number:
        :param invoicer: the issuer of the invoice (My Company: Counterparty)
        :param invoice_to: the bill to counterparty (Suppliers: Counterparty)
        :param invoice_date: date when the invoice was created
        :param due_to: date until when the invoice should be paid
        :param items: products sold in the invoice: TempProduct
        :param total_price: total price of the invoice
        :param description: additional information for the invoice
        :param terms: terms and conditions for the invoice
        :param status: "Pending", "Paid" or "Overdue"
        :param id_:
        """
        self.id = id_
        self.number = invoice_number
        self.from_ = invoicer
        self.to = invoice_to
        self.date = invoice_date
        self.due_to = due_to
        self.assets = items
        self.price = total_price
        self.description = description
        self.terms = terms
        self.status = status

    @property
    def inv_num_str(self) -> str:
        """
        Getter for invoice number as a string. Used in the generated invoice pdf
        :return: invoice number as string
        """
        return f"INV #{self.number}"

    def to_json(self):
        """Prepare data to be written to json """
        assets = to_json_helper(self.assets)
        return {
            "id": self.id,
            "number": self.number,
            "from": self.from_,
            "to": self.to,
            "date": self.date,
            "due_to": self.due_to,
            "assets": assets,
            "price": self.price,
            "description": self.description,
            "terms": self.terms,
            "status": self.status,
        }
