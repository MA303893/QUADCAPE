import Tkinter as tk


class Keypress:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('300x200')
        self.root.bind('<KeyPress>', self.onKeyPress)
    def onKeyPress(self, event):
        self.key = event.char
    def __eq__(self, other):
        return self.key == other
    def __str__(self):
        return self.key