def to_json_helper(a):
    """
    Helper function to prepare objects data to be written to json.\n
    It defines given object type and based on it returns the way\n
    it should be saved as.
    :param a: object attribute
    :return: list | tuple | dict | str | int
    """
    if isinstance(a, list) or isinstance(a, tuple) or isinstance(a, dict):
        result = []
        for item in a:
            conditions = [isinstance(item, list), isinstance(item, tuple),
                          isinstance(item, dict), isinstance(item, str), isinstance(item, int)]
            if all(conditions):
                result.append(item)
            else:
                result.append(item.to_json())
        return result

    elif isinstance(a, str) or isinstance(a, int):
        return a
    else:
        return a.to_json()
