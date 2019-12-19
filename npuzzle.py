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
import copy
import time


#directions
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class NPuzzle(QWidget):
    
    def __init__(self):
        super().__init__() 
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
        self.choice_list2 = ['3*3', '4*4', '5*5']
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
        self.help.clicked.connect(lambda:AStarSearching(Node(self.blocks),self.n).start()) 
        
        self.show()
        self.restart.setFocus()  
        
    # initialize the layout   
    def ini(self, level, size):
        # get the size of the panel
        if size == '4*4': 
            self.n = 4
        elif size == '5*5':
            self.n = 5        
        else:
            self.n = 3
            
        if level == 'Hard':
            self.l = 1000
        elif level == 'Medium':
            self.l = 100
        else:
            self.l = 20
        
        self.blocks = Blocks(self.n,self.l)        
        
        for i in reversed(range(self.gltMain.count())): 
            self.gltMain.itemAt(i).widget().setParent(None) 
        
        self.update(self.blocks)

    # key pressing listener   
    def keyPressEvent(self, event):
        key = event.key()        
        if(key == Qt.Key_Up or key == Qt.Key_W):
            self.blocks.move(Direction.UP)
        if(key == Qt.Key_Down or key == Qt.Key_S):
            self.blocks.move(Direction.DOWN)
        if(key == Qt.Key_Left or key == Qt.Key_A):
            self.blocks.move(Direction.LEFT)
        if(key == Qt.Key_Right or key == Qt.Key_D):
            self.blocks.move(Direction.RIGHT)
        self.update(self.blocks)
        
                
    # According the sequence of the number in the array, update the panel       
    def update(self,blocks):
        for row in range(self.n):
            for column in range(self.n):
                self.gltMain.addWidget(Block(blocks.blocks[row][column], self.n), row, column)

        self.setLayout(self.gltMain)
        if self.blocks.checkResult():            
            self.showMessageRestart(self.blocks.getStepNumber())
        
    def showMessageRestart(self,step):
        if QMessageBox.Ok == QMessageBox.information(self, 'Result', 'Congratulations！Total Steps: %s' % step):
                self.ini(self.level.currentText(), self.size.currentText())
        
class Blocks():
    
    def __init__(self,size,level,blocks=0,zero_row=0,zero_column=0):        
        self.n=size
        self.l=level
        # set the step counter
        self.step = 0 
        self.blocks = []         
        if blocks==0:
            # set the array        
            self.numbers = list(range(1, size*size))
            self.numbers.append(0)                      
            self.zero_row = 0
            self.zero_column = 0 
            self.creatingBlocks(size,level)
        else:
            self.blocks = blocks
            self.zero_row=zero_row
            self.zero_column=zero_column
        
    def creatingBlocks(self,size,level):
        for row in range(size):
            self.blocks.append([])
            for column in range(size):
                temp = self.numbers[row * size + column] # find the corresponding number in numbers list

                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)

        # Disrupting the array, move from the original one randomly so that the game can be completed definitely.
        for i in range(level):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.step = 0       
        
    # movement        
    def move(self, direction):
        if(direction == Direction.UP): # up
            if self.zero_row != self.n-1:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
                self.step = self.step + 1
        if(direction == Direction.DOWN): # down
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
                self.step = self.step + 1
        if(direction == Direction.LEFT): # left
            if self.zero_column != self.n-1:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
                self.step = self.step + 1
        if(direction == Direction.RIGHT): # right
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1
                self.step = self.step + 1      
    
    # get the cost step
    def getStepNumber(self):
        return self.step
      
    # get the direction that can be moved    
    def getDirection(self):
        a=[]
        if(self.zero_column!=0):
            a.append(Direction.RIGHT)
        if(self.zero_column!=self.n-1):
            a.append(Direction.LEFT)
        if(self.zero_row!=0):
            a.append(Direction.DOWN)
        if(self.zero_row!=self.n-1):
            a.append(Direction.UP)             
        return a  
    
    # calculate the Manhattan Distance of every blocks to its goal position  
    def getManDis(self):
        t=0
        it=0
        jt=0   
        for i in range(0,self.n):
            for j in range(0,self.n):
                # do not count the blank block
                if(self.blocks[i][j]!=0):
                    it=(self.blocks[i][j]-1)/self.n
                    jt=(self.blocks[i][j]-1)%self.n               
                    t=t+abs(it-i)+abs(jt-j)                    
        return t
    
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
    
    def clone(self):
        a=copy.deepcopy(self.blocks)
        return Blocks(self.n,self.l,a,self.zero_row,self.zero_column)
    
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

