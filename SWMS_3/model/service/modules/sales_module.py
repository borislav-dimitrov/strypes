import os
import sys

from model.dao.pdf_maker import PdfMaker
from model.entities.product import Product
from model.service.logger import MyLogger

from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.dto.tmp_product import TempProduct
from model.entities.transaction import Transaction
from datetime import datetime
import datetime as dt


class SalesModule:
    """Module that handles all the business logic for sales operations"""

    def __init__(self, counterparties_repository, transactions_repository, invoices_repository, logger: MyLogger,
                 pdf_maker: PdfMaker):
        self._cpty_repo = counterparties_repository
        self._tr_repo = transactions_repository
        self._inv_repo = invoices_repository
        self._logger = logger
        self._pdf_maker = pdf_maker

    @property
    def counterparties(self) -> dict:
        """Get all Counterparties"""
        return self._find_all_counterparties()

    @property
    def transactions(self) -> dict:
        """Get all Transactions"""
        return self._find_all_transactions()

    @property
    def invoices(self) -> dict:
        """Get all Invoices"""
        return self._find_all_invoices()

    # region FIND

    # Counterparties
    def _find_all_counterparties(self):
        return self._cpty_repo.find_all()

    def find_counterparty_by_id(self, id_: int) -> Counterparty | Exception:
        """Get Counterparty by ID"""
        try:
            return self._cpty_repo.find_by_id(id_)
        except Exception as ex:
            return ex

    def find_counterparty_by_attr(self, attr_name: str, attr_val, exact_val: bool = True) -> list | Exception | None:
        """Return all entities that match the given criteria"""
        try:
            return self._cpty_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    def find_all_clients_for_dropdown(self):
        all_clients = self.find_counterparty_by_attr("type", "Client")
        result = []
        for client in all_clients:
            result.append((client.id, client.name, client.payment_nr))
        return result

    # Transactions
    def _find_all_transactions(self):
        return self._tr_repo.find_all()

    def find_transaction_by_id(self, id_: int) -> Transaction | Exception:
        """Get Transaction by ID"""
        try:
            return self._tr_repo.find_by_id(id_)
        except Exception as ex:
            return ex

    def find_transaction_by_attr(self, attr_name: str, attr_val, exact_val: bool = True) -> list | Exception | None:
        """Return all entities that match the given criteria"""
        try:
            return self._tr_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # Invoices
    def _find_all_invoices(self):
        return self._inv_repo.find_all()

    def find_invoice_by_id(self, id_: int) -> Invoice | Exception:
        """Get Invoice by ID"""
        try:
            return self._inv_repo.find_by_id(id_)
        except Exception as ex:
            return ex

    def find_invoices_by_attr(self, attr_name: str, attr_val, exact_val: bool = True) -> list | Exception | None:
        """Return all entities that match the given criteria"""
        try:
            return self._inv_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # endregion

    # region CRUD

    # region Counterparties
    def create_cpty(self, name: str, phone: str, payment_nr: str, status: str, type_: str, descr: str | list[list] = "",
                    id_=None) -> Counterparty | Exception:
        """Create new Counterparty"""
        try:
            # region Validations
            if not isinstance(name, str) or len(name) < 3:
                raise TypeError("Failed creating Counterparty! Invalid name!")
            if not self.valid_uniq_cpty_name(name):
                raise Exception("Failed creating Counterparty! Counterparty name already exist!")

            if not isinstance(phone, str) or len(phone) <= 5:
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
            if type_ == "Supplier":
                if len(descr) == 0:
                    raise Exception("Failed creating Counterparty! Suppliers must have at least one product for sell!")
                descr = self.validate_supplier_products(descr)
                if isinstance(descr, Exception):
                    raise descr

            # endregion

            new_cpty = Counterparty(name, phone, payment_nr, status, type_, descr, id_)
            return self._cpty_repo.create(new_cpty)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    def update_cpty(self, entity: Counterparty, name, phone, payment_nr, status, type_, descr):
        """Update existing Counterparty"""
        try:
            # region Validations
            if not isinstance(name, str) or len(name) < 3:
                raise TypeError("Failed creating Counterparty! Invalid name!")
            if not isinstance(phone, str) or len(phone) <= 5:
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
            if type_ == "Supplier":
                if len(descr) == 0:
                    raise Exception("Failed creating Counterparty! Suppliers must have at least one product for sell!")
                descr = self.validate_supplier_products(descr)
                if isinstance(descr, Exception):
                    raise descr

            # endregion

            entity.name = name
            entity.phone = phone
            entity.payment_nr = payment_nr
            entity.status = status
            entity.type = type_
            entity.description = descr
            return entity
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame

            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    def _del_cpty_by_id(self, id_: int) -> Counterparty | Exception:
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
            all_tr = self._find_all_transactions()
            to_del = []
            # delete transactions
            for tr in all_tr:
                if tr.counterparty is cpty:
                    to_del.append(tr.id)
            for item in to_del:
                self.del_tr_by_id(item)

            return self._cpty_repo.delete_by_id(id_)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    # endregion

    # region Transactions
    def create_tr(self, type_: str, counterparty: Counterparty, assets: list, id_=None) -> Transaction | Exception:
        """Create new Transaction"""
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
                if isinstance(product, Product):
                    if type_ == "Sale":
                        new_assets.append(TempProduct(product.name, product.type, product.sell_price, product.quantity))
                    if type_ == "Purchase":
                        new_assets.append(TempProduct(product.name, product.type, product.buy_price, product.quantity))
                elif isinstance(product, list):
                    new_assets.append(TempProduct(product[0], product[1], product[2], product[3]))
                else:
                    raise TypeError("Transaction creation failed! Invalid assets!")

            # endregion
            new_tr = Transaction(type_, date, counterparty, new_assets, None, id_)
            return self._tr_repo.create(new_tr)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    def del_tr_by_id(self, id_: int) -> Transaction:
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
        """Generate Invoice from existing Transaction"""
        try:
            if not isinstance(transaction, Transaction):
                raise TypeError(f"Generating invoice failed! Invalid transaction type!")

            if transaction.type == "Purchase":
                raise TypeError(f"Generating invoice failed! You can generate invoices only for Sales!")

            if transaction.invoice is not None:
                raise Exception("Transaction already have invoice!")

            invoicer = self.find_counterparty_by_attr("type", "MyCo")[0]
            now = datetime.now()
            now_str = now.strftime("%m/%d/%Y %H:%M:%S")

            # Default due to date
            due_to_date = now + dt.timedelta(days=15)
            due_to_date = due_to_date.strftime("%m/%d/%Y %H:%M:%S")

            descr = ""
            terms = ""
            status = "Pending"
            new_inv = Invoice(self._inv_repo.gen_inv_num(), invoicer, transaction.counterparty,
                              now_str, due_to_date, transaction.assets, transaction.price, descr, terms, status)
            new_inv = self._inv_repo.create(new_inv)
            transaction.invoice = new_inv
            return new_inv
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    def del_inv_by_transaction(self, transaction: Transaction) -> Invoice | Exception:
        """Delete Invoice by ID"""
        try:
            inv = self.find_invoice_by_id(transaction.invoice.id)
            transaction.invoice = None
            return self._inv_repo.delete_by_id(inv.id)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    # endregion

    # endregion

    # region VIEW

    def get_suppliers_for_dropdown(self):
        all_sp = self.find_counterparty_by_attr("type", "Supplier")
        result = []
        for supplier in all_sp:
            result.append((supplier.id, supplier.name, supplier.payment_nr))

        return result

    def get_supplier_products(self, supp_id: int | None):
        if supp_id is None:
            supplier = self.find_counterparty_by_attr("type", "Supplier")[0]
        else:
            supplier = self.find_counterparty_by_id(supp_id)

        result = []
        for product in supplier.description:
            result.append(Product(product[0], product[1], float(product[2]), float(product[3]), 0, None))

        return result

    def create_cpty_from_view(self, name, phone, payment_nr, status, type_, description):
        if type_.lower() == "supplier":
            description = description.split(" | ")
            new_descr = []
            for product in description:
                new_descr.append(product.split(", "))
            description = new_descr

        return self.create_cpty(name, phone, payment_nr, status, type_, description)

    def update_cpty_from_view(self, name, phone, payment_nr, status, type_, description, id_):
        if type_.lower() == "supplier":
            description = description.split(" | ")
            new_descr = []
            for product in description:
                new_descr.append(product.split(", "))
            description = new_descr

        counterparty = self.find_counterparty_by_id(id_)

        return self.update_cpty(counterparty, name, phone, payment_nr, status, type_, description)

    def del_cpty_from_view(self, id_):
        return self._del_cpty_by_id(id_)

    def make_a_sale(self, cart_vars, client) -> Transaction | Exception:
        try:
            client = self.find_counterparty_by_id(int(client.split(", ")[0][1:]))
            return self.create_tr("sale", client, cart_vars)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    @staticmethod
    def sale_reduce_quantity_or_sell_all(product, amount_to_sell):
        if product.quantity > amount_to_sell:
            product.quantity -= amount_to_sell
            return "reduce", Product(product.name, product.type, product.buy_price, product.sell_price, amount_to_sell,
                                     product.assigned_wh, product.id)
        elif product.quantity == amount_to_sell:
            new_prod = Product(product.name, product.type, product.sell_price,
                               product.buy_price, product.quantity, product.assigned_wh, product.id)
            product.quantity = 0
            return "sell all", new_prod
        else:
            return "Not enough to sell!", None

    @staticmethod
    def rollback_unfinished_sales(find_product_by_id, shopping_cart_vars):
        for item in shopping_cart_vars:
            product_in_repo = find_product_by_id(item.id)
            product_in_repo.quantity += item.quantity

    @staticmethod
    def sell_clear_cart(find_product_by_id, cart_vars):
        for item in cart_vars:
            product_in_repo = find_product_by_id(item.id)
            product_in_repo.quantity += item.quantity

        cart_vars.clear()

    @staticmethod
    def sale_rem_item_from_cart(find_product_by_id, cart_vars, item_params: tuple):
        for product in cart_vars:
            if product.id == int(item_params[0]) and product.name == item_params[1]:
                product_in_repo = find_product_by_id(product.id)
                product_in_repo.quantity += int(item_params[5])
                cart_vars.remove(product)
                break

    @staticmethod
    def sell_add_item_to_cart(shopping_cart_vars, item):
        found = False

        for product in shopping_cart_vars:
            if product.id == item.id and product.name == item.name:
                product.quantity += item.quantity
                found = True
                break

        if not found:
            shopping_cart_vars.append(item)

    @staticmethod
    def sell_calc_total_price(cart_vars) -> float:
        total = 0.0
        for product in cart_vars:
            total += product.quantity * product.sell_price
        return total

    @staticmethod
    def pur_add_item_to_cart(cart_vars, item):
        found = False

        for product in cart_vars:
            if product.id == item.id and product.name == item.name:
                product.quantity += item.quantity
                found = True
                break

        if not found:
            cart_vars.append(item)

    @staticmethod
    def pur_rem_item_from_cart(cart_vars, item_params: tuple):
        for product in cart_vars:
            if product.name == item_params[1]:
                cart_vars.remove(product)
                break

    # endregion

    # region Validations
    @staticmethod
    def validate_cpty_status(status) -> str | None:
        """Validate Counterparty status"""
        valid = ("Enabled", "Disabled")
        for st in valid:
            if st.lower() == status.lower():
                return st

    @staticmethod
    def validate_cpty_type(type_) -> str | None:
        """Validate Counterparty type"""
        valid = ("Supplier", "Client", "MyCo")
        for tp in valid:
            if tp.lower() == type_.lower():
                return tp

    def counterparty_exists(self, counterparty: Counterparty) -> bool:
        """Verify if Counterparty is existing in the Counterparty Repository"""
        all_cpty = self._find_all_counterparties()
        for cpty in all_cpty:
            if counterparty is cpty:
                return True
        return False

    @staticmethod
    def validate_tr_type(type_) -> str | None:
        """Validate Transaction Type"""
        valid = ("Sale", "Purchase")
        for tp in valid:
            if tp.lower() == type_.lower():
                return tp

    @staticmethod
    def validate_supplier_products(products: list):
        for product in products:
            # Valid length
            if len(product) != 4:
                raise Exception(f"Invalid Supplier Product {product}!")
            # Valid product name
            if len(product[0]) < 3:
                raise Exception(f"Supplier Product name {product[0]} is too short!")

            # Valid product type
            if product[1].lower() == "raw materials":
                product[1] = "Raw Materials"
            elif product[1].lower() == "finished goods":
                product[1] = "Finished Goods"
            else:
                raise Exception(f"Supplier Product type {product[1]} is not valid!")

            # Valid buy price
            product[2] = float(product[2])

            # Valid sell price
            product[3] = float(product[3])
            if product[3] < product[2]:
                raise Exception(
                    f"Supplier Product sell price {product[3]} can't be lower than the buy price {product[2]}!")

        return products

    def valid_uniq_cpty_name(self, name) -> bool:
        all_entity = self._find_all_counterparties()

        for entity in all_entity:
            if entity.name.lower() == name.lower():
                return False
        return True

    # endregion

    # region Other
    def print_all_counterparties(self):
        """Print all Counterparties on the console. For debugging purposes"""
        self._cpty_repo.print_all()

    def print_all_transactions(self):
        """Print all Transactions on the console. For debugging purposes"""
        self._tr_repo.print_all()

    def print_all_invoices(self):
        """Print all Invoices on the console. For debugging purposes"""
        self._inv_repo.print_all()

    def make_relations(self):
        """
        After loading Entities from file,\n
        make the relations between the Counterparties <- Transactions <-> Invoices
        """
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

    def counterparties_count(self) -> int:
        """Get the count of all Counterparties in the CounterpartyRepository"""
        return self._cpty_repo.count()

    def transactions_count(self) -> int:
        """Get the count of all Transactions in the TransactionRepository"""
        return self._tr_repo.count()

    def invoices_count(self) -> int:
        """Get the count of all Invoices in the InvoiceRepository"""
        return self._inv_repo.count()

    def generate_invoice_pdf(self, invoice):
        curr_dir = os.getcwd()
        path = os.path.join(curr_dir, f"resources\\invoices\\invoice_{invoice.number}.pdf")
        status = self._pdf_maker.gen_pdf(invoice, path=path)

        if status:
            os.startfile(path)
            return True, "Ok"
        else:
            return False, "Failed to generate invoice!"

    # endregion

    # region Save/Load
    def load_counterparties(self):
        """Load and create all Counterparties from the file"""
        try:
            loaded = self._cpty_repo.load("./model/data/counterparties.json")
            if loaded is not None:
                for item in loaded:
                    id_, name, phone, payment_nr, status, type_, descr = loaded[item].values()
                    new = Counterparty(name, phone, payment_nr, status, type_, descr, id_)
                    self._cpty_repo.create(new)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "Critical", type(ex), tb)
            raise ex

    def load_transactions(self):
        """Load and create all Transactions from the file"""
        try:
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
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "Critical", type(ex), tb)
            raise ex

    def load_invoices(self):
        """Load and create all Invoices from the file"""
        try:
            loaded = self._inv_repo.load("./model/data/invoices.json")
            if loaded is not None:
                for item in loaded:
                    id_, num, from_, to, date, due_to, assets, price, descr, terms, status = loaded[item].values()
                    new = Invoice(num, from_, to, date, due_to, assets, price, descr, terms, status, id_)
                    self._inv_repo.create(new)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "Critical", type(ex), tb)
            raise ex

    def load_all(self):
        """Load all Entities for the SalesModule from the files and make the relations between them"""
        self.load_counterparties()
        self.load_transactions()
        self.load_invoices()
        self.make_relations()

    def save_counterparties(self):
        """Save all Counterparties to file"""
        self._cpty_repo.save("./model/data/counterparties.json")

    def save_transactions(self):
        """Save all Transactions to file"""
        self._tr_repo.save("./model/data/transactions.json")

    def save_invoices(self):
        """Save all Invoices to file"""
        self._inv_repo.save("./model/data/invoices.json")

    def save_all(self):
        """Save all Entities from the SalesModule to their files"""
        self.save_counterparties()
        self.save_transactions()
        self.save_invoices()
    # endregion
