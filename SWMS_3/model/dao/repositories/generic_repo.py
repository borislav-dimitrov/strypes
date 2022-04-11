import sys
from model.service.logger import MyLogger

from model.dao.repositories.json_repo import JsonOperations
from model.exceptions import EntityNotFoundException, EntityAttributeNotFoundException


class GenericRepository(JsonOperations):
    """
    Generic Repository class that takes care for the most part of the entities lifecycle.\n
    Extends JsonOperations class, which takes care for the save/load operations.
    """

    def __init__(self, id_generator, logger: MyLogger):
        super().__init__()
        self._entities = {}
        self._id_generator = id_generator
        self._logger = logger

    # region FIND
    def find_all(self):
        """Return all entities values from repo"""
        return list(self._entities.values())

    def find_by_id(self, id_: int):
        """Find entity by selected id"""
        found = self._entities.get(id_)
        if found is None:
            raise EntityNotFoundException(f"Entity with ID: {id_} not found!")
        return found

    def find_by_attribute(self, attr_name: str, attr_val: any, exact_val=True) -> list | None | Exception:
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
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)

    # endregion

    # region CRUD
    def create(self, entity):
        """
        Create new entity in the repository
        :param entity: entity object User | Product | Warehouse | Counterparty | Transaction | Invoice
        :return: newly created Entity
        """
        if entity.id is None:
            new_id = self._id_generator.get_next_id()
            highest_id = self.highest_id()
            if highest_id > new_id:
                entity.id = highest_id
                self._id_generator._nextId = highest_id
            else:
                entity.id = new_id
        else:
            self._id_generator._nextId += 1

        self._entities[entity.id] = entity
        return entity

    def update(self, entity) -> None:
        """
        Update already existing entity in the repo
        :param entity: entity object User | Product | Warehouse | Counterparty | Transaction | Invoice
        :return: None
        """
        entity = self.find_by_id(entity.id)
        self._entities[entity.id] = entity
        return self._entities[entity.id]

    def delete_by_id(self, id_: int):
        """
        Delete entity by selected id
        :param id_: entity id
        :return: deleted entity
        """
        old = self.find_by_id(id_)
        del self._entities[id_]
        return old

    # endregion

    # region OTHER
    def highest_id(self) -> int:
        """Find current highest ID from all existing entities"""
        all_entities = self.find_all()
        highest_id = 0
        for entity in all_entities:
            if entity.id > highest_id:
                highest_id = entity.id
        return highest_id + 1

    def count(self) -> int:
        """Find the count of the entities in current repo"""
        return len(self._entities)

    def print_all(self) -> None:
        """
        Print all entities in the repo. Mainly for debugging purposes.
        :return: None
        """
        data = self.find_all()
        if data is not None:
            for i in data:
                print(f"    {vars(i)}")
        else:
            print(f"    {data}")
    # endregion