# node class, is used in doing A* algorithm        
class Node:
    # initialize
    def __init__(self,blocks, g = 0, h = 0):
        self.blocks=blocks       
        self.father=None
        self.g = g             
        self.h = h
    
    # set the parent node
    def setParent(self,fa):
        self.father=fa  
        
    # get f(n) (total cost)    
    def getFn(self):
        fn=self.g+self.getHn() #A*
        #fn=self.g #greedy
        return fn
    
    # get h(n) (cost to the goal state)   
    def getHn(self):
        self.h=self.blocks.getManDis()
        return self.h
    
    def setG(self, g):
        self.g = g
        
    # get g(n) (cost to get to the current state)    
    def getG(self):        
        return self.g
    
    def checkEnd(self):
        result = self.blocks.checkResult()
        return result
    
    def getBlocks(self):
        return self.blocks.blocks

class AStarSearching:
    
    def __init__(self,root,size):
        
        self.openList = []        
        self.closeList = []       
        self.startNode = root         
        self.currentNode = root        
        self.pathlist = []        
        self.step = 0 
        self.n = size
    
    # get the node with minimum cost in the open list
    def getMinFNode(self):
        
        nodeTemp = self.openList[0]  
        for node in self.openList:  
            if node.getFn() < nodeTemp.getFn():  
                nodeTemp = node  
        return nodeTemp
    
    # judge whether the node is in open list
    def nodeInOpenlist(self,node):
        for nodeTmp in self.openList:  
            if nodeTmp.getBlocks() == node.getBlocks():  
                return True  
        return False
    
    # judge whether the node is in close list
    def nodeInCloselist(self,node):
        for nodeTmp in self.closeList:  
            if nodeTmp.getBlocks() == node.getBlocks():  
                return True  
        return False
    
    # return the specific node in openList
    def getNodeFromOpenList(self,node):  
        for nodeTmp in self.openList:  
            if nodeTmp.getBlocks() == node.getBlocks():  
                return nodeTmp  
        return None
    
    # check if it reaches the goal state
    def endNodeInOpenList(self):         
        for nodeTmp in self.openList:             
            if nodeTmp.blocks.checkResult():  
                return nodeTmp
        return None
    
    # search for one node
    def searchOneNode(self,node):
        
        # ignore the node which is in the closed list
        if self.nodeInCloselist(node):  
            return  
        #calculate g
        gTemp = self.step

        # If the node is not in the open list, add into it
        if self.nodeInOpenlist(node) == False:
            node.setG(gTemp)            
            self.openList.append(node)
            node.father = self.currentNode
        #If the current node is the open list, check whether the g is smaller
        #if it is smaller calculate g again
        else:
            nodeTmp = self.getNodeFromOpenList(node)
            if self.currentNode.g + gTemp < nodeTmp.g:
                nodeTmp.g = self.currentNode.g + gTemp  
                nodeTmp.father = self.currentNode  
        return;
     
    # search for the next block to move
    def searchNext(self):
        self.step += 1
        for i in self.currentNode.blocks.getDirection():
            blocksTemp = self.currentNode.blocks.clone()
            blocksTemp.move(i)
            self.searchOneNode(Node(blocksTemp));
        return;
    
    # start searching    
    def start(self):   
        #self.a =0
        tt = time.time()
        self.startNode.setG(self.step);
        self.openList.append(self.startNode)
        while True:
            # get the node in open list with minimum fn
            # add it to the close list and delete it from the open list
            #self.a=self.a+1
            #print(self.a)
            self.currentNode = self.getMinFNode()
            self.closeList.append(self.currentNode)
            self.openList.remove(self.currentNode)
            self.step = self.currentNode.getG();
            
            self.searchNext();
            
            endNode = self.endNodeInOpenList()
            if endNode!=None:
                print("Step Number:",endNode.g)
                print("Visited Nodes:",len(self.closeList)) 
                print('Time used: {} sec'.format(time.time()-tt))
                print("--------")
                while True:
                    self.pathlist.append(endNode.getBlocks())
                    if endNode.father != None:
                        endNode = endNode.father
                    else:
                        self.showPath() 
                        print("--------")                        
                        break
                break
            elif len(self.openList) == 0:
                break
            
    def showPath(self):
        for node in self.pathlist[::-1]:
            self.showMap(node)
            
    def showMap(self,array2d):
        for x in range(0, self.n):
            for y in range(0, self.n):
                print(array2d[x][y], end=',')
            print(" ")
        print("--------")
        return; 
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NPuzzle()
    sys.exit(app.exec_())
