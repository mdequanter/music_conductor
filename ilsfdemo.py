import pyautogui
import random
import paho.mqtt.client as mqttclient


#broker = "192.168.1.84";
#broker = "10.3.12.37"
broker = "127.0.0.1"

topics = ['TEMPO','LEFT','RIGHT','X','Y']
import time
import json

screenWidth = 1024
screenHeight = 768
leftWrist = 9
rightWrist = 10
leftShoulder = 5
rightShoulder = 6
leftElbow = 7
rightElbow = 8

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# Import and initialize the pygame library
import pygame
#pygame.init()
# Set up the drawing window
#screen = pygame.display.set_mode([screenWidth, screenHeight])


Xlist = []
Ylist = []

keystroke = ['a', 's', 'd', 'f', 'j', 'k', 'l', ';']



waitTime = 0.2;

leftKeys = ['a', 's', 'd']
rightKeys = ['k', 'l', ';']


def Press(key):
    pyautogui.press(key)


def setTempo(tempo):
    global waitTime
    if (tempo == 'H'):
        waitTime = 0.05
    if (tempo == 'L'):
        waitTime = 0.2
    if (tempo == 'M'):
        waitTime = 0.1


def setKeysRight(level) :
    if (level == 'H'):
        keys = ['i','i','i']
    if (level == 'L'):
        keys = ['a','a','a']
    if (level == 'M'):
        keys = ['e','y','e']
    return keys

def setKeysLeft(level) :
    if (level == 'H'):
        keys = ['o','o','o']
    if (level == 'L'):
        keys = ['z','z','z']
    if (level == 'M'):
        keys = ['u','t','u']
    return keys




def on_message(client, userdata, message):
    global leftKeys, rightKeys, Ylist,Xlist
    content = str(message.payload.decode("utf-8"))
    topic =  str(message.topic)

    if (topic == "TEMPO") :
        setTempo(content)
    if (topic == "LEFT") :
        leftKeys = setKeysLeft(content)
    if (topic == "RIGHT") :
        rightKeys = setKeysRight(content)
    if (topic == "X") :
        Xlist = json.loads(content)
    if (topic == "Y") :
        Ylist = json.loads(content)


def PlayNote(note1,note2 = False):
    if (note1) :
        player.note_on(note1, 127)
    if (note2) :
        player.note_on(note2, 127)
    if (note3) :
        player.note_on(note3, 127)
    if (note1) :
        player.note_off(note1, 127)
    if (note2) :
        player.note_off(note2, 127)
    if (note3) :
        player.note_off(note3, 127)




client=mqttclient.Client("Client1")
client.connect(broker)
client.loop_start() #start the loop

for topic in topics :
    client.subscribe(topic)

client.on_message=on_message #attach function to callback


while True:

    Press(leftKeys[random.randint(0,2)])
    Press(rightKeys[random.randint(0,2)])
    time.sleep(waitTime)

    '''
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    if (len(Xlist) >= leftWrist ) :
        pygame.draw.circle(screen, (0, 0, 255), (screenWidth - Xlist[leftWrist],Ylist[leftWrist]), 30)
    if (len(Ylist) >= rightWrist ) :
        pygame.draw.circle(screen, (255, 0, 255), (screenWidth - Xlist[rightWrist],Ylist[rightWrist]), 30)

    # Flip the display
    pygame.display.flip()
    '''

time.sleep(3600)
client.loop_stop() #stop the loop

