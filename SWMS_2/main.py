import Model.DataBase.my_db as db
import Model.Modules.all_modules as Modules


def main():
    db.spawn_logger()
    print("App is running!")
    # Fix TODOS before going on
    print("App is closing!")


if __name__ == '__main__':
    main()
