def warehouses_repo_example(wh_repo, pr_repo, print_all):
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
    # wh_repo.update(to_update)
    print("    New: ", vars(wh_repo.find_by_id(2)))

    print("\n# Repository add warehouse products { from sklad02 to sklad01 }: #")
    print("    Old products: ", wh_repo.find_by_id(1).name, [pr.name for pr in wh_repo.find_by_id(1).products], " | ",
          wh_repo.find_by_id(2).name, [pr.name for pr in wh_repo.find_by_id(2).products])
    wh_repo.add_warehouse_products(wh_repo.find_by_id(1), [pr_repo.find_by_id(3), pr_repo.find_by_id(4)])
    print("    New products: ", wh_repo.find_by_id(1).name, [pr.name for pr in wh_repo.find_by_id(1).products], " | ",
          wh_repo.find_by_id(2).name, [pr.name for pr in wh_repo.find_by_id(2).products])

    print("\n# Repository remove warehouse products { from sklad01 }: #")
    print("    Old products: ", wh_repo.find_by_id(1).name, [pr.name for pr in wh_repo.find_by_id(1).products])
    products_to_remove = [*pr_repo.find_by_attribute("name", "Turpentine"),
                          *pr_repo.find_by_attribute("name", "Thinner")]
    wh_repo.rem_warehouse_products(wh_repo.find_by_id(1), products_to_remove)
    print("    New products: ", wh_repo.find_by_id(1).name, [pr.name for pr in wh_repo.find_by_id(1).products])

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
