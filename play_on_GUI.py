import customtkinter
import tkinter
from typing_game import *

LIGHT_BLUE = "#9badbd"
MUTED_BLUE = "#6f819e"
DEEP_BLUE = "#203659"
LIGHT_YELLOW = "#958a72"
MUTED_YELLOW = "#decaa2"
DEEP_YELLOW = "#e2b714"
WHITE = "#ffffff"
LGIHT_GRAY = "#ebeef4"
GRAY = "#9d9d9d"
DARK_GRAY = "#494a4d"
DARK_DARK_GRAY = "#323437"
BLACK = "#000000"
WARNING_RED = "#f75252"


def processInput(char, action):
    if (myTracker.index >= myTracker.numChars):
        return False

    if (action == '0'):
        myTracker.processInput('del')
    elif (action == '1'):
        myTracker.processInput(char)
    elif (action == '-1'):
        if (not inputEntry.focus_get() == '.!ctkframe.!ctkentry.!entry'):
            inputEntry.focus_set()
        return True

    outputBox.configure(state=tkinter.NORMAL)

    outputBox.tag_remove('red', '1.0', 'end')
    outputBox.tag_remove('grey', '1.0', 'end')
    outputBox.tag_remove('cursor', '1.0', 'end')

    for i in range(0, myTracker.numChars):
        if (not myTracker.currentCorrectChars[i]):
            outputBox.tag_add('red', f'1.{i}', f'1.{i + 1}')


    outputBox.configure(state=tkinter.DISABLED)
    outputBox.tag_add('grey', f'1.{myTracker.index}', 'end')
    outputBox.tag_add('cursor', f'1.{myTracker.index}', f'1.{myTracker.index + 1}')
    progressLabel.configure(text=f"{myTracker.index} / {myTracker.numChars}")

    if (myTracker.index >= myTracker.numChars):
        (totalTime, wordsPerMinute, numTypos, percentCorrectStrokes, percentCorrectChars) = myTracker.calculateStats()
        feedbackDescription.configure(text=
                                      f"- Total elapsed time: {'{:.2f}'.format(totalTime)} seconds\n" +
                                      f"- WPM: {'{:.2f}'.format(wordsPerMinute)} words/min\n" +
                                      f"- Number of typos: {numTypos}\n" +
                                      f"- Correct inputs: {'{:.2f}'.format(percentCorrectStrokes * 100)}%\n" +
                                      f"- Correct final characters: {'{:.2f}'.format(percentCorrectChars * 100)}%\n")
        return False
    return True


def updateWordCountLabel(wordCount):
    wordCountLabel.configure(text="Current word count: " + '{:.0f}'.format(wordCount))


def restartGame():
    inputEntry.delete('0', 'end')
    outputBox.configure(state=tkinter.NORMAL)
    outputBox.tag_remove('red', '1.0', 'end')
    outputBox.tag_remove('grey', '1.0', 'end')
    outputBox.tag_remove('cursor', '1.0', 'end')
    outputBox.delete('1.0', 'end')

    wordCount = int(wordCountSlider.get())
    myTracker.reset(wordCount, words100, words3000)

    outputBox.insert('end', myTracker.correctWordString)

    outputBox.tag_add('cursor', '1.0', '1.1')
    outputBox.tag_add('grey', '1.0', 'end')
    outputBox.configure(state=tkinter.DISABLED)

    progressLabel.configure(text=f"{myTracker.index} / {myTracker.numChars}")

    inputEntry.focus_force()


