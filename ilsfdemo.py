import pyautogui
import random
import paho.mqtt.client as mqttclient


broker = "192.168.1.113"

topics = ['TEMPO','LEFT','RIGHT']
import time



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
        waitTime = 10
    if (tempo == 'M'):
        waitTime = 0.1


def setKeys(level) :
    if (level == 'H'):
        keys = ['k', 'l', ';']
    if (level == 'L'):
        keys = ['a', 's', 'd']
    if (level == 'M'):
        keys = ['f', 'j','k']
    return keys




def on_message(client, userdata, message):
    global leftKeys, rightKeys
    content = str(message.payload.decode("utf-8"))
    topic =  str(message.topic)
    print("message topic=",topic)
    print("message received ", content)

    if (topic == "TEMPO") :
        setTempo(content)
    if (topic == "LEFT") :
        leftKeys = setKeys(content)
    if (topic == "RIGHT") :
        rightKeys = setKeys(content)


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



time.sleep(3600)
client.loop_stop() #stop the loop

