from model.service.startup_exit import start_up, before_exit
import customtkinter as ctk

from view.components.loading_screen import MyLoading
from view.home_view import HomeView
import resources.theme_cfg as tcfg

# TODO
#   enable disabled buttons in info msg
#   sample project in GIT at intro-python\09-library-mvc
from view.login import Login


def setup_theme():
    if tcfg._THEME == "Light":
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")
    elif tcfg._THEME == "Dark":
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")


def main():
    setup_theme()
    systems = start_up()

    # loading = MyLoading(time_s=1)

    root = ctk.CTk()
    login = Login(root, "Login", (640, 360), systems["user_controller"], systems["home_controller"], grid_rows=6,
                  grid_cols=10)
    root.mainloop()

    if systems["home_controller"]._logged_user is not None:
        root = ctk.CTk()
        home_view = HomeView(root, "Home", systems, icon="resources/icons/main_ico.ico")
        root.mainloop()

    before_exit(systems)
    if systems["home_controller"]._logging_out:
        systems["home_controller"]._logging_out = False
        main()


if __name__ == '__main__':
    main()
