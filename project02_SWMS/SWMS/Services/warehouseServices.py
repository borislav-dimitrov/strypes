def get_id_for_new_wh(all_warehouses):
    highest_id = 0
    for warehouse in all_warehouses:
        if warehouse.wh_id + 1 > highest_id:
            highest_id = warehouse.wh_id

    return highest_id + 1


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
