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
    print("App is running!")
    db.print_all_users()
    db.print_all_warehouses()
    db.print_all_products()
    print("App is closing!")


if __name__ == '__main__':
    main()
