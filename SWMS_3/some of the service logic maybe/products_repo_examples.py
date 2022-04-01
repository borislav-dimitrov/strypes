def products_repo_example(pr_repo, wh_repo, print_all):
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
    # pr_repo.update(to_update)
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

