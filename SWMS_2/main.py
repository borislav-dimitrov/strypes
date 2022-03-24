import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules

# region TODOs
"""
    Continue with client, supplier modules.
"""


# endregion


def main():
    db.startup()
    print("App is running!\n\n")
    status, msg = Modules.invmgmt.create_new_inv("auto", ["My Company", "my addr", "", "my city", "BG", "7000", "0885"],
                                                 ["other Company", "other addr", "", "other city", "EN", "155", "088"],
                                                 "auto",
                                                 [["some product", "some quantity", "some price"],
                                                  ["some product", "some quantity", "some price"]],
                                                 500, "", "", "PENDING")

    print(status, msg)
    db.print_all_inv()
    state, m = Modules.invmgmt.edit_inv_from(1, 1)
    print(state, m)
    db.print_all_inv()
    print("\n\nApp is closing!")


if __name__ == '__main__':
    main()
