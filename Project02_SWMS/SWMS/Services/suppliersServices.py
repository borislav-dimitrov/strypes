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
