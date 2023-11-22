file = open('VDData.csv','a')
file.close()

#Import the following:
#    sys: parameters specific to os
#    PyQt modules
#    Generated .py code from designer
import random
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MyWidgets import *
from stackedVDGame import *

#create a QApplication: controls the execution of your application
app = QApplication(sys.argv)

#Create a QMain Window: the main window of your app
window = QMainWindow()

#Create and add the generated interface to the main window
ui = Ui_MainWindow()
ui.setupUi(window)

# CREATE DATA FILE HEADER
file = open('VDData.csv','r')
window.contents = file.read()
file.close()
if window.contents == '': #if file is empty write the following headers
    file = open('VDData.csv','w')
    file.write('Participant ID,Gender,Height (in),Weight (lbs),Age,CAGE Q1,CAGE Q2,CAGE Q3,CAGE Q4,Task Condition,Tasks Performed,\n')
    file.close()


####### BEGIN EXPERIMENT CODE - set experiment to first page ###########
ui.partID.setPlaceholderText('####')
ui.VirtualDayExp.setCurrentIndex(0)
ui.errorConsent.hide()

# CONSENT PAGE ERROR MESSAGE
def consent():
    partID = ui.partID.text()
    if (partID.isdigit() == False) or (len(partID) != 4):     # If participant ID is not 4 digits (numbers only) then show error
        ui.errorConsent.setText("EXPERIMENTER: Enter valid participant ID")
        ui.errorConsent.show()
    elif not ui.consentBox.isChecked():    # If consent box not checked show error
        ui.errorConsent.setText ("PLEASE CONFIRM YOUR CONSENT TO PARTICIPATE IN THIS EXPERIMENT")
        ui.errorConsent.show()
    else:
        file = open('VDData.csv','a')    # Write participant ID in CSV
        file.write(str(partID) + ',')
        file.close()
        ui.VirtualDayExp.setCurrentIndex(1)   # Advance to next page
# CALL CONSENT ON NEXT
ui.submitConsent.clicked.connect(consent)


##### DEMO PAGE #####
ui.errorDemo.hide()
ui.errorAge.hide()

# CUSTOMIZE ERROR MESSAGE
def checkError():
    file = open('VDData.csv','a')
    if not ui.Male.isChecked() and not ui.Female.isChecked() and not ui.Other.isChecked():
        ui.errorDemo.setText("Please select Male, Female, or Other for gender")
        ui.errorDemo.show()
    elif ui.Height.value() <= 30:
        ui.errorDemo.setText("Please enter a valid height, in inches")
        ui.errorDemo.show()
    elif ui.Weight.value() <= 50:
        ui.errorDemo.setText("Please enter a valid weight, in pounds")
        ui.errorDemo.show()
    elif ui.Age.value() < 18:
        ui.errorAge.show()
    else:
        ui.VirtualDayExp.setCurrentIndex(2)
        if ui.Male.isChecked():
            file.write(str('M') + ',')
        elif ui.Female.isChecked():
            file.write(str('F') + ',')
        else:
            file.write(str('O') + ',')
        file.write(str(ui.Height.value()) + ',' + str(ui.Weight.value()) + ',' + str(ui.Age.value()) + ',')
        file.close()
ui.submitButton.clicked.connect(checkError)

##### CAGE PAGE #####
ui.errorCAGE.hide()
def checkCAGE():
    file = open('VDData.csv','a')
    if (not ui.Y1.isChecked() and not ui.N1.isChecked()) or (not ui.Y2.isChecked() and not ui.N2.isChecked()) or (not ui.Y3.isChecked() and not ui.N3.isChecked()) or (not ui.Y4.isChecked() and not ui.N4.isChecked()):
        ui.errorCAGE.show()
    else:
        ui.VirtualDayExp.setCurrentIndex(3)
        file.write(str(ui.Y1.isChecked()) + ',' + str(ui.Y2.isChecked()) + ',' + str(ui.Y3.isChecked()) + ',' + str(ui.Y4.isChecked()) + ',')
    file.close()
ui.submitButton_2.clicked.connect(checkCAGE)

##### INSTRUCTIONS PAGE #####
def instructionsOK():
    # DIVIDE PARTICIPANTS INTO EQUAL TASK CONDITIONS
    partLines = window.contents.split('/n')
    if len(partLines) > 1:
        prevPart = partLines[-1].split(',')
        if prevPart[9] == 1:    # If there is a previous participant get their Task Condition
            window.condit = 2
        else:
            window.condit = 1
    else:    # If there is no previous participant randomly assign a Task Condition
        window.condit = random.randint(1,2)
    file = open('VDData.csv', 'a')
    file.write(str(window.condit) + ',')  # Note current participant condition
    file.close()
    ui.VirtualDayExp.setCurrentIndex(4)

