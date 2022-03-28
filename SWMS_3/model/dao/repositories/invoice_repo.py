from model.dao.repositories.generic_repo import GenericRepository


class InvoiceRepository(GenericRepository):
    def __init__(self, id_generator):
        super().__init__(id_generator)

    def find_by_inv_number(self, inv_number: int):
        for invoice in self._entities:
            if self._entities[invoice].invoice_number == inv_number:
                return self._entities[invoice]
        return None
