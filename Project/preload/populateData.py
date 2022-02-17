import helpers.dateHelpers as dh

from objects.costCentre import CostCentre
from objects.cartridge import Cartridge
from objects.user import User
from objects.printer import Printer

all_cc = []
all_crt = []
all_users = []
all_prn = []


def create_cc(cc_num, cc_name, cc_status="Active"):
    curr_id = len(all_cc) + 1
    new_cc = CostCentre(curr_id, cc_num, cc_name, cc_status)
    all_cc.append(new_cc)


def create_crt(crt_type, serial_number, barcode, cost_centre, date_bought, date_scrap, remark, status="Normal"):
    curr_id = len(all_crt) + 1
    new_crt = Cartridge(curr_id, crt_type, serial_number, barcode, cost_centre, date_bought, date_scrap, remark, status)
    all_crt.append(new_crt)


def create_user(f_name, l_name, cost_centre, status="Active"):
    curr_id = len(all_users) + 1
    new_user = User(curr_id, f_name, l_name, cost_centre, status)
    all_users.append(new_user)


def create_prn(prn_model, cost_centre, location, prn_ip, bk_counters=0,
               clr_counters=0, status="Active", rent=True):
    curr_id = len(all_prn) + 1
    new_printer = Printer(curr_id, prn_model, cost_centre, location, prn_ip, bk_counters, clr_counters, status, rent)
    all_prn.append(new_printer)


def populate_cc():
    create_cc(4311, "Supply Chain")
    create_cc(5204, "Export")
    create_cc(5210, "Finished Goods")
    create_cc(4208, "Raw Materials")
    create_cc(555, "test")
    create_cc(444, "test")
    create_cc(333, "test")
    create_cc(111, "test")
    create_cc(222, "test")
    create_cc(777, "test")
    create_cc(666, "test")


def populate_crt():
    create_crt("Xerox 3215", "sn_000001", "bc_000001_someOtherInfo", all_cc[0], dh.get_today(), "", "")
    create_crt("HP 85a", "sn_000002", "bc_000002_someOtherInfo", all_cc[1], dh.get_today(), "", "")


def populate_users():
    create_user("Ivancho", "Ivanchev", all_cc[0])
    create_user("Pencho", "Penchev", all_cc[1])


def populate_prn():
    create_prn("Lexmark 310", all_cc[0], "Administration", "192.168.0.50")
    create_prn("Lexmark 410", all_cc[0], "Administration", "192.168.0.51")
    create_prn("Xerox Workcentre 5210", all_cc[1], "some location", "192.168.0.52", 12345, 500)


def populate_main():
    populate_cc()
    populate_crt()
    populate_users()
    populate_prn()

    #return all_cc, all_crt, all_users, all_prn
