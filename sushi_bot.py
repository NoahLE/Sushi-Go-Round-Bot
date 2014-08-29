# Sushi-Go-Round Python Bot
# By DigitalMockingbird
# Updated 8/24/2014
#
# Sections
# 1. Imports
# 2. Screen specific coordinates
# 3. Grayscale sums
# 4. Coordinate related functions
# 5. Screen grabbing functions
# 6. Mouse actions and movement
# 7. Food quantity, mat folding, food checking, food making, and customer checking
# 8. The body of the bot
# 9. Main function
#
# See readme for setup and debugging logic

# ====================================================================================
# == 1. Imports - win32api and win32con is windows only
# ====================================================================================

import os
import time
from numpy import *
import win32api, win32con
import  Image, ImageGrab, ImageOps

# ====================================================================================
# == 2. Screen specific coordinates
# ====================================================================================

# The position of top left corner of the game window (first brown pixel inside the black border)
x_pad = 995
y_pad = 300

# ====================================================================================
# == 3. Grayscale sums
# ====================================================================================

seat_color_sums = [0,0,0,0,0,0]

# Gets the color sum of each chat bubble position
def get_all_grayscale_sums(chat_bubble_coordinates):
    for seat in range(0,6):
        image = ImageOps.grayscale(ImageGrab.grab(chat_bubble_coordinates[seat]))
        color_sum = array(image.getcolors())
        color_sum = color_sum.sum()
        seat_color_sums[seat] = color_sum

# Sushi color sum dictionary
# If you need to recalibrate these, run get_all_seat_color_sums and print a
sushi_types = {2235:'onigiri',
              2879:'caliroll',
              2242:'gunkan'}

# Color sums of empty seats
class empty_seat_sum:
    seat_1 = 8866
    seat_2 = 10766
    seat_3 = 11382
    seat_4 = 11922
    seat_5 = 11746
    seat_6 = 8454

# ====================================================================================
# == 4. Coordinate related functions
# ====================================================================================

# A box taken inside the white part of the chat bubble.
# This could be turned into a formula
chat_bubble_coordinates = (
    # Seat 1
    ((x_pad + 30), (y_pad + 56), (x_pad + 83), (y_pad + 80)),
    # Seat 2
    ((x_pad + 131), (y_pad + 56), (x_pad + 184), (y_pad + 80)),
    # Seat 3
    ((x_pad + 232), (y_pad + 56), (x_pad + 285), (y_pad + 80)),
    # Seat 4
    ((x_pad + 333), (y_pad + 56), (x_pad + 386), (y_pad + 80)),
    # Seat 5
    ((x_pad + 434), (y_pad + 56), (x_pad + 487), (y_pad + 80)),
    # Seat 6
    ((x_pad + 5351), (y_pad + 56), (x_pad + 588), (y_pad + 80))
)


# Menu item, phone (ordering), and menu navigation coordinates
class Cord:
    # f = Topping menu locations
    t_shrimp = (490,220)
    t_nori   = (490,280)
    t_salmon = (490,330)
    t_unagi  = (575,220)
    t_roe    = (575,280)
    t_exit   = (595,335)

    # f = Food locations
    f_shrimp = (20, 320)
    f_nori   = (20, 370)
    f_salmon = (20, 425)
    f_roe    = (80, 370)
    f_rice   = (80, 315)
    f_unagi  = (80, 425)

    phone = (560, 355)
    menu_toppings = (530, 270)
    menu_rice = (512, 290)
    menu_sake = (530, 315)
    buy_rice = (540, 280)
    normal_delivery = (490, 295)

    folding_mat = (200, 400)
    
# Skips the menu and starts a game
def startGame():
    left_click((325, 375))
    left_click((320, 190))
    left_click((320, (y_pad + 80)))
    left_click((585, 445))
    left_click((325, 360))

# Clears the plates
def clear_plates():
    left_click((80, 200))
    left_click((180, 200))
    left_click((280, 200))
    left_click((380, 200))
    left_click((480, 200))
    left_click((580, 200))

# ====================================================================================
# == 5. Screen grabbing functions
# ====================================================================================

# Takes a grayscale screenshot of game and returns a color sum
def grayscale_grab():
    box = (x_pad+1, y_pad+1, x_pad+640, y_pad+480)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return a

# Takes a screenshot of the entire game - for debugging
def screen_grab():
    b1 = (x_pad+1, y_pad+1, x_pad+640, y_pad+480)
    im = ImageGrab.grab(b1)
    im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

# ====================================================================================
# == 6. Mouse actions and movement
# ====================================================================================

