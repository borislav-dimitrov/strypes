class Invoice:
    def __init__(self, invoice_number: int, invoicer, invoice_to,
                 invoice_date: str, due_to: str, items: list, total_price: float, description: str, terms: str,
                 status: str, id_: int = None):
        self.entity_id = id_
        self.invoice_number = invoice_number
        self.from_info = invoicer
        self.to_info = invoice_to
        self.invoice_date = invoice_date
        self.due_to = due_to
        self.items = items
        self.total_price = total_price
        self.description = description
        self.terms_conditions = terms
        self.status = status
