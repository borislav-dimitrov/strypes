import Model.DataBase.my_db as db
import Model.Modules.user_mgmt as umgmt


def main():
    print("Hello World!")
    umgmt.load_users()
    db.print_all_users()


if __name__ == '__main__':
    main()
