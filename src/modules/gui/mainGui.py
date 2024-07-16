import sys
import threading
import queue
from tkinter import DISABLED, Tk, scrolledtext, Button, Frame
from tkinter import INSERT, END, WORD, NORMAL
import tkinter
from tkinter.ttk import Progressbar

from src.modules.gui.configWindow import ConfigWindow
from src.modules.dataclass.votingProcessMessage import VotingProcessMessage
from src.modules.engine.autovote import AutoVoteApp


class AutovoteGui(Tk):
    startButton: Button
    configureButton: Button
    progress: Progressbar
    text_area: scrolledtext.ScrolledText
    configWindow: ConfigWindow
    def __init__(self) -> None:
        super().__init__("Autovoter v1.1.0", None, "Autovote", useTk=True, sync= False)
        self.title('RF Banana Autovoter v1.1.0')
        self.geometry("400x250")
        self.drawGui()

        sys.stdout.write = self.outputRedirector
        sys.stderr.write = self.outputRedirector

        self.text_area: scrolledtext.ScrolledText
        self.processingQueue: queue.Queue = queue.Queue()
        self.autoVoteApp: AutoVoteApp = AutoVoteApp(self.processingQueue)


    def drawGui(self):
        self.startButton = Button(self, text='Start Voting!', command=self.startButtonAction)
        self.startButton.grid(row=1, column=0, sticky="ew")

        firstFrame = Frame(self)
        firstFrame.grid(row=0, sticky="nsew")
        self.configureButton = Button(firstFrame, text='Configure', command=self.configureButtonAction)
        self.configureButton.grid(row=0, column=1)

        self.progressVal = tkinter.DoubleVar()
        progressBar = Progressbar(firstFrame, orient="horizontal", variable= self.progressVal, length=300, mode="determinate", maximum=100)
        progressBar.grid(row=0)

        self.text_area = scrolledtext.ScrolledText(self,  
                                        wrap = WORD,  
                                        height = 10,
                                        width = 20,
                                        font = ("Times New Roman", 
                                                15)) 
        self.text_area.grid(row=2, sticky="ew")
        self.text_area.configure(state ='disabled')

    def outputRedirector(self,inputStr) -> int:
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(INSERT, inputStr)
        self.text_area.see(END)
        self.text_area.configure(state=DISABLED)
        return 1
    def readQueue(self):
        try:
            message = self.processingQueue.get(block=False)
            if message is not None:
                if isinstance(message, VotingProcessMessage):
                    self.votingMessageCallback(message)
            self.after(200, self.readQueue)
        except queue.Empty:
            self.after(200, self.readQueue)
            pass
        pass

    def votingMessageCallback(self, message: VotingProcessMessage):
        value = message.numProcessed.__float__() / message.totalAccount.__float__() * 100
        self.progressVal.set(value)
        if(message.totalAccount == message.numProcessed):
            self.startButton.config(state=NORMAL)
            self.startButton.config(text='Start Voting!')
            self.progressVal.set(100)
        pass

    def startButtonAction(self):
        self.text_area.configure(state=NORMAL)
        self.text_area.delete('1.0',END)
        self.text_area.see(END)
        self.text_area.configure(state=DISABLED)

        self.progressVal.set(0)
        t1 = threading.Thread(target=self.autoVoteApp.start)
        t1.start()
        self.startButton.config(state=DISABLED)
        self.startButton.config(text="Processing!")
        self.after(200, self.readQueue)

    def configureButtonAction(self):
        self.configWindow = ConfigWindow(self, self.autoVoteApp.appConfig)