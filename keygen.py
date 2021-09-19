from tkinter import *
from tkinter import messagebox
from tkinter.ttk import (Button, Combobox, Checkbutton)
from random import choice
from os import mkdir
import hashlib
from threading import Thread
from ftp import FTP


class Keygen(FTP):
    def __init__(self, window):
        FTP.__init__(self)

        self.window = window
        self.window.attributes('-toolwindow', 1)
        self.window.title('Keygen')
        self.window.resizable(False, False)
        self.window.geometry('400x290')

        self.interface()

        self.window.mainloop()

    def interface(self):
        self.labelFrame = LabelFrame(self.window, text='Generating keys')
        self.labelFrame.pack(fill='both', expand=True, padx=5, pady=2)

        self.nameDirInput = Entry(self.labelFrame, width=60,
                                  justify=CENTER, relief=FLAT)
        self.nameDirInput.pack(pady=10)
        self.nameDirInput.focus()
        self.nameDirInput.bind("<KeyRelease>", self.focus)

        self.placeholder = Label(
            self.nameDirInput, text='Enter the directory...', width=52, fg='#444', bg='#fff', relief=FLAT)
        self.placeholder.place(x=0, y=-2)

        self.placeholder.bind('<Enter>', self.focused)
        self.nameDirInput.bind('<Leave>', self.unfocus)

        self.countKeys = Combobox(self.window, width=5)
        self.countKeys.place(x=330, y=230)
        self.countKeys['values'] = (
            10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)
        self.countKeys.current(0)

        self.list = Listbox(self.labelFrame, relief=FLAT)
        self.list.pack(fill='both', padx=15)

        self.buttonCreateKeys = Button(
            self.labelFrame, text='Generate', width=50, command=self.generateKeys)
        self.buttonCreateKeys.place(x=10, y=209)

        self.status = IntVar()
        self.checkbutton = Checkbutton(self.labelFrame, text="Upload keys to the server automatically (Optional)",
                                       variable=self.status, command=self.accessServerUpload, cursor='hand2')
        self.checkbutton.place(x=10, y=240)

        self.isAccessServerUploadKeys = False

    def accessServerUpload(self):
        if self.status.get() == 1:
            self.isAccessServerUploadKeys = True
        else:
            self.isAccessServerUploadKeys = False

    def uploadKey(self, key):
        Thread(target=self.__uploadKey(key)).start()

    def __uploadKey(self, key):
        if self.isAccessServerUploadKeys:
            self.connent()
            self.create(key)

    def focus(self, event):
        if self.nameDirInput.get().strip() == '':
            self.placeholder.place_configure(y=-1)
        else:
            self.placeholder.place_configure(y=-20)

    def focused(self, event):
        self.placeholder.place_configure(y=-20)

    def unfocus(self, event):
        if self.nameDirInput.get().strip() == '':
            self.placeholder.place_configure(y=-1)

    def addGenegatedKeysToList(self):
        lists = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd',
                 'e', 'f', 'g', 'h', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        result = ''
        LENGTH_KEY = 25

        for i in range(LENGTH_KEY):
            result += str(choice(lists))

        self.md5 = hashlib.md5(result.encode('utf-8')).hexdigest()
        self.uploadKey(self.md5)

        open(self.nameDirInput.get().strip() + '/' + self.md5, 'w')

        self.list.insert(END, result + '\n')

    def generateKeys(self):
        if self.nameDirInput.get().strip() == '':
            messagebox.showerror(
                'KeyGen', 'Sorry, but you did not specify the directory for saving the keys!')
        else:
            try:
                self.countKey = int(self.countKeys.get())

                mkdir(self.nameDirInput.get().strip())

                for i in range(self.countKey):
                    self.addGenegatedKeysToList()

            except FileExistsError:
                for i in range(self.countKey):
                    self.addGenegatedKeysToList()

            try:
                with open(self.nameDirInput.get().strip() + '/' + 'keys.txt', 'a') as file:
                    separator = '|------------------------|'
                    file.write(separator + '\n')
                    file.writelines(self.list.get(0, END))
            except PermissionError:
                pass

            self.isAccessServerUploadKeys = False

            try:
                self.disconnent()
            except:
                pass


if __name__ == '__main__':
    Keygen(Tk())
