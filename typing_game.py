import random
import time


class TypingTracker(object):

    def __init__(self, wordCount, words100, words3000):
        wordString = ""

        for i in range(0, wordCount):
            if i % 2 == 1:
                wordString += (random.choice(words3000)).strip() + ' '
            else:
                wordString += (random.choice(words100)).strip() + ' '

        wordString = wordString.strip()

        self.index = 0
        self.correctWordString = wordString
        self.numChars = len(self.correctWordString)
        self.wordCount = wordCount



        self.currentWordString = ''
        self.currentCorrectChars = []
        for i in range(0, self.numChars):
            self.currentCorrectChars.append(True)


        self.totalTypos = 0
        self.totalKeyStrokes = 0
        self.keyStrokeTimes = []
        for i in range(0, self.numChars):
            self.keyStrokeTimes.append(0)

    def processInput(self, input):
        self.totalKeyStrokes += 1

        if input == 'del':
            if self.index > 0:
                self.index -= 1
                self.currentWordString = self.currentWordString[0:self.index]
        elif input == ' ':
            self.currentCorrectChars[self.index] = True if (self.correctWordString[self.index] == ' ') else False

            if self.index > 0:
                while (not self.correctWordString[self.index - 1] == ' '):
                    self.index += 1
        elif input.isalpha():
            self.currentWordString += input
            if input == self.correctWordString[self.index]:
                self.currentCorrectChars[self.index] = True
            else:
                self.currentCorrectChars[self.index] = False
                self.totalTypos += 1
            self.keyStrokeTimes[self.index] = time.time()

            self.index += 1

        elif input == '`':
            self.currentWordString += input
            self.keyStrokeTimes[self.index] = time.time()
            self.index += 1

        # else do nothing: this input is not important

    def calculateStats(self):
        numCorrect = 0
        for correct in self.currentCorrectChars:
            if correct: numCorrect += 1
        return ((self.keyStrokeTimes[-1] - self.keyStrokeTimes[0]),
                self.wordCount / (self.keyStrokeTimes[-1] - self.keyStrokeTimes[0]) * 60,
                self.totalTypos, 1 - self.totalTypos / self.totalKeyStrokes,
                numCorrect / self.numChars)

    def reset(self, wordCount, words100, words3000):
        # This is basically just a repeat of the constructor, without creating a new object
        wordString = ""
        for i in range(0, wordCount):
            if i % 2 == 1:
                wordString += (random.choice(words3000)).strip() + ' '
            else:
                wordString += (random.choice(words100)).strip() + ' '
        wordString = wordString.strip()
        self.index = 0
        self.correctWordString = wordString
        self.numChars = len(self.correctWordString)
        self.wordCount = wordCount
        self.currentWordString = ''
        self.currentCorrectChars = []
        for i in range(0, self.numChars):
            self.currentCorrectChars.append(True)
        self.totalTypos = 0
        self.totalKeyStrokes = 0
        self.keyStrokeTimes = []
        for i in range(0, self.numChars):
            self.keyStrokeTimes.append(0)


def initializeFiles():
    words100 = []
    with open('popular100.txt', 'r') as file100:
        for line in file100:
            words100.append(line)

    words3000 = []
    with open('popular3000.txt', 'r') as file3000:
        for line in file3000:
            words3000.append(line)

    return (words100, words3000)

