import model.dao.my_db as db
from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.tmp_products import TempProduct
from model.entities.transaction import Transaction
from model.service.startup import start_up


def main():
    start_up()


if __name__ == '__main__':
    main()