ui.OKButton.clicked.connect(instructionsOK)

###### VIRTUAL DAY GAME PAGE ######
ui.Event.hide()
ui.taskWindow.hide()
ui.startTasks.hide()
ui.debriefBtn.hide()
ui.startCard.setEnabled(False)
ui.eventCard.setDisabled(True)
ui.performTask.setDisabled(True)

# DISPLAY FIRST MESSAGE/PROMPT
ui.Reminder.setText("Welcome to Virtual Day game. Click START to begin")

# MAKE MARKER CLICKABLE
ui.marker = clickableLabel(ui.gamePage)
ui.marker.setGeometry(740,520,31,31)
markerPic = QPixmap('blue-marker.png')
ui.marker.setPixmap(markerPic)
ui.marker.setScaledContents(True)
ui.marker.setEnabled(False)
ui.marker.hide()

# MAKE START LABEL CLICKABLE
ui.start = clickableLabel(ui.gamePage)
ui.start.setGeometry(740,520,61,31)
startPic = QPixmap('start_tile.png')
ui.start.setPixmap(startPic)
ui.start.setScaledContents(True)
ui.start.setEnabled(True)

# MAKE DIE CLICKABLE
ui.dice = clickableLabel(ui.gamePage)
ui.dice.setGeometry(580,280,41,41)
diePic = QPixmap('dice-' + str(random.randint(1,6)) + '.png')
ui.dice.setPixmap(diePic)
ui.dice.setScaledContents(True)
ui.dice.hide()

def startFunction():
    ui.marker.setGeometry(740,520,31,31)
    ui.marker.show()
    ui.startCard.setEnabled(True)
    ui.start.deleteLater()
    ui.Reminder.setText("Please pick up a start card\nto see your tasks for the day")
ui.start.clicked.connect(startFunction)

# WHEN START CARD CLICKED ASSIGN TASKS BASED ON CONDITION
def pickUpStartCard():
    if window.condit == 1:
        ui.Task1Txt.setText("Take antibiotics at breakfast and dinner")
        ui.Task2Txt.setText("Submit essay at 21:00")
    else:
        ui.Task1Txt.setText("Attend lecture at 12:00 and 15:00")
        ui.Task2Txt.setText("Take cold medicine with lunch")
    ui.startTasks.setGeometry(280,160,291,201)
    ui.startTasks.setCurrentIndex(0)
    ui.startTasks.show()
    ui.startCard.setDisabled(True)     # User will not be able to view start card again
ui.startCard.clicked.connect(pickUpStartCard)

# NEXT AND OK BUTTON FUNCTIONALITY WITHIN START CARD
window.count = 0
def nextTask():
    ui.startTasks.setCurrentIndex(1)
    ui.startTaskError.hide()
    window.count +=1
    return window.count
ui.nextTaskBtn.clicked.connect(nextTask)

def OKTask():
    if window.count > 1:     # User cannot advance before repeating task instructions at least once
        ui.startTasks.hide()
        ui.dice.show()
        ui.eventCard.setEnabled(True)
        ui.performTask.setEnabled(True)
        window.needEventCard = False
        ui.Reminder.setText("Roll die by clicking on it")
    else:
        ui.startTaskError.show()
ui.OKTaskBtn.clicked.connect(OKTask)

# BACK BUTTON IN START CARD
def back():
    ui.startTasks.setCurrentIndex(0)
ui.backBtn.clicked.connect(back)

def animateDice():
    window.count += 1
    diePic = QPixmap('dice-' + str(window.count) + '.png')
    ui.dice.setScaledContents(True)
    ui.dice.setPixmap(diePic)
    if window.count == 7:
        window.dietimer.stop()
        window.dieNum = random.randint(1, 6)
        newdie = QPixmap('dice-' + str(window.dieNum) + '.png')
        ui.dice.setScaledContents(True)
        ui.dice.setPixmap(newdie)
        window.count = 1

