import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules

# region TODOs
"""
    1 think of a way of loading/creating warehouses and products
    2 Do TODOs
"""


# endregion


def main():
    db.startup()
    print("App is running!\n\n")
    db.print_all_users()
    db.print_all_warehouses()
    Modules.prmgmt.create_new_product("auto", "red paint", "raw materials", 3.5, 4.5, 1, "sklad02")
    Modules.prmgmt.create_new_product("auto", "red paint", "raw materials", 3.5, 4.5, 1001, "sklad02")
    Modules.whmgmt.hook_products_to_warehouse()
    db.print_all_products()
    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
