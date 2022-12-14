# filename: Final project.py
# student name: Shafa
# Overview: This study looks at how reaction time to identify colour differs based on the valence of priming stimuli. These priming stimuli are happy, neutral, or sad valenced faces. 
#           A state stress score is also recorded for the participant, which may act a moderator for any potential effect.
# Purpose: The rational for this study is that alterness/attention (indexed by reaction time) is possibly affect by breif temporal mood (indexed by the priming of emotionally valenced faces) wherby 
#          sad faces produce quicker reaction times because the negative stimuli may have the impact attuning our senses in a heightened fasion. This research would contribute to our understanding of 
#          the impact that emotional priming has on attention and alertness. 





# This section of the code imports all of the necessary packages for this script to run. 
import random
import numpy as np
import pandas as pd
import os
from psychopy import visual, monitors, core, event
from psychopy import gui
from datetime import datetime

# This section of the code defines a directory and where to store the data files, and where to get the images from. It creates a data file path if none exist. 
directory = os.getcwd()
path = os.path.join(directory, 'dataFiles')
path = os.path.join(directory,'images')
if not os.path.exists(path):
   os.makedirs(path)

# This section creates a subject info graphical window where the subject number, age, handedness, and current stress level can be input. It stores the subject nbr in the output file name.  
expInfo = {'subject_nr':0,'age':0, 'handedness':('right','left','ambi'), 'stress level today (1 is lowest)':('1','2','3', '4','5') }
myDlg = gui.DlgFromDict(dictionary=expInfo)
expInfo['date'] = datetime.now() 
filename = (str(expInfo['subject_nr']) + '_outputFile.csv')

# This scction defines how many blocks and how many trials within those blocks. It also defines how many total trials there are, and howmany trials in each block. 
nTrials = 10
nBlocks = 2
totalTrials = nTrials*nBlocks
nEach = int(totalTrials/2)

# This section how many different colours of dots to present, half red and half blue. 
colour = ['blue']*nEach + ['red']*nEach
face = ['happy.jpg','sad.jpg','neutral.jpg', 'neutral.jpg']*5

# This section puts all these combinations of widths, hights, and colour for each dot togehter in a list, and randomly shuffles their order. 
trials = list(zip(face, colour))
np.random.shuffle(trials)

# This sections defines lists that will make up the output aspects for the subject data, including what colour the dot was, if they were accurate, the response time, the trial number, the block number, and what face was presented. 
colours = [0]*totalTrials
accuracies = [0]*totalTrials
responseTimes = [0]*totalTrials
trialNumbers = [0]*totalTrials
blockNumbers = [0]*totalTrials
faces = [0]*totalTrials

# This section defines a monitor sets its parameters and pixel density 
mon = monitors.Monitor('myMonitor', width=35.56, distance=60)
mon.setSizePix([1920, 1080])
#This section creates a window on the monitor, 600 pixel by 600 pixel, in the colour grey. 
win = visual.Window(
 fullscr=False, 
 monitor=mon, 
 size=(600,600), 
 color='grey', 
 units='pix'
)

# This section defines the text that will make up the intrsuctions, and the dots that will make up the stimulus. As well as the fixation cross, and sets up the tracking of mouse movement. 
instructText = visual.TextStim(win, text='In each trial of this experiment, you will be presented with a face. Then a dot will appear in the middle of the screen. If this dot is red, click the r key, if this dot is blue, click the b key. Your goal is to identify the colour as quickly as possible. Press any key to begin the experiment.')
stimCircle = visual.Circle(win, size=(20,20)) 
fixation = visual.TextStim(win, text='+', color='black')
myMouse = event.Mouse(visible=True,win=win)
my_image = visual.ImageStim(win, units = 'pix')

# This section tells the window to draw the insctuction text, show it, and wait for a key press. 
instructText.draw()
win.flip()
event.waitKeys()
        
# This section defines a timer, using core.clock function 
trial_timer = core.Clock()

# This section makes a for loop that says for each block do this:
for iblock in range(nBlocks):
    # This section defines the intructions text and tells you which block you are on, then draws it
    instructText.text = 'Press any key to begin Block ' + str(iblock+1)
    instructText.draw()
    # This section presents that text, and waits for a key to be pressed. Once this key is pressed, a for loop is created within that block so that for each trial in that block, the following happens:
    win.flip()
    event.waitKeys()
    
    for itrial in range(nTrials):        
        # This section defines what trial you are on and in what block, then adds a block and trial number to what ever trial and block you were on, and defines where the colour for the trial will be located in the trial list. 
        
        overallTrial = iblock*nTrials+itrial
        blockNumbers[overallTrial] = iblock+1
        trialNumbers[overallTrial] = itrial+1
        colours[overallTrial] = trials[overallTrial][1]
        faces[overallTrial] = trials[overallTrial][0]
        
        # This section defines a colour for the dot circle, indexed from the list "trials" which was created eralier. The position will always be the same.  
        # The position of the face image is also defined here
        stimCircle.pos = (0, 0)
        stimCircle.color = trials[overallTrial][1]
        
        my_image.image = os.path.join(path,face[itrial])
        my_image.size= 400,400
        my_image.pos= 0,0
        fixation.draw()
        win.flip() #show
        core.wait(.5)
        
        my_image.draw() #draw
        win.flip() #show
        core.wait(1)
        
        fixation.draw()
        win.flip() #show
        core.wait(.25)
        
        stimCircle.draw() 
        
        
        win.flip() 
        
       
        trial_timer.reset()

        
        keys=event.waitKeys(keyList=['r', 'b'])
        
        # This section gets the reponse time and saves it, then checks if the response was correct for the colour of circle that was presented. It checks the trials list created for that trial, indexing to the first index, so colour,   
        # and then check if that equals red. If it does, then: 
        if keys:
            responseTimes[overallTrial] = trial_timer.getTime() 
            if trials[overallTrial][1] == 'red':
                # This section checks if the response was red, and if so then it records correct for that trial, if the response is not red the response as inaccurate. if the trial list does not have a red for that trial it then goes through the same process of checking if b was pressed and recording either a correct or incorect reponse for trials like that.  
                if keys[0] == 'r':
                    accuracies[overallTrial] = 'Correct'
                else:
                    accuracies[overallTrial] = 'Incorrect'
            else:
                if keys[0] == 'b':
                    accuracies[overallTrial] = 'Correct'
                else: 
                    accuracies[overallTrial] = 'Incorrect'
        
        # This section prints the block number, trial number, accuracy and response time for that trial
        print(
         'Block:',
         iblock+1,
         ', Trial:', 
         itrial+1, 
         ',', 
         trials[overallTrial][1], 
         ':', 
         accuracies[overallTrial], 
         ', RT:', 
         responseTimes[overallTrial]
        )

# This section creates a data frame of all the important info that was collected during this run for this participant 
df = pd.DataFrame(data={
 "Block Number": blockNumbers, 
 "Trial Number": trialNumbers, 
 "Colour": colours, 
 "Accuracy": accuracies, 
 "Response Time": responseTimes,
 "Face": faces,
 "Age": str(expInfo['age']),
 "Handedness": str(expInfo['handedness']),
 "Stress": str(expInfo['stress level today (1 is lowest)'])
})
df.to_csv(os.path.join(path, filename), sep=',', index=False)

# This closes the window once all blocks have run through. 
win.close()