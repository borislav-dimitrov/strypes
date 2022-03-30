def invoices_repo_example(inv_repo, cpty_repo, tr_repo, print_all):
    print("\n\nTesting invoice repository")

    # region TEST FIND
    print("\n# Repository find all: #")
    found = inv_repo.find_all()
    print_all(found)

    print("\n# Repository find by id {1}: #")
    print(f"  {vars(inv_repo.find_by_id(3))}")

    print("\n# Repository find by attribute {from_ - Firm5}: #")
    found = inv_repo.find_by_attribute("from_", cpty_repo.find_by_attribute("name", "Firm5")[0])
    print_all(found)

    print("\n# Repository find by attribute {number - -1}: #")
    found = inv_repo.find_by_attribute("number", -1)
    print_all(found)

    print("\n# Repository find by non existing attribute {nameE - Ivan}: #")
    found = inv_repo.find_by_attribute("nameE", "nnnn")
    print_all(found)
    # endregion

    # region TEST CRUD
    print("\n# Repository update entity: #")
    to_update = inv_repo.find_by_id(1)
    print("    Old: ", vars(to_update))
    to_update.date = "31/03/2022 23:59:00"
    to_update.due_to = "15/04/2022 23:59:00"
    print("    New: ", vars(inv_repo.find_by_id(1)))

    print("\n# Repository delete entity: #")
    print("Repository all Entities: ")
    found = inv_repo.find_all()
    print_all(found)

    inv_repo.delete_by_id(3, tr_repo.find_by_attribute("invoice", inv_repo.find_by_id(3))[0])

    print("Repository all Entities after deleted {3}: ")
    found = inv_repo.find_all()
    print_all(found)
    # endregion

    # region TEST OTHER
    print("\n# Repository count: #")
    print(f"    {inv_repo.count()}")
    # endregion
