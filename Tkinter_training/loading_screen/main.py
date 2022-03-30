import tkinter as tk

from loading_screen.loading import Loading


def main():
    root = tk.Tk()
    loading = Loading(root, (640, 360))
    root.mainloop()


if __name__ == '__main__':
    main()