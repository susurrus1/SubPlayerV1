import argparse
import win32gui
import speech_recognition as sr
import pynput
import mouse
from text_to_num import text2num
from desktopmagic.screengrab_win32 import getRectAsImage
import cv2
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

parser = argparse.ArgumentParser(description="Voice control for Subnautica game")
parser.add_argument("--language",default="en-US",help="choose interaction language (\"en-US\" or \"fr-FR\")",type=str)
args = parser.parse_args()

lang = args.language

#lang = "en-US"
#lang = "fr-FR"

GameLabel = "Subnautica"

# Define language-dependent messages

listeningMsg = {"en-US":"*** I'm listening:","fr-FR":"*** J'écoute:"}
analyzingMsg = {"en-US":"Analyzing...","fr-FR":"Analyse en cours..."}
heardMsg     = {"en-US":"I heard: ","fr-FR":"J'ai entendu: "}
saywhatMsg   = {"en-US":"Sorry, I didn't catch that","fr-FR":"Désolé, je n'ai pas compris"}
noreplyMsg   = {"en-US":"Sorry, the translation service is unavailable","fr-FR":"Désolé, le service de traduction n'est pas disponible"}

# Define language-dependent commands

helloCmd  = {"en-US":["hello"],"fr-FR":["coucou"]}
lightsCmd = {"en-US":["lights"],"fr-FR":["lumière","lumières"]}
debugCmd  = {"en-US":["debug"],"fr-FR":["débogage"]}
intrfcCmd = {"en-US":["interface"],"fr-FR":["interface"]}
photoCmd  = {"en-US":["photo","photos"],"fr-FR":["photo","photos"]}
moveCmd   = {"en-US":["move"],"fr-FR":["mouvement"]}
leftCmd   = {"en-US":["left"],"fr-FR":["gauche"]}
rightCmd  = {"en-US":["right"],"fr-FR":["droite"]}
upCmd     = {"en-US":["up"],"fr-FR":["haut","au"]}
downCmd   = {"en-US":["down"],"fr-FR":["bas","bah","pas","bain"]}
fwdCmd    = {"en-US":["forward"],"fr-FR":["avant"]}
bwdCmd    = {"en-US":["back"],"fr-FR":["arrière"]}
turnCmd   = {"en-US":["turn"],"fr-FR":["tourne"]}
anaCmd    = {"en-US":["analyze"],"fr-FR":["analyse"]}
stopCmd   = {"en-US":["stop"],"fr-FR":["stop"]}
endCmd    = {"en-US":["terminate"],"fr-FR":["terminer","terminé","terminez"]}

# Define trigger words to get the program's attention

triggerWords = {"en-US":["seamoth","cmos","cimaf","simos"],"fr-FR":["seamoth","simos","simmons","simons","simon"]}

windows_list = []
toplist = []
def enum_win(hwnd,result):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd,win_text))

def getDirKey(word):
    if word in leftCmd[lang]:
        dirk = "a"
    elif word in rightCmd[lang]:
        dirk = "d"
    elif word in upCmd[lang]:
        dirk = pynput.keyboard.Key.space
    elif word in downCmd[lang]:
        dirk = "c"
    elif word in fwdCmd[lang]:
        dirk = "w"
    elif word in bwdCmd[lang]:
        dirk = "s"
    else:
        dirk = None

    return dirk

def getDirVec(word):
    if word in leftCmd[lang]:
        dx = -dxscreen0
        dy = 0
    elif word in rightCmd[lang]:
        dx = dxscreen0
        dy = 0
    elif word in upCmd[lang]:
        dx = 0
        dy = -dyscreen0
    elif word in downCmd[lang]:
        dx = 0
        dy = dyscreen0
    else:
        dx = dy = 0

    return dx,dy

def wordToInt(word):
    try:
        val = int(word)
    except:
        try:
            if lang == "en-US":
                val = text2num(word,"en")
            elif lang == "fr-FR":
                val = text2num(word, "fr")
            else:
                val = 1
        except:
            val = 1

    return val

