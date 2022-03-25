import sys
import Model.DataBase.my_db as db
import Model.Repositories.counterparty_repo as cptrepo
import json as js


# region CRUD
def create_new_cprty(id_, name, phone, payment_nr, status, type_, descr=""):
    # region Validations
    if id_ == "auto":
        id_ = db.get_new_entity_id(db.counterparties)
    else:
        is_valid = db.validate_entity_id(id_, db.counterparties)
        if not is_valid:
            return False, "Invalid Invoice id!"

    if not isinstance(name, str) or len(name) < 3:
        return False, f"Invalid Counterparty name: {name}!"

    if not isinstance(phone, str) or len(phone) < 5:
        return False, f"Invalid Counterparty phone: {phone}!"

    if not isinstance(payment_nr, str) or len(payment_nr) < 5:
        return False, f"Invalid Counterparty payment number: {payment_nr}!"

    state, status = cptrepo.status_is_valid(status)
    if not state:
        return False, status

    state, type_ = cptrepo.type_is_valid(type_)
    if not state:
        return False, type_

    # endregion

    new_crpty = cptrepo.create_counterparty(id_, name, phone, payment_nr, status, type_, descr)
    db.counterparties.append(new_crpty)
    return True, "Success"


def del_cprty(id_):
    cptrepo.del_counterpart(id_, db.counterparties)
    reload_cprty()
    return True, "Success"


def edit_cprty_name(id_, name):
    if not isinstance(name, str) or len(name) < 3:
        return False, f"Invalid Counterparty name: {name}!"
    cprty = cptrepo.get_cprty_by_id(id_, db.counterparties)
    cprty.name = name
    reload_cprty()
    return True, "Success"


def edit_cprty_phone(id_, phone):
    if not isinstance(phone, str) or len(phone) < 5:
        return False, f"Invalid Counterparty phone: {phone}!"
    cprty = cptrepo.get_cprty_by_id(id_, db.counterparties)
    cprty.phone = phone
    reload_cprty()
    return True, "Success"


def edit_cprty_payment_nr(id_, payment_nr):
    if not isinstance(payment_nr, str) or len(payment_nr) < 5:
        return False, f"Invalid Counterparty payment number: {payment_nr}!"
    cprty = cptrepo.get_cprty_by_id(id_, db.counterparties)
    cprty.payment_nr = payment_nr
    reload_cprty()
    return True, "Success"


def edit_cprty_status(id_, status):
    state, status = cptrepo.status_is_valid(status)
    if not state:
        return False, status
    cprty = cptrepo.get_cprty_by_id(id_, db.counterparties)
    cprty.status = status
    reload_cprty()
    return True, "Success"


def edit_cprty_type(id_, type_):
    state, type_ = cptrepo.type_is_valid(type_)
    if not state:
        return False, type_
    cprty = cptrepo.get_cprty_by_id(id_, db.counterparties)
    cprty.type_ = type_
    reload_cprty()
    return True, "Success"


def edit_cprty_descr(id_, descr):
    cprty = cptrepo.get_cprty_by_id(id_, db.counterparties)
    cprty.description = descr
    reload_cprty()


# endregion


# region Save/Load/Reload
def save_cprty():
    output_file = "./Model/DataBase/counterparties.json"
    data = {"counterparties": []}

    for counterparty in db.counterparties:
        data["counterparties"].append({
            "entity_id": counterparty.entity_id,
            "name": counterparty.name,
            "phone": counterparty.phone,
            "payment_nr": counterparty.payment_nr,
            "status": counterparty.status,
            "type": counterparty.type_,
            "description": counterparty.description
        })

    try:
        db.save_data_to_json(data, output_file)
    except Exception as ex:
        msg = "Error saving counterparties!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def load_cprty():
    try:
        with open("./Model/DataBase/counterparties.json", "rt", encoding="utf-8") as file:
            data = js.load(file)
    except Exception as ex:
        msg = "Error reading counterparties file!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)

    db.counterparties.clear()

    try:
        for counterparty in data["counterparties"]:
            id_ = counterparty["entity_id"]
            name = counterparty["name"]
            phone = counterparty["phone"]
            payment_nr = counterparty["payment_nr"]
            status = counterparty["status"]
            type_ = counterparty["type"]
            description = counterparty["description"]

            create_new_cprty(id_, name, phone, payment_nr, status, type_, description)
    except Exception as ex:
        msg = "Error Loading counterparties!"
        tb = sys.exc_info()[2].tb_frame
        db.my_logger.log(__file__, msg, "ERROR", type(ex), tb)


def reload_cprty():
    save_cprty()
    load_cprty()
# endregion
