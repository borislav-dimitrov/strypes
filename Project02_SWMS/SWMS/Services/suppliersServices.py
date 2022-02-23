def get_supp_index_by_id(supp_id, all_suppliers):
    for supplier in range(len(all_suppliers)):
        if all_suppliers[supplier].supp_id == int(supp_id):
            return supplier


def get_supplier_by_id(supp_id, all_suppliers):
    for supplier in all_suppliers:
        if supplier.supp_id == int(supp_id):
            return supplier


def get_id_for_new_supplier(all_suppliers):
    highest_id = 0
    for supplier in all_suppliers:
        if supplier.supp_id + 1 > highest_id:
            highest_id = supplier.supp_id

    return highest_id + 1


def validate_supp_menu(menu):
    try:
        items = menu
        # Define if there are one or more products
        if "|" in items:
            items = items.split("|")
            for item in items:
                # Verify pattern for multiple products
                if len(item.split("-")) != 3:
                    print(False)
                    return False, "Invalid menu pattern!", []
            for item in items:
                item_name = item.split("-")[0].strip()
                item_type = item.split("-")[1].strip()
                # Check if product type is correct (suppliers can sell only raw materials)
                if "raw material" != item_type.lower():
                    return False, "Invalid product type!"
                item_buy_price = float(item.split("-")[2].strip())
            return True, "Success", [item_name, item_type, item_buy_price]
        else:
            # Verify pattern for one product
            if len(items.split("-")) != 3:
                return False, "Invalid menu pattern!", []
            item_name = items.split("-")[0].strip()
            item_type = items.split("-")[1].strip()
            # Check if product type is correct (suppliers can sell only raw materials)
            if "raw material" != item_type.lower():
                return False, "Invalid product type!", []
            item_buy_price = float(items.split("-")[2].strip())
            return True, "Success", [item_name, item_type, item_buy_price]
    except Exception as ex:
        print(ex)
        if "convert string to float" in str(ex):
            return False, "Invalid product price!", []

    return False, "Invalid menu pattern!", []