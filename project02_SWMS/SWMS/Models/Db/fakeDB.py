import Models.Data.loadData as Load
from Models.Data.saveData import save_products, save_all_data
from Models.Assets.user import User
from Models.Assets.product import Product
from Models.Assets.supplier import Supplier
from Models.Assets.client import Client
from Models.Assets.warehouse import Warehouse
from Models.Assets.transaction import Transaction
from Services.userServices import check_user_before_create
import Services.warehouseServices as WhServ
import Services.productServices as ProdServ


my_logger = ""
login_users = []
products = []
suppliers = []
clients = []
warehouses = []
transactions = []

opened_pages = []
curr_user = ""


# Creating
def create_users(data):
    for user in data:
        # check if user already exist
        user_available = check_user_before_create(login_users, user["user_id"], user["user_uname"], my_logger)
        if user_available is True:
            # add user
            new_user = User(user["user_id"],
                            user["user_uname"],
                            # encoding because it comes as a string from the json
                            user["user_pwd"].encode("utf-8"),  
                            user["user_type"],
                            user["user_status"],
                            user["user_last_login"], )
            login_users.append(new_user)
        else:
            return user_available
    return "Success"


def create_products(data):
    try:
        for product in data:
            p_id = ProdServ.get_id_for_new_product(products)
            p_name = product["product_name"]
            p_type = product["product_type"]
            if p_type.lower() == "raw materials":
                p_type = "Raw Materials"
            if p_type.lower() == 'finished goods':
                p_type = "Finished Goods"
            p_buy_price = product["buy_price"]
            p_sell_price = product["sell_price"]
            p_assigned_wh = product["assigned_to_wh"]
            p_quantity = int(product["quantity"])

            # Check if desired warehouse assignment exists
            if not WhServ.check_whname_exist(product["assigned_to_wh"], warehouses):
                product["assigned_to_wh"] = "none"

            # Check if assigned wh is not "none" and there is enough space
            # If no -> change product assigned_wh to none
            # Else add the product id to the warehouse wh_stored items
            if p_assigned_wh.lower() != "none":
                chosen_wh = WhServ.get_wh_by_name(p_assigned_wh, warehouses)
                free_space = WhServ.get_wh_free_space(chosen_wh)
                if p_quantity <= free_space:
                    WhServ.add_product(chosen_wh, p_id, p_quantity)
                else:
                    msg =f"Product {p_id} - {p_name} could not be assigned to {p_assigned_wh}! "\
                        f"Not enough space in warehouse! Assigning to \"none\""
                    my_logger.log(__file__, msg, "WARNING")
                    p_assigned_wh = "none"

            # Check if product already exist
            prod_exist, prod_id = ProdServ.check_product_exist(
                [p_name, p_type, p_buy_price, p_sell_price, p_assigned_wh], products)

            # If yes - add quantity, If no - create new product
            if prod_exist:
                ProdServ.add_to_existing_product(prod_id, p_quantity, products)
            else:
                new_product = Product(p_id, p_name, p_type, p_buy_price, p_sell_price, p_assigned_wh, p_quantity)
                products.append(new_product)

        my_logger.log(__file__, f"Success creating products", "DEBUG")
        return "Success"
    except Exception as ex:
        my_logger.log(__file__, f"Failed creating products! {ex}", "ERROR")
        return f"Fail! {ex}"


def create_suppliers(data):
    try:
        for supplier in data:
            new_supplier = Supplier(supplier["supplier_id"],
                                    supplier["supplier_name"],
                                    supplier["supplier_phone"],
                                    supplier["supplier_iban"],
                                    supplier["supplier_status"],
                                    supplier["buy_menu"])
            suppliers.append(new_supplier)

        my_logger.log(__file__, f"Success creating suppliers", "DEBUG")
        return "Success"
    except Exception as ex:
        my_logger.log(__file__, f"Failed loading products", "ERROR")
        return f"Fail! {ex}"


