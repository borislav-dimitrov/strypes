from Models.Data.loadData import load_users, load_products, load_suppliers, load_clients, load_warehouses, \
    load_transactions
from Models.Data.saveData import save_products, save_all_data
from Models.Assets.user import User
from Models.Assets.product import Product
from Models.Assets.supplier import Supplier
from Models.Assets.client import Client
from Models.Assets.warehouse import Warehouse
from Models.Assets.transaction import Transaction
from Services.userServices import check_user_before_create
from Services.warehouseServices import check_whname_exist

login_users = []
products = []
suppliers = []
clients = []
warehouses = []
transactions = []

opened_pages = []


# Creating
def create_users(data):
    for user in data:
        # check if user already exist
        user_available = check_user_before_create(login_users, user["user_id"], user["user_uname"])
        if user_available is True:
            # add user
            new_user = User(user["user_id"],
                            user["user_uname"],
                            user["user_pwd"].encode("utf-8"),  # encoding because it comes as a string from the json
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
            if not check_whname_exist(product["assigned_to_wh"], warehouses):
                product["assigned_to_wh"] = "none"

            new_product = Product(product["product_id"],
                                  product["product_name"],
                                  product["product_type"],
                                  product["buy_price"],
                                  product["sell_price"],
                                  product["assigned_to_wh"])
            products.append(new_product)
        return "Success"
    except Exception as ex:
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
        return "Success"
    except Exception as ex:
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
        return "Success"
    except Exception as ex:
        return f"Fail! {ex}"


def create_warehouses(data):
    try:
        for warehouse in data:
            new_warehouse = Warehouse(warehouse["wh_id"],
                                      warehouse["wh_name"],
                                      warehouse["wh_type"],
                                      warehouse["wh_capacity"],
                                      warehouse["wh_status"])
            warehouses.append(new_warehouse)
        return "Success"
    except Exception as ex:
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
        return "Success"
    except Exception as ex:
        return f"Fail! {ex}"


# Loading
def load_and_create_users():
    # clear objects before loading
    login_users.clear()
    # load the new objects
    try:
        print("Loading Users")
        users_from_file = load_users()
        if users_from_file == "none":
            return "No users found!"
        status = create_users(users_from_file)
        return status
    except TypeError as ex:

        return "Fail! Couldn't create user!"


def load_and_create_products():
    # cleanup current products
    products.clear()
    # load the new ones
    try:
        products_from_file = load_products()
        status = create_products(products_from_file)
        return status
    except Exception as ex:
        print(f"Fail! {ex}")


def load_and_create_suppliers():
    # cleanup current products
    suppliers.clear()
    # load the new ones
    try:
        suppliers_from_file = load_suppliers()
        status = create_suppliers(suppliers_from_file)
        return status
    except Exception as ex:
        print(f"Fail! {ex}")


def load_and_create_clients():
    # cleanup current products
    clients.clear()
    # load the new ones
    try:
        clients_from_file = load_clients()
        status = create_clients(clients_from_file)
        return status
    except Exception as ex:
        print(f"Fail! {ex}")


def load_and_create_warehouses():
    # cleanup current products
    warehouses.clear()
    # load the new ones
    try:
        warehouses_from_file = load_warehouses()
        status = create_warehouses(warehouses_from_file)
        return status
    except Exception as ex:
        print(f"Fail! {ex}")


def load_and_create_transactions():
    # cleanup current products
    transactions.clear()
    # load the new ones
    try:
        transactions_from_file = load_transactions()
        status = create_transactions(transactions_from_file)
        return status
    except Exception as ex:
        print(f"Fail! {ex}")


def load_all_entities():
    # ToDo
    # Log these prints in a log file
    print("Loading Warehouses...")
    warehouses_status = load_and_create_warehouses()
    print(warehouses_status)
    print("===========")

    print("Loading Products...")
    products_status = load_and_create_products()
    print(products_status)
    print("===========")

    print("Loading Suppliers...")
    suppliers_status = load_and_create_suppliers()
    print(suppliers_status)
    print("===========")

    print("Loading Clients...")
    clients_status = load_and_create_clients()
    print(clients_status)
    print("===========")

    print("Loading Transactions...")
    transactions_status = load_and_create_transactions()
    print(transactions_status)
    print("===========")


# Saving
def save_all():
    save_all_data()


# Deleting
def delete_product_by_id(prod_id):
    for prod in range(len(products) - 1):
        if products[prod].product_id == prod_id:
            products.pop(prod)
    save_products()
