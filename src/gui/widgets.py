
from itertools import count
from tkinter import ttk, filedialog, END
import customtkinter as tk
from PIL import Image
from src.constants import Constants

class UserButton(tk.CTkButton):
    _ids = count(0)
    @staticmethod
    def get_image_path():
        return Constants.PATH_TO_WORKER_RES

    def get_text(self):
        self.id = next(self._ids)
        return "User " + str(self.id)
    def __init__(self,
                 master,
                 group_id,
                 on_click=None):
        self.id = None
        self.group_id = group_id
        image = tk.CTkImage(Image.open(self.get_image_path()), size=(100, 100))
        super().__init__(
            master=master,
            image=image,
            command=lambda: on_click(self.id) if on_click.__code__.co_argcount == 2 else on_click(),
            text=self.get_text(),
            font=("Times", 24, 'bold')
        )

class ManagerButton(UserButton):
    @staticmethod
    def get_image_path():
        return Constants.PATH_TO_MANAGER_RES

    def get_text(self):
        return "Manager"

class Treeview(ttk.Treeview):
    def __init__(self, master, columns):
        counts = []
        self.count = 1
        for _ in columns:
            counts.append("#{0}".format(self.count))
            self.count += 1
        ttk.Treeview.__init__(self, columns=columns, show="headings", master=master)
        for q in range(len(columns)):
            self.heading(counts[q], text=columns[q])
            self.column(counts[q], anchor="center", width=200)

        self.tree_scroll = ttk.Scrollbar(
            master=master,
            orient=tk.VERTICAL,
            command=self.yview
        )
        self.configure(yscroll=self.tree_scroll.set)
        # self.tree_scroll.config(command=self.yview)
        self.bind("<1>", self.onMouseClick)

    def onMouseClick(self, event):
        if self.identify_region(event.x, event.y) == "separator":
            return "break"

    def grid(self, row, column):
        super().grid(
            row=row,
            column=column,
            sticky=tk.NSEW,
        )
        self.tree_scroll.grid(
            row=row,
            column=column + 1,
            sticky=tk.NSEW
        )
    def place(self, relx, rely):
        super().place(relx=relx, rely=rely, relwidth=self.count * 0.217, relheight=0.4)
        self.tree_scroll.place(relx=relx + self.count * 0.217 + 0.001, rely=rely, relheight=0.4)
        
    def pack(self):
        super().pack()

    def insertion(self, *name):
        self.insert("", "end", values=name)



class FileChooseEntry(tk.CTkEntry):

    def __init__(self, master, id, callback, text):
        self.id = id
        self.callback = callback
        super().__init__(master=master)
        self.label = tk.CTkLabel(
            master=master,
            text=text,
        )
        self.button = tk.CTkButton(
            master=master,
            text="...",
            command=self.on_button_click
        )

    def on_button_click(self):
        filename = filedialog.askopenfilename()
        if filename is None:
            return
        self.delete(0, END)
        self.insert(0, filename)
        self.callback(self.id, filename)
    def grid(self, row, column):
        self.label.grid(
            row=row,
            column=column,
            sticky=tk.NSEW
        )
        super().grid(
            row=row + 1,
            column=column,
            sticky=tk.NSEW,
        )
        self.button.grid(
            row=row + 1,
            column=column+1,
        )

    def place(self, relx, rely):
        self.label.place(
            relx=relx,
            rely=rely
        )
        super().place(
            relx=relx,
            rely=rely+ 0.05,
            relwidth=0.7
        )
        self.button.place(
            relx=relx + 0.72,
            rely=rely + 0.05,
            relwidth=0.07
        )
