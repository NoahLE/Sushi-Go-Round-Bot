Sushi-Go-Round Bot
==================

This is a really basic Python bot. It uses some very simple machine vision techniques and window coordinates to play complete rounds of the flash game Sushi-Go-Round.

The initial bot was based off of <a href="http://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117">this tutorial.</a>

<h2>Tools Used</h2>
Pycharm, Sublime, Git, VirtualEnv <br>	
Numpy, win32api

<h2>Setup</h2>
Setup should be pretty simple, especially if you are using a 1920 x 1080 resolution.

<b>For 1920 x 1080 people:</b> <br>
Open <a href="http://www.miniclip.com/games/sushi-go-round/en/">the game</a> and dock your browser on the right side of your screen (hold down the Windows / Super key and press the right arrow key until it's locked in).
<br><br>
You can check to make sure your mouse will line up with the ingame coordinates by running screen_grab_debugging.py or any of the screen grabbing functions.
<br><br>
<b>For everyone else:</b> <br>
Open <a href="http://www.miniclip.com/games/sushi-go-round/en/">the game</a> and dock your browser on the right side of your screen (hold down the Windows key and press the right arrow key until it's locked in).
<br><br>
The first thing you should do is run screen_grab_debugging.py to grab a shot of your screen. Inside of sushi_bot.py on lines 28 and 29 change x_pad and y_pad to the top left corner of the game (in the brown pixel between two black pixels). This can be done in Photoshop, Paint.net, or any other image editor of your choice. See section 2. Screen specific coordinates in sushi_bot.py.
<br><br>
After this is done, you might need to recalibrate the sushi grayscale sum (see code under 3. Grayscale sums).

<h2>For Windows users</h2>
I had a problem with screen scaling (the screen shot will be too small) which can be turned off via Control Panel > Display (move it to the far left).