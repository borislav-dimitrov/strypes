import helpers.dateHelpers as dh
import helpers.objectHelpers as oh

from objects.costCentre import CostCentre
from objects.cartridge import Cartridge
from objects.user import User
from objects.printer import Printer
from preload.loadFromJson import read_all_data

all_cc = []
all_crt = []
all_users = []
all_prn = []


def create_cc(cc_id, cc_num, cc_name, cc_status):
    new_cc = CostCentre(cc_id, cc_num, cc_name, cc_status)
    all_cc.append(new_cc)


def create_crt(crt_id, crt_type, serial_number, barcode,
               cost_centre, date_bought, date_scrap, remark, status):
    new_crt = Cartridge(crt_id, crt_type, serial_number, barcode,
                        cost_centre, date_bought, date_scrap, remark, status)
    all_crt.append(new_crt)


def create_user(user_id, f_name, l_name, cost_centre, status):
    new_user = User(user_id, f_name, l_name, cost_centre, status)
    all_users.append(new_user)


def create_prn(prn_id, prn_model, cost_centre, location, prn_ip, bk_counters,
               clr_counters, status, rent):
    new_printer = Printer(prn_id, prn_model, cost_centre, location, prn_ip, bk_counters, clr_counters, status, rent)
    all_prn.append(new_printer)


def populate_cc(data):
    for item in data:
        create_cc(item["cost_centre_id"],
                  item["cost_centre_num"],
                  item["cost_centre_name"],
                  item["cost_centre_status"])


def populate_crt(data):
    for item in data:
        create_crt(item["cartridge_id"],
                   item["cartridge_type"],
                   item["cartridge_serial"],
                   item["cartridge_barcode"],
                   oh.get_object_by_id(item["cartridge_cc_id"], all_cc),
                   item["cartridge_created"],
                   item["cartridge_scraped"],
                   item["cartridge_remark"],
                   item["cartridge_status"])


def populate_users(data):
    for item in data:
        create_user(item["users_id"],
                    item["users_f_name"],
                    item["users_l_name"],
                    oh.get_object_by_id(item["users_cc_id"], all_cc),
                    item["users_status"])


def populate_prn(data):
    for item in data:
        create_prn(item["printers_id"],
                   item["printers_model"],
                   oh.get_object_by_id(item["printers_cc_id"], all_cc),
                   item["printers_location"],
                   item["printers_ip"],
                   item["printers_blk_counters"],
                   item["printers_clr_counters"],
                   item["printers_status"],
                   item["printers_rent"])


def populate_main():
    cost_centres_data, cartridges_data, printers_data, users_data = read_all_data()
    populate_cc(cost_centres_data)
    populate_crt(cartridges_data)
    populate_prn(printers_data)
    populate_users(users_data)
