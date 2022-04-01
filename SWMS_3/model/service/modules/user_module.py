import sys

from model.entities.user import User
from model.exceptions import WeakPasswordException, InvalidUserStatusException, InvalidUserRoleException


class UserModule:
    def __init__(self, users_repository, password_manager):
        self._users = users_repository
        self._pwd_mgr = password_manager

    # region FIND

    # endregion

    # region CRUD
    def create(self, uname, pwd, role, status, last_login, id=None):
        """
        Create new user in the user repo
        :param uname:
        :param pwd:
        :param role:
        :param status:
        :param last_login:
        :param id:
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
            user = User(uname, pwd, role_, status_, last_login, id)
            return self._users.create(user)
        except Exception as ex:
            # TODO log
            tb = sys.exc_info()[2].tb_frame
            print(f"Something went wrong!\nErrType: {type(ex)}\nErr: {ex}\nTraceBack: {tb}")
            return ex

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
    def print_all(self):
        self._users.print_all()
    # endregion
