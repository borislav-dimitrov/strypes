import sys

from model.entities.user import User
from model.exceptions import WeakPasswordException, InvalidUserStatusException, InvalidUserRoleException


class UserModule:
    def __init__(self, users_repository, password_manager):
        self._users = users_repository
        self._pwd_mgr = password_manager

    # region FIND
    def find_all(self):
        return self._users.find_all()

    def find_by_id(self, id_):
        return self._users.find_by_id(id_)

    def find_by_attribute(self, attr_name: str, attr_val, exact_val=True):
        return self._users.find_by_attribute(attr_name, attr_val, exact_val)

    # endregion

    # region CRUD
    def create(self, uname, pwd, role, status, last_login="", id_=None):
        """
        Create new user in the user repo
        :param uname:
        :param pwd:
        :param role:
        :param status:
        :param last_login:
        :param id_:
        :return: new User Object | None
        """
        try:
            # validate pwd
            validation = self._pwd_mgr.check_strong_pwd(pwd)
            if validation != "Ok":
                raise WeakPasswordException(f"Failed creating user!\nPassword too weak!\n{validation}")

            # validate role
            role_ = self.validate_role(role)
            if role_ is None:
                raise InvalidUserRoleException(f"Failed creating user!\nRole {role} is not valid!")

            # validate status
            status_ = self.validate_status(status)
            if status_ is None:
                raise InvalidUserStatusException(f"Failed creating user!\nStatus {status} is not valid!")

            # encrypt pwd
            pwd = self._pwd_mgr.encrypt_pwd(pwd)
            user = User(uname, pwd, role_, status_, last_login, id_)
            return self._users.create(user)
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
            return ex

    def update(self, new_entity):
        entity = self._users.find_by_id(new_entity.id)
        entity = new_entity

    def delete_by_id(self, id_):
        return self._users.delete_by_id(id_)

    # endregion

    # region Validations
    @staticmethod
    def validate_status(status):
        valid = ("Enabled", "Disabled")
        for st in valid:
            if st.lower() == status.lower():
                return st

    @staticmethod
    def validate_role(role):
        valid = ("Administrator", "Operator")
        for rl in valid:
            if rl.lower() == role.lower():
                return rl

    # endregion

    # region OTHER
    @property
    def entities(self):
        return self._users.get_entities()

    def print_all(self):
        self._users.print_all()

    def count(self):
        return self._users.count()

    def save(self):
        self._users.save("./model/data/users.json")

    def load(self):
        loaded = self._users.load("./model/data/users.json")
        if loaded is not None:
            for item in loaded:
                id_, name, pwd, type_, status, last_login = loaded[item].values()
                new = User(name, pwd.encode("utf-8"), type_, status, last_login, id_)
                self._users.create(new)

    # endregion
