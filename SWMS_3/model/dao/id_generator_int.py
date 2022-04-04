class IdGeneratorInt:
    """
    IdGenerator class, used to generate entity id's.
    """

    def __init__(self):
        self._nextId = 0

    def get_next_id(self) -> int:
        """
        Generate next id, and increment the current one\n
        to keep the track of all ids
        :return: next id { int }
        """
        self._nextId += 1
        return self._nextId
