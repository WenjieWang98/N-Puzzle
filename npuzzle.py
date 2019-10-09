# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 22:39:53 2019

@author: 文杰
"""

import sys
import random
from enum import IntEnum
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QGridLayout, QMessageBox, QPushButton, QComboBox
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtCore import Qt

#directions
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class NPuzzle(QWidget):
    
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0        
        self.gltMain = QGridLayout()

        self.initUI()

    def initUI(self):
        # set the gap
        self.gltMain.setSpacing(10)        
        self.ini('3*3', 'Easy')
        # set width and length
        self.setFixedSize(800, 950)        
        # set the title
        self.setWindowTitle('N-puzzle')
        # set the background color
        self.setStyleSheet("background-color:#99ffff;")    
        
        # Select level
        self.level = QComboBox(self)     
        self.choice_list1 = ['Easy', 'Medium', 'Hard']
        # set tips
        self.level.setToolTip("Select difficulty level")
        # set the position
        self.level.move(240, 20)      
        self.level.setStyleSheet("background-color:white;")        
        self.level.addItems(self.choice_list1) 
        
        # Select size
        self.size = QComboBox(self)        
        self.choice_list2 = ['3*3', '4*4', '5*5','6*6']
        # set tips
        self.size.setToolTip("Select size of the panel")
        # set the position
        self.size.move(60, 20)        
        self.size.setStyleSheet("background-color:white;")        
        self.size.addItems(self.choice_list2) 
        
        # set the restart button
        self.restart = QPushButton("Restart", self)
        # set tips
        self.restart.setToolTip("Restart the game")
        # set the position
        self.restart.move(420, 20)
        # set the event
        self.restart.setStyleSheet("background-color:white;")        
        self.restart.clicked.connect(lambda:self.ini(self.level.currentText(), self.size.currentText()))
        
        # set the automatic completion button
        self.help = QPushButton("Help!", self)
        # set tips
        self.help.setToolTip("Complete the game automaticly")
        # set the position
        self.help.move(600, 20)
        # set the event
        self.help.setStyleSheet("background-color:white;")
        self.help.clicked.connect(self.Astar)     
        
        self.show()
        self.restart.setFocus()  
        
    # initialize the layout   
    def ini(self, level, size):
        # get the size of the panel
        if size == '4*4': 
            self.n = 4
        elif size == '5*5':
            self.n = 5
        elif size =='6*6':
            self.n = 6
        else:
            self.n = 3
            
        if level == 'Hard':
            self.l = 2000
        elif level == 'Medium':
            self.l = 200
        else:
            self.l = 30
        
        # set the step counter
        self.step = 0    
        # set the array        
        self.numbers = list(range(1, self.n*self.n))
        self.numbers.append(0)

        # add numbers to the array
        self.blocks = []
        for row in range(self.n):
            self.blocks.append([])
            for column in range(self.n):
                temp = self.numbers[row * self.n + column]

                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)

        # Disrupting the array, move from the original one randomly so that the game can be completed definitely.
        for i in range(self.l):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        
        for i in reversed(range(self.gltMain.count())): 
            self.gltMain.itemAt(i).widget().setParent(None) 
        
        self.update()

    # key pressing listener   
    def keyPressEvent(self, event):
        key = event.key()        
        if(key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.UP)
        if(key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.DOWN)
        if(key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.LEFT)
        if(key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.RIGHT)
        self.update()
        if self.checkResult():            
            if QMessageBox.Ok == QMessageBox.information(self, 'Result', 'Congratulations！Total Steps: %s' % self.step):
                self.ini(self.level.currentText(), self.size.currentText())
                
    # movement
    def move(self, direction):
        if(direction == Direction.UP): # up
            if self.zero_row != self.n-1:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if(direction == Direction.DOWN): # down
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if(direction == Direction.LEFT): # left
            if self.zero_column != self.n-1:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if(direction == Direction.RIGHT): # right
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1   
     
    # According the sequence of the number in the array, update the panel       
    def update(self):
        for row in range(self.n):
            for column in range(self.n):
                self.gltMain.addWidget(Block(self.blocks[row][column], self.n), row, column)

        self.setLayout(self.gltMain)
        self.step += 1
    
    # check if the game is finished    
    def checkResult(self):
        # check whether the last number is 0
        if self.blocks[self.n-1][self.n-1] != 0:
            return False

        for row in range(self.n):
            for column in range(self.n):
                # no need to check for the last number
                if row == self.n-1 and column == self.n-1:
                    pass
                # check if the numbers are matched
                elif self.blocks[row][column] != row * self.n + column + 1:
                    return False

        return True
    
    
    def Astar(self):
        None
    
# block attributes    
class Block(QLabel):
    
    def __init__(self, number, size):
        super().__init__()

        self.number = number
        self.setFixedSize(540/size, 540/size)

        # set font
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # set font color
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pa)

        # set alignment
        self.setAlignment(Qt.AlignCenter)

        # background color
        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius:10px;")
        else:
            self.setStyleSheet("background-color:orange;border-radius:10px;")
            self.setText(str(self.number))
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NPuzzle()
    sys.exit(app.exec_())
