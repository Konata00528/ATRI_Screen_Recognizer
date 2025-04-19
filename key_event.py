import keyboard
import os
#监听键盘事件函数
def key_event():
    while True:
        if keyboard.is_pressed('win+space'):
            os.system('python get_screenshot.py')
            os.system('python GUI.py')
key_event()