import Model.DataBase.my_db as db


def main():
    print(db.my_logger)
    db.my_logger = db.spawn_logger()
    db.my_logger.log()
    print(db.my_logger)
    print("Hello World!")


if __name__ == '__main__':
    main()
