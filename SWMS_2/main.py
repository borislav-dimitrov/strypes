import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules

# region TODOs
"""
    client module/repo
    supplier module/repo
    transaction module/repo
"""


# endregion


def main():
    db.startup()
    print("App is running!\n\n")
    Modules.invmgmt.generate_invoice(3)
    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
