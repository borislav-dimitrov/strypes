def get_object_by_id(obj_id, objects):
    for item in objects:
        if item.asset_id == obj_id:
            return item
