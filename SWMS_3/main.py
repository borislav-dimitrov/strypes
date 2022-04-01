import model.dao.my_db as db
from model.service.startup import start_up


def main():
    start_up()
    db.user_module.print_all()
    new_usr = db.user_module.create("Joro", "Parola!@#", "ozperator", "enabled", "")
    print("exception" in str(type(new_usr)).lower())
    db.user_module.print_all()


if __name__ == '__main__':
    # create_objects()

    # a = wh_repo.find_by_id(2)
    # pr_repo.find_by_id(1).assigned_wh = wh_repo.find_by_id(2)
    # pr_repo.find_by_id(2).assigned_wh = wh_repo.find_by_id(2)
    # a.products.append(pr_repo.find_by_id(1))
    # a.products.append(pr_repo.find_by_id(2))
    # print(a.to_json())

    # SAVE
    # usr_repo.save("./model/data/users.json")
    # pr_repo.save("./model/data/products.json")
    # wh_repo.save("./model/data/warehouses.json")
    # cpty_repo.save("./model/data/counterparties.json")
    # tr_repo.save("./model/data/transactions.json")
    # inv_repo.save("./model/data/invoices.json")

    main()
