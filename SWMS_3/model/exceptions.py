"""Custom Exceptions"""


class EntityNotFoundException(Exception):
    pass


class EntityAttributeNotFoundException(Exception):
    pass


class EntityIsAlreadyInWarehouseException(Exception):
    pass


class WeakPasswordException(Exception):
    pass


class InvalidUserStatusException(Exception):
    pass


class InvalidUserRoleException(Exception):
    pass


class InvalidObjectTypeException(Exception):
    pass
