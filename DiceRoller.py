#import the GPIO and time packages
import RPi.GPIO as GPIO
import time
from pynput import keyboard
print("started")

# Some commment!!!!

#def threadingDemo(): 
 #   print("GeeksforGeeks\n") 
  
#timer = threading.Timer(2.0, threadingDemo) 
#timer.start() 

#Set up Dice Defs'
class Dice:
    def __init__(self, Name, TriggerKey, GpioPort, Active):
        self.Name = Name = Name
        self.TriggerKey = TriggerKey
        self.GpioPort = GpioPort
        self.Active = Active
D4 = Dice('D4', keyboard.KeyCode.from_char('/'),1, False)
D6 = Dice("D6", keyboard.KeyCode.from_char('*'), 11, False)
D8 = Dice("D8", keyboard.KeyCode.from_char('-'), 13, False)
D10 = Dice("D10", keyboard.KeyCode.from_char('+'), 15, False)
D12 = Dice("D12", keyboard.Key.backspace, 13, False)
D20 = Dice("D20", keyboard.Key.enter, 14, False)

DiceSet = {D4, D6, D8, D10, D12, D20}



# populate numbers 1->9 as keycodes
NumbersAsKeyCodes = set()
for x in range(9):
    charnum = str(x+1)[0]
    print charnum
    NumbersAsKeyCodes.add(keyboard.KeyCode.from_char(charnum))

NumberOfDiceToRoll = 0


def on_press(key):
    #store if this -dice key- has been pressed
    for Dice in DiceSet:
       if key == Dice.TriggerKey:
           Dice.Active = True
    #if a number key has been pressed, roll all active dice n times
    if key in NumbersAsKeyCodes:
       NumberOfDiceToRoll = int(key.char)
       for Dice in DiceSet:
        if Dice.Active:
            print ('Rolling ',Dice.Name)
            for z in range(NumberOfDiceToRoll):
                roll_dice(Dice.GpioPort)

    if key == keyboard.Key.esc:
        print('Escape key pressed. exiting')
        listener.stop()

def roll_dice(GpioPort):
    
    #.1 is my fav
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GpioPort, GPIO.OUT)
    GPIO.output(GpioPort,True)
    time.sleep(.1)
    GPIO.output(GpioPort,False)
    time.sleep(.1)
    GPIO.cleanup()
    print(GpioPort,'rolled')

def on_release(key):
    try:
     #reset input key combination tracking
       for Dice in DiceSet:
        if key == Dice.TriggerKey:
            Dice.Active = False
        if key in NumbersAsKeyCodes:
            NumberOfDiceToRoll = 0
    
    except KeyError:
        pass



with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()



'''GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
print("Starting")
time.sleep(1)
# loop through 50 times, on/off for 1 second
for i in range(100):
    GPIO.output(7,True)
    time.sleep(.1)
    GPIO.output(7,False)
    time.sleep(.1)
    print("iteration"+str(i))
GPIO.cleanup()
print("done")'''
