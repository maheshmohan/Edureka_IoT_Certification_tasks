from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep

interrupted = False
count = 0
sense = SenseHat()

def stop_timer():
  global interrupted
  interrupted = True

sense.stick.direction_any = stop_timer

while not interrupted:
  sense.show_letter( str(count))
  count=count+1
  sleep(1)