import json


class JsonOperations:
    def save(self, file_path):
        with open(file_path, "wt", encoding="utf-8") as f:
            json.dump(self._entities, f, indent=4, default=dumper)

    def load(self, file_path):
        with open(file_path, "rt", encoding="utf-8") as f:
            data = json.load(f)
            return data


def dumper(obj):
    try:
        return obj.to_json()
    except Exception as ex:
        print(ex)
