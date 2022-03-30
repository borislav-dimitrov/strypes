import tkinter as tk


def main():
    root = tk.Tk()
    root.title("Responsive GUI")
    root.geometry("800x400+500+300")
    rows = 3
    cols = 4

    for row in range(0, rows):
        tk.Grid.rowconfigure(root, row, weight=1)

    for col in range(0, cols):
        tk.Grid.columnconfigure(root, col, weight=1)

    btn_1 = tk.Button(root, text="Button 1")
    btn_2 = tk.Button(root, text="Button 2")

    btn_1.grid(row=0, column=0, sticky="nsew")
    btn_2.grid(row=1, column=0, sticky="nsew")

    root.mainloop()


if __name__ == '__main__':
    main()
