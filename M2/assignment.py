from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep

interrupted = False
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

def update_menu():
	sense.clear()
	if menu_item == 0:
		sense.show_message("RAINBOW PREDICTOR", text_colour = blue)
	elif menu_item == 1:
		sense.show_message("WEATHER LOGGER", text_colour = red)
	elif menu_item == 2:
		sense.show_message("TIGHTROPE", text_colour = green)
	else:
		sense.show_message("COMPASS MAZE", text_colour = violet)

def start_rainbow_predictor():
	#yet to implement
	print("in rainbow")

def select_clicked():
  global interrupted, in_menu
  if not interrupted:
  	interrupted = True
  	in_menu = True
  	update_menu()
  elif in_menu:
  	if menu_item == 0:
  		start_rainbow_predictor()

def move_up_the_menu(event):
	print("menu up")
	global menu_item
	if event.action != ACTION_RELEASED:
		menu_item = menu_item+1
		print(menu_item)
		update_menu()

def move_down_the_menu():
	print("menu up")
	global menu_item
	if event.action != ACTION_RELEASED:
		menu_item = menu_item-1
		print(menu_item)
		update_menu()

sense.stick.direction_middle = select_clicked
sense.stick.direction_right = move_up_the_menu
sense.stick.direction_left = move_down_the_menu

while True:
	while not interrupted:
	  sense.show_letter( str(count))
	  count=count+1
	  sleep(1)

#sense.set_pixels(show_rainbow())
