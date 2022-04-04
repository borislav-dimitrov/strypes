import json


class JsonOperations:
    """
    JsonOperations class, which takes care for the save/load operations.
    """
    def save(self, file_path):
        """Save all entities from the current repo to json file"""
        with open(file_path, "wt", encoding="utf-8") as f:
            json.dump(self._entities, f, indent=4, default=dumper)

    @staticmethod
    def load(file_path)->dict:
        """Load entities from json file"""
        data = None
        try:
            with open(file_path, "rt", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception as ex:
            print(ex)
        finally:
            return data


def dumper(obj):
    """This is how every entity is represented to be saved in the json file"""
    try:
        return obj.to_json()
    except Exception as ex:
        print(ex)
