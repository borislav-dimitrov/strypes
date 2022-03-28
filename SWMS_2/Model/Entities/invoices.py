class Invoice:
    def __init__(self, entity_id, invoice_number, from_info, to_info, invoice_date, due_to, items, total_price, description,
                 terms_conditions, status):
        """
        :param entity_id:
        :param invoice_number:
        :param from_info: List [company_name, address1, address2, city, state/province, zip/postal, phone]
        :param to_info: List [company_name, address1, address2, city, state/province, zip/postal, phone]
        :param invoice_date:
        :param items:
        :param total_price:
        :param description: Additional information
        :param terms_conditions: Conditions (i.e. "Payment due 15 days")
        :param status:
        """
        self.entity_id = entity_id
        self.invoice_number = invoice_number
        self.from_info = from_info
        self.to_info = to_info
        self.invoice_date = invoice_date
        self.due_to = due_to
        self.items = items
        self.total_price = total_price
        self.description = description
        self.terms_conditions = terms_conditions
        self.status = status
