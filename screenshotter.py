import pyautogui
import win32gui

import time
import keyboard


def screenshot(cur, window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))

            im = pyautogui.screenshot(region=(x, y, x1, y1))
            str = r"C:\Users\yashd\Desktop\rootsim{}.png".format(cur)
            im.save(str)
            return im
        else:
            print('Window not found!')
    else:
        str = "Root simulation ", cur
        im = pyautogui.screenshot(str)
        im.save("C:\Desktop")
        return im




for i in range(20):
    
    im = screenshot(i, 'Root Simulation')

    keyboard.press('SPACE')
    #keyboard.press('f4')
    #keyboard.release('f4')
    keyboard.release('SPACE')

    time.sleep(0.1)          
    
# if im:
#     im.show()