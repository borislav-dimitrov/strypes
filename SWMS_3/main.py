import model.dao.my_db as db
from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.tmp_products import TempProduct
from model.entities.transaction import Transaction
from model.service.startup import start_up


def main():
    start_up()

    transactions = db.sales_module.find_transaction_by_attr("type", "purchase", exact_val=False)
    for transaction in transactions:
        inv = db.sales_module.gen_inv_from_tr(transaction)
        print(inv)



if __name__ == '__main__':
    main()
