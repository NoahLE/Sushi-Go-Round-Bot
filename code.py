# Sushi-Go-Round Python Bot
# By DigitalMockingbird
# Updated 8/24/2014
#
# Sections
# 1. Imports
# 2. Coordinate related functions (you need to change this if you have a different configuration)
# 3. Static location based functions (these are based on the top left corner of the flash game 
#	     being (1, 1) so no resize should be necessary)
#
# See readme for setup and debugging logic

# ============================================================================
# == 1. Imports - win32api and win32con is windows only
# ============================================================================

import os
import time
from numpy import *
import win32api, win32con
import  Image, ImageGrab, ImageOps

# ============================================================================
# == 2. Coordinate related functions
# ============================================================================

# The position of top left corner of the game window (first brown pixel inside the black border)
x_pad = 995
y_pad = 300

chat_bubble_coordinates = [
    
]

# Checks each of the seats for a customer
def get_all_seat_color_sums():
    get_seat_one_sum()
    get_seat_two_sum()
    get_seat_three_sum()
    get_seat_four_sum()
    get_seat_five_sum()
    get_seat_six_sum()

# Checks each seat to see if there is a person sitting there by getting the color sum of each
#     chat bubble location and returning the value.
def get_seat_one_sum():
    # Chat bubble top left and bottom right corners
    # If you need to readjust these you should only need to change the X values
    box = (1025,356,1078,380)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    # Uncomment im.save if you would like to see what the program is using for the color sum
	# im.save(os.getcwd() + '\\seat_one__' + str(int(time.time())) + '.png', 'PNG')
    return a

def get_seat_two_sum():
    box = (1126,356,1179,380)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_three_sum():
    box = (1227,356,1280,380)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_four_sum():
    box = (1328,356,1381,380)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_five_sum():
    box = (1429,356,1482,380)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

def get_seat_six_sum():
    box = (1530,356,1583,380)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    return a

# ============================================================================
# == 3. Coordinate related functions
# ============================================================================

# Sushi color sum dictionary
# If you need to recalibrate these, run get_all_seat_color_sums and print a
sushiTypes = {2235:'onigiri',
              2879:'caliroll',
              2242:'gunkan'}

# Color sums of empty seats
class Blank:
    seat_1 = 8866
    seat_2 = 10766
    seat_3 = 11382
    seat_4 = 11922
    seat_5 = 11746
    seat_6 = 8454

# Menu item, phone (ordering), and menu navigation coordinates
# F = Food locations
# T = Topping menu locations
class Cord:
    f_shrimp = (20,320)
    f_nori   = (20,370)
    f_salmon = (20,425)
    f_roe    = (80,370)
    f_rice   = (80,315)
    f_unagi  = (80,425)

    phone = (560,355)
    menu_toppings = (530,270)
    menu_rice = (512,290)
    menu_sake = (530,315)
    buy_rice = (540,280)
    normal_delivery = (490,295)

    t_shrimp = (490,220)
    t_nori   = (490,280)
    t_salmon = (490,330)
    t_unagi  = (575,220)
    t_roe    = (575,280)
    t_exit   = (595,335)

    folding_mat = (200, 400)
    
# Skips the menu and starts a game
def startGame():
    left_click((320, 190))
    left_click((320, 380))
    left_click((585, 445))
    left_click((325, 360))

# Clears the plates
def clear_tables():
    left_click((80, 200))
    left_click((180, 200))
    left_click((280, 200))
    left_click((380, 200))
    left_click((480, 200))
    left_click((580, 200))

# ============================================================================
# == 3. Screen grabber
# ============================================================================

# Takes a grayscale screenshot of game and returns a color sum
def grab():
    box = (x_pad+1, y_pad+1, x_pad+640, y_pad+480)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return a

# Takes a screenshot of the entire game
def screenGrab():
    b1 = (x_pad+1, y_pad+1, x_pad+640, y_pad+480)
    im = ImageGrab.grab(b1)
    #im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

# ============================================================================
# == 3. Mouse actions and movement
# ============================================================================

# Simulates a mouse click
def left_click(coordinates_of_item):
    win32api.SetCursorPos((x_pad + coordinates_of_item[0], y_pad + coordinates_of_item[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.01)
    # Gave the game a second to catch up
    time.sleep(.1)

# Finds the mouse and returns its coordinates
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x, y

# ============================================================================
# == 3. Food quantity, mat folding, food checking, food making, and customer checking
# ============================================================================

# The default ingredient count
foodQuantity = {'shrimp':5,
                'rice':10,
                'nori':10,
                'roe':10,
                'salmon':5,
                'unagi':5}

# Folds the sushi mat
def foldMat():
    print 'trying to fold'
    left_click(Cord.folding_mat)
    
    time.sleep(.1)

# if any quantity is less than 4, buy more
def checkFood():
    for i, j in foodQuantity.items():
        if i == 'nori' or i == 'rice' or i == 'roe':
            if j <= 4:
                print '%s is low and needs to be replenished' % i
                buyFood(i)

# Algorithms for making each sushi type
def makeFood(food):
    if food == 'caliroll':
        print 'Making a caliroll'
        # keeps track internally of food count so it can perform efficient
        #     resupplies
        foodQuantity['rice'] -= 1
        foodQuantity['nori'] -= 1
        foodQuantity['roe'] -= 1
        # 'clicks' the location of each ingredient
        left_click(Cord.f_rice)
        
        time.sleep(.05)
        left_click(Cord.f_nori)
        
        time.sleep(.05)
        left_click(Cord.f_roe)
        
        time.sleep(.1)
        # Folds the mat and moves onto scanning
        foldMat()
        time.sleep(1.5)

    elif food == 'onigiri':
        print 'Making onigiri'
        foodQuantity['rice'] -= 2
        foodQuantity['nori'] -= 1
        left_click(Cord.f_rice)
        
        time.sleep(.05)
        left_click(Cord.f_rice)
        
        time.sleep(.05)
        left_click(Cord.f_nori)
        
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)

    elif food == 'gunkan':
        print 'Making a gunkan'
        foodQuantity['rice'] -= 1
        foodQuantity['nori'] -= 1
        foodQuantity['roe'] -= 2
        left_click(Cord.f_rice)
        
        time.sleep(.05)
        left_click(Cord.f_nori)
        
        time.sleep(.05)
        left_click(Cord.f_roe)
        
        time.sleep(.05)
        left_click(Cord.f_roe)
        
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)

