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
# from datetime import datetime, time
from numpy import *
import win32api, win32con
import  Image, ImageGrab, ImageOps

# ====================================================================================
# == 2. Screen specific coordinates
# ====================================================================================

# The position of top left corner of the game window (first brown pixel inside the black border)
x_pad = 974
y_pad = 86
# x_pad = 995
# y_pad = 300

# ====================================================================================
# == 3. Grayscale sums
# ====================================================================================

# Gets the color sum of each chat bubble position
def get_all_grayscale_sums(chat_bubble_coordinates):
    seat_color_sums = [0, 0, 0, 0, 0, 0]
    for seat in range(0, 6):
        image = ImageOps.grayscale(ImageGrab.grab(chat_bubble_coordinates[seat]))
        color_sum = array(image.getcolors())
        color_sum = color_sum.sum()
        seat_color_sums[seat] = color_sum
    return seat_color_sums

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
    ((x_pad + 535), (y_pad + 56), (x_pad + 588), (y_pad + 80))
)

# Menu item, phone (ordering), and menu navigation coordinates
class Cord:
    phone = (560, 355)
    menu_toppings = (530, 270)
    topping_exit = (595, 335)
    menu_rice = (512, 290)
    rice_exit = (585, 335)
    normal_delivery = (490, 290)

    buy_nori = (470, 275)
    buy_roe = (555, 275)
    buy_rice = (515, 275)
    
    folding_mat = (200, 400)
    use_nori = (35, 390)
    use_roe = (90, 390)
    use_rice = (90, 330)

# Skips the menu and starts a game
def start_game():
    left_click((325, 375))
    left_click((320, 190))
    left_click((320, 390))
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
    box = (x_pad, y_pad, x_pad+640, y_pad+480)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return a

# Takes a screenshot of the entire game - for debugging
def screen_grab():
    box = (x_pad, y_pad, x_pad+640, y_pad+480)
    im = ImageGrab.grab(box)
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

# ====================================================================================
# == 6. Mouse actions and movement
# ====================================================================================

