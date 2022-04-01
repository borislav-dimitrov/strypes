import model.dao.my_db as db

# DAO's
from model.dao.id_generator_int import IdGeneratorInt
from model.dao.password_manager import PasswordManager
from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.invoice_repo import InvoiceRepository

# Entities
from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.product import Product
from model.entities.transaction import Transaction
from model.entities.user import User
from model.entities.warehouse import Warehouse
from model.service.modules.sales_module import SalesModule
from model.service.modules.user_module import UserModule
from model.service.modules.warehousing_module import WarehousingModule


def create_entities_from_loaded(data, repo, entity_type):
    if entity_type is User:
        for item in data:
            id_, name, pwd, type_, status, last_login = data[item].values()
            new = User(name, pwd, type_, status, last_login, id_)
            repo.create(new)
    if entity_type is Product:
        for item in data:
            id_, name, type_, b_price, s_price, qty, wh = data[item].values()
            new = Product(name, type_, b_price, s_price, qty, wh, id_)
            repo.create(new)
    if entity_type is Warehouse:
        for item in data:
            id_, name, type_, capacity, products, status = data[item].values()
            new = Warehouse(name, type_, capacity, products, status, id_)
            repo.create(new)
    if entity_type is Counterparty:
        for item in data:
            id_, name, phone, pay_nr, status, type_, descr = data[item].values()
            new = Counterparty(name, phone, pay_nr, status, type_, descr, id_)
            repo.create(new)
    if entity_type is Transaction:
        for item in data:
            id_, type_, date, cpty, assets, price, invoice = data[item].values()
            new = Transaction(type_, date, cpty, assets, invoice, id_)
            repo.create(new)
    if entity_type is Invoice:
        for item in data:
            id_, num, from_, to, date, due_date, assets, price, descr, terms, stat = data[item].values()
            new = Invoice(num, from_, to, date, due_date, assets, price, descr, terms, stat, id_)
            repo.create(new)


