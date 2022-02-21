from Models.Data.loadData import load_users, load_products, load_suppliers
from Models.Assets.user import User
from Models.Assets.product import Product
from Models.Assets.supplier import Supplier
from Services.userServices import check_user_before_create

login_users = []
products = []
suppliers = []
curr_user = None


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
            new_product = Product(product["product_id"],
                                  product["product_name"],
                                  product["product_type"],
                                  product["buy_price"],
                                  product["sell_price"])
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
                                    supplier["supplier_status"])
            suppliers.append(new_supplier)
        return "Success"
    except Exception as ex:
        return f"Fail! {ex}"


def load_and_create_users():
    # clear objects before loading
    login_users.clear()
    # load the new objects
    try:
        users_from_file = load_users()
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


def load_all_entities():
    # ToDo
    # Log these prints in a log file
    print("Loading Products...")
    products_status = load_and_create_products()
    print(products_status)

    print("Loading Suppliers...")
    suppliers_status = load_and_create_suppliers()
    print(suppliers_status)
