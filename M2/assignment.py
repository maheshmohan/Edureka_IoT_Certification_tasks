from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep
import pygal
import random

exit_timer = False
exit_game = False
count = 0
menu_item = 0
in_menu = False
in_game = False
sense = SenseHat()

#VIBGYOR colour codes
violet = (148,0,211)
indigo = (75,0,130)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
orange = (255,125,0)
red = (255,0,0)
nothing = (0,0,0)

def show_rainbow():
    V = violet
    I = indigo
    B = blue
    G = green
    Y = yellow
    O = orange
    R = red
    N = nothing
    rainbow = [
        R, R, R, R, R, R, R, R,
        R, O, O, O, O, O, O, O,
        R, O, Y, Y, Y, Y, Y, Y,
        R, O, Y, G, G, G, G, G,
        R, O, Y, G, B, B, B, B,
        R, O, Y, G, B, I, I, I,
        R, O, Y, G, B, I, V, V,
        R, O, Y, G, B, I, V, N,
        ]
    return rainbow

def clear_display():
    O = nothing
    blank = [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        ]
    return blank

def draw_path1():
    Y = yellow
    O = nothing
    path = [
        Y, Y, Y, Y, O, O, O, O,
        O, O, O, Y, O, O, O, O,
        O, O, O, Y, Y, Y, Y, Y,
        O, O, O, O, O, O, O, Y,
        O, O, O, Y, Y, Y, O, Y,
        O, O, O, Y, O, Y, O, Y,
        O, Y, Y, Y, O, Y, O, Y,
        O, Y, O, O, O, Y, Y, Y,
        ]
    return path

def draw_path2():
    Y = yellow
    O = nothing
    path = [
        Y, Y, Y, O, O, O, O, O,
        O, O, Y, O, O, O, O, O,
        O, O, Y, Y, Y, O, O, O,
        O, O, O, O, Y, O, O, O,
        O, O, O, O, Y, Y, Y, O,
        O, O, O, O, O, O, Y, O,
        O, O, O, O, O, O, Y, O,
        O, O, O, O, O, O, Y, Y,
        ]
    return path

win_pixels = [(1,7),(7,7)]

paths = [draw_path1, draw_path2]

def update_menu():
    global menu_item
    sense.set_pixels(clear_display())
    if menu_item == 0:
        sense.show_message("RAINBOW PREDICTOR", text_colour = blue)
    elif menu_item == 1:
        sense.show_message("WEATHER LOGGER", text_colour = red)
    elif menu_item == 2:
        sense.show_message("TIGHTROPE", text_colour = green)
    else:
        sense.show_message("COMPASS MAZE", text_colour = violet)

def select_clicked(event):
    global interrupted, in_menu, in_game, exit_game, exit_timer
    if event.action != ACTION_RELEASED:
        print("selected")
        if not exit_timer:
          exit_timer = True
          in_menu = True
          update_menu()
        elif in_menu:
            if menu_item == 0:
                start_rainbow_predictor()
            elif menu_item == 1:
                start_weather_logger()
            elif menu_item == 2:
                start_tightrope()
            elif menu_item == 3:
                start_compass_maze()
        elif in_game:
            print("in-game")

def move_up_the_menu(event):
    print("menu up")
    global menu_item,in_menu
    if event.action != ACTION_RELEASED and in_menu:
        menu_item = menu_item+1
        print(menu_item)
        update_menu()

def move_down_the_menu(event):
    print("menu down")
    global menu_item
    if event.action != ACTION_RELEASED and in_menu:
        menu_item = menu_item-1
        print(menu_item)
        update_menu()

def exit_game(event):
    print("exit_game")
    if event.action != ACTION_RELEASED and in_game:
        in_menu = True
        in_game = False
        exit_game = True
        update_menu()

def start_rainbow_predictor():
    global in_menu, in_game, exit_game
    sense.set_pixels(clear_display())
    print("in rainbow")
    exit_game = False
    in_menu = False
    in_game = True
    for count in range(0,10):
        print("temp: " + str(sense.get_temperature())+" humidity: "+str(sense.get_humidity()))
        if sense.get_temperature() > 20 and sense.get_humidity() > 80:
          sense.set_pixels(show_rainbow())
        else:
          sense.set_pixels(clear_display())
        sleep(1)
    exit_game = True
    in_game=False
    in_menu=True
    update_menu()

def start_weather_logger():
    global in_menu, in_game, exit_game
    print("in weather_logger")
    exit_game = False
    in_menu = False
    in_game = True
    for count in range(0,15):
        mytempfile = open('weather_temp.txt','a')
        mytempfile.write(str(sense.get_temperature()))
        mytempfile.write('\n')
        mytempfile.close()
        sleep(2)

    plot=[]

    file = open('weather_temp.txt','r')
    for line in file.read().splitlines():
      if line:
        plot.append(float(line))
    file.close()

    weather_plot = pygal.Line(fill=True)
    weather_plot.add('temp',plot)

    weather_plot.title = 'Weather'
    weather_plot.xlabels = range(1,len(plot) + 1)

    weather_plot.render()
    exit_game = True
    in_game=False
    in_menu=True
    update_menu()

def start_tightrope():
    print("in tightrope")
    global in_menu, in_game, exit_game
    print("in weather_logger")
    exit_game = False
    in_menu = False
    in_game = True
    
    tries = 0
    win = False
    path = random.randint(0,1)
    print(path)

    sense.set_pixels(paths[path]())
    win_pixel=win_pixels[path]

    while not tries >= 3 and not win:
        char_x=0
        char_y=0
        sense.set_pixel(char_x,char_y,blue)
        while True:
            acceleration = sense.get_accelerometer_raw()
            x = acceleration['x']
            y = acceleration['y']
            z = acceleration['z']
            
            x=round(x, 0)
            y=round(y, 0)
            z=round(z, 0)

            print("x={0}, y={1}, z={2}".format(x, y, z))
            
            char_x = char_x + int(x)
            char_y = char_y + int(y)
            print(str(char_x),"+",str(char_y))
            
            if char_x > 7:
                char_x = 7
            if char_x < 1:
                char_x = 0
            if char_y > 7:
                char_x = 7
            if char_y < 1:
                char_y = 0
            
            print(sense.get_pixel(int(char_x),int(char_y)))
            
            if sense.get_pixel(int(char_x),int(char_y)) == [0,0,0]:
                sense.set_pixels(clear_display())
                sense.set_pixels(paths[path]())
                sense.set_pixel(char_x,char_y,blue)
                tries = tries+1
                break
            elif (char_x,char_y)==win_pixel:
                win = True
                break
            else:
                sense.set_pixel(char_x,char_y,blue)
                sleep(2)
    if win:
        sense.show_message("You Won!", text_colour=green)
    else:
        sense.show_message("You Lose!", text_colour=red)
    
    exit_game = True
    in_game=False
    in_menu=True
    update_menu()

def start_compass_maze():
    print("in compass_maze")

sense.stick.direction_middle = select_clicked
sense.stick.direction_right = move_up_the_menu
sense.stick.direction_left = move_down_the_menu
sense.stick.direction_down = exit_game

while True:
    while not exit_timer:
        sense.show_letter( str(count))
        count=count+1
        if count == 10:
            count=0 
        sleep(1)

#sense.set_pixels(show_rainbow())
