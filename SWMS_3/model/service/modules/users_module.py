import sys

from model.dao.password_manager import PasswordManager
from model.service.logger import MyLogger

from model.entities.user import User
from model.exceptions import WeakPasswordException, InvalidUserStatusException, InvalidUserRoleException


class UserModule:
    """Module that handles all the business logic for the Users"""

    def __init__(self, users_repository, password_manager: PasswordManager, logger: MyLogger):
        self._usr_repo = users_repository
        self._pwd_mgr = password_manager
        self._logger = logger

    # region FIND
    def _find_all(self) -> dict:
        """Get all Users in the Repository"""
        return self._usr_repo.find_all()

    def find_by_id(self, id_: int) -> User:
        """Get User by ID"""
        return self._usr_repo.find_by_id(id_)

    def find_by_attribute(self, attr_name: str, attr_val: any, exact_val=True) -> list | None | Exception:
        """Return all entities that match the given criteria"""
        return self._usr_repo.find_by_attribute(attr_name, attr_val, exact_val)

    # endregion

    # region CRUD
    def create(self, uname, pwd, role, status, last_login="", id_=None) -> User | Exception:
        """Create new user in the user repo"""
        try:
            # validate uname
            if len(uname) < 4:
                raise Exception(f"Failed creating user!\nUsername too short!")
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
            return self._usr_repo.create(user)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    def update(self, user, uname, pwd, role, status, last_login=None) -> User | Exception:
        """Update existing User in the Repository with new one"""
        try:
            # region Validations

            # validate uname
            if len(uname) < 4:
                raise Exception(f"Failed updating user!\nUsername too short!")

            # validate pwd
            validation = self._pwd_mgr.check_strong_pwd(pwd)
            if validation != "Ok":
                raise WeakPasswordException(f"Failed updating user!\nPassword too weak!\n{validation}")

            # validate role
            role_ = self.validate_role(role)
            if role_ is None:
                raise InvalidUserRoleException(f"Failed updating user!\nRole {role} is not valid!")

            # validate status
            status_ = self.validate_status(status)
            if status_ is None:
                raise InvalidUserStatusException(f"Failed updating user!\nStatus {status} is not valid!")

            # encrypt pwd
            pwd = self._pwd_mgr.encrypt_pwd(pwd)

            # endregion

            # Change props
            user.name = uname
            user.password = pwd
            user.type = role_
            user.status = status_
            if last_login is not None:
                user.last_login = last_login

            return user
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    def delete_by_id(self, id_) -> User | Exception:
        try:
            return self._usr_repo.delete_by_id(id_)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "ERROR", type(ex), tb)
            return ex

    # endregion

    # region Validations
    @staticmethod
    def validate_status(status) -> str | None:
        """Validate User Status"""
        valid = ("Enabled", "Disabled")
        for st in valid:
            if st.lower() == status.lower():
                return st

    @staticmethod
    def validate_role(role) -> str | None:
        """Validate User Role"""
        valid = ("Administrator", "Operator")
        for rl in valid:
            if rl.lower() == role.lower():
                return rl

    # endregion

    # region OTHER
    @property
    def users(self) -> dict:
        """users getter"""
        return self._usr_repo.find_all()

    def print_all(self):
        """Print all Users. For Debugging purposes"""
        self._usr_repo.print_all()

    def count(self) -> int:
        """Get the count of the users in the Repository"""
        return self._usr_repo.count()

    # endregion

    # region Save/Load
    def save(self):
        """Save the Users to file"""
        self._usr_repo.save("./model/data/users.json")

    def load(self):
        """Load and create User Objects from file"""
        try:
            loaded = self._usr_repo.load("./model/data/users.json")
            if loaded is not None:
                for item in loaded:
                    id_, name, pwd, type_, status, last_login = loaded[item].values()
                    new = User(name, pwd.encode("utf-8"), type_, status, last_login, id_)
                    self._usr_repo.create(new)
        except Exception as ex:
            tb = sys.exc_info()[2].tb_frame
            self._logger.log(__file__, str(ex), "Critical", type(ex), tb)
            raise ex

    # endregion

    # region VIEW
    def del_from_view(self, usr_id, curr_user):
        user_to_del = self.find_by_id(usr_id)
        if curr_user is user_to_del:
            return Exception(f"You can't delete the current user!")

        return self.delete_by_id(usr_id)
    # endregion
