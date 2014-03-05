import ImageGrab, Image, ImageOps
import os
import time
import win32api, win32con
from numpy import *

# position of top left game window
x_pad = 997
y_pad = 335


# food types (with color sum) and food quantities
sushiTypes = {1467:'onigiri',
              1585:'caliroll',
              1197:'gunkan',}

foodQuantity = {'shrimp':5,
                'rice':10,
                'nori':10,
                'roe':10,
                'salmon':5,
                'unagi':5}


# coordinates of ingredients, phone menu, and buttons
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


# color sum when empty
class Blank:
    seat_1 = 8172
    seat_2 = 9286
    seat_3 = 9377
    seat_4 = 9899
    seat_5 = 9240
    seat_6 = 9458


# take screenshot of game
def screenGrab():
    b1 = (x_pad+1, y_pad+1, x_pad+640, y_pad+480)
    im = ImageGrab.grab(b1)
    #im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return im


# grayscale screenshot of game with color sum
def grab():
    box = (x_pad+1, y_pad+1, x_pad+640, y_pad+480)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    return a


# mouse operations
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
##    print "Click."
    time.sleep(.01)


## adjusts mouse to game window
def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))


# gets mouse coordinates
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print x, y


# starting menu navigation -> ends with game starting
def startGame():
    mousePos((320, 190))
    leftClick()
    time.sleep(.1)
    mousePos((320, 380))
    leftClick()
    time.sleep(.1)
    mousePos((585, 445))
    leftClick()
    time.sleep(.1)
    mousePos((325, 360))
    leftClick()
    time.sleep(.1)

# cycles through tables to clean plates
def clear_tables():
    mousePos((90, 200))
    leftClick()

    mousePos((190, 200))
    leftClick()

    mousePos((290, 200))
    leftClick()

    mousePos((390, 200))
    leftClick()

    mousePos((650, 200))
    leftClick()

    mousePos((590, 200))
    leftClick()

    time.sleep(1)

# making the different types of sushi
def makeFood(food):
    if food == 'caliroll':
        print 'Making a caliroll'
        foodQuantity['rice'] -= 1 
        foodQuantity['nori'] -= 1 
        foodQuantity['roe'] -= 1  
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_nori)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_roe)
        leftClick()
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)
        
	
    elif food == 'onigiri':
        print 'Making a onigiri'
        foodQuantity['rice'] -= 2  
        foodQuantity['nori'] -= 1  
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_nori)
        leftClick()
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)

    elif food == 'gunkan':
        foodQuantity['rice'] -= 1  
        foodQuantity['nori'] -= 1  
        foodQuantity['roe'] -= 2   
        mousePos(Cord.f_rice)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_nori)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_roe)
        leftClick()
        time.sleep(.05)
        mousePos(Cord.f_roe)
        leftClick()
        time.sleep(.1)
        foldMat()
        time.sleep(1.5)


# if any quantity is less than 4, buy more
def checkFood():
    for i, j in foodQuantity.items():
        if i == 'nori' or i == 'rice' or i == 'roe':
            if j <= 4:
                print '%s is low and needs to be replenished' % i
                buyFood(i)


