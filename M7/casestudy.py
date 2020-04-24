from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep
import pygal
import random
import numpy as np

sense = SenseHat()

p1turn = True
p2turn = False

won = False
board_filled = False
exit_condition = False

#VIBGYOR colour codes
violet = (148,0,211)
indigo = (75,0,130)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
orange = (255,125,0)
red = (255,0,0)
nothing = (0,0,0)

global pixp1, pixp2

pixp1 = [1,1]
pixp2 = [0,0]

win_board = [[0,0,0],
             [0,0,0],
             [0,0,0]]

cell_clear = True

def cell_occupied(pixel):
    if sense.get_pixel(pixel[0],pixel[1]) == [248, 252, 0] or sense.get_pixel(pixel[0],pixel[1]) == [0, 0, 248]:
        cell_clear = False
        return True
    elif pixel[0]-1 >=0 and pixel[1]-1 >= 0 and sense.get_pixel(pixel[0]-1,pixel[1]-1) == [0, 0, 248]:
        cell_clear = False
        return True
    elif pixel[0]+1 <= 7 and pixel[1]+1 <= 7 and sense.get_pixel(pixel[0]+1,pixel[1]+1) == [248, 252, 0]:
        cell_clear = False
        return True
    cell_clear = True
    return False

def show_board():
    V = violet
    I = indigo
    B = blue
    G = green
    Y = yellow
    O = orange
    R = red
    N = nothing
    board = [
        N, N, B, N, N, B, N, N,
        N, N, B, N, N, B, N, N,
        B, B, B, B, B, B, B, B,
        N, N, B, N, N, B, N, N,
        N, N, B, N, N, B, N, N,
        B, B, B, B, B, B, B, B,
        N, N, B, N, N, B, N, N,
        N, N, B, N, N, B, N, N,
        ]
    return board

def move_right(event):
    global pixp1, pixp2
    print("move_right"+str(pixp1)+str(pixp2))
    if event.action != ACTION_RELEASED:
        if p1turn:
            sense.set_pixels(board)
            pixp1[0] = pixp1[0]+3
            if pixp1[0] > 7:
                pixp1[0] = pixp1[0] - 9
            if cell_occupied(pixp1):
                sense.set_pixel(pixp1[0],pixp1[1],red)
            else:
                sense.set_pixel(pixp1[0],pixp1[1],yellow)
        if p2turn:
            sense.set_pixels(board)
            pixp2[0] = pixp2[0]+3
            if pixp2[0] > 7:
                pixp2[0] = pixp2[0] - 9
            if cell_occupied(pixp2):
                sense.set_pixel(pixp2[0],pixp2[1],red)
            else:
                sense.set_pixel(pixp2[0],pixp2[1],green)
            
def move_left(event):
    global pixp1, pixp2
    print("move_left"+str(pixp1)+str(pixp2))
    if event.action != ACTION_RELEASED:
        if p1turn:
            sense.set_pixels(board)
            pixp1[0] = pixp1[0]-3
            if pixp1[0] < 0:
                pixp1[0] = pixp1[0] + 9
            if cell_occupied(pixp1):
                sense.set_pixel(pixp1[0],pixp1[1],red)
            else:
                sense.set_pixel(pixp1[0],pixp1[1],yellow)
        if p2turn:
            sense.set_pixels(board)
            pixp2[0] = pixp2[0]-3
            if pixp2[0] < 0:
                pixp2[0] = pixp2[0] + 9
            if cell_occupied(pixp2):
                sense.set_pixel(pixp2[0],pixp2[1],red)
            else:
                sense.set_pixel(pixp2[0],pixp2[1],green)
            
def move_up(event):
    global pixp1, pixp2
    print("move_up"+str(pixp1)+str(pixp2))
    if event.action != ACTION_RELEASED:
        if p1turn:
            sense.set_pixels(board)
            pixp1[1] = pixp1[1]-3
            if pixp1[1] < 0:
                pixp1[1] = pixp1[1] + 9
            if cell_occupied(pixp1):
                sense.set_pixel(pixp1[0],pixp1[1],red)
            else:
                sense.set_pixel(pixp1[0],pixp1[1],yellow)
        if p2turn:
            sense.set_pixels(board)
            pixp2[1] = pixp2[1]-3
            if pixp2[1] < 0:
                pixp2[1] = pixp2[1] + 9
            if cell_occupied(pixp2):
                sense.set_pixel(pixp2[0],pixp2[1],red)
            else:
                sense.set_pixel(pixp2[0],pixp2[1],green)

