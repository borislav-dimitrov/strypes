import tkinter as tk


class Table:
    def __init__(self, parent, data):
        # data should be 2d array, and first array should be the headers

        for r in range(len(data)):
            for c in range(len(data[0])):
                if r == 0:
                    # column headers styling
                    self.e = tk.Entry(parent, width=20, fg='black',
                                      font=('Arial', 20, 'bold'))
                else:
                    # rows text styling
                    self.e = tk.Entry(parent, width=20, fg='black',
                                      font=('Arial', 16, ))
                self.e.grid(row=r, column=c)
                self.e.insert(r, data[r][c])
                self.e.configure(state='disabled')
