import Models.Db.fakeDB as DB
import json
import Services.warehouseServices as WhServ


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
        if not WhServ.check_whname_exist(product.assigned_to_wh, DB.warehouses):
            product.assigned_to_wh = "none"

        data["products"].append({
            "product_id": product.product_id,
            "product_name": product.product_name,
            "product_type": product.product_type,
            "buy_price": product.buy_price,
            "sell_price": product.sell_price,
            "assigned_to_wh": product.assigned_to_wh
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


def save_clients():
    output_file = "./Models/Db/clients.json"
    data = {
        "clients": []
    }
    for client in DB.clients:
        data["clients"].append({
            "client_id": client.client_id,
            "client_name": client.client_name,
            "client_phone": client.client_phone,
            "client_iban": client.client_iban,
            "client_status": client.client_status
        })
    save_data_to_json(data, output_file)


def save_warehouses():
    output_file = "./Models/Db/warehouses.json"
    data = {
        "warehouses": []
    }
    for warehouse in DB.warehouses:
        data["warehouses"].append({
            "wh_id": warehouse.wh_id,
            "wh_name": warehouse.wh_name,
            "wh_type": warehouse.wh_type,
            "wh_capacity": warehouse.wh_capacity,
            "wh_status": warehouse.wh_status
        })
    save_data_to_json(data, output_file)


def save_transactions():
    output_file = "./Models/Db/transactions.json"
    data = {
        "transactions": []
    }
    for transaction in DB.transactions:
        data["transactions"].append({
            "tr_id": transaction.tr_id,
            "tr_type": transaction.tr_type,
            "tr_date": transaction.tr_date,
            "tr_price": transaction.tr_price,
            "buyer_seller": transaction.buyer_seller,
            "assets_traded": transaction.assets_traded
        })
    save_data_to_json(data, output_file)


def save_all_data():
    save_users()
    save_warehouses()
    save_products()
    save_suppliers()
    save_clients()
    save_transactions()
