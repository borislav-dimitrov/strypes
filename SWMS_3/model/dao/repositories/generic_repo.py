import sys

from model.exceptions import EntityNotFoundException, EntityAttributeNotFoundException


class GenericRepository:
    def __init__(self, IdGenerator):
        self._entities = {}
        self._IdGenerator = IdGenerator

    # region FIND
    def find_all(self):
        return self._entities.values()

    def find_by_id(self, id_: int):
        found = self._entities.get(id_)
        if found is None:
            raise EntityNotFoundException(f"Entity with ID: {id_} not found!")
        return found

    def find_by_attribute(self, attr_name: str, attr_val):
        """
        Return all entities that match the given criteria\n
        :param attr_name: attribute we want to search
        :param attr_val: attribute value we want to filter with
        :return: all entities matching the criteria or None
        """
        result = []
        try:
            for entity in self._entities:
                found = getattr(self._entities[entity], attr_name, "<attr not found>")
                if found == "<attr not found>":
                    raise EntityAttributeNotFoundException(f"Entity doesn't have attribute '{attr_name}'!")

                if found == attr_val:
                    result.append(self._entities[entity])

            if len(result) > 0:
                return result
            else:
                return None
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")

    # endregion

    # region CRUD
    def create(self, entity):
        entity.id = self._IdGenerator.get_next_id()
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
    # endregion