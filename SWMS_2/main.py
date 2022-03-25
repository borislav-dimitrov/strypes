import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules

# region TODOs
"""
    Add my firm informaton load/save/reload in counterparties module and include it in db.startup
    modify invoices
        inv number to be int
        when done with invoices hook invoices to transactions
"""


# endregion


def main():
    db.startup()
    print("App is running!\n\n")
    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
