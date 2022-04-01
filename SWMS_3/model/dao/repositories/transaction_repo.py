from model.dao.repositories.generic_repo import GenericRepository
from model.entities.tmp_products import TempProduct


class TransactionRepository(GenericRepository):
    def __init__(self, id_generator):
        super().__init__(id_generator)

    # TODO this should be in service layer
    @staticmethod
    def update_tr_products(transaction, products_info: list[list[str, str, float, int]]):
        tr_invoice = transaction.invoice
        new_products = []
        for product in products_info:
            new_products.append(TempProduct(product[0], product[1], product[2], product[3]))

        transaction.assets = new_products
        transaction.calc_price()

        if tr_invoice is not None:
            tr_invoice.assets = new_products
            tr_invoice.price = transaction.price
