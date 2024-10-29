from tkinter import *
from tkinter import ttk

class menu:
    def __init__(self, root):
        root.title("Gerenciamento de estoque")
        root.grid()
        mainFrame = ttk.Frame(root, padding= "3 3 12 12")
        mainFrame.grid(column=0, row=0, sticky=(N,W,E,S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
root=Tk()
menu(root)
root.mainloop()