def performAction(cmdl):
    global more

    if len(cmdl) >= 2:
        if cmdl[1] in helloCmd[lang]:
            print("Hello!")
        elif cmdl[1] in lightsCmd[lang]:
            #mouse.click(pynput.mouse.Button.right,1)
            mouse.right_click()
        elif cmdl[1] in debugCmd[lang]:
            keybd.tap(pynput.keyboard.Key.f1)
        elif cmdl[1] in intrfcCmd[lang]:
            keybd.tap(pynput.keyboard.Key.f6)
        elif cmdl[1] in photoCmd[lang]:
            keybd.tap(pynput.keyboard.Key.f11)
        elif cmdl[1] in moveCmd[lang]:
            if len(cmdl) >= 3:
                dirk = getDirKey(cmdl[2])
                if dirk != None:
                    if len(cmdl) >= 4:
                        duration = wordToInt(cmdl[3])
                    else: # default is move for 1 sec
                        duration = 1
                    keybd.press(dirk)
                    sleep(duration)
                    keybd.release(dirk)
        elif cmdl[1] in turnCmd[lang]:
            if len(cmdl) >= 3:
                dx,dy = getDirVec(cmdl[2])
                if dx != 0 or dy != 0:
                    if len(cmdl) >= 4:
                        duration = wordToInt(cmdl[3])
                    else: # default is turn for 1 unit
                        duration = 1
                    #print("duration = ",duration)
                    #mouse.position = (xscreen0, yscreen0)
                    for tstep in range(duration):
                        mouse._os_mouse.move_to(xscreen0,yscreen0)
                        #mouse.position = (xscreen0, yscreen0)
                        sleep(0.001)
                        #sleep(1)
                        #mouse.move(dx,dy)
                        mouse._os_mouse.move_relative(dx,dy)
                        sleep(0.1)
                        #print("moved to: ",mouse.position)
        elif cmdl[1] in anaCmd[lang]:
            print("analysis functionality not fully implemented")
            screenshot = getRectAsImage(position)
            screenarr  = np.array(screenshot)
            #screenarr  = cv2.cvtColor(screenarr, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(screenarr,cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray,100,200)
            plt.imshow(edges,cmap='gray')
            plt.show()
            plt.pause(2.0)
            plt.close()
            #cv2.imshow("Analysis",edges)
            #cv2.waitKey(0)
        elif cmdl[1] in stopCmd[lang]:
            print("stop functionality not yet implemented")
        elif cmdl[1] in endCmd[lang]:
            more = False
            print("ending program")

def SRcallback(recognizer,audio):
    global phrase
    phrase = None
    try:
        print(analyzingMsg[lang])
        phrase = recognizer.recognize_google(audio,language=lang)
        phrase = phrase.lower()
    except sr.UnknownValueError:
        print(saywhatMsg[lang])
        print(listeningMsg[lang])
    except sr.RequestError:
        print(noreplyMsg[lang])

def getPhrase(mic):
    with mic as source:
        try:
            spoken = rec.listen(source, phrase_time_limit=5)
            print(analyzingMsg[lang])
            phrase = rec.recognize_google(spoken,language=lang)
            phrase = phrase.lower()
        except:
            phrase = None

    return phrase

# Initializations

win32gui.EnumWindows(enum_win,toplist)

game_hwnd = None
defbox    = [0,0,1920,1080] # Default box

wincnt = 0

for (hwnd,win_text) in windows_list:
    if win_text == "Subnautica":
        wincnt += 1
        game_hwnd = hwnd
        position = win32gui.GetWindowRect(game_hwnd)
        #print("found: hwnd = ", hwnd, ", win_text = ", win_text,", position = ",position)
        print("Found game window titled \"%s\" with id = %d and coordinates (%d,%d,%d,%d)"%(win_text,game_hwnd,position[0],position[1],position[2],position[3]))
        #win32gui.ShowWindow(game_hwnd,6)
        #win32gui.ShowWindow(game_hwnd,9)

if wincnt > 1:
    print("Multiple windows found with the name \"",GameLabel,"\", please close duplicate windows")
    game_hwnd = None
    position  = defbox
    print("assuming screen coordinates: ",position)

if game_hwnd == None:
    position = defbox
    print("Game window not found, assuming screen coordinates: ",position)

# Locate the middle of the screen
xscreen0 = (position[2]-position[0])//2
yscreen0 = (position[3]-position[1])//2

# Unit mouse displacements in pixels
dxscreen0 = 20
dyscreen0 = 20

plt.ion()  # to ensure calls to show() are non-blocking

#mouse = pynput.mouse.Controller()
keybd = pynput.keyboard.Controller()

rec = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    rec.adjust_for_ambient_noise(source)

#listen = rec.listen_in_background(mic,SRcallback)
print(listeningMsg[lang])

# Start main loop

phrase = None
more   = True
while more:
    phrase = getPhrase(mic)

    if phrase != None:
        print(heardMsg[lang]+phrase)
        wordl = phrase.split()
        #print("trigger = ",wordl[0])
        if wordl[0] in triggerWords[lang]:
            performAction(wordl)
        #phrase = None
        print(listeningMsg[lang])
    else:
        print(saywhatMsg[lang])
        print(listeningMsg[lang])

