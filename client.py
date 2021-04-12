from pygame import display, RESIZABLE, font, QUIT, KEYDOWN, K_w, K_UP, K_s, K_DOWN, K_a, K_LEFT, K_d, K_RIGHT, K_SPACE, init, time
from pygame import draw as dra
from pygame import event as eve
from pygame import quit as pq
from tkinter import messagebox, Tk
import socket
from threading import Thread
from pickle import dumps, loads
import sys


init()                                                                          # INITIALIZE ALL IMPORTED PYGAME MODULES

### SOCKET SETUP ###
IP = "85.216.159.112"                                                           # IP FOR THE SERVER DEFAULT "85.216.159.112"
PORT = 50001                                                                    # PORT FOR SERVER DEFAULT 50001
ADDR = (IP, PORT)
DISCONN = "!?DISCONNECT"                                                        # DISCONNECT MESSAGE
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                           # AF_INET - IPv4
s.connect(ADDR)                                                                 # CONNECT TO SERVER
### SOCKET SETUP ###
### CLOUDS SETUP ###
WIDTH_CLOUDS, HEIGHT_CLOUDS = 100,100                                           # WIDTH = x; HEIGHT = y
VEL = HEIGHT_CLOUDS                                                             # VELOCITY IS THE SAME AS THE HEIGHT OF CLOUDS
x_cloud, y_cloud = 600, 600                                                     # CLOUD'S SPAWN POSITION
RESPAWN_CLOUD = x_cloud, y_cloud                                                # CLOUD'S RESPAWN POSITION
CLOUD_COLOUR = (255,255,255)                                                    # CLOUD'S COLOUR DEFAULT (255,255,255)
RAIN_COLOUR = (129,129,142)                                                     # RAIN CLOUD COLOUR DEFAULT (129,129,142)
x_rain, y_rain = 600, 0                                                         # RAIN CLOUD'S SPAWN POSITION
RESPAWN_RAIN = x_rain, y_rain                                                   # RAIN CLOUD'S RESPAWN POSITION
### CLOUDS SETUP ###
### WIN  SETUP + BASIC VARIABLE SETUP###
run = True                                                                      # MAIN LOOP False - CLOSE APP
WIN_CLOUD_COLOUR = (255,255,255)                                                # WHITE (NON-RAIN) CLOUD WIN TEXT COLOUR, DEFAULT - (255,255,255)
cloud = False                                                                   # ACCEPTED VALUES: False-white (non-rain) cloud, True-black (rain) cloud
WIDTH, HEIGHT = 1300, 700
WIN = display.set_mode((WIDTH, HEIGHT), RESIZABLE)                              # WIDTH = x; HEIGHT = y
display.set_caption("CLOUDS")
BG = (165,176,246)                                                              # BACK GROUND COLOUR DEFAULT (165,176,246)
BORDER_LINE_COLOR = (0,0,0)                                                     # COLOUR FOR WHITE CLOUD'S BORDER DEFAULT (0,0,0)
LINE_COLOUR = (255, 255, 255)
FPS = 60                                                                        # FRAMES PER SECOND - MAIN FUNCION DELAY
BORDER_UP = 0                                                                   # MAX y FOR CLOUDS
BORDER_DOWN = HEIGHT - HEIGHT_CLOUDS                                            # MAX x FOR CLOUDS ()
BORDER_LEFT = 0
BORDER_RIGHT = WIDTH - WIDTH_CLOUDS
### WIN  SETUP + BASIC VARIABLE SETUP ###
### WIN TEXT SETUP ###
FONT = font.SysFont('algerian', 60)                                             # WIN TEXT FONT AND SIZE, CHANGE VARIABLE "WIN_CLOUD_COLOUR" TO CHANGE THE COLOUR
SECONDS = 2                                                                     # WIN SCREEN VISIBLE FOR $ SECONDS DEFAULT 2
COUNT_DELAY_CLOUD = SECONDS * FPS                                               # ADDITIONAL VARIABLES FOR TEXT DELAY/COUNTDOWN
COUNT_DELAY_RAIN = SECONDS * FPS                                                # ADDITIONAL VARIABLES FOR TEXT DELAY/COUNTDOWN
odcount_cloud = False                                                           # ADDITIONAL VARIABLES FOR TEXT DELAY/COUNTDOWN
count_cloud = 0                                                                 # ADDITIONAL VARIABLES FOR TEXT DELAY/COUNTDOWN
### WIN TEXT SETUP ###
### LIGHTNING SETUP ###
countdown_bool_rain = False                                                     # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
boom_ready, boom = True, False                                                  # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
BOOM_COLOUR = (255, 255, 0)                                                     # LIGHTNING COLOUR DEFAULT (255,255,0)
boom_d = 0.25                                                                   # LIGHTNING LENGHT IN SECONDS DEFAULT 0.25
boom_wait = 1                                                                   # LIGHTNING RECHARGE DELAY DEFAULT 1
boom_timer = boom_wait * FPS                                                    # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
BOOM_TIME = boom_wait * FPS                                                     # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
boom_display_timer = boom_d * FPS                                               # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
BOOM_DISPLAY_TIME = boom_d * FPS                                                # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
countdown_rain = 0                                                              # ADDITIONAL VARIABLES FOR LIGHTNING DELAY/COUNTDOWN
### LIGHTNING SETUP ###

