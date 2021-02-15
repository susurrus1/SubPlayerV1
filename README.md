# SubPlayerV1
Improved vocal commands for seamoth vehicle in Subnautica

This project was inspired by user Sentdex's cyberpython2077 project (https://github.com/Sentdex/cyberpython2077).

* Installation notes:
=====================

The seamoth.v1.py code was tested with python 3.7 and modules were installed using the Conda package management system.  Before running the program, make sure you have the following python modules installed:

argparse
win32gui
speech_recognition
pynput
mouse
text_to_num
desktopmagic
cv2
numpy
matplotlib
time

All of these should install normally using the "pip install" command, with the possible exception of speech_recognition, which also requires PyAudio to be installed.  If the command

pip install PyAudio

fails, you may need to directly install the binaries via

pip install pipwin
pipwin install PyAudio

* Usage notes:
==============

the seamoth.v1.py code accepts the "--language" option which lets you choose between English and French as the language for the spoken commands.  You can run the code as

python seamoth.v1.py --language "en-US"

or

python seamoth.v1.py --language "fr-FR"

If the language option is not given, the default is English.  Once started, the program is always listening, but to execute a command, the spoken phrase must start with an activation word.  In English, the activation word is "seamoth" in French, due to limitations of the recognizer the word is currently the name "Simon" (as it is pronounced in French).  Thus, to check that the program is working correctly, for the English version you can try:

seamoth hello

and in the French version:

simon coucou

In both cases, the program should respond with "Hello!" if it understood your phrase.  Some commands to try:

English		French
-------------------------
lights		lumières
debug		débogage
interface	interface
photo		photo
-------------------------

Note that the interface command, which toggles on and off the game interface is buggy even when you press the F6 key in the game, and may need to be issued a few times before it works.
To move the vehicle in a given direction for x seconds (where x is an integer number):

English			French
----------------------------------------------------
move left x seconds	mouvement gauche x secondes
move right x seconds	mouvement droite x secondes
move forward x seconds	mouvement avant x secondes
move back x seconds	mouvement arrière x secondes
move up x seconds	mouvement haut x secondes
move down x seconds	mouvement bas x secondes
----------------------------------------------------

There are also commands to change the direction the vehicle is pointing.  Note that the commands are given in some number of degrees, but the actual amount will depend (among other things) on the sensitivity setting of your mouse, so you should experiment with this command to get a feel for how to use it in your game setup:

English			French
----------------------------------------------
turn left x degrees	tourne gauche x degrés
turn right x degrees	tourne droite x degrés
turn up x degrees	tourne haut x degrés
turn down x degrees	tourne bas x degrés
----------------------------------------------

Finally, an experimental command has been implemented which might eventually be used for automated navigation of the seamoth with obstacle avoidance.  The command

English		French
-----------------------
analyze		analyse
-----------------------

will briefly pop up a window showing the current scene as viewed by a Canny edge detector.  The window will disappear after 2 seconds, and the command can then be issued again as many times as desired.

To exit the seamoth.v1.py program, you can issue the command

English		French
------------------------
terminate	terminer
------------------------

As a final recommendation, make sure to wait until your previous sentence was processed before issuing a new command, or the program might get confused and ignore your command.
