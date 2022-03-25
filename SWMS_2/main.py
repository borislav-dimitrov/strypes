import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules

# region TODOs
"""
    client module/repo
    supplier module/repo
    transaction module/repo
    modify invoices
        inv number to be int
        when done with invoices hook invoices to transactions
"""


# endregion


def main():
    db.startup()
    print("App is running!\n\n")
    db.print_all_transactions()
    # Modules.trmgmt.create_transact("auto", "sale", db.counterparties[0],
    #                                [("asset1", 3, 5.0), ("asset2", 2, 7.0)])
    # db.print_all_transactions()
    # Modules.trmgmt.save_transact()
    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
