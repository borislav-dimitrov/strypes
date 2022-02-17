import json

def read_cc():
    file = open("./assets/costCentres.json")
    data = json.load(file)
    all_info = []
    for line in data["cost_centres"]:
        all_info.append(line)

    return all_info


def read_crt():
    file = open("./assets/cartridges.json")
    data = json.load(file)
    all_info = []
    for line in data["cartridges"]:
        all_info.append(line)

    return all_info


def read_prn():
    file = open("./assets/printers.json")
    data = json.load(file)
    all_info = []
    for line in data["printers"]:
        all_info.append(line)

    return all_info


def read_users():
    file = open("./assets/users.json")
    data = json.load(file)
    all_info = []
    for line in data["users"]:
        all_info.append(line)

    return all_info


def read_all_data():
    cost_centres_data = read_cc()
    cartridges_data = read_crt()
    printers_data = read_prn()
    users_data = read_users()

    return cost_centres_data, cartridges_data, printers_data, users_data
