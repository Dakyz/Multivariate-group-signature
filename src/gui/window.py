import sys

sys.path.append("gui/")
from widgets import *
from constants import Constants
tk.set_appearance_mode("light")
tk.set_default_color_theme("blue")


class Window:
    def __init__(self):
        self.root = tk.CTk()
        self.root.title("Company Interaction")
        self.root.option_add("*tearOff", False)
        self.root.geometry("1400x600")
        self.root.resizable(False, False)

        main_frame = tk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nswe")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.left_frame = tk.CTkFrame(main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nswe")

        self.right_frame = tk.CTkFrame(main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nswe")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.create_company(self.left_frame, 1)
        self.create_company(self.right_frame, 2)

        separator = ttk.Separator(self.root, orient='vertical')
        separator.place(relx=0.5, rely=0, relheight=1)

        self.root.after(50, lambda: self.center(self.root))

    def create_company(self, master, group_id):
        manager = ManagerButton(master=master, on_click=self.on_manager_click, group_id=group_id)
        manager.grid(row=0, column=1)

        user1 = UserButton(master=master, on_click=self.on_user_click, group_id=group_id)
        user1.grid(row=1, column=0)

        user2 = UserButton(master=master, on_click=self.on_user_click, group_id=group_id)
        user2.grid(row=1, column=1)

        user3 = UserButton(master=master, on_click=self.on_user_click, group_id=group_id)
        user3.grid(row=1, column=2)

        for i in range(3):
            master.rowconfigure(i, weight=1)
            master.columnconfigure(i, weight=1)

    def on_user_click(self, id):
        print(f"User {id} clicked")
        top_level = tk.CTkToplevel(master=self.root)
        top_level.title(f"User {id} Menu")
        top_level.geometry("600x600")
        self.root.after(20, lambda: self.center(top_level))

    def on_manager_click(self):
        print(f"Manager clicked")
        top_level = tk.CTkToplevel(master=self.root)
        top_level.title(f"Manager Menu")
        top_level.geometry("600x600")
        self.root.after(20, lambda: self.center(top_level))

    def mainloop(self):
        self.root.mainloop()

    @staticmethod
    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
