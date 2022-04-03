import sys

from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.tmp_products import TempProduct
from model.entities.transaction import Transaction
from datetime import datetime


class SalesModule:
    def __init__(self, counterparties_repository, transactions_repository, invoices_repository):
        self._cpty_repo = counterparties_repository
        self._tr_repo = transactions_repository
        self._inv_repo = invoices_repository

    @property
    def counterparties(self):
        return self.find_all_counterparties()

    @property
    def transactions(self):
        return self.find_all_transactions()

    @property
    def invoices(self):
        return self.find_all_invoices()

    # region FIND
    # Counterparties
    def find_all_counterparties(self):
        return self._cpty_repo.find_all()

    def find_counterparty_by_id(self, id_: int):
        try:
            return self._cpty_repo.find_by_id(id_)
        except Exception as ex:
            return ex

    def find_counterparty_by_attr(self, attr_name: str, attr_val, exact_val: bool = True):
        try:
            return self._cpty_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # Transactions
    def find_all_transactions(self):
        return self._tr_repo.find_all()

    def find_transaction_by_id(self, id_):
        try:
            return self._tr_repo.find_by_id(id_)
        except Exception as ex:
            return ex

    def find_transaction_by_attr(self, attr_name: str, attr_val, exact_val: bool = True):
        try:
            return self._tr_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # Invoices
    def find_all_invoices(self):
        return self._inv_repo.find_all()

    def find_invoice_by_id(self, id_: int):
        try:
            return self._inv_repo.find_by_id(id_)
        except Exception as ex:
            return ex

    def find_invoices_by_attr(self, attr_name: str, attr_val, exact_val: bool = True):
        try:
            return self._inv_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # endregion

    # region CRUD

    # region Counterparties
    def create_cpty(self, name: str, phone: str, payment_nr: str, status: str, type_: str, descr: str = "",
                    id_=None) -> Counterparty | Exception:
        try:
            # region Validations
            if not isinstance(name, str):
                raise TypeError("Failed creating Counterparty! Invalid name!")
            if not isinstance(phone, str):
                raise TypeError("Failed creating Counterparty! Invalid phone number!")
            if not isinstance(payment_nr, str) or len(payment_nr) <= 5:
                raise TypeError("Failed creating Counterparty! Invalid payment number!")
            if not isinstance(status, str):
                raise TypeError("Failed creating Counterparty! Invalid status!")
            status = self.validate_cpty_status(status)
            if status is None:
                raise TypeError("Failed creating Counterparty! Invalid status")
            if not isinstance(type_, str):
                raise TypeError("Failed creating Counterparty! Invalid type!")
            type_ = self.validate_cpty_type(type_)
            if type_ is None:
                raise TypeError("Failed creating Counterparty! Invalid type!")
            # endregion
            new_cpty = Counterparty(name, phone, payment_nr, status, type_, descr, id_)
            return self._cpty_repo.create(new_cpty)
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            # print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
            return ex

    def update_cpty(self, entity: Counterparty):
        if not isinstance(entity, Counterparty):
            raise TypeError("Invalid entity!")
        self._cpty_repo.update(entity)

    def _del_cpty_by_id(self, id_: int):
        """
        Be careful!\n
        This will delete the counterparty with all of his transactions/invoices.\n
        If you want to soft delete, change status to Disabled and the counterparty won't be visible\n
        in the Operators interface, while history for transactions/invoices will still be accessible.
        """
        try:
            if not isinstance(id_, int):
                raise TypeError("Invalid ID!")
            cpty = self.find_counterparty_by_id(id_)
            all_tr = self.find_all_transactions()
            to_del = []
            # delete transactions
            for tr in all_tr:
                if tr.counterparty is cpty:
                    to_del.append(tr.id)
            for item in to_del:
                self.del_tr_by_id(item)

            return self._cpty_repo.delete_by_id(id_)
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            # print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
            return ex

    # endregion

    # region Transactions
    def create_tr(self, type_: str, counterparty: Counterparty, assets: list, id_=None):
        try:
            # region Validations
            if not isinstance(type_, str):
                raise TypeError("Transaction creation failed! Invalid type!")
            type_ = self.validate_tr_type(type_)
            if type_ is None:
                raise TypeError("Transaction creation failed! Invalid type!")

            date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

            if not isinstance(counterparty, Counterparty):
                raise TypeError("Transaction creation failed! Invalid Counterparty!")
            exists = self.counterparty_exists(counterparty)
            if not exists:
                raise TypeError("Transaction creation failed! Counterparty not found!")

            if not isinstance(assets, list):
                raise TypeError("Transaction creation failed! Invalid assets!")
            new_assets = []
            for product in assets:
                if not isinstance(product, list):
                    raise TypeError("Transaction creation failed! Invalid assets!")
                new_assets.append(TempProduct(product[0], product[1], product[2], product[3]))

            # endregion
            new_tr = Transaction(type_, date, counterparty, new_assets, None, id_)
            return self._tr_repo.create(new_tr)
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            # print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
            return ex

    def del_tr_by_id(self, id_):
        """
        Caution!\n
        This will also delete the transaction invoice if there is any!
        """
        tr = self.find_transaction_by_id(id_)
        inv = tr.invoice
        self.del_inv_by_id(inv.id)

        return self._tr_repo.delete_by_id(tr.id)

    # endregion

    # region Invoices
    def _create_inv(self, entity):
        return self._inv_repo.create(entity)

    def gen_inv_from_tr(self, transaction: Transaction) -> Invoice | Exception:
        try:
            if not isinstance(transaction, Transaction):
                raise TypeError(f"Generating invoice failed! Invalid transaction type!")

            if transaction.type == "Purchase":
                raise TypeError(f"Generating invoice failed! You can generate invoices only for Sales!")

            invoicer = self.find_counterparty_by_attr("type", "MyCo")[0]
            now = datetime.now()
            now = now.strftime("%m/%d/%Y %H:%M:%S")
            # TODO default due_to date
            due_to_date = ""
            descr = ""
            terms = ""
            status = "Pending"
            new_inv = Invoice(self._inv_repo.gen_inv_num(), invoicer, transaction.counterparty,
                              now, due_to_date, transaction.assets, transaction.price, descr, terms, status)
            new_inv = self._inv_repo.create(new_inv)
            transaction.invoice = new_inv
            return new_inv
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            # print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
            return ex

    def del_inv_by_id(self, id_):
        inv = self.find_invoice_by_id(id_)
        tr = self.find_transaction_by_attr("invoice", inv)[0]
        tr.invoice = None
        return self._inv_repo.delete_by_id(inv.id)

    # endregion

    # endregion

    # region Validations
    @staticmethod
    def validate_cpty_status(status):
        valid = ("Enabled", "Disabled")
        for st in valid:
            if st.lower() == status.lower():
                return st

    @staticmethod
    def validate_cpty_type(type_):
        valid = ("Supplier", "Client", "MyCo")
        for tp in valid:
            if tp.lower() == type_.lower():
                return tp

    def counterparty_exists(self, counterparty: Counterparty):
        all_cpty = self.find_all_counterparties()
        for cpty in all_cpty:
            if counterparty is cpty:
                return True
        return False

    @staticmethod
    def validate_tr_type(type_):
        valid = ("Sale", "Purchase")
        for tp in valid:
            if tp.lower() == type_.lower():
                return tp

    # endregion

    # region Other
    def print_all_counterparties(self):
        self._cpty_repo.print_all()

    def print_all_transactions(self):
        self._tr_repo.print_all()

    def print_all_invoices(self):
        self._inv_repo.print_all()

    def make_relations(self):
        all_tr = self.transactions
        all_inv = self.invoices

        # Make transactions relations
        for tr in all_tr:
            if isinstance(tr.counterparty, dict):
                cpty = self.find_counterparty_by_id(tr.counterparty["id"])
                if cpty is not None:
                    tr.counterparty = cpty
            if isinstance(tr.invoice, dict):
                inv = self.find_invoices_by_attr("number", tr.invoice["number"])[0]
                if inv is not None:
                    tr.invoice = inv
                tr.invoice.assets = tr.assets
                tr.invoice.price = tr.price

        # Make invoices relations
        for inv in all_inv:
            if isinstance(inv.from_, dict):
                from_ = self.find_counterparty_by_id(inv.from_["id"])
                if from_ is not None:
                    inv.from_ = from_
            if isinstance(inv.to, dict):
                to = self.find_counterparty_by_id(inv.to["id"])
                if to is not None:
                    inv.to = to

    def counterparties_count(self):
        return self._cpty_repo.count()

    def transactions_count(self):
        return self._tr_repo.count()

    def invoices_count(self):
        return self._inv_repo.count()

    # endregion

    # region Save/Load
    def load_counterparties(self):
        loaded = self._cpty_repo.load("./model/data/counterparties.json")
        if loaded is not None:
            for item in loaded:
                id_, name, phone, payment_nr, status, type_, descr = loaded[item].values()
                new = Counterparty(name, phone, payment_nr, status, type_, descr, id_)
                self._cpty_repo.create(new)

    def load_transactions(self):
        loaded = self._tr_repo.load("./model/data/transactions.json")
        if loaded is not None:
            for item in loaded:
                id_, type_, date, cpty, assets, price, invoice = loaded[item].values()
                new_assets = []
                for product in assets:
                    tmp = TempProduct(product["name"], product["type"], product["price"], product["quantity"])
                    new_assets.append(tmp)
                new = Transaction(type_, date, cpty, new_assets, invoice, id_)
                self._tr_repo.create(new)

    def load_invoices(self):
        loaded = self._inv_repo.load("./model/data/invoices.json")
        if loaded is not None:
            for item in loaded:
                id_, num, from_, to, date, due_to, assets, price, descr, terms, status = loaded[item].values()
                new = Invoice(num, from_, to, date, due_to, assets, price, descr, terms, status, id_)
                self._inv_repo.create(new)

    def load_all(self):
        self.load_counterparties()
        self.load_transactions()
        self.load_invoices()
        self.make_relations()

    def save_counterparties(self):
        self._cpty_repo.save("./model/data/counterparties.json")

    def save_transactions(self):
        self._tr_repo.save("./model/data/transactions.json")

    def save_invoices(self):
        self._inv_repo.save("./model/data/invoices.json")

    def save_all(self):
        self.save_counterparties()
        self.save_transactions()
        self.save_invoices()
    # endregion
