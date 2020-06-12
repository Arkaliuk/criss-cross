import tkinter as tk
import tkinter.ttk as ttk


class Cells(ttk.LabelFrame):

    def __init__(self, root, cols=1, rows=1, title='', text='', justify='left', font='Menlo 13', bd=0, *args, **kwargs):
        ttk.LabelFrame.__init__(self, root, text=title, *args, **kwargs)
        self.grup = []
        for i in range(cols * rows):
            cell = tk.Label(self, text=text, font=font, justify=justify, **kwargs)
            cell.grid(column=i % cols, row=i // cols, sticky='nsew')
            self.grup.append(cell)

    def bind_(self, event, func, n):
        self.grup[n].bind(event, lambda x: func(n))


class Radiogrup(ttk.LabelFrame):
    grup = []

    def __init__(self, root, items=tuple(), *args, **kwargs):
        ttk.LabelFrame.__init__(self, root, *args, **kwargs)
        self.var = tk.IntVar()
        for i, text in enumerate(items):
            rb = ttk.Radiobutton(self, text=text, variable=self.var, value=i)
            rb.grid(sticky='we')
            self.grup.append(rb)