# DICE ROLL FUNCTION
def diceRoll():
    window.currentX = ui.marker.x()    # Get current marker coordinates
    window.currentY = ui.marker.y()
    window.count = 1
    window.dietimer = QTimer()
    window.dietimer.timeout.connect(animateDice)
    window.dietimer.start(100)
    ui.Reminder.setText("Click on your game piece to advance\nit the number shown on die")
    ui.marker.setEnabled(True)
    ui.dice.setEnabled(False)

ui.dice.clicked.connect(diceRoll)

# MARKER MOVEMENT FUNCTION
def makingMoves():
    window.x = ui.marker.x()
    window.y = ui.marker.y()
    moved = False
    if window.currentY == 520:    # if position of marker is on the bottom row and
        if (window.currentX - window.dieNum * 30) > 380:    # result of die roll doesn't overshoot then leftward movement
            if window.x > (window.currentX - window.dieNum * 30):   # until new position is reached
                ui.marker.setGeometry(window.x - 10,520,31,31)
                moved = True
        else:      # marker must turn upward at some point
            if window.x > 380:      # while marker is still along bottom row keep moving left
                ui.marker.setGeometry(window.x - 10,520,31,31)
                moved = True
            else:     # while the marker does not exceed the remaining moves, go upward
                if window.y > (520 - (window.dieNum * 30 - (window.currentX - 380))):
                    ui.marker.setGeometry(380,window.y - 10,31,31)
                    moved = True
    elif window.currentX == 380:     # position of marker is on the left
        if (window.currentY - window.dieNum * 30) > 160:    # if die roll doens't overshoot then move marker upward
            if window.y > (window.currentY - window.dieNum * 30):    # until new position is reached
                ui.marker.setGeometry(380,window.y - 10,31,31)
                moved = True
        else:    # if marker needs to turn right at some point
            if window.y > 160:   # while marker is still along left keep moving up
                ui.marker.setGeometry(380,window.y - 10,31,31)
                moved = True
            else:     # while marker does not exceed the remaining moves, go right
                if window.x < (380 + (window.dieNum * 30 - (window.currentY - 160))):
                    ui.marker.setGeometry(window.x + 10,160,31,31)
                    moved = True
    elif window.currentY == 160:
        if (window.currentX + window.dieNum * 30) < 770:
            if window.x < window.currentX + window.dieNum * 30:
                ui.marker.setGeometry(window.x + 10,160,31,31)
                moved = True
        else:
            if window.x < 770:
                ui.marker.setGeometry(window.x + 10,160,31,31)
                moved = True
            else:
                if window.y < (160 + (window.dieNum * 30 - (770 - window.currentX))):
                    ui.marker.setGeometry(770,window.y + 10,31,31)
                    moved = True
    elif window.currentX == 770:
        if (window.currentY + window.dieNum * 30) <= 490:
            if window.y < (window.currentY + window.dieNum * 30):
                ui.marker.setGeometry(770,window.y + 10,31,31)
                moved = True
        else:
            if window.y < 490:
                ui.marker.setGeometry(770,window.y + 10,31,31)
                moved = True
            else:
                ui.marker.setGeometry(770,490,31,31)
                ui.debriefBtn.show()
                window.timer.stop()
                ui.performTask.setDisabled(True)
                ui.eventCard.setDisabled(True)
                ui.marker.setDisabled(True)
    # If event tile is passed (except when marker is already sitting on event tile at die roll): set needEventCard variable to True, and disable die
    if not ((window.currentX == 650 and window.currentY == 520) or (window.currentX == 530 and window.currentY == 520) or (window.currentX == 380 and window.currentY == 400) or (window.currentX == 410 and window.currentY == 160) or (window.currentX == 770 and window.currentY == 160)):
        if (window.y == 520 and (window.x == 650 or window.x == 530)) or (window.x == 380 and window.y == 400) or (window.y == 160 and (window.x == 410 or window.x == 770)):
            window.needEventCard = True
            ui.dice.setEnabled(False)
    if (window.currentX == 650 and window.currentY == 520) and window.x == 530:    # If the marker is sitting on first event tile and passes the second event tile, need event card
        window.needEventCard = True
        ui.dice.setEnabled(False)
    # Once marker stops moving: if player needs Event Card, set reminder text. If not, tell player to roll again.
    if moved == False:
        window.finalx = ui.marker.x()
        window.finaly = ui.marker.y()
        window.timer.stop()
        ui.marker.setEnabled(False)
        if not (window.finalx == 770 and window.finaly == 490): # If marker is not on last square
            if window.needEventCard == False:
                ui.Reminder.setText("Roll the die to continue")
            else:
                ui.Reminder.setText("Please pick up an\nEvent Card")
            # Once marker stops moving set time label to display corresponding time
            if window.finaly == 520:
                hours = (710 - window.finalx)/90
                hour = int(hours) + 8
                min = (hours - int(hours)) * 60
            elif window.finalx == 380:
                hours = (520 - window.finaly)/90
                hour = int(hours) + 11
                min = ((hours - int(hours)) + (2/3)) * 60
            elif window.finaly == 160:
                hours = (window.finalx - 380)/90
                hour = int(hours) + 15
                min = ((hours - int(hours)) + (2/3)) * 60
            elif window.finalx == 770:
                hours = (window.finaly - 160)/90
                hour = int(hours) + 20
                min = (hours - int(hours)) * 60
            ui.Timer.setText(str("{:02}".format(hour) + ":" + str("{:02}".format(round(min))))) # Display time as 2 hour digits and 2 minute digits
        else:     # Marker is on last square and game is done
            ui.Reminder.setText("You have completed the game.\nThanks for playing!")
            ui.debriefBtn.show()
            ui.Timer.setText("00:00")