def move_down(event):
    global pixp1, pixp2
    print("move_down"+str(pixp1)+str(pixp2))
    if event.action != ACTION_RELEASED:
        if p1turn:
            sense.set_pixels(board)
            pixp1[1] = pixp1[1]+3
            if pixp1[1] > 7:
                pixp1[1] = pixp1[1] - 9
            if cell_occupied(pixp1):
                sense.set_pixel(pixp1[0],pixp1[1],red)
            else:
                sense.set_pixel(pixp1[0],pixp1[1],yellow)
        if p2turn:
            sense.set_pixels(board)
            pixp2[1] = pixp2[1]+3
            if pixp2[1] > 7:
                pixp2[1] = pixp2[1] - 9
            if cell_occupied(pixp2):
                sense.set_pixel(pixp2[0],pixp2[1],red)
            else:
                sense.set_pixel(pixp2[0],pixp2[1],green)
                

def checkRows(brd):
    for row in brd:
        if len(set(row)) == 1:
            return row[0]
    return 0

def checkDiagonals(brd):
    if len(set([brd[i][i] for i in range(len(brd))])) == 1:
        return brd[0][0]
    if len(set([brd[i][len(brd)-i-1] for i in range(len(brd))])) == 1:
        return brd[0][len(brd)-1]
    return 0

def checkWin(brd):
    #transposition to check rows, then columns
    for newBoard in [brd, np.transpose(brd)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(brd)
        
def update_winboard(player):
    global win_board
    if player == "1":
        idx = int((pixp1[0]-1)/3)
        idy = int((pixp1[1]-1)/3)
        win_board[idx][idy] = player
    elif player == "2":
        idx = int(pixp2[0]/3)
        idy = int(pixp2[1]/3)
        win_board[idx][idy] = player
        
def cell_select(event):
    global pixp1, pixp2, p1turn, p2turn, win_board
    if event.action != ACTION_RELEASED:
        if cell_clear:
            if p1turn:
                sense.set_pixel(pixp1[0],pixp1[1],yellow)
                board[pixp1[0]+(8*pixp1[1])]=yellow
                sense.set_pixel(pixp1[0],pixp1[1]-1,yellow)
                board[pixp1[0]+(8*(pixp1[1]-1))]=yellow
                sense.set_pixel(pixp1[0]-1,pixp1[1],yellow)
                board[(pixp1[0]-1)+(8*pixp1[1])]=yellow
                update_winboard("1")
                p1turn = False
                p2turn = True
            elif p2turn:
                sense.set_pixel(pixp2[0],pixp2[1],green)
                board[pixp2[0]+(8*pixp2[1])]=green
                update_winboard("2")
                p1turn = True
                p2turn = False
            if checkWin(win_board)=="1":
                sense.clear()
                exit_condition = True
                p1turn = False
                p2turn = False
                sense.show_message("Player1 WINS!!")
            elif checkWin(win_board)=="2":
                sense.clear()
                exit_condition = True
                p1turn = False
                p2turn = False
                sense.show_message("Player2 WINS!!")

sense.stick.direction_middle = cell_select
sense.stick.direction_right = move_right
sense.stick.direction_left = move_left
sense.stick.direction_down = move_down
sense.stick.direction_up = move_up

board = show_board()
sense.set_pixels(show_board())
while not exit_condition:
    while p1turn:
        if cell_occupied(pixp1):
            sense.set_pixels(board)
            sense.set_pixel(pixp1[0],pixp1[1],red)
        else:
            sense.set_pixels(board)
            sense.set_pixel(pixp1[0],pixp1[1],yellow)
    while p2turn:
        if cell_occupied(pixp2):
            sense.set_pixels(board)
            sense.set_pixel(pixp2[0],pixp2[1],red)
        else:
            sense.set_pixels(board)
            sense.set_pixel(pixp2[0],pixp2[1],green)
sleep()