import tkinter
from tkinter import Toplevel, Listbox, Button, EXTENDED, END, DISABLED, Misc, NORMAL
from typing import Tuple
from src.modules.configuration.config import Config
from src.modules.gui.accountInputWindow import AccountInputWindow


class ConfigWindow(Toplevel):
    config: Config
    userListBox: Listbox
    addButton: Button
    deleteButton: Button
    saveButton: Button
    accountInputWindow: Toplevel
    newUserInput: Tuple[str, str]
    needSave: bool
    def __init__(self, master: Misc, config: Config, xPos: int, yPos: int) -> None:
        super().__init__(master=master, padx=2, pady=5)
        self.title("Configuration")
        self.geometry(f'200x250+{xPos}+{yPos}')
        self.config = config
        self.needSave = False
        self.debugModeVar = tkinter.BooleanVar(master=self, value=self.config.debugMode)
        self.drawGui()
        self.checkListBoxSelect()
        self.checkNotSaved()

    def drawGui(self):
        self.userListBox = Listbox(self, selectmode=EXTENDED, width=30)
        for account in self.config.accounts:
            self.userListBox.insert(END, account.username)
        self.addButton = Button(self, text="Add Account", command=self.addAccountButtonAction)
        self.deleteButton = Button(self, text="Delete", state=DISABLED, command=self.deleteButtonAction)
        self.saveButton = Button(self, text="Save", state=DISABLED, command=self.saveButtonAction)
        self.debugModeCheckbox = tkinter.Checkbutton(self, text="Debug Mode", variable=self.debugModeVar, command=self.debugModeCheckboxAction)
        self.userListBox.grid(row=0, columnspan=2)
        self.addButton.grid(row=1, column=0, sticky="news")
        self.deleteButton.grid(row=1, column=1, sticky="news")
        self.saveButton.grid(row=3, columnspan=2, sticky="news")
        self.debugModeCheckbox.grid(row=2, columnspan=2, sticky="w")

    def checkListBoxSelect(self):
        if len(self.userListBox.curselection()) > 0:
            self.deleteButton.configure(state=NORMAL)
        else:
            self.deleteButton.configure(state=DISABLED)
        self.after(200, self.checkListBoxSelect)
    
    def checkNotSaved(self):
        if self.needSave:
            self.saveButton.configure(state=NORMAL)
        else:
            self.saveButton.configure(state=DISABLED)
        self.after(200, self.checkNotSaved)
    
    def addAccountButtonAction(self):
        self.accountInputWindow = AccountInputWindow(self)
        if self.accountInputWindow.input is not None:
            self.config.addAccount(*self.accountInputWindow.input)
            self.userListBox.insert(END, self.accountInputWindow.input[0])
            self.needSave = True

    def deleteButtonAction(self):
        for selectedAccount in self.userListBox.curselection()[::-1]:
            self.config.deleteAccount(selectedAccount)
            self.userListBox.delete(selectedAccount)
        self.userListBox.selection_clear(0)
    def saveButtonAction(self):
        self.config.saveChangesToJson()
        self.needSave = False
    def debugModeCheckboxAction(self):
        self.config.debugMode = self.debugModeVar.get()
        self.needSave = True