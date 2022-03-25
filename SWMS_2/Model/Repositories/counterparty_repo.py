from Model.Entities.counterparty import Counterparty


# region Validations
def status_is_valid(status):
    allowed = ("ENABLED", "DISABLED")
    for stat in allowed:
        if stat.lower() == status.lower():
            return True, stat
    return False, "Invalid status!"


def type_is_valid(type_):
    allowed = ("Client", "Supplier", "Myself")
    for typ in allowed:
        if typ.lower() == type_.lower():
            return True, typ
    return False, "Invalid type!"


# endregion

# region CRUD
def create_counterparty(id_, name, phone, payment_nr, status, type_, descr):
    new_cprty = Counterparty(id_, name, phone, payment_nr, status, type_, descr)
    return new_cprty


def del_counterpart(id_, all_cprty):
    for counterparty in all_cprty:
        if counterparty.entity_id == id_:
            cprty_name = counterparty.name
            index = get_cprty_index(id_, all_cprty)
            all_cprty.pop(index)
            return True, f"Counterparty {cprty_name} successfully deleted!"
        return False, f"Counterparty with id {id_} not found!"


# endregion

# region GET OBJECTS
def get_cprty_by_id(id_, all_cprty):
    for counterparty in all_cprty:
        if counterparty.entity_id == id_:
            return counterparty
    return None


def get_cprty_index(id_, all_cprty):
    for counterparty in all_cprty:
        if counterparty.entity_id == id_:
            return all_cprty.index(counterparty)
# endregion
