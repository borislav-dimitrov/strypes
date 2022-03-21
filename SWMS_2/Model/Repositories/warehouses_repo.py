from Model.Entities.warehouse import Warehouse


# region Checks
def validate_name(name, all_wh):
    for warehouse in all_wh:
        if warehouse.wh_name.lower() == name.lower():
            return False, "Warehouse already exist"
    return True, ""


def validate_type(type_, all_types):
    for t in all_types:
        if type_.lower() == t.lower():
            return t
    return -1


def validate_status(status):
    if status.lower() == "enabled":
        return "ENABLED"
    elif status.lower() == "disabled":
        return "DISABLED"
    else:
        return -1


# endregion


# region CRUD
def create_warehouse(id_, name, type_, capacity, products: list, status):
    new_wh = Warehouse(id_, name, type_, capacity, products, status)
    return new_wh


def delete_warehouse(id_, all_wh: list[Warehouse]):
    for warehouse in all_wh:
        if warehouse.entity_id == id_:
            deleted_wh_name = warehouse.wh_name
            index = get_wh_index(id_, all_wh)
            all_wh.pop(index)
            return True, f"Warehouse {deleted_wh_name} deleted successfully!"
    return False, f"Warehouse with id of {id_} not found!"


# endregion


# region GET OBJECTS
def get_wh_by_id(wh_id: int, all_whs: list[Warehouse]):
    """
    Get Warehouse object buy its id
    :param wh_id: Warehouse id as int
    :param all_whs: All current Warehouses
    :return: Warehouse object / None
    """
    for warehouse in all_whs:
        if warehouse.entity_id == wh_id:
            return warehouse
    return None


def get_wh_index(id_, all_wh):
    for warehouse in all_wh:
        if warehouse.entity_id == id_:
            return all_wh.index(warehouse)
    return None


def get_wh_by_name(name, all_wh):
    for warehouse in all_wh:
        if warehouse.wh_name.lower() == name.lower():
            return warehouse
    return None
# endregion