if __name__ == '__main__':
    (words100, words3000) = initializeFiles()

    myTracker = TypingTracker(15, words100, words3000)


    customtkinter.set_default_color_theme("dark-blue")
    customtkinter.set_appearance_mode("dark")
    textColour = "#E2B714"


    mainWindow = customtkinter.CTk(fg_color=(LGIHT_GRAY, BLACK))
    mainWindow.title("Typing Game")
    mainWindow.geometry("1400x500")
    mainWindow.grid_columnconfigure((0, 2), weight=0)
    mainWindow.grid_columnconfigure((1,), weight=1)
    mainWindow.grid_rowconfigure(0, weight=1)

    leftSidebarFrame = customtkinter.CTkFrame(mainWindow, width=140, corner_radius=0, bg_color=(LGIHT_GRAY, DARK_GRAY))
    leftSidebarFrame.grid(row=0, column=0, sticky='nsew', rowspan=2)
    leftSidebarFrame.grid_rowconfigure(2, weight=1)

    titleLabel = customtkinter.CTkLabel(leftSidebarFrame,
                                        text="Typing Game",
                                        font=("Verdana", 30, tkinter.font.BOLD),
                                        text_color=(DEEP_BLUE, DEEP_YELLOW))
    titleLabel.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

    welcomeLabel = customtkinter.CTkLabel(leftSidebarFrame, text="type as fast as you can!",
                                          font=("Verdana", 30, tkinter.font.BOLD),
                                          text_color=(DEEP_BLUE, DEEP_YELLOW))
    welcomeLabel.grid(row=1, column=0, padx=10, pady=10, sticky='nw')


    wordCountLabel = customtkinter.CTkLabel(leftSidebarFrame, text="Current word count: 15",
                                            font=("Consolas", 20),
                                            text_color=(DEEP_BLUE, DEEP_YELLOW))
    wordCountLabel.grid(row=3, column=0, sticky='w', padx=20, pady=0)


    wordCountSlider = customtkinter.CTkSlider(leftSidebarFrame, button_color=(DEEP_BLUE, DEEP_YELLOW),
                                              from_=1, to=50, number_of_steps=49, command=updateWordCountLabel)
    wordCountSlider.grid(row=4, column=0, sticky='w', padx=20, pady=0)
    wordCountSlider.set(15)

    wordCountSetButton = customtkinter.CTkButton(leftSidebarFrame, corner_radius=13,
                                                 border_width=2,
                                                 border_color=(DEEP_BLUE, DEEP_YELLOW),
                                                 fg_color='transparent',
                                                 hover_color=(LIGHT_BLUE, LIGHT_YELLOW),
                                                 text="Restart",
                                                 text_color=(DEEP_BLUE, DEEP_YELLOW),
                                                 font=("Consolas", 28),
                                                 command=restartGame)
    wordCountSetButton.grid(row=5, column=0, sticky='sw', padx=20, pady=20)


    inputEntry = customtkinter.CTkEntry(master=mainWindow, validate='all', width=0, height=0)
    validationCommandName = inputEntry.register(processInput)
    inputEntry.configure(validatecommand=(validationCommandName, '%S', '%d'))
    inputEntry.grid(row=0, column=1, sticky='nw', padx=50, pady=50)

    outputBox = customtkinter.CTkTextbox(mainWindow, corner_radius=10,
                                         wrap='word',
                                         border_spacing=100,
                                         fg_color=(WHITE, DARK_DARK_GRAY),
                                         font=('Consolas', 28),
                                         text_color=(DEEP_BLUE, WHITE))
    outputBox.insert('end', myTracker.correctWordString)
    outputBox.tag_config('red', foreground=WARNING_RED, underline=1)
    outputBox.tag_config('grey', foreground=GRAY, underline=0)
    outputBox.tag_config('cursor', foreground=BLACK, background=MUTED_YELLOW, underline=0)
    outputBox.tag_add('cursor', '1.0', '1.1')
    outputBox.tag_add('grey', '1.0', 'end')
    outputBox.configure(state=tkinter.DISABLED)
    outputBox.grid(row=0, column=1, padx=7, pady=7, sticky='nsew')


    progressLabel = customtkinter.CTkLabel(mainWindow, bg_color=(WHITE, DARK_DARK_GRAY),
                                           fg_color='transparent',
                                           font=("Consolas", 20),
                                           text_color=(DEEP_BLUE, DEEP_YELLOW),
                                           text=f"{myTracker.index} / {myTracker.numChars}", )
    progressLabel.grid(row=0, column=1, sticky='s', pady=70)


    rightSidebarFrame = customtkinter.CTkFrame(mainWindow, width=200, corner_radius=0, bg_color=(WHITE, DARK_GRAY))
    rightSidebarFrame.grid(row=0, column=2, sticky='nsew', rowspan=2)
    rightSidebarFrame.rowconfigure(1, weight=1)


    feedbackLabel = customtkinter.CTkLabel(rightSidebarFrame, text="              Stats              ",
                                           font=("Verdana", 24, tkinter.font.BOLD),
                                           justify='left',
                                           text_color=(DEEP_BLUE, DEEP_YELLOW))
    feedbackLabel.grid(row=0, column=0, sticky='nw', padx=5, pady=20)


    feedbackDescription = customtkinter.CTkLabel(rightSidebarFrame, text="",
                                                 font=("Consolas", 14),
                                                 justify='left',
                                                 text_color=(DEEP_BLUE, DEEP_YELLOW))
    feedbackDescription.grid(row=1, column=0, sticky='nw', padx=5, pady=0)



    inputEntry.after(1000, lambda: inputEntry.focus_force())
    mainWindow.mainloop()

