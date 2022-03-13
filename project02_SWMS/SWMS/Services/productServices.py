def get_product_by_id(prod_id, all_products):
    for product in all_products:
        if product.product_id == int(prod_id):
            return product


def get_prod_index_by_id(pid, all_products):
    for prod in range(len(all_products)):
        if all_products[prod].product_id == int(pid):
            return prod


def get_id_for_new_product(all_products):
    highest_id = 0
    for product in all_products:
        if product.product_id + 1 > highest_id:
            highest_id = product.product_id

    return highest_id + 1


def get_all_products_assigned_to_wh(wh_name, all_products):
    products_found = []
    for product in all_products:
        if product.assigned_to_wh == wh_name:
            products_found.append(product)
    return products_found


def get_all_sellable_products(all_products):
    all_sellable = []
    for product in all_products:
        if "finished goods" in product.product_type.lower() and "none" not in product.assigned_to_wh.lower():
            all_sellable.append(
                f"{product.product_id} | {product.product_name} | "
                f"{product.assigned_to_wh} | {product.sell_price} | {product.quantity}")
    return all_sellable


def get_products_info_by_id(product_ids, all_products):
    """
    Receive a list with product id/ids
    Return list of product's info
    :param product_ids: list with id's
    :param all_products: list with all products
    :return: list with product/s info
    """
    info = []
    if not isinstance(product_ids, list) and not isinstance(all_products, list):
        return

    for product in all_products:
        if product.product_id in product_ids:
            info.append(product.get_self_info())

    return info


def check_product_exist(product_info, all_products):
    """
    Check if same product already exist
    :param product_info: Name, Type, buy price, sell price, assigned to wh
    :param all_products: All existing products
    :return: True, product id / False, -1
    """

    for product in all_products:
        if product.product_name == product_info[0]:
            if product.product_type == product_info[1]:
                if float(product.buy_price) == float(product_info[2]):
                    if float(product.sell_price) == float(product_info[3]):
                        if product.assigned_to_wh == product_info[4]:
                            return True, product.product_id

    return False, -1


def add_to_existing_product(existing_product_id, amount_to_add, all_products):
    """
    Add quantity to existing product
    :param existing_product_id: The product we want to increase
    :param amount_to_add: How much to increase
    :param all_products: List with all current products
    :return: None
    """
    product = get_product_by_id(existing_product_id, all_products)
    product.quantity += int(amount_to_add)
