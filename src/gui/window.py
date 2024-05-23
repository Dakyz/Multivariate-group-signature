import sys
from tkinter import IntVar
import pickle
from src.utils.ContractSchemes import ContractSchemes
from src.utils.Repository import Repository
from src.utils.GroupSchemes import GroupSchemes
from tkinter import messagebox

sys.path.append("gui/")
from src.gui.widgets import *
from src.constants import Constants

tk.set_appearance_mode("light")
tk.set_default_color_theme("blue")


class Window:
    def __init__(self):
        # create root window and set main params for it
        self.root = tk.CTk()
        self.root.title("Company Interaction")
        self.root.option_add("*tearOff", False)
        self.root.geometry("1400x600")
        self.root.resizable(False, False)

        # singleton instance for db interaction
        self.repository = Repository()
        self.group_schemes = GroupSchemes()
        self.contract_schemes = ContractSchemes()

        main_frame = tk.CTkFrame(self.root)
        main_frame.grid(row=0, column=0, sticky="nswe")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # create frames for companies
        self.left_frame = tk.CTkFrame(main_frame)
        self.left_frame.grid(row=0, column=0, sticky="nswe")

        self.right_frame = tk.CTkFrame(main_frame)
        self.right_frame.grid(row=0, column=1, sticky="nswe")

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # create
        self.create_company(self.left_frame, 0)
        self.create_company(self.right_frame, 1)

        # widget for company separation
        separator = ttk.Separator(self.root, orient='vertical')
        separator.place(relx=0.5, rely=0, relheight=1)

        # should make little delay for centering window
        self.root.after(50, lambda: self.center(self.root))

        self.checkbox_list = {}
        self.files = {}
        self.signs = {}

    def create_company(self, master, group_id):
        # create manager
        manager = ManagerButton(master=master, on_click=self.on_manager_click, group_id=group_id)
        manager.grid(row=0, column=1)
        self.repository.add_company(group_id)
        company = self.group_schemes.get_group_scheme(group_id)
        company.setup()

        # create 3 users
        for i in range(3):
            user = UserButton(
                master=master,
                on_click=self.on_user_click,
                group_id=group_id
            )
            user.grid(row=1, column=i)

            # create user params in db
            # TODO: set real sk
            company.join(user.id)

            # configure correct grid
            master.rowconfigure(i, weight=1)
            master.columnconfigure(i, weight=1)

    # trigger for user button click
    def on_user_click(self, id):
        print(f"User {id} clicked")
        top_level = tk.CTkToplevel(master=self.root)
        top_level.title(f"User {id} Menu")
        top_level.geometry("800x600")

        params_label = tk.CTkLabel(
            master=top_level,
            text="Parameters:",
            font=("Times", 24, 'bold'),
        )
        params_label.place(
            relx=0.1,
            rely=0.05
        )

        params = Treeview(
            master=top_level,
            columns=["Param", "Value"]
        )
        params.place(
            relx=0.1,
            rely=0.1
        )
        params.insertion(
            "Username", self.repository.get_username(id)
        )
        params.insertion(
            "Email", self.repository.get_user_emai(id)
        )
        params.insertion(
            "Secret Key", self.repository.get_user_sk(id)
        )
        params.insertion(
            "Pubic Key", self.repository.get_user_pk(id)
        )

        def onFileChoose(id, path):
            self.files[id] = path

        file_choose_entry = FileChooseEntry(
            master=top_level,
            id=id,
            callback=onFileChoose,
            text="Input file"
        )
        self.files[id] = file_choose_entry
        file_choose_entry.place(
            relx=0.1,
            rely=0.52
        )

        def onSignChoose(id, path):
            self.signs[id] = path

        file_choose_entry = FileChooseEntry(
            master=top_level,
            id=id,
            callback=onSignChoose,
            text="Sign file"
        )
        self.files[id] = file_choose_entry
        file_choose_entry.place(
            relx=0.1,
            rely=0.72
        )

        try:
            value = self.checkbox_list[id]
        except KeyError:
            value = IntVar()
            self.checkbox_list[id] = value

        checkbox = tk.CTkCheckBox(
            master=top_level,
            command=lambda: self.onChooseSigner(id, value.get()),
            text="Choose signer",
            variable=value
        )
        checkbox.place(
            relx=0.1,
            rely=0.85
        )

        sign_button = tk.CTkButton(
            master=top_level,
            command=self.sign,
            text="Sign"
        )
        sign_button.place(
            relx=0.1,
            rely=0.93
        )

        verify_button = tk.CTkButton(
            master=top_level,
            command=lambda : self.verify(self.files[id], self.signs[id]),
            text="Verify"
        )
        verify_button.place(
            relx=0.4,
            rely=0.93
        )

        self.checkbox_list[id] = value
        self.root.after(20, lambda: self.center(top_level))

    def verify(self, input_file, sign_file):

        contract_schemes = self.contract_schemes._contract_schemes

        try:
            with open(input_file, "r") as f:
                msg = hash(f.read())

            with open(sign_file, "rb") as f:
                sign = pickle.load(f)
        except Exception:
            messagebox.showerror("Error", "Choose input file and sign file")
            return

        result = contract_schemes.verify(
            msg,
            sign
        )
        if result == 1:
            messagebox.showinfo("Yes!", "Sign is correct")
        else:
            messagebox.showerror("NO!!", "Sign is not correct")


    def onChooseSigner(self, id, value):
        if value == 1:
            print(f"Chosen {id}")

            # company 1

            if id < 3:
                for i in range(3):
                    if id != i:
                        try:
                            self.checkbox_list[i].set(0)
                        except KeyError:
                            continue
            # company 2
            else:
                for i in range(3, 6):
                    if id != i:
                        try:
                            self.checkbox_list[i].set(0)
                        except KeyError:
                            continue
        self.root.update_idletasks()

    def sign(self):
        signer1, signer2 = -1, -1
        for i in range(3):
            try:
                if self.checkbox_list[i].get() == 1:
                    signer1 = i
            except KeyError:
                continue

        for i in range(3, 6):
            try:
                if self.checkbox_list[i].get() == 1:
                    signer2 = i
            except KeyError:
                continue

        if signer1 == -1 or signer2 == -1:
            messagebox.showerror("Error", "Choose 2 signers")
            return

        print(f"signer1 = {signer1}, signer2 = {signer2}")
        contract_schemes = self.contract_schemes._contract_schemes

        try:
            with open(self.files[signer1], "r") as f:
                msg1 = hash(f.read())

            with open(self.files[signer2], "r") as f:
                msg2 = hash(f.read())
        except Exception:
            messagebox.showerror("Error", "Choose file to sign")
            return


        contract_schemes.sign_step1(
            company_id=0
        )
        contract_schemes.sign_step1(
            company_id=1
        )

        contract_schemes.sign_step2(
            user_id=signer1,
            company_id=0,
            msg=msg1
        )
        contract_schemes.sign_step2(
            user_id=signer2,
            company_id=1,
            msg=msg2
        )

        contract_schemes.sign_step3(
            company_id=0,
            other_company_id=1
        )
        contract_schemes.sign_step3(
            company_id=1,
            other_company_id=0
        )

        sign1 = contract_schemes.sign_step4(
            company_id=0,
            other_company_id=1
        )


        sign2 = contract_schemes.sign_step4(
            company_id=1,
            other_company_id=0
        )

        with open("sign1", "wb") as f:
            pickle.dump(sign1, f)

        with open("sign2", "wb") as f:
            pickle.dump(sign2, f)

    def on_manager_click(self):
        print(f"Manager clicked")
        top_level = tk.CTkToplevel(master=self.root)
        top_level.title(f"Manager Menu")
        top_level.geometry("600x600")

        def onSignChoose(_, path):
           self.signs[-1] = path

        file_choose_entry = FileChooseEntry(
            master=top_level,
            id=-1,
            callback=onSignChoose,
            text="Sign file"
        )
        file_choose_entry.place(
            relx=0.1,
            rely=0.42
        )

        open_button = tk.CTkButton(
            master=top_level,
            text="Open",
            command=self.open
        )
        open_button.place(
            relx=0.1,
            rely=0.8
        )

        self.root.after(20, lambda: self.center(top_level))

    def open(self):
        group_schemes = self.group_schemes.get_group_scheme(0)

        try:
            with open(self.signs[-1], "rb") as f:
                sign = pickle.load(f)
        except Exception:
            messagebox.showerror("Error", "Choose sign file")
            return

        result = group_schemes.open(
            sign[2],
            self.repository.get_all_pk()
        )
        messagebox.showinfo("Open", f"{result}")

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
