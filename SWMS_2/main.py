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
    db.print_all_counterparties()
    db.print_all_transactions()
    db.print_all_inv()
    print()
    status, msg, new_tr = Modules.trmgm
    status, msg, new_inv = Modules.invmgmt.create_new_inv("auto", "auto", db.counterparties[0],
                                                          db.counterparties[0], "auto", "26-03-2022 00:00:00",
                                                          db.transactions[0].assets, "", "", "pending")
    print(status, msg, new_inv)
    Modules.trmgmt.edit_transact_invoice(1, new_inv.invoice_number)
    Modules.trmgmt.save_transact()
    Modules.invmgmt.save_inv()
    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
