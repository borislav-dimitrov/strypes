from model.service.logger import MyLogger
from model.service.modules.users_module import UserModule
from view.components.item_form import ItemForm


class UserController:
    def __init__(self, user_module: UserModule, logger: MyLogger):
        self.view = None
        self._module = user_module
        self._logger = logger

    # region Save/Load/Reload

    def load(self):
        self._module.load()

    def save(self):
        self._module.save()

    def reload(self):
        self.save()
        self.load()

    # endregion

    # region Login/Auth

    def login(self, username, password):
        user = self._module.find_by_attribute("name", username.lower())
        if user is not None:
            valid_pwd = self._module._pwd_mgr.compare(password, user[0].password)
            if valid_pwd:
                return True, "Login successful!", user[0]
            else:
                return False, "Wrong password!", None
        return False, "User not found!", None

    # endregion

    # region FIND
    @property
    def users(self):
        return self._module.users

    # endregion

    # region CRUD
    def create_user(self, uname, pwd, role, status, last_login=""):
        result = self._module.create(uname, pwd, role, status, last_login)

    # endregion

    def show_add_user(self):
        form = ItemForm(self.view, (0, "", bytes, "", "", ""), self.create_user())
