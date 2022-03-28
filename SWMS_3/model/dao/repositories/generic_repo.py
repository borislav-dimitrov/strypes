from model.exceptions import EntityNotFoundException


class GenericRepository:
    def __init__(self, id_generator):
        self._entities = {}
        self._id_generator = id_generator

    def entities_getter(self):
        return self._entities

    def find_all(self):
        return self._entities.values()

    def find_by_id(self, id_):
        found = self._entities.get(id_)
        if found is None:
            raise EntityNotFoundException(f"Entity with ID: {id_} not found!")
        return found

    def create(self, entity):
        entity.id = self._id_generator.get_next_id()
        self._entities[entity.id] = entity
        return entity

    def update(self, entity):
        entity = self.find_by_id(entity.id)
        self._entities[entity.id] = entity

    def delete_by_id(self, id_):
        old = self.find_by_id(id_)
        del self._entities[id_]
        return old

    def count(self):
        return len(self._entities)
