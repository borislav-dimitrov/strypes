import tkinter as tk
from model.service.startup_exit import start_up, before_exit

from view.home_view import HomeView

from view.login import Login


def main():
    systems = start_up()

    root = tk.Tk()
    login = Login(root, "Login", (640, 360), systems["user_controller"], systems["home_controller"], grid_rows=6,
                  grid_cols=10)
    root.mainloop()

    if systems["home_controller"]._logged_user is not None:
        root = tk.Tk()
        home_view = HomeView(root, "Home", systems, icon="resources/icons/main_ico.ico")
        root.mainloop()

    before_exit(systems)
    if systems["home_controller"]._logging_out:
        systems["home_controller"]._logging_out = False
        main()


if __name__ == '__main__':
    main()
