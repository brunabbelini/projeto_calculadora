from display import Display
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QGridLayout, QPushButton
from util import isEmpty, isNumOrDot, isValidNumber
from variables import MEDIUM_FONT_SIZE


class Button(QPushButton): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)


class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._gridMask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['',  '0', '.', '='],
        ]
        self.display = display
        self._makeGrid()

    def _makeGrid(self):
        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')

                self.addWidget(button, rowNumber, colNumber)
                buttonSlot = self._makeButtonDisplaySlot(
                    self._insertButtonTextToDisplay,
                    button,
                )
                button.clicked.connect(buttonSlot) # type: ignore

    # def _makeGrid(self):
    #     for i, row in enumerate(self._gridMask):
    #         for j, buttonText in enumerate(row):
    #             if buttonText == '':
    #                 continue
                
    #             if buttonText == '0':
    #                 button = Button(buttonText)
    #                 # self.addWidget(button, i, j, 1, 2)
    #                 self.addWidget(button, 4, 0, 1, 2)
    #                 # j += 1
    #             else: 
    #                 button = Button(buttonText)
    #                 if not isNumOrDot(buttonText) and not isEmpty(buttonText):
    #                     button.setProperty('cssClass', 'specialButton')

    #                 self.addWidget(button, i, j)
    #                 buttonSlot = self._makeButtonDisplaySlot(
    #                     self._insertButtonTextToDisplay,
    #                     button,
    #                 )
    #                 button.clicked.connect(buttonSlot) # type: ignore
                    

    def _makeButtonDisplaySlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        self.display.insert(buttonText)
        