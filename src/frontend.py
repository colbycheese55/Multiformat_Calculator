import customtkinter as ctk
from tkinter import messagebox as mb
from backend import calculate, generateOutput, HistoryLog, getReadme


root = ctk.CTk()
root.geometry("600x500")
root.title("Multiformat Calculator")
history = HistoryLog()
showHistory = False

# Functions
def solve(*args):
    expression = entryBox.get("1.0", ctk.END)
    if len(args) > 0: # delete the extra \n
        entryBox.delete("1.0", ctk.END)
        entryBox.insert(ctk.END, expression.replace("\n", ""))
    result, flags, error = calculate(expression)
    if error is not False:
        writeResultBox(f"Error: {error}")
        return
    output = generateOutput(result, flags)
    history.addEntry(output, result, expression)
    output = history.getHistory() if showHistory is True else output
    writeResultBox(output)

def toggleHistory(*args):
    global showHistory
    showHistory = not showHistory
    text = history.getHistory() if showHistory is True else ""
    writeResultBox(text)

def writeResultBox(text: str):
    resultBox.configure(state=ctk.NORMAL)
    resultBox.delete("1.0", ctk.END)
    resultBox.insert(ctk.END, text)
    resultBox.configure(state=ctk.DISABLED)

def clear(*args):
    writeResultBox("")
    entryBox.delete("1.0", ctk.END)


# Textboxes and labels
padding = 5
labelFont = ("Franklin Gothic Heavy", 22)
textFont = ("Calibri", 17)

entryBox = ctk.CTkTextbox(root, width=400, height=100, font=textFont)
entryBox.grid(row=2, rowspan=3, column=0, columnspan=5, padx=padding, pady=padding)

resultBox = ctk.CTkTextbox(root, width=400, height=300, font=textFont)
resultBox.grid(row=6, rowspan=9, column=0, columnspan=5, padx=padding, pady=padding)
resultBox.configure(state=ctk.DISABLED)

entryLabel = ctk.CTkLabel(root, text="Enter Expression", font=labelFont)
entryLabel.grid(row=1, rowspan=1, column=0, columnspan=5)

resultLabel = ctk.CTkLabel(root, text="Results", font=labelFont)
resultLabel.grid(row=5, rowspan=1, column=0, columnspan=5)


# Buttons
btnParams = {"width": 70, "height": 3, "font": labelFont}

clearBtn = ctk.CTkButton(root, text="Clear", **btnParams, command=clear)
clearBtn.grid(row=4, rowspan=1, column=6, columnspan=2)

helpBtn = ctk.CTkButton(root, text="Help", **btnParams, command=lambda: mb.showinfo("Help", getReadme()))
helpBtn.grid(row=8, rowspan=1, column=6, columnspan=2)

histBtn = ctk.CTkCheckBox(root, text="Show History", **btnParams, command=toggleHistory)
histBtn.grid(row=7, rowspan=1, column=7, columnspan=2)

solveBtn = ctk.CTkButton(root, text="Solve", **btnParams, command=solve)
solveBtn.grid(row=2, rowspan=1, column=6, columnspan=2)


# Key Binds
root.bind("<Return>", solve)
root.bind("<Control-d>", clear)
root.bind("<Control-w>", lambda _: root.destroy())


root.mainloop()