from Views.mainScreen import MainScreen
import tkinter as tk
import config as CFG
import Views.importAllViews as Views
from Views.onFirstStart import FirstUser
import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ


def main():
    # clear opened windows
    DB.opened_pages = []
    # reset the user on startup
    user = "none"

    # load users and data from file
    # Todo - loading statuses may be logged in log file
    status = DB.load_and_create_users()
    DB.load_all_entities()

    if "Fail" in status:
        return
    elif status != "Success" and status != "No users found!":
        TkServ.create_msg("Warning!", status)
    elif status == "No users found!":
        # If no users found create the first admin account
        screen = tk.Tk()
        first_run = FirstUser(screen, "first_registration", "Create First User", CFG.REG_WIDTH, CFG.REG_HEIGHT, 5, 5)
        screen.mainloop()
        if first_run.tmp_user == "terminate":
            quit()
        else:
            DB.create_users([first_run.tmp_user])
            # save users to file if it was first login and new user has been created
            DB.save_all_data()

    # login and set the current user
    login_screen = tk.Tk()
    login = Views.Login(login_screen, "login_page", "Login", CFG.LOGIN_WIDTH, CFG.LOGIN_HEIGHT, 5, 5)
    login_screen.mainloop()
    user = login.logged_user
    if user == "none":
        return

    # Render main screen
    screen = tk.Tk()
    main_screen = MainScreen(screen, "main_screen", "Simple Warehouse Management System", CFG.RES_WIDTH, CFG.RES_HEIGHT,
                             30, 10,
                             user)
    screen.mainloop()
    if main_screen.logout_status:
        main()


if __name__ == '__main__':
    main()