#
# def create_objects():
#     global usr_repo, wh_repo, pr_repo
#     print("### Start creating entities ###")
#
#     # region USERS
#     user1 = User("Ivan", "!@#asd", "Administrator", "Enabled")
#     usr_repo.create(user1)
#     user2 = User("Ivan", "!@#asd", "Administrator", "Enabled")
#     usr_repo.create(user2)
#     user3 = User("Andrei", "asd#@!", "Operator", "Enabled")
#     usr_repo.create(user3)
#     user4 = User("Petar", "asd#@!", "Operator", "Enabled")
#     usr_repo.create(user4)
#
#     print("# User Repository Created Entities #")
#     # endregion
#
#     # region WAREHOUSES
#     wh1 = Warehouse("sklad01", "Finished Goods", 5000, [], "Enabled")
#     wh_repo.create(wh1)
#     wh2 = Warehouse("sklad02", "Raw Materials", 4555, [], "Enabled")
#     wh_repo.create(wh2)
#     print("# Warehouse Repository Created Entities #")
#     # endregion
#
#     # region PRODUCTS
#     pr1 = Product("Red Paint", "Finished Goods", 10.0, 12.0, 200, {
#         "id": 1,
#         "name": "sklad01",
#     })
#     pr2 = Product("Red Paint", "Finished Goods", 10.0, 12.0, 200, {
#         "id": 1,
#         "name": "sklad01",
#     })
#     pr3 = Product("Turpentine", "Raw Materials", 5.0, 7.0, 200, {
#         "id": 2,
#         "name": "sklad02",
#     })
#     pr4 = Product("Thinner", "Raw Materials", 5.0, 7.0, 200, {
#         "id": 2,
#         "name": "sklad02",
#     })
#     pr5 = Product("Purple Paint", "Raw Materials", 10.0, 12.0, 100, {
#         "id": 2,
#         "name": "sklad02",
#     })
#     pr6 = Product("material2", "Raw Materials", 10.0, 12.0, 300, {
#         "id": 2,
#         "name": "sklad02",
#     })
#     pr7 = Product("material3", "Finished Goods", 10.0, 12.0, 300, None)
#     pr8 = Product("material4", "Finished Goods", 10.0, 12.0, 300, None)
#     all_products = [pr1, pr2, pr3, pr4, pr5, pr6, pr7, pr8]
#     for product in all_products:
#         pr_repo.create(product)
#
#     # TODO should go in service layer
#     # for product in all_products:
#     #     new_pr = pr_repo.create(product)
#     #     if new_pr.assigned_wh is not None:
#     #         found = wh_repo.find_by_attribute("name", new_pr.assigned_wh)
#     #         new_pr.assigned_wh = found[0]
#     #         found[0].products.append(new_pr)
#     #
#     #         pr_repo.update(new_pr)
#     #         wh_repo.update(found[0])
#
#     print("# Product Repository Created Entities #")
#     # endregion
#
#     # region COUNTERPARTIES
#     cpty1 = Counterparty("Firm1", "+35988215743", "BG123456", "Enabled", "Client", "")
#     cpty2 = Counterparty("Firm2", "+35988215743", "BG123456", "Enabled", "Client", "")
#     cpty3 = Counterparty("Firm3", "+35988215743", "BG123456", "Enabled", "Client", "")
#     cpty4 = Counterparty("Firm4", "+35988215743", "BG123456", "Enabled", "Supplier",
#                          ["material5", "Finished Goods", 10.0, 11.0, None])
#     cpty5 = Counterparty("Firm5", "+35988215743", "BG123456", "Enabled", "Supplier",
#                          ["material6", "Raw Materials", 8.0, 10.0, None])
#     cpty6 = Counterparty("Firm6", "+35988215743", "BG123456", "Enabled", "Supplier",
#                          ["material7", "Raw Materials", 6.5, 9.5, None])
#     cpty7 = Counterparty("My Company", "+35988215743", "BG222222", "Enabled", "MyCo", "")
#
#     cpty_repo.create(cpty1)
#     cpty_repo.create(cpty2)
#     cpty_repo.create(cpty3)
#     cpty_repo.create(cpty4)
#     cpty_repo.create(cpty5)
#     cpty_repo.create(cpty6)
#     cpty_repo.create(cpty7)
#     print("# Counterparty Repository Created Entities #")
#     # endregion
#
#     # region TRANSACTIONS
#     tr1 = Transaction("Sale", "29/03/2022 08:40:32", {
#         "id": 1,
#         "name": "Firm1",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "Client",
#         "descr": ""
#     }, [["material4", "Finished Goods", 12.3, 5], ["material5", "Finished Goods", 12.65, 7]], 1)
#
#     tr2 = Transaction("Sale", "30/03/2022 10:40:32", {
#         "id": 3,
#         "name": "Firm3",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "Client",
#         "descr": ""
#     }, [["material4", "Finished Goods", 12.2, 5], ["material5", "Finished Goods", 12.15, 7]], 2)
#
#     tr3 = Transaction("Purchase", "29/03/2022 11:40:32", {
#         "id": 5,
#         "name": "Firm5",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "supplier",
#         "descr": ["material6", "Raw Materials", 8.0, 10.0, None]
#     }, [["material4", "Finished Goods", 10.5, 5], ["material5", "Finished Goods", 10.3, 7]], 3)
#
#     tr4 = Transaction("Purchase", "30/03/2022 12:40:32", {
#         "id": 6,
#         "name": "Firm6",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "supplier",
#         "descr": ["material7", "Raw Materials", 6.5, 9.5, None]
#     }, [["material4", "Finished Goods", 10.9, 5], ["material5", "Finished Goods", 10.3, 7]], 4)
#
#     tr_repo.create(tr1)
#     tr_repo.create(tr2)
#     tr_repo.create(tr3)
#     tr_repo.create(tr4)
#
#     # TODO this should be in service layer
#     # all_tr = tr_repo.get_entities()
#     # for transaction in all_tr:
#     #     current_tr = all_tr[transaction]
#     #     if current_tr.invoice is not None:
#     #         invoice = inv_repo.find_by_attribute("number", current_tr.invoice)[0]
#     #         # Link invoice to transaction
#     #         current_tr.invoice = invoice
#     #
#     #         # Link invoice assets/price/to/from to transaction
#     #         invoice.assets = current_tr.assets
#     #         invoice.price = current_tr.price
#     #         if current_tr.type_ == "Sale":
#     #             invoice.to = current_tr.counterparty
#     #         if current_tr.type_ == "Purchase":
#     #             invoice.from_ = current_tr.counterparty
#     print("# Transactions Repository Created Entities #")
#     # endregion
#
#     # region INVOICES
#     inv1 = Invoice(inv_repo.gen_inv_num(), {
#         "id": 7,
#         "name": "My Company",
#         "phone": "+35988215743",
#         "payment_nr": "BG222222",
#         "status": "Enabled",
#         "type": "MyCo",
#         "descr": ""
#     }, {"id": 1,
#         "name": "Firm1",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "Client",
#         "descr": ""
#         }, "30/03/2022 09:23:32", "10/04/2022 23:59:59",
#                    [["material4", "Finished Goods", 12.3, 5], ["material5", "Finished Goods", 12.65, 7]], 150.05,
#                    "no descr", "no terms", "Pending")
#     inv_repo.create(inv1)
#
#     inv2 = Invoice(inv_repo.gen_inv_num(), {
#         "id": 7,
#         "name": "My Company",
#         "phone": "+35988215743",
#         "payment_nr": "BG222222",
#         "status": "Enabled",
#         "type": "MyCo",
#         "descr": ""
#     }, {"id": 3,
#         "name": "Firm3",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "Client",
#         "descr": ""
#         }, "30/03/2022 09:23:32", "10/04/2022 23:59:59",
#                    [["material4", "Finished Goods", 12.2, 5], ["material5", "Finished Goods", 12.15, 7]], 146.05,
#                    "no descr", "no terms", "Pending")
#
#     inv_repo.create(inv2)
#
#     inv3 = Invoice(inv_repo.gen_inv_num(), {
#         "id": 7,
#         "name": "My Company",
#         "phone": "+35988215743",
#         "payment_nr": "BG222222",
#         "status": "Enabled",
#         "type": "MyCo",
#         "descr": ""
#     }, {"id": 6,
#         "name": "Firm6",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "Supplier",
#         "descr": ["material7", "Raw Materials", 6.5, 9.5, None]
#         }, "30/03/2022 09:23:32", "10/04/2022 23:59:59",
#                    [["material4", "Finished Goods", 10.5, 5], ["material5", "Finished Goods", 10.3, 7]], 124.6,
#                    "no descr", "no terms", "Pending")
#     inv_repo.create(inv3)
#
#     inv4 = Invoice(inv_repo.gen_inv_num(), {
#         "id": 7,
#         "name": "My Company",
#         "phone": "+35988215743",
#         "payment_nr": "BG222222",
#         "status": "Enabled",
#         "type": "MyCo",
#         "descr": ""
#     }, {"id": 6,
#         "name": "Firm6",
#         "phone": "+35988215743",
#         "payment_nr": "BG123456",
#         "status": "Enabled",
#         "type": "Supplier",
#         "descr": ["material7", "Raw Materials", 6.5, 9.5, None]
#         }, "30/03/2022 09:23:32", "10/04/2022 23:59:59",
#                    [["material4", "Finished Goods", 10.9, 5], ["material5", "Finished Goods", 10.3, 7]], 126.6,
#                    "no descr", "no terms", "Pending")
#     inv_repo.create(inv4)
#     print("# Invoice Repository Created Entities #")
#     # endregion


