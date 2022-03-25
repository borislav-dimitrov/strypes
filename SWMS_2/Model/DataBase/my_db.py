from Model.Entities.logger import MyLogger
import Resources.config as cfg
import json as js
import Model.Modules.all_modules as Modules

# region Tracking
my_logger = ""
curr_user = ""
opened_pages = []
# endregion

# region Entities
users = []
products = []
suppliers = []
clients = []
warehouses = []
invoices = []

# endregion

allowed_types = cfg.WAREHOUSE_TYPES


def spawn_logger():
    global my_logger
    my_logger = MyLogger(cfg.LOG_ENABLED, cfg.DEFAULT_LOG_FILE,
                         cfg.LOG_LEVEL, cfg.REWRITE_LOG_ON_STARTUP)


# region Prints
def print_all_users():
    for user in users:
        print(user.entity_id, user.user_name, user.user_type, user.user_status, user.last_login)


def print_all_products():
    for product in products:
        print(product.entity_id, product.product_name, product.product_type, product.buy_price, product.sell_price,
              product.quantity, product.assigned_wh)


def print_all_warehouses():
    for warehouse in warehouses:
        print(warehouse.entity_id, warehouse.wh_name, warehouse.wh_type,
              warehouse.wh_capacity, warehouse.wh_products, warehouse.wh_status)


def print_all_inv():
    for invoice in invoices:
        print(invoice.entity_id, invoice.invoice_number, "\n", invoice.from_info, "\n", invoice.to_info,
              "\n", invoice.invoice_date, invoice.items, invoice.total_price, invoice.description, "\n",
              invoice.terms_conditions, invoice.status)


# endregion


def get_new_entity_id(all_current_entities):
    current_ids = [0]
    id = 0
    for entity in all_current_entities:
        current_ids.append(int(entity.entity_id))

    while id in current_ids:
        id += 1

    return id


def validate_entity_id(id_, all_entities):
    for item in all_entities:
        if item.entity_id == id_:
            return False
    return True


def save_data_to_json(data, file):
    with open(file, "wt", encoding="utf-8") as f:
        f.write(js.dumps(data, indent=4))


def startup():
    spawn_logger()
    Modules.umgmt.load_users()
    Modules.whmgmt.load_whs()
    Modules.prmgmt.load_products()
    Modules.whmgmt.hook_products_to_warehouse()
    # Modules.invmgmt.load_inv()
