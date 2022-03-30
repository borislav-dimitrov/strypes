from model.dao.repositories.generic_repo import GenericRepository


class InvoiceRepository(GenericRepository):
    def __init__(self, IdGenerator):
        super().__init__(IdGenerator)

    def gen_inv_num(self):
        next_inv_num = 0
        for invoice in self._entities:
            if self._entities[invoice].number > next_inv_num:
                next_inv_num = self._entities[invoice].number
        return next_inv_num + 1

    def delete_by_id(self, id_, transaction):
        super().delete_by_id(id_)
        transaction.invoice = None
