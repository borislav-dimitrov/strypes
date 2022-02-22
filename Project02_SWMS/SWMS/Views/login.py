from tkinter import *
from config import *
from Controls.loginScreen import *
from Services.tkinterServices import *
import time


def on_exit(screen):
    screen.destroy()
    quit()


def log(screen):
    username = screen.nametowidget("uname_entry")
    password = screen.nametowidget("pwd_entry")
    header = screen.nametowidget("login_msg")

    global current_user
    current_user = user_is_valid(username.get(), password.get())

    if ".User" in str(type(current_user)):
        header.config(text="Login Success!")
        screen.update()
        time.sleep(0.5)
        screen.destroy()
    else:
        header.config(text="Invalid user or password!")


def log_in():
    screen = Tk()
    x = (screen.winfo_screenwidth() / 2) - (LOGIN_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (LOGIN_HEIGHT / 2)
    screen.geometry(f"{LOGIN_WIDTH}x{LOGIN_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Login")

    setup_grid(screen, LOGIN_WIDTH, LOGIN_HEIGHT, 5, 5)

    Label(screen, text="Log In", font=("Arial", 18, "bold"), name="login_header").grid(row=0, column=1, columnspan=3)
    Label(screen, text="Username", font=("Arial", 13)).grid(row=1, column=1)
    Label(screen, text="Password", font=("Arial", 13)).grid(row=2, column=1)
    Entry(screen, width=25, name="uname_entry").grid(row=1, column=2, columnspan=2)
    Entry(screen, width=25, name="pwd_entry", show="*").grid(row=2, column=2, columnspan=2)
    Button(screen, text="Login", width=15, height=2,
           bg="lightgray", command=lambda: log(screen)).grid(row=3, column=2)
    Label(screen, text="", font=("Arial", 18, "bold"), name="login_msg").grid(row=4, column=1, columnspan=3)

    screen.protocol("WM_DELETE_WINDOW", lambda: on_exit(screen))
    screen.mainloop()

    try:
        if current_user:
            return current_user
        else:
            return "fake"
    except Exception as ex:
        if "not defined" in str(ex):
            return "fake"
        else:
            print(ex)
