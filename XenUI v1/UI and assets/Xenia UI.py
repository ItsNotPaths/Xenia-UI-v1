# mock up UI for proof of concept
# make assets
# render background, side panel, play opening sound + music and make intro animation?
# thx to https://www.svgrepo.com/ for button icons
import pygame
import sys
from sys import exit
import math
import random
import time
import os
from pygame import mixer
import shutil
import subprocess


screen_width = 1000
screen_height = 563
# 1000 x 563
ui_objects = []
intro_objects = []
run = False
Yv = -6
fade = 300
games = []
banners = []
rawscroll = 0
GameButtons = []
FNULL = open(os.devnull, 'w')

def setup_pygame():
    global keycodes, keynames, screen, clock
    pygame.init()
    pygame.display.set_caption('XenUI by Paths (v1.0)')
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    keycodes = open(r'UI and assets\pygame keycodes.txt', 'r')
    keycodes = keycodes.readlines()
    keynames = open(r'UI and assets\pygame keynames.txt', 'r')
    keynames = keynames.readlines()
    for i, v in enumerate(keycodes):
        keycodes[i] = keycodes[i].strip()
        keynames[i] = keynames[i].strip()
    return(screen, clock)

def tick(framerate):
    clock.tick(framerate)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(), exit()

def getKeys():
    global keysPressed
    keysPressed = list()
    keys = pygame.key.get_pressed()
    for i in keycodes:
        if keys[eval(i)]:
            keysPressed.append(i)

def load_assets():
    global ui_assets, testsurface, banners, Root, imgW, imgH, ratio, Font2Render
    gamesroot = Root + '\Games'
    ui_objects.append([pygame.transform.scale(pygame.image.load(r'UI and assets\close.png').convert_alpha(), (40, 40)), 14, 500, 60, 60, 'close'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(r'UI and assets\credits.png').convert_alpha(), (40, 40)), 14, 440, 60, 60, 'credits'])
    ui_objects.append([pygame.transform.scale(pygame.image.load(r'UI and assets\settings.png').convert_alpha(), (40, 40)), 14, 380, 60, 60, 'settings'])
    for i, v in enumerate(games):
        img = pygame.image.load(gamesroot + '\\' + v[0] + '\\' + v[1])
        imgW = img.get_width()
        imgH = img.get_height()
        if imgW > imgH:
            ratio = imgW / imgH
        else:
            ratio = imgH / imgW
        img = pygame.transform.scale(img, (880, 850 / ratio))
        imgW = img.get_width()
        imgH = img.get_height()
        banners.append([img, (100, 20), (0, (imgH / 2) - 50, 880, 100)])
    for i, v in enumerate(games):
        GameButtons.append([pygame.transform.scale(pygame.image.load(r'UI and assets\play.png').convert_alpha(), (60, 60)), 900, 40 + (120 * i), 60, 60, v[0]])
    pygame.font.init()
    Font2Render = pygame.font.SysFont(Font, 30)


def load_games():
    for file in os.listdir(Root + '\Games'):
        gamename = os.fsdecode(file)
        pngname = 'NULL'
        xexname = 'NULL'
        tomlname = 'NULL'
        for file in os.listdir(Root + '\Games' + '\\' + gamename):
            if file.endswith('.png'):
                pngname = os.fsdecode(file)
            if file == gamename:
                xexname = Root + gamename + gamename + 'default.xex'
            if file.endswith('.toml'):
                tomlname = os.fsdecode(file)
        if pngname == 'NULL':
            pngname = Root + r'XenUI v1\UI and assets\default.png'
        games.append([gamename, pngname, xexname, tomlname])

def render():
    global GameButtons
    screen.blit(pygame.transform.scale(pygame.image.load(r'UI and assets\bg.png').convert_alpha(), (1000, 563)), (0, 0))
    screen.blit(pygame.transform.scale(pygame.image.load(r'UI and assets\sidebar.png').convert_alpha(), (80, 563)), (0, 0))
    dark = pygame.Surface((880, 100), 32)
    dark.set_alpha(200, pygame.RLEACCEL)
    for i, v in enumerate(ui_objects):
        screen.blit(ui_objects[i][0], (ui_objects[i][1], ui_objects[i][2]))
    # here is the code for the banners (and effects, and name, and play button)
    for i, v in enumerate(banners):
        screen.blit(v[0], (v[1][0], v[1][1] + (i * 120) + (rawscroll * 10)), v[2])
        screen.blit(dark, (v[1][0], v[1][1] + (i * 120) + (rawscroll * 10)))
        NameText = Font2Render.render(games[i][0], False, (250, 250, 250))
        Font2Render.set_bold(True)
        screen.blit(NameText, (v[1][0] + 40, v[1][1] + 30 + (i * 120) + (rawscroll * 10)))
    for i, v in enumerate(GameButtons):
        screen.blit(GameButtons[i][0], (v[1], v[2]))
        GameButtons[i][2] = 40 + (120 * i) + (rawscroll * 10)

