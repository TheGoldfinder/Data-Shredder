from tkinter import END, Button, Checkbutton, IntVar, StringVar, Label, Entry, Tk
from random import randrange
from os import path, walk, remove as os_remove


class App(Tk):
    def __init__(self):
        super().__init__()

        self.checkBoxValue = IntVar()
        self.feedbackText = StringVar()

        # Create window
        self.geometry("300x400")
        self.title("Shredder")
        self.resizable(False, False)

        # Window Elements
        self.label = Label(self, text="Path")
        self.label.config(font=("Arial", 12))
        self.label.place(relx=0.13, rely=0.25, anchor="center")

        self.textBox = Entry(self, width=28)
        self.textBox.config(font=("Arial", 12))
        self.textBox.place(relx=0.5, rely=0.3, anchor="center")

        self.feedback = Label(
            self, textvariable=self.feedbackText, foreground="#d10e0e")
        self.feedback.config(font=("Arial", 12))
        self.feedback.place(relx=0.5, rely=0.55, anchor="center")

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
        # get checkBox value
        value = self.checkBoxValue.get()

        # converts from int to bool and returns it
        return bool(value)

    def shredder(self):
        # get values from inputs
        path = self.getAndCheckInputFromTextField()
        shouldDeleteFilesAfter = self.getCheckBoxValue()

        # resets feedback fieldd
        self.feedback.text = ""

        # sort false path out
        if type(path) == bool:
            print("False input")
            self.feedbackText.set("False input")
            return

        # get all files in path
        fileNames = []
        for (root, dirs, files) in walk(path):
            fileNames = files
            break

        print(f"{fileNames}")

        for fileName in fileNames:
            # read all bytes
            with open(f"{path}\{fileName}", "rb") as binaryFile:
                binaryCode = binaryFile.read()

            print(f"\n\nName: {fileName}")
            print(f"\n{binaryCode}\n")
            # replace the python byte chars
            binaryCode = str(binaryCode).replace("b'", "")
            binaryCode = str(binaryCode).replace("'", "")

            # Try check if file is emty
            try:
                splitBinaryCode = str(binaryCode).split("\\")
            except:
                continue

            # check if emty elements in list
            for element in splitBinaryCode:
                if element == "" or " " in element:
                    splitBinaryCode.remove(element)

            print(str(splitBinaryCode))

            # smash the list randomized into a string
            writeToFile = ""
            firstTime = True
            for binaryIndex in splitBinaryCode:
                if firstTime:
                    writeToFile = writeToFile + f"\\"
                    firstTime = False

                element = splitBinaryCode[randrange(
                    0, len(splitBinaryCode)-1)]
                splitBinaryCode.remove(element)

                writeToFile = writeToFile + f"{element}\\"

            # write the smashed string to file
            with open(f"{path}\{fileName}", "wb") as writeBinaryFile:
                writeBinaryFile.write(bytes(writeToFile, "utf-8"))

            if shouldDeleteFilesAfter:
                os_remove(f"{path}\{fileName}")

            self.feedbackText.set("Done!")


if __name__ == '__main__':
    App().mainloop()
