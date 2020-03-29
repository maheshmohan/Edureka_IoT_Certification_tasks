from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep
import pygal
import subprocess
sense = SenseHat()

cpu_temp = str(subprocess.check_output("vcgencmd measure_temp", shell=True))
temp = (sense.get_temperature_from_pressure() + sense.get_temperature_from_humidity()) / 2

array = cpu_temp.split("=")
array2 = array[1].split("'")

cpu_temp = float(array2[0])
#print(cpu_temp)
#print(temp)
#reference - https://www.raspberrypi.org/forums/viewtopic.php?t=152498
corrected_val=temp - ((cpu_temp - temp)/5.466)-6


print("temperature: "+str(round(corrected_val,2)))
print("humidity :"+str(round(sense.get_humidity(),2))+"%")
