from tkinter import messagebox

from model.entities.user import User
from model.service.logger import MyLogger
from model.service.modules.users_module import UserModule
from view.components.item_form import ItemForm
from view.user_management_view import UserManagementView


class UserController:
    def __init__(self, user_module: UserModule, logger: MyLogger):
        self.view: UserManagementView = None
        self.service = user_module
        self._logger = logger

    # region Save/Load/Reload

    def load(self):
        self.service.load()

    def save(self):
        self.service.save()

    def reload(self):
        self.save()
        self.load()

    # endregion

    # region Login/Auth

    def login(self, username, password):
        user = self.service.find_by_attribute("name", username.lower())
        if user is not None:
            valid_pwd = self.service._pwd_mgr.compare(password, user[0].password)
            if valid_pwd:
                return True, "Login successful!", user[0]
            else:
                return False, "Wrong password!", None
        return False, "User not found!", None

    # endregion

    # region FIND
    @property
    def users(self):
        return self.service.users

    # endregion

    # region CRUD
    def create_user(self, uname, pwd, role, status, last_login=""):
        result = self.service.create(uname, pwd, role, status, last_login)
        if isinstance(result, User):
            self.reload()
            self.view.refresh()
            messagebox.showinfo("Info!", f"User {result.name} has been created successfully!", parent=self.view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.view.parent)
        return result

    def update_user(self, uname, pwd, role, status, last_login, id_):
        user = self.service.find_by_id(int(id_))
        result = self.service.update(user, uname, pwd, role, status, last_login)
        if isinstance(result, User):
            self.reload()
            self.view.refresh()
            messagebox.showinfo("Info!", f"User {result.name} has been updated successfully!", parent=self.view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.view.parent)
        return result

    def del_user(self):
        selected = self.view.item_list.get_selected_items()

        if len(selected) < 1:
            messagebox.showwarning("Warning!", "Please make a selection first!", parent=self.view.parent)
            return

        user_id = int(selected[0][0])
        user_to_del = self.service.find_by_id(user_id)
        if self.view.curr_user is user_to_del:
            return Exception(f"You can't delete the current user!")
        result = self.service.delete_by_id(user_id)

        if isinstance(result, User):
            self.reload()
            self.view.refresh()
            messagebox.showinfo("Info!", f"User {result.name} successfully deleted!", parent=self.view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.view.parent)

        # endregion

        # region VIEW

    def show_create_user(self):
        form = ItemForm(self.view.parent, User("", "", "", "", ""), self, height=250)

    def show_edit_user(self):
        selected = self.view.item_list.get_selected_items()

        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.view.parent)
            return

        user_id = int(selected[0][0])
        user = self.service.find_by_id(user_id)
        form = ItemForm(self.view.parent, user, self, height=250, edit=True)

    # endregion

    def close(self):
        self.view.open_views.remove(self.view.page_name)
        self.view.parent.destroy()
