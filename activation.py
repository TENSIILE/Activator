from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Button
import hashlib
from threading import Thread
from ftp import FTP


class Activate(FTP):
    def __init__(self, window):
        FTP.__init__(self)

        self.window = window
        self.window.attributes('-toolwindow', 1)
        self.window.title('Activating the program')
        self.window.resizable(False, False)
        self.window.geometry('400x100')

        self.interface(window)

        self.LENGTH_KEY = 25

        self.window.mainloop()

    def interface(self, window):
        self.labelFrame = LabelFrame(self.window, text='Activate the key')
        self.labelFrame.pack(fill='both', expand=True, padx=5, pady=2)

        self.vcmd = (window.register(self.validate), '%P')

        self.key = Entry(self.labelFrame, width=58, justify=CENTER,
                         relief=FLAT, validate='key', validatecommand=self.vcmd)
        self.key.pack(pady=10)
        self.key.bind('<KeyRelease>', self.checkLenKey)
        self.key.focus()

        self.input = Label(
            self.key, text='Enter the key...', width=52, bg='#fff', relief=FLAT, fg='#999')
        self.input.place(x=0, y=-2)
        self.input.bind('<Enter>', self.focus)

        self.key.bind('<Button-1>', self.focus)
        self.window.bind('<Button-1>', self.unfocus)

        self.accessBtn = Button(
            self.labelFrame, text='Confirm', command=self.accessing)
        self.accessBtn.pack(fill='both', padx=15)
        self.accessBtn.config(state=DISABLED)

    def focus(self, event):
        self.input.place_configure(y=-20)

    def unfocus(self, event):
        if self.key.get() == '':
            self.input.place_configure(y=-1)

    def checkLenKey(self, event):
        if len(self.key.get().strip()) >= self.LENGTH_KEY:
            self.accessBtn.config(state=ACTIVE)
        else:
            self.accessBtn.config(state=DISABLED)

    def validate(self, value):
        if len(value) <= self.LENGTH_KEY:
            return True
        else:
            return False

    def accessing(self):
        Thread(target=self.__accessing).start()

    def __accessing(self):
        if self.key.get().strip() == '':
            messagebox.showerror('Activating the program',
                                 'Sorry, but you did not enter the activation key!')
        else:
            self.accessBtn.config(state=DISABLED)
            self.isAccess = False

            self.contentKeysOld = str(self.key.get().strip())

            self.contentKeys = hashlib.md5(
                self.contentKeysOld.encode('utf-8')).hexdigest()

            self.connent()

            self.files = self.getFiles()

            for i in self.files:
                if len(i) == 32:
                    if self.contentKeys == i:
                        self.isAccess = True
                        break
                    else:
                        self.isAccess = False
            try:
                self.showing()
                self.disconnent()
            except:
                pass

    def saveKey(self):
        with open('keys.ini', 'w') as file:
            file.write('Your key:' + str(self.contentKeysOld) +
                       '|' + str(self.contentKeys))

    def showing(self):
        if self.isAccess:
            messagebox.showinfo('Activating the program',
                                'Successfully! Thanks for activating the product!')

            self.delete(self.contentKeys)
            self.copy(self.contentKeys)

            self.saveKey()
        else:
            messagebox.showerror('Activating the program',
                                 'Error! There is no such key!')
            self.accessBtn.config(state=ACTIVE)


if __name__ == '__main__':
    Activate(Tk())
