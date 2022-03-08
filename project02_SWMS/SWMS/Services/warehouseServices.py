def get_id_for_new_wh(all_warehouses):
    highest_id = 0
    for warehouse in all_warehouses:
        if warehouse.wh_id + 1 > highest_id:
            highest_id = warehouse.wh_id

    return highest_id + 1


def get_wh_by_name(name, all_warehouses):
    """
    Get warehouse { object } by name
    :param name: Desired warehouse name
    :param all_warehouses: List with all existing warehouses { objects }
    :return: Warehouse { object }
    """
    for warehouse in all_warehouses:
        if warehouse.wh_name.lower() == name.lower():
            return warehouse


def get_wh_by_id(wh_id, all_warehouses):
    for warehouse in all_warehouses:
        if warehouse.wh_id == int(wh_id):
            return warehouse


def get_wh_index_by_id(wh_id, all_warehouses):
    for warehouse in range(len(all_warehouses)):
        if all_warehouses[warehouse].wh_id == int(wh_id):
            return warehouse


def check_whname_exist(name, all_warehouses):
    for warehouse in all_warehouses:
        if warehouse.wh_name == name:
            return True
    return False


def add_product(warehouse, product_id, product_quantity):
    """
    Add product to warehouse
    :param warehouse: Chosen warehouse { object }
    :param product_id: Product id to add
    :param product_quantity: Amount products to add
    :return: None
    """
    if len(warehouse.wh_stored) == 0:
        warehouse.wh_stored.append(f"{product_id} x {product_quantity}")
    else:
        for product in range(len(warehouse.wh_stored)):
            current_prod_id = int(warehouse.wh_stored[product].split("x")[0].strip())
            if int(product_id) == current_prod_id:
                new_info = f"{current_prod_id} x {product_quantity}"
                if new_info not in warehouse.wh_stored:
                    warehouse.wh_stored[product] = new_info
                    return
            else:
                new_info = f"{product_id} x {product_quantity}"
                if new_info not in warehouse.wh_stored:
                    warehouse.wh_stored.append(new_info)
                    return


def remove_product(warehouse, product_id, amount):
    """
    Remove product amount from warehouse
    :param warehouse: Chosen warehouse { object }
    :param product_id: Product id to remove
    :param amount: How many products to remove
    :return: None
    """
    for product in range(len(warehouse.wh_stored)):
        current_prod_id = int(warehouse.wh_stored[product].split("x")[0].strip())
        if int(product_id) == current_prod_id:
            quantity = int(warehouse.wh_stored[product].split("x")[1].strip())
            new_quantity = quantity - int(amount)
            if new_quantity <= 0:
                warehouse.wh_stored.remove(warehouse.wh_stored[product])
                return
            else:
                warehouse.wh_stored[product] = f"{current_prod_id} x {new_quantity}"
                return


def get_wh_free_space(warehouse):
    """
    Return the free space of the chosen warehouse
    :param warehouse: The desired warehouse { object }
    :return: Current free space { int }
    """
    free_space = warehouse.wh_capacity
    for rec in range(len(warehouse.wh_stored)):
        current_amount = warehouse.wh_stored[rec].split("x")[1].strip()
        free_space -= int(current_amount)

    return free_space

