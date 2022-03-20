import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules

# region TODOs
"""
    1.1 Implement warehouses
        1.2 Do TODOs
"""


# endregion


def main():
    db.spawn_logger()
    print("App is running!")
    Modules.whmgmt.create_new_wh("auto", "Virtual", "Virtual", 99999999999999999, [], "ENABLED")
    Modules.whmgmt.create_new_wh("auto", "sklad01", "raw materials", 10000, [], "ENABLED")
    Modules.whmgmt.create_new_wh("auto", "sklad02", "finished goods", 10000, [], "ENABLED")

    db.print_all_warehouses()
    print("App is closing!")


if __name__ == '__main__':
    main()
