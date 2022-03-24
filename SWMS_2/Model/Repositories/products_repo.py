from Model.Entities.product import Product


# region Validations
def validate_type(type_, types):
    prod_type = "none"
    for item in types:
        if type_.lower() in item.lower():
            prod_type = item
    if prod_type == "none":
        print(f"Invalid product type {type_}!")
        return False
    return prod_type


def validate_price(price):
    if isinstance(price, float):
        return price
    if isinstance(price, int):
        return float(price)
    return False


def validate_assigned_wh(wh, all_wh):
    for warehouse in all_wh:
        if warehouse.wh_name.lower() == wh.lower():
            return True
    return False


def check_product_exist(name, type_, b_price, s_price, quantity, assigned_wh, all_prods):
    for product in all_prods:
        if product.product_name == name and product.product_type == type_ and product.buy_price == b_price and product.sell_price == s_price and product.quantity == quantity and product.assigned_wh == assigned_wh:
            return True, product
    return False, -1


# endregion

# region CRUD
def create_product(id_, name, type_, bprice, sprice, quantity, assigned_wh):
    new_prod = Product(id_, name, type_, bprice, sprice, quantity, assigned_wh)
    return new_prod


def delete_product(id_, all_products):
    for product in all_products:
        if product.entity_id == id_:
            name = product.product_name
            index = get_product_index(id_, all_products)
            all_products.pop(index)
            return True, f"Product {name} successfully deleted!"
    return False, f"Product with id of {id_} not found!"


# endregion

# region GET OBJECTS
def get_product_by_id(id_, all_products):
    for product in all_products:
        if product.entity_id == id_:
            return product
    return None


def get_product_index(id_, all_products):
    for product in all_products:
        if product.entity_id == id_:
            return all_products.index(product)
    return None
# endregion
