class SalesModule:
    def __init__(self, counterparties_repository, transactions_repository, invoices_repository):
        self._counterparties = counterparties_repository
        self._transactions = transactions_repository
        self._invoices = invoices_repository
