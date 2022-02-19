def get_product_by_id(prod_id, products):
    for product in products:
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
