from Model.Entities.product import Product


# region Checks

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
