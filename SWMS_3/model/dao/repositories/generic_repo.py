import sys
import model.dao.my_db as db

from model.dao.repositories.json_repo import JsonOperations
from model.exceptions import EntityNotFoundException, EntityAttributeNotFoundException


class GenericRepository(JsonOperations):
    def __init__(self, id_generator):
        super().__init__()
        self._entities = {}
        self._id_generator = id_generator

    # region FIND
    def find_all(self):
        return self._entities.values()

    def find_by_id(self, id_: int):
        found = self._entities.get(id_)
        if found is None:
            raise EntityNotFoundException(f"Entity with ID: {id_} not found!")
        return found

    def find_by_attribute(self, attr_name: str, attr_val, exact_val=True):
        """
        Return all entities that match the given criteria\n
        :param attr_name: attribute we want to search
        :param attr_val: attribute value we want to filter with
        :param exact_val: match exact value or contain
        :return: all entities matching the criteria or None
        """
        result = []
        try:
            for entity in self._entities:
                found = getattr(self._entities[entity], attr_name, "<attr not found>")
                if found == "<attr not found>":
                    raise EntityAttributeNotFoundException(f"Entity doesn't have attribute '{attr_name}'!")

                if exact_val:
                    if attr_val == found:
                        result.append(self._entities[entity])
                else:
                    if isinstance(attr_val, str):
                        if attr_val.lower() in found.lower():
                            result.append(self._entities[entity])
                    elif attr_val in found:
                        result.append(self._entities[entity])

            if len(result) > 0:
                return result
            else:
                return None
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            msg = "Something went wrong!"
            db.logger.log(__file__, msg, "ERROR", type(ex), tb)

    # endregion

    # region CRUD
    def create(self, entity):
        if entity.id is None:
            entity.id = self._id_generator.get_next_id()
        else:
            self._id_generator._nextId += 1

        self._entities[entity.id] = entity
        return entity

    def update(self, entity):
        entity = self.find_by_id(entity.id)
        self._entities[entity.id] = entity

    def delete_by_id(self, id_):
        old = self.find_by_id(id_)
        del self._entities[id_]
        return old

    # endregion

    # region OTHER
    def count(self):
        return len(self._entities)

    def get_entities(self):
        return self._entities

    def print_all(self):
        data = self.find_all()
        if data is not None:
            for i in data:
                print(f"    {vars(i)}")
        else:
            print(f"    {data}")
    # endregion