def create_clients(data):
    try:
        for client in data:
            new_client = Client(client["client_id"],
                                client["client_name"],
                                client["client_phone"],
                                client["client_iban"],
                                client["client_status"])
            clients.append(new_client)

        my_logger.log(__file__, f"Success creating clients", "DEBUG")
        return "Success"
    except Exception as ex:
        my_logger.log(__file__, f"Failed creating clients", "ERROR")
        return f"Fail! {ex}"


def create_warehouses(data):
    try:
        for warehouse in data:
            new_warehouse = Warehouse(warehouse["wh_id"],
                                      warehouse["wh_name"],
                                      warehouse["wh_type"],
                                      warehouse["wh_capacity"],
                                      [],  # warehouse["wh_stored"],
                                      warehouse["wh_status"])
            warehouses.append(new_warehouse)

        my_logger.log(__file__, f"Success creating warehouses", "DEBUG")
        return "Success"
    except Exception as ex:
        my_logger.log(__file__, f"Failed creating warehouses", "ERROR")
        return f"Fail! {ex}"


def create_transactions(data):
    try:
        for transaction in data:
            new_transaction = Transaction(transaction["tr_id"],
                                          transaction["tr_type"],
                                          transaction["tr_date"],
                                          transaction["tr_price"],
                                          transaction["buyer_seller"],
                                          transaction["assets_traded"])
            transactions.append(new_transaction)

        my_logger.log(__file__, f"Success creating transactions", "DEBUG")
        return "Success"
    except Exception as ex:
        my_logger.log(__file__, f"Failed creating transactions", "ERROR")
        return f"Fail! {ex}"


# Loading
def load_and_create_users():
    # clear objects before loading
    login_users.clear()
    # load the new objects
    try:
        users_from_file = Load.load_users()
        if users_from_file == "none":
            return "No users found!"
        status = create_users(users_from_file)

        my_logger.log(__file__, f"Successfully loaded users!", "DEBUG")
        return status
    except TypeError as ex:
        my_logger.log(__file__, f"Failed creating user! {ex}", "ERROR")
        return "Fail! Couldn't create user!"


def load_and_create_products():
    # cleanup current products
    products.clear()
    # load the new ones
    my_logger.log(__file__, "Loading Products...", "INFO")
    products_from_file = Load.load_products()
    status = create_products(products_from_file)
    return status


def load_and_create_suppliers():
    # cleanup current products
    suppliers.clear()
    # load the new ones
    my_logger.log(__file__, "Loading Suppliers...", "INFO")
    suppliers_from_file = Load.load_suppliers()
    status = create_suppliers(suppliers_from_file)
    return status


def load_and_create_clients():
    # cleanup current products
    clients.clear()
    # load the new ones
    my_logger.log(__file__, "Loading Clients...", "INFO")
    clients_from_file = Load.load_clients()
    status = create_clients(clients_from_file)
    return status


def load_and_create_warehouses():
    # cleanup current products
    warehouses.clear()
    # load the new ones
    my_logger.log(__file__, "Loading Warehouses...", "INFO")
    warehouses_from_file = Load.load_warehouses()
    status = create_warehouses(warehouses_from_file)
    return status


def load_and_create_transactions():
    # cleanup current products
    transactions.clear()
    # load the new ones
    my_logger.log(__file__, "Loading Transactions...", "INFO")
    transactions_from_file = Load.load_transactions()
    status = create_transactions(transactions_from_file)
    return status


def load_all_entities():
    load_and_create_warehouses()

    load_and_create_products()

    load_and_create_suppliers()

    load_and_create_clients()

    load_and_create_transactions()


# Saving
def save_all():
    save_all_data()

# Deleting
# def delete_product_by_id(prod_id):
#     for prod in range(len(products) - 1):
#         if products[prod].product_id == prod_id:
#             products.pop(prod)
#     save_products()
