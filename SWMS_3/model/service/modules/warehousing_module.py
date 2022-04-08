import sys
from model.service.logger import MyLogger

from model.entities.product import Product
from model.entities.warehouse import Warehouse
from model.exceptions import EntityIsAlreadyInWarehouseException, EntityNotFoundException


class WarehousingModule:
    """Module that handles all the business logic for the Warehouse and Product operations"""

    def __init__(self, product_repository, warehouse_repository, logger: MyLogger):
        self._pr_repo = product_repository
        self._wh_repo = warehouse_repository
        self._logger = logger

    # region FIND
    # Products
    def _find_all_products(self) -> dict:
        """Get all existing Products"""
        return self._pr_repo.find_all()

    def find_product_by_id(self, id_: int) -> Product:
        """Get Product by ID"""
        return self._pr_repo.find_by_id(id_)

    def find_product_by_attribute(self, attr_name: str, attr_val: any,
                                  exact_val: bool = True) -> list | Exception | None:
        """Get Products matching the given criteria"""
        try:
            return self._pr_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # Warehouses
    def _find_all_warehouses(self) -> dict:
        """Get all Warehouses"""
        return self._wh_repo.find_all()

    def find_wh_by_id(self, id_: int) -> Warehouse:
        """Get Warehouse by ID"""
        return self._wh_repo.find_by_id(id_)

    def find_wh_by_attribute(self, attr_name: str, attr_val, exact_val=True) -> list | Exception | None:
        """Get Warehouses matching given criteria"""
        try:
            return self._wh_repo.find_by_attribute(attr_name, attr_val, exact_val)
        except Exception as ex:
            return ex

    # endregion

    # region CRUD
    def create_product(self, name: str, type_: str, b_price: float, s_price: float, qty: int, wh: Warehouse | None,
                       id_=None) -> Product | Exception:
        """Create new Product in the ProductRepo"""
        try:
            # region validate
            type_ = self.validate_type(type_)
            if type_ is None:
                raise TypeError(f"Creating Product Failed! Invalid Product type!")

            if not isinstance(b_price, float) or b_price == 0.0:
                raise TypeError(f"Creating Product Failed! Invalid Product buy price!")

            if not isinstance(s_price, float) or s_price == 0.0:
                raise TypeError(f"Creating Product Failed! Invalid Product sell price!")
            if s_price < b_price:
                raise TypeError(f"Creating Product Failed! Sell Price can't be lower than Buy Price!")

            if not isinstance(qty, int) or qty == 0:
                raise TypeError(f"Creating Product Failed! Invalid Product quantity!")

            if wh is not None:
                if not isinstance(wh, Warehouse):
                    raise TypeError(f"Creating Product Failed! Invalid Warehouse!")
                if not self.warehouse_exists(wh):
                    raise EntityNotFoundException(f"Creating Product Failed! Warehouse does not exist!")
                if self.wh_free_space(wh) < qty:
                    print("wh have no space, assigning none wh")
                    wh = None
            # endregion
            pr = Product(name, type_, b_price, s_price, qty, wh, id_)
            pr = self._pr_repo.create(pr)
            return pr
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def create_wh(self, name: str, type_: str, capacity: int, products_: list, status: str,
                  id_=None) -> Warehouse | Exception:
        """Create new Warehouse in the WarehouseRepository"""
        try:
            # region validations
            if len(name) < 2:
                raise Exception(f"Creating Warehouse Failed! Name is too short!")

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
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def update_product(self, product: Product, name: str, type_: str, b_price: float, s_price: float, qty: int,
                       wh: Warehouse | None, id_=None) -> Product | Exception:
        """Update existing Product"""
        try:
            # region validate
            type_ = self.validate_type(type_)
            if type_ is None:
                raise TypeError(f"Creating Product Failed! Invalid Product type!")

            if not isinstance(b_price, float) or b_price == 0.0:
                raise TypeError(f"Creating Product Failed! Invalid Product buy price!")

            if not isinstance(s_price, float) or s_price == 0.0:
                raise TypeError(f"Creating Product Failed! Invalid Product sell price!")
            if s_price < b_price:
                raise TypeError(f"Creating Product Failed! Sell Price can't be lower than Buy Price!")

            if not isinstance(qty, int) or qty == 0:
                raise TypeError(f"Creating Product Failed! Invalid Product quantity!")

            if wh is not None:
                if not isinstance(wh, Warehouse):
                    raise TypeError(f"Creating Product Failed! Invalid Warehouse!")
                if not self.warehouse_exists(wh):
                    raise EntityNotFoundException(f"Creating Product Failed! Warehouse does not exist!")
                if self.wh_free_space(wh) < qty:
                    print("wh have no space, assigning none wh")
                    wh = None
            # endregion

            product.name = name
            product.type = type_
            product.buy_price = b_price
            product.sell_price = s_price
            product.quantity = qty
            product.assigned_wh = wh
            return product
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def update_warehouse(self, wh: Warehouse, name: str, type_: str, capacity: int, products_: list, status: str,
                         id_=None) -> Warehouse | Exception:
        """Update existing Warehouse"""
        try:
            # region validations
            if len(name) < 2:
                raise Exception(f"Updating Warehouse Failed! Name is too short!")

            type_ = self.validate_type(type_)
            if type_ is None:
                raise TypeError(f"Updating Warehouse Failed! Invalid Warehouse type!")

            if not isinstance(capacity, int):
                raise TypeError(f"Updating Warehouse Failed! Invalid Warehouse capacity!")

            if not isinstance(products_, list):
                raise TypeError(f"Updating Warehouse Failed! Invalid products type!")
            # TODO validate products

            status = self.validate_wh_status(status)
            if status is None:
                raise TypeError(f"Updating Warehouse Failed! Invalid Warehouse status!")

            # endregion
            wh.name = name
            wh.type = type_
            wh.capacity = capacity
            wh.status = status
            return wh
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def delete_product_by_id(self, id_: int) -> Product | str:
        """Delete Product by ID"""
        try:
            old_prod = self._pr_repo.find_by_id(id_)

            if old_prod.assigned_wh is not None:
                old_prod.assigned_wh.products.remove(old_prod)

            return self._pr_repo.delete_by_id(id_)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return msg

    def delete_wh_by_id(self, id_: int) -> Warehouse | str:
        """Delete Warehouse by ID"""
        try:
            old = self._wh_repo.find_by_id(id_)

            # remove products assigned warehouse
            for product in old.products:
                product.assigned_wh = None

            return self._wh_repo.delete_by_id(id_)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return msg

    def product_change_wh(self, product: Product, wh: Warehouse | None):
        """Change Product assigned Warehouse"""
        if wh is None:
            self.wh_remove_product(product.assigned_wh, product)
        else:
            self.wh_add_product(wh, product)

    def wh_add_product(self, warehouse: Warehouse, product: Product):
        """Add Product to Warehouse"""
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
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    def wh_remove_product(self, warehouse: Warehouse, product: Product):
        """Remove Product from Warehouse"""
        try:
            if product.assigned_wh is None:
                return
            product.assigned_wh = None
            if product in warehouse.products:
                warehouse.products.remove(product)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            self._logger.log(__file__, msg, "ERROR", type(ex), tb)
            return ex

    # endregion

    # region Validations
    @staticmethod
    def validate_wh_status(status) -> str | None:
        """Validate Warehouse Status"""
        valid = ("Enabled", "Disabled")
        for st in valid:
            if st.lower() == status.lower():
                return st

    @staticmethod
    def validate_type(type_) -> str | None:
        """Validate Warehouse Type"""
        valid = ("Finished Goods", "Raw Materials")
        for tp in valid:
            if tp.lower() == type_.lower():
                return tp

    def warehouse_exists(self, warehouse: Warehouse) -> bool:
        """Verify if Warehouse is existing in current Repository"""
        all_whs = self._find_all_warehouses()
        for wh in all_whs:
            if warehouse is wh:
                return True
        return False

    # endregion

    # region OTHER
    @property
    def products(self) -> dict:
        """Products getter"""
        return self._pr_repo.find_all()

    def print_all_products(self):
        """Print all Products. For debugging purposes."""
        self._pr_repo.print_all()

    def products_count(self) -> int:
        """Get the count of all existing Products"""
        return self._pr_repo.count()

    @property
    def warehouses(self) -> dict:
        """Warehouses getter"""
        return self._wh_repo.find_all()

    def print_all_wh(self):
        """Print all Warehouses. For debugging purposes."""
        self._wh_repo.print_all()

    def wh_count(self):
        """Get the count of all existing Warehouses"""
        return self._wh_repo.count()

    @staticmethod
    def wh_free_space(warehouse: Warehouse) -> int:
        # if not isinstance(warehouse, Warehouse):
        #     raise TypeError(f"Invalid warehouse")
        tmp_count = 0
        for product in warehouse.products:
            tmp_count += product.quantity
        return warehouse.capacity - 0

    def link_products_with_wh(self):
        """Create the relations between Product <-> Warehouse"""
        all_products = self._find_all_products()
        for product in all_products:
            if product.assigned_wh is not None:
                found_wh = self.find_wh_by_attribute("name", product.assigned_wh["name"])[0]
                if self.wh_free_space(found_wh) >= product.quantity:
                    self.product_change_wh(product, found_wh)
                else:
                    self.product_change_wh(product, None)

    # endregion

    # region Save/Load
    def save_products(self):
        """Save the Products to file"""
        self._pr_repo.save("./model/data/products.json")

    def save_warehouses(self):
        """Save the Warehouses to file"""
        self._wh_repo.save("./model/data/warehouses.json")

    def load_products(self):
        """Load and create the Product Objects from file"""
        loaded = self._pr_repo.load("./model/data/products.json")
        if loaded is not None:
            for item in loaded:
                id_, name, type_, b_price, s_price, qty, wh = loaded[item].values()
                new = Product(name, type_, b_price, s_price, qty, wh, id_)
                self._pr_repo.create(new)

    def load_warehouses(self):
        """Load and create the Warehouse Objects from file"""
        loaded = self._pr_repo.load("./model/data/warehouses.json")
        if loaded is not None:
            for item in loaded:
                id_, name, type_, capacity, products, status = loaded[item].values()
                new = Warehouse(name, type_, capacity, [], status, id_)
                self._wh_repo.create(new)

    def load_all(self):
        """Load all Entities in the Warehousing Module and create the relations between them"""
        self.load_products()
        self.load_warehouses()
        self.link_products_with_wh()

    def save_all(self):
        """Save all Entities from the Warehousing Module to their files"""
        self.save_products()
        self.save_warehouses()

    # endregion

    # region VIEW
    def create_product_from_view(self, name, type_, b_price, s_price, qty, warehouse):
        if warehouse != "None":
            warehouse = self.find_wh_by_attribute("name", warehouse, exact_val=False)
            if warehouse is None:
                return Exception("Warehouse not found!")
            warehouse = warehouse[0]
        else:
            warehouse = None

        return self.create_product(name, type_, b_price, s_price, qty, warehouse)

    def update_product_from_view(self, name, type_, b_price, s_price, qty, warehouse, id_):
        if warehouse != "None":
            warehouse = self.find_wh_by_attribute("name", warehouse, exact_val=False)
            if warehouse is None:
                return Exception("Warehouse not found!")
            warehouse = warehouse[0]
        else:
            warehouse = None

        product = self.find_product_by_id(id_)
        return self.update_product(product, name, type_, b_price, s_price, qty, warehouse)
    # endregion
