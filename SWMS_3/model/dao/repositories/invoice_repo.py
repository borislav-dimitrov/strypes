from model.dao.repositories.generic_repo import GenericRepository


class InvoiceRepository(GenericRepository):
    """
    InvoiceRepository class that extends GenericRepository with\n
    method for generating the highest invoice number.
    """
    def __init__(self, id_generator):
        super().__init__(id_generator)

    def gen_inv_num(self)-> int:
        """
        Generates the highest possible invoice number based on\n
        the already existing invoices in the repo.
        :return: new invoice number
        """
        next_inv_num = 0
        for invoice in self._entities:
            if self._entities[invoice].number > next_inv_num:
                next_inv_num = self._entities[invoice].number
        return next_inv_num + 1
