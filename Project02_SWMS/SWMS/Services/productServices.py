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

