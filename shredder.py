from tkinter import END, Button, Checkbutton, IntVar, Label, Entry, Tk
from random import randrange
from os import path, walk
from time import sleep


class App(Tk):
    def __init__(self):
        super().__init__()

        self.checkBoxValue = IntVar()

        # Create window
        self.geometry("300x400")
        self.title("Shredder")
        self.resizable(False, False)

        self.label = Label(self, text="Path")
        self.label.config(font=("Arial", 12))
        self.label.place(relx=0.13, rely=0.25, anchor="center")

        self.textBox = Entry(self, width=28)
        self.textBox.config(font=("Arial", 12))
        self.textBox.place(relx=0.5, rely=0.3, anchor="center")

        self.feedback = Label(self, text="", foreground="#d10e0e")
        self.feedback.config(font=("Arial", 12,))

        self.shredderBtn = Button(
            self, width=12, height=3, text="Shredder", command=self.shredder)
        self.shredderBtn.config(font=("Arial", 12))
        self.shredderBtn.place(relx=0.5, rely=0.7, anchor="center")

        self.shouldDelete = Checkbutton(
            self, text="Delete files after shredder", variable=self.checkBoxValue)
        self.shouldDelete.config(font=("Arial", 8))
        self.shouldDelete.place(relx=0.5, rely=0.85, anchor="center")

    def getAndCheckInputFromTextField(self):
        # get text input
        # https://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-widget
        textInput = self.textBox.get()

        # reset text box
        self.textBox.delete(0, END)
        self.textBox.insert(0, "")

        # check if actual path
        if path.isdir(textInput):
            return textInput
        else:
            return False

    def getCheckBoxValue(self):
        value = self.checkBoxValue.get()

        if value == 1:
            return True
        elif value == 0:
            return False

    def shredder(self):
        path = self.getAndCheckInputFromTextField()
        shouldDeleteFilesAfter = self.getCheckBoxValue()

        if type(path) == bool:
            print("False input")
            return

        fileNames = []
        for (root, dirs, files) in walk(path):
            fileNames = files
            break

        print(f"{fileNames}\n\n")

        for fileName in fileNames:
            with open(f"{path}\{fileName}", "rb") as binaryFile:
                binaryCode = binaryFile.read()

            try:
                print(f"Name: {fileName}")
                print(f"\n{binaryCode}\n")
                binaryCode = str(binaryCode).replace("b'", "")
                binaryCode = str(binaryCode).replace("'", "")
                splitBinaryCode = str(binaryCode).split("\\")
                for element in splitBinaryCode:
                    if element == "" or " " in element:
                        splitBinaryCode.pop(element)
                print(str(splitBinaryCode))
            except:
                pass

            writeToFile = ""
            firstTime = True
            for dex in splitBinaryCode:
                if firstTime:
                    writeToFile = writeToFile + f"\\"
                    firstTime = False

                element = splitBinaryCode[randrange(
                    0, len(splitBinaryCode)-1)]
                splitBinaryCode = splitBinaryCode.remove(element)

                writeToFile = writeToFile + f"{element}\\"

            with open(f"{path}\{fileName}", "wb") as writeBinaryFile:
                writeBinaryFile.write(bytes(writeToFile))


if __name__ == '__main__':
    App().mainloop()
