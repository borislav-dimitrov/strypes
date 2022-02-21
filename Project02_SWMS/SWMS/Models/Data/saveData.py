import Models.Db.fakeDB as DB
import json


def save_data_to_json(data, file):
    with open(file, "w") as output:
        output.write(json.dumps(data, indent=4))


def save_users():
    output_file = "./Models/Db/loginUsers.json"
    data = {
        "login_users": []
    }
    for user in DB.login_users:
        data["login_users"].append({
            "user_id": user.user_id,
            "user_uname": user.user_name.lower(),
            "user_pwd": user.user_pwd.decode("utf-8"),  # we are using decode, so we can store it in the JSON
            "user_type": user.user_type,
            "user_status": user.user_status,
            "user_last_login": user.user_last_login
        })

    save_data_to_json(data, output_file)


def save_products():
    output_file = "./Models/Db/products.json"
    data = {
        "products": []
    }
    for product in DB.products:
        data["products"].append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_type": product.product_type,
            "buy_price": product.buy_price,
            "sell_price": product.sell_price
        })
    save_data_to_json(data, output_file)


def save_suppliers():
    output_file = "./Models/Db/suppliers.json"
    data = {
        "suppliers": []
    }
    for supplier in DB.suppliers:
        data["suppliers"].append({
            "supplier_id": supplier.supp_id,
            "supplier_name": supplier.supp_name,
            "supplier_phone": supplier.supp_phone,
            "supplier_iban": supplier.supp_iban,
            "supplier_status": supplier.supp_status
        })
    save_data_to_json(data, output_file)


def save_all_data():
    save_users()
    save_products()
    save_suppliers()
