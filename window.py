import tkinter as tk
from tkinter import ttk


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Forest")
        self.root.option_add("*tearOff", False) # This is always a good idea
        # Create a style
        style = ttk.Style(self.root)

        # Import the tcl file
        self.root.tk.call("source", "forest-dark.tcl")

        # Set the theme with the theme_use method
        style.theme_use("forest-dark")

    def mainloop(self):
        self.root.mainloop()
        

