import threading
import queue
from tkinter import DISABLED, Tk, scrolledtext, Button, Frame
from tkinter import INSERT, END, WORD, NORMAL
import tkinter
from tkinter.ttk import Progressbar

from src.modules.dataclass.textMessage import TextMessage
from src.modules.gui.configWindow import ConfigWindow
from src.modules.dataclass.votingProcessMessage import VotingProcessMessage
from src.modules.engine.autovote import AutoVoteApp


class AutovoteGui(Tk):
    startButton: Button
    configureButton: Button
    progress: Progressbar
    textArea: scrolledtext.ScrolledText
    configWindow: ConfigWindow
    def __init__(self) -> None:
        super().__init__("Autovoter v1.1.0", None, "Autovote", useTk=True, sync= False)
        self.title('RF Banana Autovoter v1.1.0')
        self.iconbitmap(default="./_internal/banana-voter.ico")
        self.geometry("385x270")
        self.resizable(False, False)
        self.configure(padx=10, pady=5)
        self.drawGui()
        self.textArea: scrolledtext.ScrolledText
        self.processingQueue: queue.Queue = queue.Queue()
        self.autoVoteApp: AutoVoteApp = AutoVoteApp(self.processingQueue)


    def drawGui(self):
        self.startButton = Button(self, text='Start Voting!', command=self.startButtonAction)
        self.startButton.grid(row=1, sticky="ew")

        firstFrame = Frame(self)
        firstFrame.grid(row=0, sticky="nsew")
        self.configureButton = Button(firstFrame, text='Configure', 
                                      command=self.configureButtonAction)
        self.configureButton.grid(row=0, column=1)

        self.progressVal = tkinter.DoubleVar()
        progressBar = Progressbar(firstFrame, 
                                  orient="horizontal", 
                                  variable= self.progressVal, 
                                  length=300, mode="determinate", 
                                  maximum=100)
        progressBar.grid(row=0)

        self.textArea = scrolledtext.ScrolledText(self,  
                                        wrap = WORD,  
                                        height = 10,
                                        width = 10,
                                        font = ("Times New Roman", 
                                                15)) 
        self.textArea.grid(row=2, sticky="ew")
        self.textArea.configure(state ='disabled')

    def outputRedirector(self,inputStr) -> int:
        self.textArea.configure(state=NORMAL)
        self.textArea.insert(INSERT, inputStr)
        self.textArea.see(END)
        self.textArea.configure(state=DISABLED)
        return 1
    def readQueue(self):
        try:
            message = self.processingQueue.get(block=False)
            if message is not None:
                if isinstance(message, VotingProcessMessage):
                    self.votingMessageCallback(message)
                elif isinstance(message, TextMessage):
                    self.textMessageCallback(message)
            self.after(200, self.readQueue)
        except queue.Empty:
            self.after(200, self.readQueue)

    def votingMessageCallback(self, message: VotingProcessMessage):
        value = float(message.numProcessed) / float(message.totalAccount) * 100
        self.progressVal.set(value)
        if(message.totalAccount == message.numProcessed):
            self.startButton.config(state=NORMAL)
            self.startButton.config(text='Start Voting!')
            self.progressVal.set(100)

    def textMessageCallback(self, message: TextMessage):
        value = message.textMessage
        self.textArea.configure(state=NORMAL)
        self.textArea.insert(INSERT, value)
        self.textArea.insert(END,'\n')
        self.textArea.see(END)
        self.textArea.configure(state=DISABLED)

    def startButtonAction(self):
        self.textArea.configure(state=NORMAL)
        self.textArea.delete('1.0',END)
        self.textArea.see(END)
        self.textArea.configure(state=DISABLED)

        self.progressVal.set(0)
        t1 = threading.Thread(target=self.autoVoteApp.start)
        t1.start()
        self.startButton.config(state=DISABLED)
        self.startButton.config(text="Processing!")
        self.after(200, self.readQueue)

    def configureButtonAction(self):
        rootX = self.winfo_rootx()
        rootY = self.winfo_rooty()
        if not hasattr(self, "configWindow") or not self.configWindow.winfo_exists() :
            self.configWindow = ConfigWindow(self, self.autoVoteApp.appConfig, rootX, rootY)
        else:
            self.configWindow.focus_set()