def load_and_create_entities(usr_repo, pr_repo, wh_repo, cpty_repo, tr_repo, inv_repo):
    # LOAD
    loaded_users = usr_repo.load("./model/data/users.json")
    loaded_products = pr_repo.load("./model/data/products.json")
    loaded_warehouses = wh_repo.load("./model/data/warehouses.json")
    loaded_counterparties = cpty_repo.load("./model/data/counterparties.json")
    loaded_transactions = tr_repo.load("./model/data/transactions.json")
    loaded_invoices = inv_repo.load("./model/data/invoices.json")

    create_entities_from_loaded(loaded_users, usr_repo, User)
    create_entities_from_loaded(loaded_products, pr_repo, Product)
    create_entities_from_loaded(loaded_warehouses, wh_repo, Warehouse)
    create_entities_from_loaded(loaded_counterparties, cpty_repo, Counterparty)
    create_entities_from_loaded(loaded_transactions, tr_repo, Transaction)
    create_entities_from_loaded(loaded_invoices, inv_repo, Invoice)


def start_up():
    # region INIT
    # region INIT REPOS
    usr_id_seq = IdGeneratorInt()
    usr_repo = GenericRepository(usr_id_seq)

    wh_id_seq = IdGeneratorInt()
    wh_repo = GenericRepository(wh_id_seq)

    pr_id_seq = IdGeneratorInt()
    pr_repo = GenericRepository(pr_id_seq)

    cpty_id_seq = IdGeneratorInt()
    cpty_repo = GenericRepository(cpty_id_seq)

    tr_id_seq = IdGeneratorInt()
    tr_repo = GenericRepository(tr_id_seq)

    inv_id_seq = IdGeneratorInt()
    inv_repo = InvoiceRepository(inv_id_seq)
    # endregion

    # region INIT MODULES
    db.user_module = UserModule(usr_repo, PasswordManager())
    db.warehousing_module = WarehousingModule(pr_repo, wh_repo)
    db.sales_module = SalesModule(cpty_repo, tr_repo, inv_repo)
    # endregion

    # endregion

    load_and_create_entities(usr_repo, pr_repo, wh_repo, cpty_repo, tr_repo, inv_repo)


def before_exit():
    pass