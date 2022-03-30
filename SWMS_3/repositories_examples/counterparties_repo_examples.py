def counterparties_repo_example(cpty_repo, print_all):
    print("\n\n### Testing Counterparty repository ###")

    # region TEST FIND
    print("\n# Repository find all: #")
    found = cpty_repo.find_all()
    print_all(found)

    print("\n# Repository find by id {4}: #")
    print(f"  {vars(cpty_repo.find_by_id(4))}")

    print("\n# Repository find by attribute {name - Firm2}: #")
    found = cpty_repo.find_by_attribute("name", "Firm2")
    print_all(found)

    print("\n# Repository find by attribute {name - nnnnnn}: #")
    found = cpty_repo.find_by_attribute("name", "nnnn")
    print_all(found)

    print("\n# Repository find by non existing attribute {nameE - Ivan}: #")
    found = cpty_repo.find_by_attribute("nameE", "nnnn")
    print_all(found)
    # endregion

    # region TEST CRUD
    print("\n# Repository update entity: #")
    to_update = cpty_repo.find_by_id(2)
    print("    Old: ", vars(to_update))
    to_update.payment_nr = "BG11111111"
    to_update.type = "Supplier"
    to_update.description = ["material8", "Raw Materials", 5.5, 7.5, None]
    # cpty_repo.update(to_update)
    print("    New: ", vars(cpty_repo.find_by_id(2)))

    print("\n# Repository delete entity: #")
    print("Repository all Entities: ")
    found = cpty_repo.find_all()
    print_all(found)

    cpty_repo.delete_by_id(2)

    print("Repository all Entities after deleted {2}: ")
    found = cpty_repo.find_all()
    print_all(found)
    # endregion

    # region TEST OTHER
    print("\n# Repository count: #")
    print(f"    {cpty_repo.count()}")
    # endregion

