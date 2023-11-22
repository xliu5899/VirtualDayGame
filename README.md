# VirtualDayGame
VIRTUAL DAY PROGRAM

EXPERIMENTAL OVERVIEW
The aim of this experiment is to test prospective memory under the influence of alcohol. The design is based on the Virtual Week task created by Rendell and Craik (2000), which is a computer simulation of living a week in the form of a board game. Participants are randomly sorted into an alcohol or placebo condition, and must remember to perform tasks at certain points in the game. The ability of participants to successfully carry out tasks at the correct times will determine the effect, if any, that alcohol has on prospective memory. Implications for this experiment could lead to greater understanding and further study of the ability of alcohol-dependent patients and recovering alcoholics to remember plans and function in society.
My experimental program, Virtual Day, is a simplified version of Virtual Week in which a participant must only make one circuit around the board. Each circuit represents one full day, and within each day participants will undergo ordinary daily events such as eating breakfast or going shopping. These events are represented by Event Cards that the participant must pick up after passing pre-demarcated points on the board. Event Cards will tell the participant which event is happening (e.g.: breakfast), and ask the participant to make a selection from a list of choices (e.g.: what food will they eat). The purpose of event cards are to simulate approximations of regular daily events to make the game seem more real. 
At the start of the game, participants are given two tasks that they must remember to complete throughout the course of the virtual day. These tasks are either event-based or time-based. Event-based tasks are dependent on a specific event that occurs during the day, for example taking medicine at mealtimes. Time-based tasks should be performed at a specific time of day, for example keeping an appointment with the doctor. In the Virtual Day game, a participant does not actually undergo the task, but rather can select to complete a task by opening a separate task window. No prompt is given if a participant misses their task trigger.
The hypothesis for this experiment is that alcohol has a negative main effect on task performance, with a stronger effect on time-based tasks.

DESCRIPTION OF PROCEDURE
  1.	Participants and Design: This is a double-blind independent two-group study, and participants will be pre-randomized to receive alcohol or placebo. Their participant IDs will be given to the administering experimenter, who will be blind to their condition. Participants should be social drinkers but not have an unhealthy relationship with alcohol. 
  2.	Procedure
    a.	Experimenter will be given a cup of either alcohol or placebo labelled with the corresponding participant ID.
    b.	Experimenter must administer the drink to the participant, who will have two minutes to finish it.
    c.	Experimenter will then run the program, and input the participant ID in the first field. The participant then takes over to give their consent, demographic data, and complete the CAGE questionnaire.
    d.	The game will prompt the participant to pick up a Start Card containing the tasks they must complete. Experimenter should make sure participant repeats aloud the tasks they are given, two times each.
    e.	Experimenter will remain in the room while participant completes the game, and then debrief the participant.
    f.	The experimenter will then refer the participant to the waiting room, where they must be held for an additional 30 minutes.
    g.	If the participant did not close out of the program, the experimenter should close and re-run to prepare for the next participant. 

EXPERIMENTER’S MANUAL
  1.	To Run
    a.	Open program folder and double-click VirtualDayGame.py to open in PyCharm.
    b.	Run by clicking on the green play button on the top right.
  2.	Inputs
    a.	Consent Page
      i.	Participant ID is a four digit number. This is found on the cup containing participant’s drink.
    b.	Demographics Page
      i.	Gender, Height (in) and Weight (lbs), are collected for future analysis, as these factors contribute to variation in how the effects of alcohol are experienced.
      ii.	Age must be over 18 as this is an alcohol study
  c.	CAGE Questionnaire
      i.	Participants must select Y/N for each question. These are stored in output file for future analysis.
  d.	Virtual Day Game
      i.	Each square on the board represents 20 minutes of the day. Each day begins at 8AM and ends at midnight. The green E squares indicate events. When a participant’s game piece passes an E, he/she must pick up an Event Card.
        1.	Please reference timekeeper.xlsx, located in the program folder, for a list of numbered squares (tiles), the virtual time they correspond to, their positions on the board, and which events can occur at each event square. 
      ii.	Time of day will be displayed in the timer at the center of the board, and it corresponds with the square that the participant’s game piece is on. Clockwise movement around the board represents the passing of time.
      iii.	Participants are equally randomized into 2 task conditions. Different task conditions will have different tasks:
        1.	Task Condition 1
          a.	Take antibiotics at breakfast and dinner
          b.	Submit essay at 21:00
        2.	Task Condition 2
          a.	Attend lecture at 12:00 and 15:00
          b.	Take cold medicine with lunch
      iv.	Participants begin by pressing START. They should follow the prompts in the center of the screen.
      v.	To pick up a Start or Event Card, simply click on the corresponding representations on the board.
      vi.	Participants must click on the die to roll and then click on their game piece to automatically advance the number shown on the die.
      vii.	For event-based tasks, participants should click on Perform Task button within the event card. For time-based tasks, they should click on Perform Task button on the board after their marker passes the indicated time and before the next die roll.
        1.	Every time a participant clicks a Perform Task button it will be recorded and the position (either event or time) will also be recorded
  3.	Output File
    a.	All results will be recorded in a csv file called VDData, located in the program folder. The first row contains headers. Each row after that contains participant data.
      i.	Column A: Participant ID
      ii.	Column B: Gender
      iii.	Column C: Height
      iv.	Column D: Weight
      v.	Column E: Age
      vi.	Column F: CAGE Q1 (contains TRUE for yes or FALSE for no)
      vii.	Column G: CAGE Q2 (contains TRUE for yes or FALSE for no)
      viii.	Column H: CAGE Q3 (contains TRUE for yes or FALSE for no)
      ix.	Column I: CAGE Q4 (contains TRUE for yes or FALSE for no)
      x.	Column J: Task Condition (1 or 2)
      xi.	Column K and on: Will contain tasks performed in the following format
        1.	event: task performed
        2.	time: task performed
  4.	To Exit
    a.	X out of the program window

PROGRAM HIGHLIGHTS
•	Participant ID box will return error if it’s not 4 numbers.
•	Task condition is assigned based on previous participant’s condition to ensure equal number of participants assigned to each set of tasks
•	Use of counter in OKTask function connected to the OK button of the Start Card to make sure user repeats reading the tasks at least once.
•	Animation of die with QTimer using counter to cycle through the numbered dice pictures each time die is “rolled”.
•	Animation of game piece:
  o	Connected to the number rolled on die
  o	On click, game piece automatically moves the correct number of tiles
  o	Game piece rounds corners and continues only the amount left on die roll
•	Passing event square disables die and prompts player to pick up an Event Card
  o	needEventCard boolean variable makes sure that Event Cards can only be picked up when event card is needed.
•	Time label calculates and displays the correct time depending on the square the game piece lands on.
•	Start label, game piece, and die are clickable labels

REFERENCES:
Rendell, P. G., & Craik, F. I. (2000). Virtual week and actual week: Age-related differences in prospective memory. Applied Cognitive Psychology,14(7), 43-62. doi:10.1002/acp.770
