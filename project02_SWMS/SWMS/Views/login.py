import tkinter as tk
import Services.tkinterServices as TkServ
import time
import Models.Db.fakeDB as DB
import Services.userServices as UserServ


class Login:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols):
        self.m_screen = m_screen
        self.page_name = page_name
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.title = title
        self.logged_user = "none"

        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.m_screen.resizable(False, False)
        self.m_screen.title(self.title)

        TkServ.setup_grid(self.m_screen, self.width, self.height, self.grid_cols, self.grid_rows)

        self.header_lbl = tk.Label(self.m_screen, text="Log In", font=("Arial", 18, "bold"), name="login_header")
        self.header_lbl.grid(row=0, column=1, columnspan=3)

        self.uname_lbl = tk.Label(self.m_screen, text="Username", font=("Arial", 13))
        self.uname_lbl.grid(row=1, column=1)

        self.pwd_lbl = tk.Label(self.m_screen, text="Password", font=("Arial", 13))
        self.pwd_lbl.grid(row=2, column=1)

        self.uname_entry = tk.Entry(self.m_screen, width=25, name="uname_entry")
        self.uname_entry.grid(row=1, column=2, columnspan=2)

        self.pwd_entry = tk.Entry(self.m_screen, width=25, name="pwd_entry", show="*")
        self.pwd_entry.grid(row=2, column=2, columnspan=2)

        self.login_btn = tk.Button(self.m_screen, text="Login", width=15, height=2,
                                   bg="lightgray", command=lambda: self.submit())
        self.login_btn.grid(row=3, column=2)

        self.login_msg = tk.Label(self.m_screen, text="", font=("Arial", 18, "bold"), name="login_msg")
        self.login_msg.grid(row=4, column=1, columnspan=3)

    def user_is_valid(self):
        for user in DB.login_users:
            if user.user_name.lower() == self.uname_entry.get().lower() and UserServ.compare_pwd(self.pwd_entry.get(),
                                                                                                 user.user_pwd):
                return user

        return False

    def submit(self):
        current_user = self.user_is_valid()

        if current_user:
            self.logged_user = current_user
            self.login_msg.config(text="Login Success!")
            self.m_screen.update()
            time.sleep(0.5)
            self.m_screen.destroy()
        else:
            self.login_msg.config(text="Invalid user or password!")
