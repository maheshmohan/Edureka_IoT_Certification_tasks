from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep

sense = SenseHat()

#for count in range(0,5):
while True:
    event = sense.stick.wait_for_event()
    if event.direction == "middle" and event.action == ACTION_RELEASED:
        north = sense.get_compass()
        #sense.set_imu_config(True, True, True)
        #o = sense.get_orientation()
        #north = o["yaw"]
        north = int(round(north,0))
        print(north)
        if north < 100 and north > 80:
            sense.show_letter('W')
        elif north < 10 and north > 350:
            sense.show_letter('N')
        elif north < 280 and north > 260:
            sense.show_letter('E')
        elif north < 190 and north > 170:
            sense.show_letter('S')