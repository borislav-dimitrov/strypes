def users_repo_example(usr_repo, print_all):
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
    # usr_repo.update(to_update)
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
