from PyQt5.QtWidgets import QPushButton ,QWidget ,QApplication ,QSystemTrayIcon ,QMenu,QLabel,QScrollArea ,QVBoxLayout
from PyQt5.QtGui import QIcon ,QPixmap
from PyQt5.QtCore import Qt ,QRect
import sys
import os
from swich import QSwitchButton
import json
app = QApplication(sys.argv) #创建Qt应用
icon = QIcon(".\\pictures\\icon.ico") #加载图标到icon
print('主程序已启动')
#读取配置文件
json_file = 'config.json'
with open(json_file,'r') as open_file:
    config_dict = json.load(open_file)
open_file.close()

#设置窗口
setting_window = QWidget()
Placeholding = QLabel(setting_window)
setting_window.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
setting_text = QLabel("设置",Placeholding)
setting_text.setGeometry(350,10,70,50)
setting_text.setStyleSheet('font-family: "Microsoft YaHei";font-weight: bold')

#关闭按钮
close_button = QPushButton(Placeholding)
close_button.setGeometry(654,3,70,70)
close_button.setIcon(QIcon(".\\pictures\\close_button.png"))
close_button.setIconSize(close_button.size())
close_button.setStyleSheet('border:0;padding:0')
close_button.clicked.connect(lambda:save_setting())
#全部开关初始化
MR_switch = QSwitchButton(Placeholding)
MR_switch.setGeometry(QRect(600,100,100,50))
FR_switch = QSwitchButton(Placeholding)
FR_switch.setGeometry(QRect(600,180,100,50))

#展开设置窗口
def open_setting():
    if config_dict['MR'] == 'True':
        MR_switch.setOn()
    else:
        MR_switch.setOff()
    if config_dict['FR'] == 'True':
        FR_switch.setOn()
    else:
        FR_switch.setOff()
    setting_window.show()

#多语言识别功能
multi_recognition = QLabel("多语言识别",Placeholding)
multi_recognition.setStyleSheet('font-family: "Microsoft YaHei";font-size: 30px;font-weight: bold')
MR_introduce = QLabel("开启后可以识别多种语言(不开也能同时识别中英),此功能无法和快速识别同时开启",Placeholding)
MR_introduce.setStyleSheet('font-family: "Microsoft YaHei";font-size: 15px')
MR_introduce.setGeometry(10,155,700,30)
multi_recognition.setGeometry(10,100,150,50)

#快速识别功能
fast_recognition = QLabel("快速识别",Placeholding)
fast_recognition.setStyleSheet('font-family: "Microsoft YaHei";font-size: 30px;font-weight: bold')
FR_introduce = QLabel("开启后仍能识别中英文速度,但精度降低,此功能无法和多语言识别同时开启(任何开关发生冲突此项最优先)",Placeholding)
FR_introduce.setStyleSheet('font-family: "Microsoft YaHei";font-size: 15px')
FR_introduce.setGeometry(10,235,700,30)
fast_recognition.setGeometry(10,180,150,50)

#GPU加速
gpu_boost = QLabel("GPU加速",Placeholding)
gpu_boost.setStyleSheet('font-family: "Microsoft YaHei";font-size: 30px;font-weight: bold')
gpu_boost.setGeometry(10,260,150,50)
gpu_boost_introduce = QLabel("开启后识别速度会提高",Placeholding)
gpu_boost_introduce.setStyleSheet('font-family: "Microsoft YaHei";font-size: 15px')
gpu_boost_introduce.setGeometry(10,315,700,30)


#缓存
clear_cache = QLabel("清除缓存",Placeholding)
clear_cache.setStyleSheet('font-family: "Microsoft YaHei";font-size: 30px;font-weight: bold')
clear_cache.setGeometry(10,340,150,50)
clear_button = QPushButton(Placeholding)
clear_button.setGeometry(600,340,100,50)
clear_button.setText("清除缓存")
clear_button.clicked.connect(lambda:os.popen('del /f /s /q .\\cache\\*'))
clear_cache_introduce = QLabel("清除在识别过程中产生的缓存文件",Placeholding)
clear_cache_introduce.setStyleSheet('font-family: "Microsoft YaHei";font-size: 15px')
clear_cache_introduce.setGeometry(10,395,700,30)


#保存设置并退出
def save_setting():
    global json_file,config_dict,MR_switch,FR_switch
    switches = [MR_switch,FR_switch]
    keys = ['MR','FR']
    def update_config_dict(switch,config_key):
        global json_file,config_dict,MR_switch,FR_switch
        state = str(switch.getState())
        config_dict[config_key] = state
    count = 0
    for switch in switches:
        update_config_dict(switch,keys[count])
        count += 1

    open_file = open(json_file,'w')
    json.dump(config_dict,open_file,indent=4)
    setting_window.close()
    open_file.close()

#样式设置
Placeholding.setMinimumSize(700,3000)
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setWidget(Placeholding)
layout = QVBoxLayout()
layout.addWidget(scroll_area)
setting_window.setLayout(layout)
setting_window.resize(800,600)
setting_window.setWindowTitle('设置')


#关于窗口初始化
aboutwindow = QWidget()
label = QLabel(aboutwindow)
aboutwindow.resize(1600,900)
pixHAp = QPixmap(".\\pictures\\background.jpg")
label.setPixmap(pixHAp)
label.setScaledContents(True)
label.setGeometry(0,0,aboutwindow.width(),aboutwindow.height())
aboutwindow.setWindowFlags(Qt.FramelessWindowHint)
aboutwindow.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
#关于窗口文本
about_text1 = QLabel("ATRI智能识屏工具\n一款高性能的屏幕识别器",aboutwindow)
about_text1.setStyleSheet('font-family: "Microsoft YaHei";font-size: 50px;color: #1ED8F9;font-weight: bold')
about_text1.move(50,70)
about_text2 = QLabel("Developed by Konata00528\nVersion:1.0.0",aboutwindow)
about_text2.setStyleSheet('font-family: "Microsoft YaHei";font-size: 20px;color: #1ED8F9;font-weight: bold')
about_text2.setGeometry(1300,810,300,90)
about_text3 = QLabel("本工具完全开源免费,请勿倒卖",aboutwindow)
about_text3.setStyleSheet('font-family: "Microsoft YaHei";font-size: 20px;color: #CD6872;font-weight: bold')
about_text3.setGeometry(650,845,300,90)
#关闭按钮
close_button = QPushButton(aboutwindow)
close_button.setGeometry(1500,30,70,70)
close_button.setIcon(QIcon(".\\pictures\\close_button.png"))
close_button.setIconSize(close_button.size())
close_button.setStyleSheet('border:0;padding:0')
close_button.clicked.connect(lambda:aboutwindow.close())



#系统托盘初始化
tray_icon = QSystemTrayIcon(icon)
tray_icon.setIcon(icon)
tray_icon.setVisible(True)
tray_icon.setToolTip("高性能的屏幕识别器正在工作哒\n按下win+空格识屏")
tray_icon.setParent(aboutwindow)
#托盘菜单初始化
menu = QMenu()
settings = menu.addAction("设置")
about_action = menu.addAction("关于")
exit_action = menu.addAction("退出")
menu.addAction(exit_action)
tray_icon.setContextMenu(menu)
#设置按钮
settings.triggered.connect(lambda:open_setting())
#退出按钮
exit_action.triggered.connect(lambda:os.popen('taskkill /f /IM python.exe'))
#关于按钮
about_action.triggered.connect(lambda:aboutwindow.show())

os.popen("key_event.py")
tray_icon.show()
print('键盘监听程序已启动')
app.exec()