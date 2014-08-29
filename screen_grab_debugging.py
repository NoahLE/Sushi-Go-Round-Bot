import ImageGrab
import os
import time

# Global Variables
x_pad = 995
y_pad = 300

"""
All coordinates are based on a right docked Firefox window
 with the bookmarks toolbar shown and with a 1920x1080
 screen resolution
"""

def screenGrab():
    # selects only game in screen shot
    box = (x_pad+1, y_pad+1,x_pad+640, y_pad+480)
    # snapshot of screen
    im = ImageGrab.grab(box)
    # saves in current work directory with name based on time of pic
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time()))
            + '.png', 'PNG')

def main():
    screenGrab()

if __name__ == '__main__':
    main()

# (997,335,1636,814)