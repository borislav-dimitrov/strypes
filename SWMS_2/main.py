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
    # state, msg = Modules.cpmgmt.create_new_cprty("auto", "M&BM", "1234567", "BG123", "enabled", "Supplier",
    #                                              {"sellable": [("terpentine", 2.0), ("thinner", 4.0),
    #                                                            ("pigment(BK)", 10.0)]})
    db.print_all_counterparties()

    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
