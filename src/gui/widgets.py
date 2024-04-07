
from itertools import count
from tkinter import ttk
import customtkinter as tk
from PIL import Image
from constants import Constants

class Entry(ttk.Entry):

    def __init__(self, master):
        super().__init__(master=master)


class Button(ttk.Button):

    def __init__(self, master):
        super().__init__(master=master)

class UserButton(tk.CTkButton):
    _ids = count(1)
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