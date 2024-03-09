from tkinter import ttk


class Entry(ttk.Entry):

    def __init__(self, master):
        super().__init__(master=master)


class Button(ttk.Button):

    def __init__(self, master):
        super().__init__(master=master)