# resupplying ingredients
def buyFood(food):
    if food == 'rice':
        left_click(Cord.phone)
        time.sleep(.1)
        
        left_click(Cord.menu_rice)
        time.sleep(.05)
        
        s = screenGrab()
        print 'test'
        time.sleep(.1)
        if s.getpixel(Cord.buy_rice) != (127, 127, 127):
            print 'rice is available'
            left_click(Cord.buy_rice)
            time.sleep(.1)
            
            left_click(Cord.normal_delivery)
            foodQuantity['rice'] += 10
            time.sleep(.1)
            
            time.sleep(2.5)
        else:
            print 'rice is NOT available'
            left_click(Cord.t_exit)
            
            time.sleep(1)
            buyFood(food)
    if food == 'nori':
        left_click(Cord.phone)
        time.sleep(.1)
        
        left_click(Cord.menu_toppings)
        time.sleep(.05)
        
        s = screenGrab()
        print 'test'
        time.sleep(.1)
        if s.getpixel(Cord.t_nori) != (33, 30, 11):
            print 'nori is available'
            left_click(Cord.t_nori)
            time.sleep(.1)
            
            left_click(Cord.normal_delivery)
            foodQuantity['nori'] += 10
            time.sleep(.1)
            
            time.sleep(2.5)
        else:
            print 'nori is NOT available'
            left_click(Cord.t_exit)
            
            time.sleep(1)
            buyFood(food)
    if food == 'roe':
        left_click(Cord.phone)
        time.sleep(.1)
        
        left_click(Cord.menu_toppings)
        time.sleep(.05)
        
        s = screenGrab()
        time.sleep(.1)
        if s.getpixel(Cord.t_roe) != (127, 61, 0):
            print 'roe is available'
            left_click(Cord.t_roe)
            time.sleep(.1)
            
            left_click(Cord.normal_delivery)
            foodQuantity['roe'] += 10
            time.sleep(.1)
            
            time.sleep(2.5)
        else:
            print 'roe is NOT available'
            left_click(Cord.t_exit)
            
            time.sleep(1)
            buyFood(food)

# Checks each of the chat bubbles and returns the sushi type
def check_bubs():
    clear_tables()

    checkFood()
    s1 = get_seat_one_sum()
    if s1 != Blank.seat_1:
        if sushiTypes.has_key(s1):
            print 'Table 1 is occupied and needs %s' % sushiTypes[s1]
            makeFood(sushiTypes[s1])
        else:
            print 'Sushi not found!!\n sushiType = %i' % s1
    else:
        print 'Table 1 unoccupied'

    checkFood()
    s2 = get_seat_two_sum()
    if s2 != Blank.seat_2:
        if sushiTypes.has_key(s2):
            print 'Table 2 is occupied and needs %s' % sushiTypes[s2]
            makeFood(sushiTypes[s2])
        else:
            print 'Sushi not found!!\n sushiType = %i' % s2
    else:
        print 'Table 2 unoccupied'

    checkFood()
    s3 = get_seat_three_sum()
    if s3 != Blank.seat_3:
        if sushiTypes.has_key(s3):
            print 'Table 3 is occupied and needs %s' % sushiTypes[s3]
            makeFood(sushiTypes[s3])
        else:
            print 'Sushi not found!!\n sushiType = %i' % s3
    else:
        print 'Table 3 unoccupied'

    checkFood()
    s4 = get_seat_four_sum()
    if s4 != Blank.seat_4:
        if sushiTypes.has_key(s4):
            print 'Table 4 is occupied and needs %s' % sushiTypes[s4]
            makeFood(sushiTypes[s4])
        else:
            print 'Sushi not found!!\n sushiType = %i' % s4
    else:
        print 'Table 4 unoccupied'

    clear_tables()
    checkFood()
    s5 = get_seat_five_sum()
    if s5 != Blank.seat_5:
        if sushiTypes.has_key(s5):
            print 'Table 5 is occupied and needs %s' % sushiTypes[s5]
            makeFood(sushiTypes[s5])
        else:
            print 'Sushi not found!!\n sushiType = %i' % s5
    else:
        print 'Table 5 unoccupied'

    checkFood()
    s6 = get_seat_six_sum()
    if s6 != Blank.seat_6:
        if sushiTypes.has_key(s6):
            print 'Table 1 is occupied and needs %s' % sushiTypes[s6]
            makeFood(sushiTypes[s6])
        else:
            print 'Sushi not found!!\n sushiType = %i' % s6
    else:
        print 'Table 6 unoccupied'

    clear_tables()
   

# ============================================================================
# == 3. Main
# ============================================================================
def main():
    startGame()
    while True:
        check_bubs()

if __name__ == '__main__':
    main()