# CONTINUE TO DEBFRIEF BUTTON
def nextPage():
    file = open("VDData.csv", "a")
    file.write("\n")
    file.close()
    ui.VirtualDayExp.setCurrentIndex(5)
ui.debriefBtn.clicked.connect(nextPage)

# MARKER ANIMATION FUNCTION USING QTIMER
def animate():
    window.timer = QTimer()
    window.timer.timeout.connect(makingMoves)
    window.timer.start(50)
    ui.dice.setEnabled(True)
ui.marker.clicked.connect(animate)

# EVENT CARD
def event():
    if window.needEventCard == True:
        ui.dice.hide()
        ui.marker.hide()
        window.eventShown = True
        rand = random.randint(1, 2)
        ui.Event.setGeometry(100, 130, 671, 441)
        ui.eventError.hide()
        # Depending on which event tile is passed, randomly show an event card that corresponds with that tile
        if window.finaly == 520 and window.finalx <= 650 and window.finalx >= 560:
            ui.eventTxt.setText("You are having breakfast. What do you eat?")
            window.eventVar = "Breakfast"
            if rand == 1:
                eventPicture = QPixmap('breakfast1.jpeg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("Eggs and toast")
                ui.option2.setText("Fruit and coffee")
                ui.option3.setText("Cappuccino and a pastry")
                ui.Event.show()
            else:
                eventPicture = QPixmap('breakfast2.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("Pancakes and bacon")
                ui.option2.setText("A smoothie")
                ui.option3.setText("Bagel and cream cheese")
                ui.Event.show()
        elif window.finaly < 430 and window.finalx == 380:
            ui.eventTxt.setText("You are having lunch. What do you eat?")
            window.eventVar = "Lunch"
            if rand == 1:
                eventPicture = QPixmap('lunch1.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("A sandwich and soup")
                ui.option2.setText("A protein shake")
                ui.option3.setText("Slice of pizza")
                ui.Event.show()
            else:
                eventPicture = QPixmap('lunch2.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("Chicken caesar salad")
                ui.option2.setText("Pasta bowl")
                ui.option3.setText("Skip lunch")
                ui.Event.show()
        elif window.finaly == 520 and window.finalx < 560 :
            if rand == 1:
                ui.eventTxt.setText("Time to head to the library. What are you working on today?")
                window.eventVar = "Library"
                eventPicture = QPixmap('library.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("Read a psychology textbook")
                ui.option2.setText("Program an experiment in Python")
                ui.option3.setText("Email your professors about the unreasonable workload")
                ui.Event.show()
            else:
                ui.eventTxt.setText("You decide to swing by the gym. What kind of workout do you do?")
                window.eventVar = "Gym"
                eventPicture = QPixmap('gym.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("A bootcamp style class")
                ui.option2.setText("Swim a few laps")
                ui.option3.setText("Hit the weights")
                ui.Event.show()
        elif window.finalx > 380 and window.finalx <= 560 and window.finaly == 160:
            if rand == 1:
                ui.eventTxt.setText("You are having afternoon tea with your friend Jill. What do you get?")
                window.eventVar = "Tea"
                eventPicture = QPixmap('tea.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("Black tea and a scone")
                ui.option2.setText("Chai latte")
                ui.option3.setText("Herbal tea and a sandwich")
                ui.Event.show()
            else:
                ui.eventTxt.setText("﻿You go to the store to buy a birthday gift for your niece. What do you buy?")
                window.eventVar = "Store"
                eventPicture = QPixmap('store.jpg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("A dollhouse")
                ui.option2.setText("A sketchpad and set of colored pencils")
                ui.option3.setText("A toy guitar")
                ui.Event.show()
        elif window.finaly <= 310 and window.finalx == 770:
            ui.eventTxt.setText("You are having dinner. What do you eat?")
            window.eventVar = "Dinner"
            if rand == 1:
                eventPicture = QPixmap('dinner1.jpeg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("﻿Indian takeout")
                ui.option2.setText("﻿Vegetable lasagna")
                ui.option3.setText("﻿Sushi")
                ui.Event.show()
            else:
                eventPicture = QPixmap('dinner2.jpeg')
                ui.eventPic.setPixmap(eventPicture)
                ui.eventPic.setScaledContents(True)
                ui.option1.setText("﻿Steak and potatoes")
                ui.option2.setText("﻿Fish and roasted vegetables")
                ui.option3.setText("﻿Stew and bread")
                ui.Event.show()
    window.needEventCard = False
ui.eventCard.clicked.connect(event)

# DEFINE EVENT CARD OK BUTTON

def eventOK():
    if not ui.option1.isChecked() and not ui.option2.isChecked() and not ui.option3.isChecked():
        ui.eventError.show()
    else:
        ui.Event.hide()
        ui.dice.setEnabled(True)
        ui.marker.show()
        ui.dice.show()
        ui.Reminder.setText("Please roll die\nto continue")
        window.eventShown = False
        window.needEventCard = False
ui.eventOK.clicked.connect(eventOK)

# TASK PERFORMANCE
# When perform task button in main window is clicked, get time
def TaskBtn():
    ui.taskWindow.setGeometry(380,160,401,371)
    ui.marker.hide()
    ui.dice.hide()
    ui.taskWindow.show()
    timePerformed = ui.Timer.text()
    file = open("VDData.csv","a")
    file.write(str(timePerformed))
    file.close()
ui.performTask.clicked.connect(TaskBtn)
# When perform task button within event card is clicked, record corresponding event
def eventTaskBtn():
    ui.taskWindow.setGeometry(380,160,401,371)
    ui.marker.hide()
    ui.dice.hide()
    ui.taskWindow.show()
    file = open("VDData.csv","a")
    file.write(window.eventVar)
    file.close()
ui.eventTask.clicked.connect(eventTaskBtn)

# RECORD WHICH TASK PERFORMED
def antibio():
    file = open("VDData.csv","a")
    file.write(": antibio,")
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.antibioTask.clicked.connect(antibio)
def momBday():
    file = open("VDData.csv","a")
    file.write(": Mom bday card,")
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.momTask.clicked.connect(momBday)
def submitEssay():
    file = open("VDData.csv","a")
    file.write(": submit essay,")
    file.close()
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.essayTask.clicked.connect(submitEssay)
def libBook():
    file = open("VDData.csv","a")
    file.write(": return book,")
    file.close()
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.bookTask.clicked.connect(libBook)
def coldMeds():
    file = open("VDData.csv","a")
    file.write(": cold meds,")
    file.close()
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.medicineTask.clicked.connect(coldMeds)
def lecture():
    file = open("VDData.csv","a")
    file.write(": lecture,")
    file.close()
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.lectureTask.clicked.connect(lecture)
def cancel():
    file = open("VDData.csv", "a")
    file.write(": cancel,")
    file.close()
    ui.taskWindow.hide()
    if window.eventShown == False:
        ui.marker.show()
        ui.dice.show()
ui.cancelTask.clicked.connect(cancel)

####### DEBRIEF/CAT GIF PAGE #########
# Create a QLabel widget with QMovie GIF playing
catGIF = QLabel(ui.catPage)
catGIF.setGeometry(390,150,601,501)
cat = QMovie("catFistBump.gif")
catGIF.setMovie(cat)
cat.start()

# Thank you blinking label
thankYou = coloredLabel(ui.catPage)
MyFont = QFont("Geneva", 18)
thankYou.setFont(MyFont)
thankYou.setText("THANKS FOR PLAYING HERE'S A CAT")
thankYou.setWordWrap(True)
thankYou.setGeometry(330, 330, 341, 41)
thankYou.blink("magenta","transparent")


# END EXPERIMENT CODE
window.show()
sys.exit(app.exec_())
