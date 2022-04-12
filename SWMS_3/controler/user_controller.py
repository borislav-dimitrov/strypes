from tkinter import messagebox

from model.entities.user import User
from model.service.logger import MyLogger
from model.service.modules.users_module import UserModule
from view.components.item_form import ItemForm
from view.user_management_view import UserManagementView


class UserController:
    def __init__(self, user_module: UserModule, logger: MyLogger):
        self.view: UserManagementView = None
        self.module = user_module
        self.logger = logger

    # region Save/Load/Reload

    def load(self):
        self.module.load()

    def save(self):
        self.module.save()

    def reload(self):
        self.save()
        self.load()

    # endregion

    # region Login/Auth

    def login(self, username, password):
        user = self.module.find_by_attribute("name", username.lower())
        if user is not None:
            valid_pwd = self.module._pwd_mgr.compare(password, user[0].password)
            if valid_pwd:
                return True, "Login successful!", user[0]
            else:
                return False, "Wrong password!", None
        return False, "User not found!", None

    # endregion

    # region FIND
    @property
    def users(self):
        return self.module.users

    # endregion

    # region CRUD
    def create_user(self, uname, pwd, role, status, last_login):
        # We don't modify login history manually from view
        result = self.module.create(uname, pwd, role, status, "")
        if isinstance(result, User):
            self.reload()
            self.view.refresh()
            messagebox.showinfo("Info!", f"User {result.name} has been created successfully!", parent=self.view.parent)
            self.logger.log(__file__, f"Created user - {result.name}.", "INFO")
        else:
            messagebox.showerror("Error!", result, parent=self.view.parent)
        return result

    def update_user(self, uname, pwd, role, status, last_login, id_):
        user = self.module.find_by_id(int(id_))
        result = self.module.update(user, uname, pwd, role, status, None)
        if isinstance(result, User):
            self.reload()
            self.view.refresh()
            messagebox.showinfo("Info!", f"User {result.name} has been updated successfully!", parent=self.view.parent)
            self.logger.log(__file__, f"Updated user - {result.name}.", "INFO")
        else:
            messagebox.showerror("Error!", result, parent=self.view.parent)
        return result

    def del_user(self):
        selected = self.view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.view.parent)
            return

        user_id = int(selected[0][0])
        result = self.module.del_from_view(user_id, self.view.curr_user)

        if isinstance(result, User):
            self.reload()
            self.view.refresh()
            messagebox.showinfo("Info!", f"User {result.name} successfully deleted!", parent=self.view.parent)
            self.logger.log(__file__, f"Deleted user - {result.name}.", "INFO")
        else:
            messagebox.showerror("Error!", result, parent=self.view.parent)
        return result

    # endregion

    # region VIEW

    def show_create_user(self):
        form = ItemForm(self.view.parent,
                        User("", "", "", "", ""), self, "Create User", height=250)

    def show_edit_user(self):
        selected = self.view.item_list.get_selected_items()

        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.view.parent)
            return

        user_id = int(selected[0][0])
        user = self.module.find_by_id(user_id)
        form = ItemForm(self.view.parent, user, self, "Update User", height=250, edit=True)

    # endregion

    def close(self):
        self.view.open_views.remove(self.view.page_name)
        self.view.parent.destroy()
