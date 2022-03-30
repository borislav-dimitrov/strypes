def transactions_repo_example(tr_repo, cpty_repo, print_all):
    print("\n\nTesting transaction repository")

    # region TEST FIND
    print("\n# Repository find all: #")
    found = tr_repo.find_all()
    print_all(found)

    print("\n# Repository find by id {4}: #")
    print(f"  {vars(tr_repo.find_by_id(4))}")

    print("\n# Repository find by attribute {date - 30/03/2022}: #")
    found = tr_repo.find_by_attribute("date", "30/03/2022", exact_val=False)
    print_all(found)

    print("\n# Repository find by attribute {date - 01/01/1999}: #")
    found = tr_repo.find_by_attribute("date", "01/01/1999")
    print_all(found)

    print("\n# Repository find by non existing attribute {nameE - Ivan}: #")
    found = tr_repo.find_by_attribute("nameE", "nnnn")
    print_all(found)
    # endregion

    # region TEST CRUD
    print("\n# Repository update entity: #")
    to_update = tr_repo.find_by_id(1)
    print("    Old: ", vars(to_update))
    to_update.date = "25/03/2022 10:00:00"
    to_update.counterparty = cpty_repo.find_by_id(4)
    tr_repo.update_tr_products(to_update, [["material4", "Finished Goods", 12.0, 20],
                                           ["material5", "Finished Goods", 12.0, 30]])
    # to_update.calc_price() this is done in update_tr products
    # tr_repo.update(to_update)
    print("    New: ", vars(tr_repo.find_by_id(2)))

    print("\n# Repository delete entity: #")
    print("Repository all Entities: ")
    found = tr_repo.find_all()
    print_all(found)

    tr_repo.delete_by_id(4)

    print("Repository all Entities after deleted {4}: ")
    found = tr_repo.find_all()
    print_all(found)
    # endregion

    # region TEST OTHER
    print("\n# Repository count: #")
    print(f"    {tr_repo.count()}")
    # endregion