def intro_update():
    global fade
    for i in intro_objects:
        i[0].set_alpha(fade)
        screen.blit(i[0], (i[1][0], i[1][1]))
    pygame.display.update();

# applying setting variables now
settings = open(r'UI and assets\settings and info.txt', 'r')
settings = settings.readlines()
for i, v in enumerate(settings):
    settings[i] = str(v.strip('\n'))
settings[2] = 'Root = r' + settings[2]
for i in settings:
    exec(i)
icon = pygame.image.load(r'UI and assets\canary.png')
load_games()
setup_pygame()
pygame.display.set_icon(icon)
load_assets()
# now setting up the startup animation and mixer for sfx
if playintro == True:
    mixer.init()
    mixer.music.load(r'UI and assets\startup.wav')
    mixer.music.set_volume(0.3)
    intro_objects.append([pygame.transform.scale(pygame.image.load(r'UI and assets\intro bg.png').convert_alpha(), (1000, 563)), (0, 0)])
    intro_objects.append([pygame.image.load(r'UI and assets\xenia back.png').convert_alpha(), ((screen_width / 2) - 120, (screen_height / 2) - 100)])
    intro_objects.append([pygame.image.load(r'UI and assets\X.png').convert_alpha(), ((screen_width / 2) - 60, (screen_height / 2) - 100)])
    # starting animation
    for i in range (37):
        time.sleep(1 / 60)
        intro_objects[2][1] = (intro_objects[2][1][0], intro_objects[2][1][1] + Yv)
        Yv += .4
        intro_update()
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) - 40)
    intro_update()
    mixer.music.play() 
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) + 15)
    intro_objects[1][1] = ((screen_width / 2) - 120, (screen_height / 2) - 40)
    intro_update()
    Yv = -3.4
    for i in range (38):
        time.sleep(1 / 60)
        intro_objects[2][1] = (screen_width / 2) - 60, ((intro_objects[2][1][1]) + Yv)
        intro_objects[1][1] = (screen_width / 2) - 120, ((intro_objects[1][1][1]) + Yv)
        Yv += .1
        intro_update()
    intro_objects[2][1] = ((screen_width / 2) - 60, (screen_height / 2) - 45)
    intro_objects[1][1] = ((screen_width / 2) - 120, (screen_height / 2) - 100)
    intro_update()
    time.sleep(.3)
    # startup sequence has ended
    run = True
else:
    run = True

while run:
    tick(60)
    render()
    intro_update()
    fade -= 10
    getKeys()
    for i, v in enumerate(ui_objects):
        if ui_objects[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - ui_objects[i][1], pygame.mouse.get_pos()[1] - ui_objects[i][2] )):
            ui_objects[i][0].set_alpha(200 - ui_objects[i][0].get_alpha()/ 3)
            if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                if v[5] == 'close':
                    pygame.quit(), exit()
                if v[5] == 'settings':
                    os.startfile(r'UI and assets\settings and info.txt')
                if v[5] == 'credits':
                    os.startfile(r'UI and assets\credits.txt')
        else:
            ui_objects[i][0].set_alpha(ui_objects[i][0].get_alpha() - -20 / 3)
    for i, v in enumerate(GameButtons):
        if GameButtons[i][0].get_rect().collidepoint((pygame.mouse.get_pos()[0] - GameButtons[i][1], pygame.mouse.get_pos()[1] - GameButtons[i][2] )):
            GameButtons[i][0].set_alpha(200 - GameButtons[i][0].get_alpha()/ 3)
            if pygame.mouse.get_pressed(num_buttons=3)[0] == True:
                try:
                    os.remove(Root + '\\' + 'xenia-canary-config.toml')
                except:
                    pass
                for i2, v2 in enumerate(games):
                    if v2[0] == GameButtons[i][5]:
                        shutil.copyfile(Root + '\Games' + '\\' + v2[0] + '\\' + games[i2][3], Root + '\\' + games[i2][3])
                        try:
                            os.remove(Root + '\\' + 'xenia-canary.config.toml')
                        except:
                            pass
                        os.rename(Root + '\\' + games[i2][3], Root + '\\' + 'xenia-canary.config.toml')
                        os.startfile(Root + '\\' + 'Games' + '\\' + v2[0] + '\\' + v2[0] + '\\' + 'default.xex')
                        if CloseLaunch == True:
                            pygame.quit(), exit()
        else:
            GameButtons[i][0].set_alpha(GameButtons[i][0].get_alpha() - -20 / 3)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                rawscroll += 1
            elif event.button == 5:
                rawscroll -= 1
    if rawscroll > 0:
        rawscroll = 0
    pygame.display.update();