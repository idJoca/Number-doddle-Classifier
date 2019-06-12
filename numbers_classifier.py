from graphics import *
from nn import NeuralNetwork
import random
from ctypes import windll, Structure, c_long, byref
import math
import pickle

#======================Variables========================

TRAIN_FLAG = True
target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
rects = [] 
colors = []
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
nrAnwsers = 0
is_drawing = False
drawings = []
anwsers = []
rate = 0
correctAnwsers = 0
width = 400
height = 400
resolution = 10
cols = int(width / resolution)
rows = int(height / resolution)

#=======================================================

#======================Functions========================

def move_window(abx, aby, win, width=400, height=400):
    # get screen width and height
    screen_width = win._root().winfo_screenwidth()
    screen_height = win._root().winfo_screenheight()
    abx = (screen_width/abx)
    aby = (screen_height/aby)
    # calculate position x and y coordinates
    x = int((screen_width/abx) - (width/abx))
    y = int((screen_height/aby) - (height/aby))
    win.master.geometry('%dx%d+%d+%d' % (width, height, x, y))


def Mouse(point):
    x = point.getX()
    y = point.getY()
    index = int(math.floor(y / resolution) * cols + math.ceil(x / resolution)) % (rows * cols)
    rects[index].undraw()
    rects[index].setFill("white")   
    colors[index] = 1
    rects[index].draw(win)

def trainBrain():
    random.seed()
    index = random.randint(0, len(numbers)-1)
    text.setText(numbers[index])
    for i in range(0, len(numbers)):
        if (i != index):
            target[i] = 0
        else:
            target[i] = 1    

def showGuess(guesses):
    bet = max(guesses)
    Anwsers = []
    index = guesses.index(bet)     
    text2.setText(numbers[index])
    for i in range(0, len(numbers)):
        if i != index:
            Anwsers.append(0)
        else:
            Anwsers.append(1)    
    global correctAnwsers
    if target == Anwsers:
        correctAnwsers += 1
    rate = correctAnwsers / nrAnwsers * 100
    #print(rate)    
    text3.setText("{0:.2f}".format(rate) + "%")

def testCorrectRate():
    global nrAnwsers, correctAnwsers, rate
    for i in range(0, 100):
        j = random.randint(0, len(drawings)-1)
        guess = brain.guess(drawings[j]).toArray()
        bet = max(guess)
        index = guess.index(bet) 
        Anwsers = []  
        nrAnwsers += 1
        for i in range(0, len(numbers)):
            if i != index:
                Anwsers.append(0)
            else:
                Anwsers.append(1) 
        if anwsers[j] == Anwsers:
            correctAnwsers += 1
    rate = correctAnwsers / nrAnwsers * 100
    print(rate)

def createGrid():
    for i in range(0, int(cols)):
        for j in range(0, int(rows)):
            rect = Rectangle(Point(j * resolution, i * resolution), Point(j * resolution + resolution, i * resolution + resolution))           
            rect.setFill("black")
            colors.append(0)
            rect.setWidth(0)
            rect.draw(win)
            rects.append(rect)

def setupWindows():  
    global win, win2, win3, text, text2WIn3, text2, text3
    #Windows 1 declarations
    win = GraphWin("Number Classifier", width, height)
    win.setBackground("black")
    move_window(200, 300, win)

    #Windows 2 declarations
    win2 = GraphWin("Draw this number:", width, height)
    win2.setBackground("black")
    move_window(1500, 300, win2)

    text = Text(Point(width/2, height/2-100), "Desenhe esse número:")
    text.setSize(14)
    text.setTextColor("white")
    text.draw(win2)

    text = Text(Point(width/2, height/2), "")
    text.setSize(36)
    text.setTextColor("white")
    text.draw(win2)

    #Windows 3 declarations
    win3 = GraphWin("The Ia think it's:", width, height)
    win3.setBackground("black") 
    move_window(800, 300, win3)

    text2WIn3 = Text(Point(width/2, height/2-100), "A IA acha que é:")
    text2WIn3.setSize(14)
    text2WIn3.setTextColor("white")
    text2WIn3.draw(win3)

    text3 = Text(Point(width-50, height-10), "")
    text3.setSize(14)
    text3.setTextColor("white")
    text3.draw(win3)
    
    text2 = Text(Point(width/2, height/2), "")
    text2.setSize(36)
    text2.setTextColor("white")
    text2.draw(win3)
    
    text3.setText("{0:.2f}".format(rate) + "%")

#======================================================

brain = NeuralNetwork((cols * rows), 805, 10)
brain.recoverState()

with open ('drawings', 'rb') as drawingsFile:
    drawings = pickle.load(drawingsFile)

with open ('anwsers', 'rb') as anwsersFile:
    anwsers = pickle.load(anwsersFile)


if (TRAIN_FLAG):
    for i in range(0, 200):
        random.seed()
        index = random.randint(0, len(drawings)-1)
        brain.train(drawings[index], anwsers[index])    
    brain.saveState()   

testCorrectRate()

setupWindows()

createGrid()

trainBrain()

while(True):         
    random.seed()
    absoluteX = win.winfo_rootx()
    absoluteY = win.winfo_rooty()
    absoluteMouseX, absoluteMouseY = win.winfo_pointerxy()
    relativeMouseX = absoluteMouseX - absoluteX
    relativeMouseY = absoluteMouseY - absoluteY
    mouse_click = win.checkMouse()
    if(mouse_click != None):
        is_drawing = not(is_drawing)
        if (not(is_drawing)):  
            nrAnwsers += 1
            #print("entrou")       
            #brain.train(colors.copy(), target)              
            guess = brain.guess(colors.copy())
            showGuess(guess.toArray()) 
            drawings.append(colors.copy())
            anwsers.append(target.copy())            
            with open('drawings', 'wb') as drawingsFile:
                pickle.dump(drawings, drawingsFile)
            with open('anwsers', 'wb') as anwsersFile:
                pickle.dump(anwsers, anwsersFile)
            #print(colors)
            #print(drawings)                                  
            for i in range(0, len(colors)):
                colors[i] = 0 
            #print(guess.toArray())                               
            trainBrain()     
            brain.saveState()  
            

    if(is_drawing):        
        if(mouse_click != None):
            for rect in rects:
                rect.undraw()
        if ((relativeMouseX >= 0 and relativeMouseY >= 0) and (relativeMouseX <= width and relativeMouseY <= height)):
            Mouse(Point(relativeMouseX, relativeMouseY))
    
   
    
