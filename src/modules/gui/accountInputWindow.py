from tkinter import Button, Entry, Label, Toplevel, Misc
from typing import Tuple

class AccountInputWindow(Toplevel):
    saveButton: Button
    usernameInput: Entry
    passwordInput: Entry
    input: Tuple[str, str]
    def __init__(self, master: Misc) -> None:
        super().__init__(master=master, width=250, height=100, padx=2, pady=5)
        self.title("Input New Account")
        self.drawGui()

    def drawGui(self):
        Label(self, text="Username").grid(row=0, column=0)
        Label(self, text="Password").grid(row=1, column=0)
        self.usernameInput = Entry(self)
        self.passwordInput = Entry(self, show="*")
        self.saveButton = Button(self, text="Save", command=self.saveButtonAction)

        self.usernameInput.grid(row=0, column=1)
        self.passwordInput.grid(row=1, column=1)
        self.saveButton.grid(row=3, columnspan=3)

        self.transient()
        self.grab_set()
        self.master.wait_window(self)

    def saveButtonAction(self):
        self.input = (self.usernameInput.get(), self.passwordInput.get())
        self.destroy()