# resupplying ingredients
def buyFood(food):
    if food == 'rice':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_rice)
        time.sleep(.05)
        leftClick()
        s = screenGrab()
        print 'test'
        time.sleep(.1)
        if s.getpixel(Cord.buy_rice) != (127, 127, 127):
            print 'rice is available'
            mousePos(Cord.buy_rice)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.normal_delivery)
            foodQuantity['rice'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
        else:
            print 'rice is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'nori':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        time.sleep(.05)
        leftClick()
        s = screenGrab()
        print 'test'
        time.sleep(.1)
        if s.getpixel(Cord.t_nori) != (33, 30, 11):
            print 'nori is available'
            mousePos(Cord.t_nori)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.normal_delivery)
            foodQuantity['nori'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
        else:
            print 'nori is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)
    if food == 'roe':
        mousePos(Cord.phone)
        time.sleep(.1)
        leftClick()
        mousePos(Cord.menu_toppings)
        time.sleep(.05)
        leftClick()
        s = screenGrab()
        time.sleep(.1)
        if s.getpixel(Cord.t_roe) != (127, 61, 0):
            print 'roe is available'
            mousePos(Cord.t_roe)
            time.sleep(.1)
            leftClick()
            mousePos(Cord.normal_delivery)
            foodQuantity['roe'] += 10
            time.sleep(.1)
            leftClick()
            time.sleep(2.5)
        else:
            print 'roe is NOT available'
            mousePos(Cord.t_exit)
            leftClick()
            time.sleep(1)
            buyFood(food)

# folds the sushi
def foldMat():
    print 'trying to fold'
    mousePos(Cord.folding_mat)
    leftClick()
    time.sleep(.1)

# gets the different seats and checks the color sum to see if there's a
# person requesting sushi
def get_seat_one():
    box = (1022,399,1085,407)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    # im.save(os.getcwd() + '\\seat_one__' + str(int(time.time())) + '.png', 'PNG')
    return a


def get_seat_two():
    box = (1123,399,1186,407)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
##    im.save(os.getcwd() + '\\seat_two__' + str(int(time.time())) + '.png', 'PNG')    
    return a


def get_seat_three():
    box = (1224,399,1287,407)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
##    im.save(os.getcwd() + '\\seat_three__' + str(int(time.time())) + '.png', 'PNG')    
    return a


def get_seat_four():
    box = (1325,399,1388,407)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
##    im.save(os.getcwd() + '\\seat_four__' + str(int(time.time())) + '.png', 'PNG')    
    return a


def get_seat_five():
    box = (1426,399,1489,407)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
##    im.save(os.getcwd() + '\\seat_five__' + str(int(time.time())) + '.png', 'PNG')    
    return a


def get_seat_six():
    box = (1527,399,1590,407)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    a = array(im.getcolors())
    a = a.sum()
    print a
    # im.save(os.getcwd() + '\\seat_six__' + str(int(time.time())) + '.png', 'PNG')
    return a


#checks the seats (looped)
def get_all_seats():
    get_seat_one()
    get_seat_two()
    get_seat_three()
    get_seat_four()
    get_seat_five()
    get_seat_six()


# checks to see which sushi type the person wants
def check_bubs():
    checkFood()
    s1 = get_seat_one()
    if s1 != Blank.seat_1:
        if sushiTypes.has_key(s1):
            print 'table 1 is occupied and needs %s' % sushiTypes[s1]
            makeFood(sushiTypes[s1])
        else:
            print 'sushi not found!\n sushiType = %i' % s1
    else:
        print 'Table 1 unoccupied'
    clear_tables()
    checkFood()
    s2 = get_seat_two()
    if s2 != Blank.seat_2:
        if sushiTypes.has_key(s2):
            print 'table 2 is occupied and needs %s' % sushiTypes[s2]
            makeFood(sushiTypes[s2])
        else:
            print 'sushi not found!\n sushiType = %i' % s2
    else:
        print 'Table 2 unoccupied'

    checkFood()
    s3 = get_seat_three()
    if s3 != Blank.seat_3:
        if sushiTypes.has_key(s3):
            print 'table 3 is occupied and needs %s' % sushiTypes[s3]
            makeFood(sushiTypes[s3])
        else:
            print 'sushi not found!\n sushiType = %i' % s3
    else:
        print 'Table 3 unoccupied'

    checkFood()
    s4 = get_seat_four()
    if s4 != Blank.seat_4:
        if sushiTypes.has_key(s4):
            print 'table 4 is occupied and needs %s' % sushiTypes[s4]
            makeFood(sushiTypes[s4])
        else:
            print 'sushi not found!\n sushiType = %i' % s4
    else:
        print 'Table 4 unoccupied'

    clear_tables()
    checkFood()
    s5 = get_seat_five()
    if s5 != Blank.seat_5:
        if sushiTypes.has_key(s5):
            print 'table 5 is occupied and needs %s' % sushiTypes[s5]
            makeFood(sushiTypes[s5])
        else:
            print 'sushi not found!\n sushiType = %i' % s5
    else:
        print 'Table 5 unoccupied'

    checkFood()
    s6 = get_seat_six()
    if s6 != Blank.seat_6:
        if sushiTypes.has_key(s6):
            print 'table 1 is occupied and needs %s' % sushiTypes[s6]
            makeFood(sushiTypes[s6])
        else:
            print 'sushi not found!\n sushiType = %i' % s6
    else:
        print 'Table 6 unoccupied'
    clear_tables()

# run baby run
def main():
    startGame()
    while True:
        check_bubs()

if __name__ == '__main__':
    main()