# Simulates a mouse click
def left_click(item_coordinates):
    win32api.SetCursorPos((x_pad + item_coordinates[0], y_pad + item_coordinates[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    # Gave the game a second to catch up
    time.sleep(.2)

# Finds the mouse and returns its coordinates
def get_cords():
    x, y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x, y

# ====================================================================================
# == 7. Food quantity, mat folding, food checking, food making, and customer checking
# ====================================================================================

# if any quantity is less than 4, buy more
def check_ingredient_count():
    for food, food_count in food_quantity.items():
        if food == 'nori' or food == 'rice' or food == 'roe':
            # checks and buys a resupply of low ingredients
            if food_count <= 3:
                # print '%s is low and needs to be replenished' % food
                buy_food(food)

# resupplying ingredients
def buy_food(food):
    clear_plates()
    left_click(Cord.phone)
    if food == 'rice':
        left_click(Cord.menu_rice)
    else:
        left_click(Cord.menu_toppings)

    s = screen_grab()

    if food == 'rice':
        if (s.getpixel(Cord.buy_rice)) == (237, 166, 171):
            # print 'Rice is available.'
            # buys and delivers rice
            left_click(Cord.buy_rice)
            time.sleep(.3)
            left_click(Cord.normal_delivery)
            # adds 10 for quantity tracking
            food_quantity['rice'] += 10
            # clear plates and pause for 4 seconds (resupply has a delay)
            time.sleep(3)
        elif (s.getpixel(Cord.buy_rice)) == (118, 83, 85):
            # if none available loop until you can buy some
            print 'Rice is NOT available.'
            left_click(Cord.rice_exit)
            time.sleep(5)
            buy_food('rice')
        else:
            print 'Idk if I can buy anything'

    if food == 'nori':
        if (s.getpixel(Cord.buy_nori)) == (218, 246, 255):
            # print 'Nori is available.'
            left_click(Cord.buy_nori)
            time.sleep(.3)
            left_click(Cord.normal_delivery)
            food_quantity['nori'] += 10
            time.sleep(3)
        elif (s.getpixel(Cord.buy_nori)) == (109, 123, 127):
            print 'Nori is NOT available'
            left_click(Cord.topping_exit)
            time.sleep(5)
            buy_food('nori')
        else:
            print 'Idk if I can buy anything'

    if food == 'roe':
        if (s.getpixel(Cord.buy_roe)) == (218, 246, 255):
            # print 'Roe is available.'
            left_click(Cord.buy_roe)
            time.sleep(.3)
            left_click(Cord.normal_delivery)
            food_quantity['roe'] += 10
            time.sleep(3)
        elif (s.getpixel(Cord.buy_roe)) == (109, 123, 127):
            print 'Roe is NOT available'
            left_click(Cord.topping_exit)
            time.sleep(5)
            buy_food('roe')
        else:
            print 'Idk if I can buy anything'

# Algorithms for making each sushi type
def make_food(food):
    if food == 2879:
        # print 'Making a caliroll'
        # keeps track internally of food count so it can perform efficient
        #     resupplies
        food_quantity['rice'] -= 1
        food_quantity['nori'] -= 1
        food_quantity['roe'] -= 1
        # 'clicks' the location of each ingredient
        left_click(Cord.use_nori)
        left_click(Cord.use_roe)
        left_click(Cord.use_rice)
        # Folds the mat and moves onto scanning
        left_click(Cord.folding_mat)
        time.sleep(.5)

    elif food == 2235:
        # print 'Making onigiri'
        food_quantity['rice'] -= 2
        food_quantity['nori'] -= 1
        left_click(Cord.use_rice)
        left_click(Cord.use_nori)
        left_click(Cord.use_rice)
        left_click(Cord.folding_mat)
        time.sleep(.5)

    elif food == 2242:
        # print 'Making a gunkan'
        food_quantity['rice'] -= 1
        food_quantity['nori'] -= 1
        food_quantity['roe'] -= 2
        left_click(Cord.use_roe)
        left_click(Cord.use_rice)
        left_click(Cord.use_nori)
        left_click(Cord.use_roe)
        left_click(Cord.folding_mat)
        time.sleep(.5)

# ====================================================================================
# == 8. The body of the bot
# ====================================================================================

def bot_calibration():
    # The default ingredient count
    global food_quantity
    food_quantity = {'rice':10, 'nori':10, 'roe':10}

    # Sushi color sum dictionary
    global sushi_sums
    sushi_sums = ['onigiri', 2235, 'caliroll', 2879, 'gunkan', 2242]

    global empty_seat_sum
    empty_seat_sum = get_all_grayscale_sums(chat_bubble_coordinates)

    # # Last time this seat was used
    # global seat_timestamps
    # seat_timestamps = [0, 0, 0, 0, 0, 0]

    # for seat in range(0,6):
    #     seat_timestamps[seat] = int(time.time())

    # # Time for food to arrive and be eaten at a seat
    # global seat_cooldown
    # seat_cooldown = [11, 13, 17, 18, 21, 25]

# ====================================================================================
# == 8. The body of the bot
# ====================================================================================

# Checks each of the chat bubbles and returns the sushi type
def check_customers():
    clear_plates()
    time.sleep(5)
    clear_plates()
    time.sleep(5)
    for seat in range(0,6):
        # Time that has passed since last person sitting here was served
        # time_elapsed = (int(time.time()) - seat_timestamps[seat])
        # if time_elapsed > seat_cooldown[seat]:
            # print time_elapsed - seat_cooldown[seat]
            # Scan bubbles
            seat_sum = get_all_grayscale_sums(chat_bubble_coordinates)
            # If seat is not empty
            if seat_sum[seat] != empty_seat_sum[seat]:
                # They're gone, clear the plates
                check_ingredient_count()
                make_food(seat_sum[seat])
                # seat_cooldown.insert(seat, int(time.time()))

# ====================================================================================
# == 9. Main
# ====================================================================================

def main():
    # Skip menus
    start_game()
    bot_calibration()
    while True:
        check_customers()

if __name__ == '__main__':
    main()