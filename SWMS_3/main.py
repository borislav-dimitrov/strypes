import tkinter as tk

from controler.main_controller import MainController

from view.home_view import HomeView
from view.login import Login


def main():
    main_controller = MainController()
    main_controller.startup()

    root = tk.Tk()
    login = Login(root, "Login", (640, 360), main_controller, grid_rows=6, grid_cols=10)
    main_controller.view = login
    root.mainloop()

    if main_controller.logged_user is not None:
        root = tk.Tk()
        home_view = HomeView(root, "Home", main_controller)
        main_controller.view = home_view
        root.mainloop()

    main_controller.before_exit()

    if main_controller.logging_out:
        main_controller.logging_out = False
        main()


if __name__ == '__main__':
    main()
