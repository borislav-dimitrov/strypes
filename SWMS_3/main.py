from model.dao.id_generator_int import IdGeneratorInt
from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.product_repo import ProductRepository
from model.dao.repositories.warehouse_repo import WarehouseRepository
from model.entities.product import Product
from model.entities.user import User
from model.entities.warehouse import Warehouse

# TODO password manager class
# TODO remove_products_from_wh method in warehouse repo

usr_id_seq = IdGeneratorInt()
usr_repo = GenericRepository(usr_id_seq)

wh_id_seq = IdGeneratorInt()
wh_repo = WarehouseRepository(wh_id_seq)

pr_id_seq = IdGeneratorInt()
pr_repo = ProductRepository(pr_id_seq)


def create_objects_and_link_them():
    global usr_repo, wh_repo, pr_repo
    print("### Start creating entities and links between them ###")

    # region USERS
    user1 = User("Ivan", "!@#asd", "Administrator", "Enabled", "")
    usr_repo.create(user1)
    user2 = User("Ivan", "!@#asd", "Administrator", "Enabled", "")
    usr_repo.create(user2)
    user3 = User("Andrei", "asd#@!", "Operator", "Enabled", "")
    usr_repo.create(user3)
    user4 = User("Petar", "asd#@!", "Operator", "Enabled", "")
    usr_repo.create(user4)

    print("# User Repository Created Entities #")
    # endregion

    # region WAREHOUSES
    wh1 = Warehouse("sklad01", "Finished Goods", 5000, [], "Enabled")
    wh_repo.create(wh1)
    wh2 = Warehouse("sklad02", "Raw Materials", 4555, [], "Enabled")
    wh_repo.create(wh2)
    print("# Warehouse Repository Created Entities #")
    # endregion

    # region PRODUCTS
    pr1 = Product("Red Paint", "Finished Goods", 10.0, 12.0, 200, "sklad01")
    pr2 = Product("Red Paint", "Finished Goods", 10.0, 12.0, 200, "sklad01")
    pr3 = Product("Turpentine", "Raw Materials", 5.0, 7.0, 200, "sklad02")
    pr4 = Product("Thinner", "Raw Materials", 5.0, 7.0, 200, "sklad02")
    pr5 = Product("Purple Paint", "Raw Materials", 10.0, 12.0, 100, "sklad02")
    pr6 = Product("material2", "Raw Materials", 10.0, 12.0, 300, "sklad02")
    pr7 = Product("material3", "Finished Goods", 10.0, 12.0, 300, None)
    pr8 = Product("material4", "Finished Goods", 10.0, 12.0, 300, None)
    all_products = [pr1, pr2, pr3, pr4, pr5, pr6, pr7, pr8]

    for product in all_products:
        new_pr = pr_repo.create(product)
        if new_pr.assigned_wh is not None:
            found = wh_repo.find_by_attribute("name", new_pr.assigned_wh)
            new_pr.assigned_wh = found[0]
            found[0].products.append(new_pr)

            pr_repo.update(new_pr)
            wh_repo.update(found[0])

    print("# Product Repository Created Entities #")
    print("# Linked Products with Warehouses #")
    # endregion


def print_all(data):
    if data is not None:
        for i in data:
            print(f"    {vars(i)}")
    else:
        print(f"    {data}")


def user_test_repo():
    global usr_repo
    print("\n\n### Testing user repository ###")

    # region TEST FIND
    print("\n# Repository find all: #")
    found = usr_repo.find_all()
    print_all(found)

    print("\n# Repository find by id {1}: #")
    print(f"  {vars(usr_repo.find_by_id(1))}")

    print("\n# Repository find by attribute {name - Ivan}: #")
    found = usr_repo.find_by_attribute("name", "Ivan")
    print_all(found)

    print("\n# Repository find by attribute {name - nnnnnn}: #")
    found = usr_repo.find_by_attribute("name", "nnnn")
    print_all(found)

    print("\n# Repository find by non existing attribute {nameE - Ivan}: #")
    found = usr_repo.find_by_attribute("nameE", "nnnn")
    print_all(found)
    # endregion

    # region TEST CRUD
    print("\n# Repository update entity: #")
    to_update = usr_repo.find_by_id(1)
    print("    Old: ", vars(to_update))
    to_update.password = "new_password!@#"
    to_update.type = "Operator"
    usr_repo.update(to_update)
    print("    New: ", vars(usr_repo.find_by_id(1)))

    print("\n# Repository delete entity: #")
    print("Repository all Entities: ")
    found = usr_repo.find_all()
    print_all(found)

    usr_repo.delete_by_id(3)

    print("Repository all Entities after deleted {3}: ")
    found = usr_repo.find_all()
    print_all(found)
    # endregion

    # region TEST OTHER
    print("\n# Repository count: #")
    print(f"    {usr_repo.count()}")
    # endregion