def recv():                                                                     # RECIEVES INFORMATION FROM SERVER
    global x_cloud, y_cloud, x_rain, y_rain
    while run == True:
        recieved = loads(s.recv(1024))

        if recieved == ("boom", "boom"):
            space_boom()

        if recieved != ("boom", "boom"):
            if cloud == True:
                x_cloud, y_cloud = recieved
            if cloud == False:
                x_rain, y_rain = recieved
def setup_threading():                                                          # PUTS recv() IN A THREAD
    thread = Thread(target=recv)
    thread.start()
    if cloud == True:
        s.send(dumps((x_rain, y_rain)))
    elif cloud == False:
        s.send(dumps((x_cloud, y_cloud)))
def setup_tk():                                                                 # YES/NO WINDOW AT THE START
    global cloud
    window = Tk()
    window.wm_withdraw()
    cloud = messagebox.askyesno("Cloud", "Do you want to be black (rain) cloud - YES or white (non-rain) cloud - NO")
def event():                                                                    # CHECKS FOR EVENTS
    global y_cloud, x_cloud, x_rain, y_rain, run, boom_timer, BOOM_TIME, boom_display_timer, recv_bool
    for event in eve.get():
        if event.type == QUIT:
            run = False
            recv_bool = False
            s.send(dumps(DISCONN))
            pq()
            s.close()
        elif event.type == KEYDOWN:
            if cloud == False:                                                  # ACCEPTED VALUES: False-white (non-rain) cloud, True-black (rain) cloud
                if ((event.key == K_w or event.key == K_UP) and (y_cloud - VEL) >= (BORDER_UP)):
                    y_cloud -= VEL
                    s.send(dumps((x_cloud,y_cloud)))
                if ((event.key == K_s or event.key == K_DOWN) and (y_cloud + VEL) <= (BORDER_DOWN)):
                    y_cloud += VEL
                    s.send(dumps((x_cloud,y_cloud)))
                if ((event.key == K_a or event.key == K_LEFT) and (x_cloud - VEL) >= (BORDER_LEFT)):
                    x_cloud -= VEL
                    s.send(dumps((x_cloud,y_cloud)))
                if ((event.key == K_d or event.key == K_RIGHT) and (x_cloud + VEL) <= (BORDER_RIGHT)):
                    x_cloud += VEL
                    s.send(dumps((x_cloud,y_cloud)))
            elif cloud == True:                                                 # ACCEPTED VALUES: False - white (non-rain) cloud, True - black (rain) cloud
                if ((event.key == K_w or event.key == K_UP) and (y_rain - VEL) >= (BORDER_UP)):
                    y_rain -= VEL
                    s.send(dumps((x_rain,y_rain)))
                if ((event.key == K_s or event.key == K_DOWN) and (y_rain + VEL) <= (BORDER_DOWN)):
                    y_rain += VEL
                    s.send(dumps((x_rain,y_rain)))
                if ((event.key == K_a or event.key == K_LEFT) and (x_rain - VEL) >= (BORDER_LEFT)):
                    x_rain -= VEL
                    s.send(dumps((x_rain,y_rain)))
                if ((event.key == K_d or event.key == K_RIGHT) and (x_rain + VEL) <= (BORDER_RIGHT)):
                    x_rain += VEL
                    s.send(dumps((x_rain,y_rain)))
                if event.key == K_SPACE and boom_timer == BOOM_TIME:
                    s.send(dumps(("boom", "boom")))
                    space_boom()
