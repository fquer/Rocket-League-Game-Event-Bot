import keyboard
import pyautogui as pag
from time import sleep, time
import os
import numpy as np
import random
import easyocr
reader = easyocr.Reader(['en'])

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INIT_SLEEP = 3
FIND_AND_CLICK = 0.5
FIND_AND_CLICK_END = 1

FIND_AND_CLICK_TIMEOUT = 60
WAIT_FOR_FIND_GAME_TIMEOUT = 500

FIND_AND_CLICK_WAIT_END = 2
FIND_AND_CLICK_WAIT_SLEEP = 1
WAIT_FOR_FIND_GAME_SLEEP = 1
PLAY_GAME_SLEEP = 0.5

FORFEIT_ESC_SLEEP = 1

DEFINED_KEYS_THROTTLE = ['w', 's']
DEFINED_KEYS_STEER = ['a', 'd', 'o']
DEFINED_KEYS_SLEEP = [0.5, 1, 1.5, 2, 2.5, 3, 3.5]

def findItem(item):
    try:
        x, y = pag.locateCenterOnScreen('bot_ss\\' + item + '.PNG', grayscale=False, confidence = 0.9)
        return [x, y]
    except:
        return False

def findAndClickItem(item):
    pos = findItem(item)
    if pos == False:
        print('Item cant clicked : ' + item)
        return False
    else:
        pag.moveTo(pos[0], pos[1])
        sleep(FIND_AND_CLICK)
        pag.click()
        print('Item clicked : ' + item)
        sleep(FIND_AND_CLICK_END)
        return True

def findAndClickItemWait(item):
    startTime = time()
    while True:
        if findAndClickItem(item):
            return True
        elif time() - startTime > FIND_AND_CLICK_TIMEOUT:
            print('time out ' + item)
            break
        print('Waited ' + str(FIND_AND_CLICK_WAIT_SLEEP) + ' seconds. For ' + item)
        sleep(FIND_AND_CLICK_WAIT_SLEEP)
    sleep(FIND_AND_CLICK_WAIT_END)

def getText(input):
    referans = findItem('referans')

    if referans == False:
        print('cant find getText references')
        return False
    else:
        pos = referans
    
    im = pag.screenshot()
    if input == 'matchTime':
        img_cropped = im.crop((pos[0] + 473, pos[1] + 26, pos[0] + 567, pos[1] + 56))
    
    result = reader.readtext(np.array(img_cropped), detail = 0)
    if result != []:
        return result[0]
    else:
        return 'nok'

def getMatchStatus():
    matchTime = getText('matchTime')
    if matchTime != False:
        if matchTime[0] == '4':
            return 'GameStarted'
        elif matchTime[0] == '3':
            return 'TimeToFF'
        else:
            return 'CantGetStatus'
    else:
        return False

def playGame():
    print('PIPE: Play game.')
    while True:
        throttleKey = random.choice(DEFINED_KEYS_THROTTLE)
        steerKey = random.choice(DEFINED_KEYS_STEER)
        keySleep = random.choice(DEFINED_KEYS_SLEEP)
        keyboard.press(throttleKey)
        keyboard.press(steerKey)
        sleep(keySleep)
        keyboard.release(throttleKey)
        keyboard.release(steerKey)
        pag.click(button='right')
        sleep(PLAY_GAME_SLEEP)

        if getMatchStatus() == 'TimeToFF':
            forfeitMatch()
            waitForFindGame()
            return True
        elif findItem('playlist'):
            waitForNewGame()
            return True

def forfeitMatch():
    print('PIPE: Forfeit match.')
    keyboard.press_and_release('esc')
    sleep(FORFEIT_ESC_SLEEP)
    findAndClickItem('forfeit')
    findAndClickItem('yesButton')

def waitForNewGame():
    print('PIPE: Wait for new game.')
    if findAndClickItemWait('playlist'):
        findAndClickItem('casual')
        findAndClickItem('1v1')

def waitForFindGame():
    print('PIPE: Wait for find game.')
    startTime = time()
    while True:
        if getMatchStatus() == 'GameStarted':
            playGame()
            return True
        elif findItem('playlist'):
            waitForNewGame()
            return True
        elif time() - startTime > WAIT_FOR_FIND_GAME_TIMEOUT:
            print('time out wait for find game')
            return False
            
        sleep(WAIT_FOR_FIND_GAME_SLEEP)

# Main
if __name__ == '__main__':
    # giris
    sleep(INIT_SLEEP)
    findAndClickItem('casual')
    findAndClickItem('1v1')

    while True:
        waitForFindGame()      