def warehouse_test_repo():
    global wh_repo, pr_repo
    print("\n\n### Testing warehouse repository ###")

    # region TEST FIND
    print("\n# Repository find all: #")
    found = wh_repo.find_all()
    print_all(found)

    print("\n# Repository find by id {1}: #")
    print(f"    {vars(wh_repo.find_by_id(1))}")

    print("\n# Repository find by attribute {capacity - 5000}: #")
    found = wh_repo.find_by_attribute("capacity", 5000)
    print_all(found)

    print("\n# Repository find by product: #")
    found = wh_repo.find_by_product(pr_repo.find_by_id(1))
    print_all(found)

    print("\n# Repository find by attribute {capacity - -1}: #")
    found = wh_repo.find_by_attribute("capacity", -1)
    print_all(found)

    print("\n# Repository find by non existing attribute {nameE - Ivan}: #")
    found = wh_repo.find_by_attribute("nameE", "Ivan")
    print_all(found)
    # endregion

    # region TEST CRUD
    print("\n# Repository update entity: #")
    to_update = wh_repo.find_by_id(2)
    print("    Old: ", vars(to_update))
    to_update.capacity = 5
    to_update.status = "Disabled"
    wh_repo.update(to_update)
    print("    New: ", vars(wh_repo.find_by_id(2)))

    print("\n# Repository update warehouse products { move from sklad02 to sklad01 }: #")
    print("    Old products: ", wh_repo.find_by_id(1).name, [pr.name for pr in wh_repo.find_by_id(1).products], " | ",
          wh_repo.find_by_id(2).name, [pr.name for pr in wh_repo.find_by_id(2).products])
    wh_repo.add_warehouse_products(wh_repo.find_by_id(1), [pr_repo.find_by_id(3), pr_repo.find_by_id(4)])
    print("    New products: ", wh_repo.find_by_id(1).name, [pr.name for pr in wh_repo.find_by_id(1).products], " | ",
          wh_repo.find_by_id(2).name, [pr.name for pr in wh_repo.find_by_id(2).products])

    print("\n# Repository delete entity: #")
    print("Repository all Entities: ")
    found = wh_repo.find_all()
    print_all(found)

    wh_repo.delete_by_id(2)

    print("Repository all Entities after deleted {2}: ")
    found = wh_repo.find_all()
    print_all(found)
    # endregion

    # region TEST OTHER
    print("\n# Repository count: #")
    print(f"    {wh_repo.count()}")
    # endregion


def product_test_repo():
    global pr_repo, wh_repo
    print("\n\n### Testing product repository ###")

    # region TEST FIND
    print("\n# Repository find all: #")
    found = pr_repo.find_all()
    print_all(found)

    print("\n# Repository find by id {1}: #")
    print(f"    {vars(pr_repo.find_by_id(1))}")

    print("\n# Repository find by attribute {name - Purple Paint}: #")
    found = pr_repo.find_by_attribute("name", "Purple Paint")
    print_all(found)

    print("\n# Repository find by attribute {quantity - -1}: #")
    found = pr_repo.find_by_attribute("quantity", -1)
    print_all(found)

    print("\n# Repository find by non existing attribute {nameE - Ivan}: #")
    found = pr_repo.find_by_attribute("nameE", "Ivan")
    print_all(found)
    # endregion

    # region TEST CRUD
    print("\n# Repository update entity: #")
    to_update = pr_repo.find_by_id(1)
    print("    Old: ", vars(to_update), to_update.assigned_wh.name)
    to_update.name = "Purple Paint"
    to_update.sell_price = 100.0
    pr_repo.update(to_update)
    print("    New: ", vars(pr_repo.find_by_id(1)), pr_repo.find_by_id(1).assigned_wh.name)

    print("\n# Repository update product assigned warehouse: #")
    to_update = pr_repo.find_by_id(1)
    print("    Old: ", vars(to_update), to_update.assigned_wh.name)
    pr_repo.update_assigned_wh(to_update, wh_repo.find_by_id(2))
    print("    New: ", vars(pr_repo.find_by_id(1)), pr_repo.find_by_id(1).assigned_wh.name)

    print("\n# Repository update product assigned warehouse to the same warehouse: #")
    to_update = pr_repo.find_by_id(1)
    print("    Old: ", vars(to_update), to_update.assigned_wh.name)
    pr_repo.update_assigned_wh(to_update, wh_repo.find_by_id(2))
    print("    New: ", vars(pr_repo.find_by_id(1)), pr_repo.find_by_id(1).assigned_wh.name)

    print("\n# Repository delete entity: #")
    print("Repository all Entities: ")
    found = pr_repo.find_all()
    print_all(found)

    pr_repo.delete_by_id(3)

    print("Repository all Entities after deleted {3}: ")
    found = pr_repo.find_all()
    print_all(found)
    # endregion

    # region TEST OTHER
    print("\n# Repository count: #")
    print(f"    {pr_repo.count()}")
    # endregion


def counterparty_test_repo():
    print("Testing counterparty repository")


def transaction_test_repo():
    print("Testing transaction repository")


def invoice_test_repo():
    print("Testing invoice repository")


if __name__ == '__main__':
    create_objects_and_link_them()
    # user_test_repo()
    # print()
    # print()
    warehouse_test_repo()
    # print()
    # print()
    # product_test_repo()
    # print()
    # print()
    # counterparty_test_repo()
    # transaction_test_repo()
    # invoice_test_repo()