# Simulates a mouse click
def left_click(coordinates_of_item):
    win32api.SetCursorPos((x_pad + coordinates_of_item[0], y_pad + coordinates_of_item[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    # Gave the game a second to catch up
    time.sleep(.1)

# Finds the mouse and returns its coordinates
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x, y

# ====================================================================================
# == 7. Food quantity, mat folding, food checking, food making, and customer checking
# ====================================================================================

# The default ingredient count
food_quantity = {'shrimp':5,
                'rice':10,
                'nori':10,
                'roe':10,
                'salmon':5,
                'unagi':5}

# if any quantity is less than 4, buy more
def check_ingredient_count():
    for food, food_count in food_quantity.items():
        if food == 'nori' or food == 'rice' or food == 'roe':
            # checks and buys a resupply of low ingredients
            if food_count <= 3:
                print '%s is low and needs to be replenished' % food
                buy_food(food)

# Algorithms for making each sushi type
def make_food(food):
    if food == 'caliroll':
        print 'Making a caliroll'
        # keeps track internally of food count so it can perform efficient
        #     resupplies
        food_quantity['rice'] -= 1
        food_quantity['nori'] -= 1
        food_quantity['roe'] -= 1
        # 'clicks' the location of each ingredient
        left_click(Cord.f_rice)
        left_click(Cord.f_nori)
        left_click(Cord.f_roe)
        # Folds the mat and moves onto scanning
        left_click(Cord.folding_mat)

    elif food == 'onigiri':
        print 'Making onigiri'
        food_quantity['rice'] -= 2
        food_quantity['nori'] -= 1
        left_click(Cord.f_rice)
        left_click(Cord.f_rice)
        left_click(Cord.f_nori)
        left_click(Cord.folding_mat)

    elif food == 'gunkan':
        print 'Making a gunkan'
        food_quantity['rice'] -= 1
        food_quantity['nori'] -= 1
        food_quantity['roe'] -= 2
        left_click(Cord.f_rice)
        left_click(Cord.f_nori)
        left_click(Cord.f_roe)
        left_click(Cord.f_roe)
        left_click(Cord.folding_mat)

# resupplying ingredients
def buy_food(food):
    clear_plates()
    if food == 'rice':
        # Opens the phone and enters the rice menu
        left_click(Cord.phone)
        left_click(Cord.menu_rice)
        s = screen_grab()
        # Checks the color sum to see if you have enough money
        if s.getpixel(Cord.buy_rice) != (127, 127, 127):
            print 'rice is available'
            # buys and delivers rice
            left_click(Cord.buy_rice)
            left_click(Cord.normal_delivery)
            # adds 10 for quantity tracking
            food_quantity['rice'] += 10
            # clear plates and pause for 4 seconds (resupply has a delay)
            clear_plates()
            time.sleep(4)
        else:
            # if none available loop until you can buy some
            print 'rice is NOT available'
            buy_food(food)

    if food == 'nori':
        left_click(Cord.phone)
        left_click(Cord.menu_toppings)
        s = screen_grab()
        if s.getpixel(Cord.t_nori) != (33, 30, 11):
            print 'nori is available'
            left_click(Cord.t_nori)
            left_click(Cord.normal_delivery)
            food_quantity['nori'] += 10
            clear_plates()
            time.sleep(4)
        else:
            print 'nori is NOT available'
            buy_food(food)

    if food == 'roe':
        left_click(Cord.phone)
        left_click(Cord.menu_toppings)
        s = screen_grab()
        if s.getpixel(Cord.t_roe) != (127, 61, 0):
            print 'roe is available'
            left_click(Cord.t_roe)
            left_click(Cord.normal_delivery)
            food_quantity['roe'] += 10
            clear_plates()
            time.sleep(4)
        else:
            print 'roe is NOT available'
            buy_food(food)

# ====================================================================================
# == 8. The body of the bot
# ====================================================================================

# Checks each of the chat bubbles and returns the sushi type
def check_customers():
    clear_plates()
    # Loops through each seat
    for seat in range(0,6):
        # Check and resupply low ingredients
        check_ingredient_count()
        # Get grayscale sum to check for sushi requests
        get_all_grayscale_sums(chat_bubble_coordinates)
        seat_sum = seat_color_sums[seat]
        if seat_sum != empty_seat_sum.seat_1:
            # Detect and make sushi
            if sushi_types.has_key(seat_sum):
                print 'Table {0} is occupied and needs {1}.'.format(seat, sushi_types[seat_sum])
                make_food(sushi_types[seat_sum])
            else:
                # print 'Table {0} is unoccupied.'.format(seat)
                clear_plates()
   

# ====================================================================================
# == 9. Main
# ====================================================================================
def main():
    try:
        while True:
            startGame()
            while True:
                check_customers()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()