import sys
import model.dao.my_db as db

from model.entities.product import Product
from model.entities.warehouse import Warehouse
from model.exceptions import EntityIsAlreadyInWarehouseException, EntityNotFoundException


class WarehousingModule:
    def __init__(self, product_repository, warehouse_repository):
        self._pr_repo = product_repository
        self._wh_repo = warehouse_repository

    # region FIND
    # Products
    def find_all_products(self):
        return self._pr_repo.find_all()

    def find_product_by_id(self, id_):
        return self._pr_repo.find_by_id(id_)

    def find_product_by_attribute(self, attr_name: str, attr_val, exact_val: bool = True):
        return self._pr_repo.find_by_attribute(attr_name, attr_val, exact_val)

    # Warehouses
    def find_all_warehouses(self):
        return self._wh_repo.find_all()

    def find_wh_by_id(self, id_):
        return self._wh_repo.find_by_id(id_)

    def find_wh_by_attribute(self, attr_name: str, attr_val, exact_val=True):
        return self._wh_repo.find_by_attribute(attr_name, attr_val, exact_val)

    # endregion

    # region CRUD
    def create_product(self, name: str, type_: str, b_price: float, s_price: float, qty: int, wh: Warehouse | None,
                       id_=None) -> Product | Exception:
        """
        Create new product in the product repo
        :return: new Product Object | Exception
        """
        try:
            # region validate
            type_ = self.validate_type(type_)
            if type_ is None:
                raise TypeError(f"Creating Product Failed! Invalid Product type!")

            if not isinstance(b_price, float):
                raise TypeError(f"Creating Product Failed! Invalid Product buy price!")

            if not isinstance(s_price, float):
                raise TypeError(f"Creating Product Failed! Invalid Product sell price!")

            if not isinstance(qty, int):
                raise TypeError(f"Creating Product Failed! Invalid Product quantity!")

            if wh is not None:
                if not isinstance(wh, Warehouse):
                    raise TypeError(f"Creating Product Failed! Invalid Warehouse!")
                if not self.warehouse_exists(wh):
                    raise EntityNotFoundException(f"Creating Product Failed! Warehouse does not exist!")
            # endregion
            pr = Product(name, type_, b_price, s_price, qty, wh, id_)
            pr = self._pr_repo.create(pr)
            self.product_change_wh(pr, wh)
            return pr
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def create_wh(self, name: str, type_: str, capacity: int, products_: list, status: str,
                  id_=None) -> Warehouse | Exception:
        """
        Create new warehouse in the warehouse repo
        :return: new Warehouse Object | Exception
        """
        try:
            # region validations
            type_ = self.validate_type(type_)
            if type_ is None:
                raise TypeError(f"Creating Warehouse Failed! Invalid Warehouse type!")

            if not isinstance(capacity, int):
                raise TypeError(f"Creating Warehouse Failed! Invalid Warehouse capacity!")

            if not isinstance(products_, list):
                raise TypeError(f"Creating Warehouse Failed! Invalid products type!")
            if len(products_) != 0:
                raise TypeError(f"Creating Warehouse Failed! Only empty warehouses can be created!")

            status = self.validate_wh_status(status)
            if status is None:
                raise TypeError(f"Creating Warehouse Failed! Invalid Warehouse status!")

            # endregion
            wh = Warehouse(name, type_, capacity, products_, status, id_)
            return self._wh_repo.create(wh)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def update_product(self, new_entity: Product):
        entity = self._pr_repo.find_by_id(new_entity.id)
        entity = new_entity

    def update_warehouse(self, new_entity: Warehouse):
        entity = self._wh_repo.find_by_id(new_entity.id)
        entity = new_entity

    def delete_product_by_id(self, id_: int):
        try:
            old_prod = self._pr_repo.find_by_id(id_)

            if old_prod.assigned_wh is not None:
                old_prod.assigned_wh.products.remove(old_prod)

            return self._pr_repo.delete_by_id(id_)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def delete_wh_by_id(self, id_: int):
        try:
            old = self._wh_repo.find_by_id(id_)

            # remove products assigned warehouse
            for product in old.products:
                product.assigned_wh = None

            return self._wh_repo.delete_by_id(id_)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def product_change_wh(self, product: Product, wh: Warehouse | None):
        if wh is None:
            self.wh_remove_product(product.assigned_wh, product)
        else:
            self.wh_add_product(wh, product)

    def wh_add_product(self, warehouse: Warehouse, product: Product):
        try:
            if product.assigned_wh is None:
                warehouse.products.append(product)
                product.assigned_wh = warehouse
            elif product.assigned_wh is warehouse:
                raise EntityIsAlreadyInWarehouseException(
                    f"Product {product.name} is already in warehouse {warehouse.name}!")
            else:
                if isinstance(product.assigned_wh, dict):  # On startup when loading from file it is dict
                    old_wh = self.find_wh_by_id(product.assigned_wh["id"])
                else:
                    old_wh = product.assigned_wh
                self.wh_remove_product(old_wh, product)
                warehouse.products.append(product)
                product.assigned_wh = warehouse
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    @staticmethod
    def wh_remove_product(warehouse: Warehouse, product: Product):
        try:
            if product.assigned_wh is None:
                return
            product.assigned_wh = None
            if product in warehouse.products:
                warehouse.products.remove(product)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    # endregion

    # region Validations
    @staticmethod
    def validate_wh_status(status):
        valid = ("Enabled", "Disabled")
        for st in valid:
            if st.lower() == status.lower():
                return st

    @staticmethod
    def validate_type(type_):
        valid = ("Finished Goods", "Raw Materials")
        for tp in valid:
            if tp.lower() == type_.lower():
                return tp

    def warehouse_exists(self, warehouse):
        all_whs = self.find_all_warehouses()
        for wh in all_whs:
            if warehouse is wh:
                return True
        return False

    # endregion

    # region OTHER
    @property
    def products(self):
        return self._pr_repo.get_entities()

    def print_all_products(self):
        self._pr_repo.print_all()

    def products_count(self):
        return self._pr_repo.count()

    @property
    def warehouses(self):
        return self._wh_repo.get_entities()

    def print_all_wh(self):
        self._wh_repo.print_all()

    def wh_count(self):
        return self._wh_repo.count()

    def link_products_with_wh(self):
        all_products = self.find_all_products()
        for product in all_products:
            if product.assigned_wh is not None:
                found_wh = self.find_wh_by_attribute("name", product.assigned_wh["name"])[0]
                self.product_change_wh(product, found_wh)

    # endregion

    # region Save/Load
    def save_products(self):
        self._pr_repo.save("./model/data/products.json")

    def save_warehouses(self):
        self._wh_repo.save("./model/data/warehouses.json")

    def load_products(self):
        loaded = self._pr_repo.load("./model/data/products.json")
        if loaded is not None:
            for item in loaded:
                id_, name, type_, b_price, s_price, qty, wh = loaded[item].values()
                new = Product(name, type_, b_price, s_price, qty, wh, id_)
                self._pr_repo.create(new)

    def load_warehouses(self):
        loaded = self._pr_repo.load("./model/data/warehouses.json")
        if loaded is not None:
            for item in loaded:
                id_, name, type_, capacity, products, status = loaded[item].values()
                new = Warehouse(name, type_, capacity, [], status, id_)
                self._wh_repo.create(new)

    def load_all(self):
        self.load_products()
        self.load_warehouses()
        self.link_products_with_wh()
        print()

    def save_all(self):
        self.save_products()
        self.save_warehouses()
    # endregion
