from model.service.logger import MyLogger
from model.service.modules.users_module import UserModule
import customtkinter as ctk
import tkinter as tk


class UserController:
    def __init__(self, user_module: UserModule, logger: MyLogger):
        self._module = user_module
        self._logger = logger

    def login(self, username, password):
        user = self._module.find_by_attribute("name", username.lower())
        if user is not None:
            valid_pwd = self._module._pwd_mgr.compare(password, user[0].password)
            if valid_pwd:
                return True, "Login successful!", user[0]
            else:
                return False, "Wrong password!", None
        return False, "User not found!", None

    def load(self):
        self._module.load()

    def save(self):
        self._module.save()

    def reload(self):
        self.save()
        self.load()

    # region GUI
    @staticmethod
    def create_user_btn_click(m_screen, header, text_font, text_bold, text_color, main_color, hover_color, cols):
        header.configure(text="Create New User")

        # Create Labels
        uname_lbl = ctk.CTkLabel(m_screen, text="Username:", text_font=text_bold, text_color=text_color)
        uname_lbl.grid(row=10, column=3, columnspan=2, sticky="e")
        pwd_lbl = ctk.CTkLabel(m_screen, text="Password:", text_font=text_bold, text_color=text_color)
        pwd_lbl.grid(row=10, column=17, columnspan=2, sticky="e")
        type_lbl = ctk.CTkLabel(m_screen, text="Type:", text_font=text_bold, text_color=text_color)
        type_lbl.grid(row=17, column=3, columnspan=2, sticky="e")
        status_lbl = ctk.CTkLabel(m_screen, text="Status:", text_font=text_bold, text_color=text_color)
        status_lbl.grid(row=17, column=17, columnspan=2, sticky="e")

        # Create Inputs
        uname_entry = ctk.CTkEntry(m_screen, text_font=text_bold)
        uname_entry.grid(row=10, column=6, columnspan=4, sticky="we")
        pwd_entry = ctk.CTkEntry(m_screen, text_font=text_bold, show="*")
        pwd_entry.grid(row=10, column=20, columnspan=4, sticky="we")

        # Create Radio Buttons
        type_var = tk.StringVar()
        type_var.set("Operator")
        admin_rb = ctk.CTkRadioButton(m_screen, text="Administrator", variable=type_var, value="Administrator",
                                      text_font=text_font, text_color=text_color)
        admin_rb.grid(row=16, column=5, columnspan=2, rowspan=2, sticky="wen", pady=(20, 0))
        operator_rb = ctk.CTkRadioButton(m_screen, text="Operator", variable=type_var, value="Operator",
                                         text_font=text_font, text_color=text_color)
        operator_rb.grid(row=17, column=5, columnspan=2, rowspan=2, sticky="wes", pady=(0, 20))

        status_var = tk.StringVar()
        status_var.set("Enabled")
        enabled_rb = ctk.CTkRadioButton(m_screen, text="Enabled", variable=status_var, value="Enabled",
                                        text_font=text_font, text_color=text_color,
                                        fg_color=main_color, hover_color=hover_color)
        enabled_rb.grid(row=16, column=19, columnspan=2, rowspan=2, sticky="wen", pady=(20, 0))
        disabled_rb = ctk.CTkRadioButton(m_screen, text="Disabled", variable=type_var, value="Disabled",
                                         text_font=text_font, text_color=text_color,
                                         fg_color=main_color, hover_color=hover_color)
        disabled_rb.grid(row=17, column=19, columnspan=2, rowspan=2, sticky="wes", pady=(0, 20))

        # Create Buttons
        create_btn = ctk.CTkButton(m_screen, text="Create", text_font=text_bold,
                                   fg_color=main_color, hover_color=hover_color)
        create_btn.grid(row=24, column=int(cols // 2) - 2, columnspan=5, sticky="nsew")

    @staticmethod
    def update_user_btn_click(m_screen, header, text_font, text_bold, text_color, main_color, hover_color, cols):
        header.configure(text="Update User")

        # Create Labels
        uname_lbl = ctk.CTkLabel(m_screen, text="Username:", text_font=text_bold, text_color=text_color)
        uname_lbl.grid(row=10, column=3, columnspan=2, sticky="e")
        pwd_lbl = ctk.CTkLabel(m_screen, text="Password:", text_font=text_bold, text_color=text_color)
        pwd_lbl.grid(row=10, column=17, columnspan=2, sticky="e")
        type_lbl = ctk.CTkLabel(m_screen, text="Type:", text_font=text_bold, text_color=text_color)
        type_lbl.grid(row=17, column=3, columnspan=2, sticky="e")
        status_lbl = ctk.CTkLabel(m_screen, text="Status:", text_font=text_bold, text_color=text_color)
        status_lbl.grid(row=17, column=17, columnspan=2, sticky="e")

        # Create Inputs
        uname_entry = ctk.CTkEntry(m_screen, text_font=text_bold)
        uname_entry.grid(row=10, column=6, columnspan=4, sticky="we")
        pwd_entry = ctk.CTkEntry(m_screen, text_font=text_bold, show="*")
        pwd_entry.grid(row=10, column=20, columnspan=4, sticky="we")

        # Create Radio Buttons
        type_var = tk.StringVar()
        type_var.set("Operator")
        admin_rb = ctk.CTkRadioButton(m_screen, text="Administrator", variable=type_var, value="Administrator",
                                      text_font=text_font, text_color=text_color)
        admin_rb.grid(row=16, column=5, columnspan=2, rowspan=2, sticky="wen", pady=(20, 0))
        operator_rb = ctk.CTkRadioButton(m_screen, text="Operator", variable=type_var, value="Operator",
                                         text_font=text_font, text_color=text_color)
        operator_rb.grid(row=17, column=5, columnspan=2, rowspan=2, sticky="wes", pady=(0, 20))

        status_var = tk.StringVar()
        status_var.set("Enabled")
        enabled_rb = ctk.CTkRadioButton(m_screen, text="Enabled", variable=status_var, value="Enabled",
                                        text_font=text_font, text_color=text_color,
                                        fg_color=main_color, hover_color=hover_color)
        enabled_rb.grid(row=16, column=19, columnspan=2, rowspan=2, sticky="wen", pady=(20, 0))
        disabled_rb = ctk.CTkRadioButton(m_screen, text="Disabled", variable=type_var, value="Disabled",
                                         text_font=text_font, text_color=text_color,
                                         fg_color=main_color, hover_color=hover_color)
        disabled_rb.grid(row=17, column=19, columnspan=2, rowspan=2, sticky="wes", pady=(0, 20))

        # Create Buttons
        create_btn = ctk.CTkButton(m_screen, text="Update", text_font=text_bold,
                                   fg_color=main_color, hover_color=hover_color)
        create_btn.grid(row=24, column=int(cols // 2) - 2, columnspan=5, sticky="nsew")
    # endregion