def draw():                                                                     # DRAWS THE WINDOW
    global win_angry, BG, boom, x_cloud, y_cloud, x_rain, y_rain, countdown_bool_rain, boom_display_timer
    WIN.fill(BG)
    dra.rect(WIN, CLOUD_COLOUR, (x_cloud, y_cloud, WIDTH_CLOUDS, HEIGHT_CLOUDS))
    dra.rect(WIN, RAIN_COLOUR, (x_rain, y_rain, WIDTH_CLOUDS, HEIGHT_CLOUDS))
    for coord in range (WIDTH//VEL):
        dra.line(WIN, LINE_COLOUR, ((coord+1)*VEL, BORDER_UP), ((coord+1)*VEL, BORDER_DOWN+WIDTH_CLOUDS), width=3)
    for coord in range(HEIGHT//VEL):
        if coord == 0:
            dra.line(WIN, BORDER_LINE_COLOR, (BORDER_LEFT, (coord+1)*VEL), (BORDER_RIGHT+WIDTH_CLOUDS, (coord+1)*VEL), width=3)
        else:
            dra.line(WIN, LINE_COLOUR, (BORDER_LEFT, (coord+1)*VEL), (BORDER_RIGHT+WIDTH_CLOUDS, (coord+1)*VEL), width=3)
    if odcount_cloud == True:
        cloud_win()
    if countdown_bool_rain == True:
        rain_win()
    if boom_display_timer+1 <= BOOM_DISPLAY_TIME:
        boom_coord = [(x_rain-100, y_rain, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain+100, y_rain, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain-100, y_rain-100, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain+100, y_rain+100, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain-100, y_rain+100, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain+100, y_rain-100, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain, y_rain-100, WIDTH_CLOUDS, HEIGHT_CLOUDS), (x_rain, y_rain+100, WIDTH_CLOUDS, HEIGHT_CLOUDS)]
        for coord in boom_coord:
            dra.rect(WIN, BOOM_COLOUR, coord)
            # print(coord[0:2], (x_cloud, y_cloud))
            if coord[0:2] == (x_cloud, y_cloud) or (x_rain, y_rain) == (x_cloud, y_cloud):
                x_cloud, y_cloud = RESPAWN_CLOUD
                x_rain, y_rain = RESPAWN_RAIN
                boom_display_timer = BOOM_DISPLAY_TIME
                countdown_bool_rain = True
        display.update()
    display.update()
def space_boom():                                                               # I LITELARY DON'T KNOW WHAT THIS DOES
    global boom, boom_timer, boom_display_timer
    boom = True
    boom_timer = 0
    boom_display_timer = 0
def ctrl_cloud():                                                               # CONTROLS CLOUD'S WIN SCREEN DELAY
    global odcount_cloud, count_cloud, x_cloud, y_cloud, x_rain, y_rain
    if y_cloud == 0:
        odcount_cloud = True
        x_cloud, y_cloud = RESPAWN_CLOUD
        x_rain, y_rain = RESPAWN_RAIN
    if y_cloud != 0 and odcount_cloud == True:
        count_cloud += 1
        if count_cloud == COUNT_DELAY_CLOUD:
            count_cloud = 0
            odcount_cloud = False
def cloud_win():                                                                # WRITES CLOUD'S WIN TEXT
    text = FONT.render('White mracik has won', True, WIN_CLOUD_COLOUR)
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    WIN.blit(text, textRect)
def boom_func():                                                                # CONTROLS RAIN CLOUD LIGHTNING DELAY
    global boom_timer, boom_display_timer
    if boom_timer+1 <= BOOM_TIME:
        boom_timer += 1
    if boom_display_timer+1 <= BOOM_DISPLAY_TIME:
        boom_display_timer += 1
        print(boom_display_timer, BOOM_DISPLAY_TIME)
def boom_touch_ctrl():                                                          # CONTROLS RAIN CLOUD LIGHTNING DELAY IF LIGHTNING TOUCHED CLOUD
    global x_cloud, y_cloud, x_rain, y_rain, countdown_bool_rain, COUNT_DELAY_RAIN, countdown_rain
    if countdown_rain+1 <= COUNT_DELAY_RAIN and countdown_bool_rain == True:
        countdown_rain += 1
    elif countdown_rain == COUNT_DELAY_RAIN and countdown_bool_rain == True:
        countdown_rain = 0
        countdown_bool_rain = False
def rain_win():                                                                 # WRITES RAIN CLOUD'S WIN TEXT
    text = FONT.render('Rain mracik has won', True, (129,129,142))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2)
    WIN.blit(text, textRect)
def main():                                                                     # MAIN FUNCTION
    clock = time.Clock()
    while run:
        clock.tick(FPS)                                                         # DELAY TO PROVIDE STABLE FPS
        ctrl_cloud()
        boom_touch_ctrl()
        boom_func()
        draw()
        event()
if __name__ == "__main__":
    setup_tk()
    setup_threading()
    main()
