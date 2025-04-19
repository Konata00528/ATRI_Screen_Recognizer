import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton, QScrollArea, QVBoxLayout
from PIL import Image
import pyperclip
import os
# 窗口初始化
app = QApplication(sys.argv)
desktop = QDesktopWidget()  # 创建一个QDesktopWidget实例来获取屏幕信息
width = desktop.screenGeometry().width()  # 获取屏幕的宽度和高度
height = desktop.screenGeometry().height()
left = desktop.screenGeometry().left()  # 获取主屏幕的左上角坐标
top = desktop.screenGeometry().top()

GUI = QWidget()
GUI.setWindowTitle('识别结果')
GUI.setGeometry(left, top, width, height)
GUI.setWindowFlags(GUI.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
background = QLabel(GUI)
background.setPixmap(QPixmap('.\\cache\\screenshot.jpg'))

def get_pixel_color(image_path, x, y):  # 获取指定坐标 (x, y) 处的颜色以确定是否启用深色主题
    with Image.open(image_path) as img:
        color = img.getpixel((x, y))
        return color

color = get_pixel_color('.\\cache\\screenshot.jpg', 350, height - 100)
if color[0] > 200 and color[1] > 200 and color[2] > 200:
    darkmode = True
else:
    darkmode = False

def read_file_to_list(file_path, encode, usefloat):  # 逐行读取txt
    with open(file_path, 'r', encoding=encode) as file:
        lines = file.readlines()
    # 去除每行末尾的换行符
    if usefloat == False:
        lines = [line.strip() for line in lines]
    else:
        lines = [float(line.strip()) for line in lines]
    return lines

def data_process():  # 字符位置计算
    global word_widths
    global words_heights
    global words_R
    global words_D
    global positions
    positions = read_file_to_list('.\\cache\\locations.txt','utf-8',True)
    word_widths = []
    words_heights = []
    words_R = []
    words_D = []
    for i in range(0,int(len(positions)),4):
        width = positions[i + 2] - positions[i]
        height = positions[i + 1] - positions[i + 3]
        word_R = positions[i]
        word_D = positions[i + 1]
        word_widths.append(width)
        words_heights.append(height)
        words_R.append(word_R)
        words_D.append(word_D)

buttons = []
contents = []

def init_words_select():  # 初始化选取字符功能
    global word_widths
    global positions
    global words
    global button
    global contents
    words = read_file_to_list('.\\cache\\contents.txt', 'utf-8', False)
    def on_button_click(text):
        if text in contents:
            contents.remove(text)
        else:
            contents.append(text)
    for i in range(len(words)):
        button = QPushButton(words[i], GUI)
        button.setCheckable(True)
        button.clicked.connect(lambda checked, t=words[i]: on_button_click(t))

        button.setGeometry(int(words_R[i]), int(words_D[i]), int(word_widths[i]), int(words_heights[i]))
        if word_widths[i] / words_heights[i] > 10:
            button.setFont(QFont('微软雅黑', 3))
        button.setStyleSheet("""
            QPushButton {
                border: 2px solid #0000FF;  /* 设置边框宽度、样式和颜色 */
                border-radius: 5px;         /* 设置边框圆角 */
                background-color: #FFFFFF;  /* 设置背景颜色 */
                color: #000000;             /* 设置文字颜色 */
            }
            QPushButton:checked {
                border-color: #FF0000;      /* 设置选中时的边框颜色 */
            }
            QPushButton:hover {
                border-color: #FF0000;      /* 设置鼠标悬停时的边框颜色 */
            }
        """)
        button.raise_()
        button.hide()
        buttons.append(button)

def words_select():  # 选取字符
    os.system('python OCR.py')
    init_words_select()
    global buttons
    print(len(buttons))
    for button in buttons:
        button.show()

def copy():  # 复制
    global contents
    string = ''
    for i in range(len(contents)):
        string += contents[i] + ' '
    pyperclip.copy(string)

# 窗口底部工具栏
tool_bar = QLabel(GUI)
tool_bar.setGeometry(-700, height - 130, 700, 100)  # 初始位置在屏幕左边缘之外
if darkmode == True:
    tool_bar.setStyleSheet("""
        QLabel {
            border-top-right-radius: 45px;  /* 设置顶部左圆角 */
            border-bottom-right-radius: 45px; /* 设置顶部右圆角 */
            background-color: #4D4D4D;     /* 设置背景颜色 */
        }
    """)
else:
    tool_bar.setStyleSheet("""
        QLabel {
            border-top-right-radius: 45px;  /* 设置顶部左圆角 */
            border-bottom-right-radius: 45px; /* 设置顶部右圆角 */
            background-color: #E6E6E6;     /* 设置背景颜色 */
        }
    """)
#插件栏
plugin_area = QScrollArea(GUI)
plugin_area.setWidgetResizable(True)
plugin_area.setStyleSheet("""
    QScrollArea {
        border: 5px solid gray;  /* 设置边框宽度、样式和颜色 */
        border-radius: 0px;         /* 设置边框圆角 */
    }
""")
plugin = QWidget()
plugin_area.setWidget(plugin)

# 关闭按钮
close_button = QPushButton(GUI)
close_button.setGeometry(-780, height - 117, 70, 70)  # 初始位置在工具栏初始位置之外
close_button.clicked.connect(lambda: close_toolbar())
if darkmode == True:
    close_button.setIcon(QIcon('.\\pictures\\toolbar_dark\\close_dark.png'))
else:
    close_button.setIcon(QIcon('.\\pictures\\toolbar_light\\close_light.png'))
close_button.setIconSize(close_button.size())
close_button.setStyleSheet('border:0;padding:0')
close_button.setToolTip('关闭')

# OCR取字按钮
ocr_button = QPushButton(GUI)
ocr_button.setGeometry(-680, height - 117, 70, 70)  # 初始位置在工具栏初始位置之外
ocr_button.clicked.connect(lambda: words_select())
if darkmode == True:
    ocr_button.setIcon(QIcon('.\\pictures\\toolbar_dark\\ocr_dark.png'))
else:
    ocr_button.setIcon(QIcon('.\\pictures\\toolbar_light\\ocr_light.png'))
ocr_button.setIconSize(ocr_button.size())
ocr_button.setStyleSheet('border:0;padding:0')
ocr_button.setToolTip('OCR取字')

# 复制按钮
copy_button = QPushButton(GUI)
copy_button.setGeometry(-580, height - 117, 70, 70)  # 初始位置在工具栏初始位置之外
copy_button.clicked.connect(copy)
if darkmode == True:
    copy_button.setIcon(QIcon('.\\pictures\\toolbar_dark\\copy_dark.png'))
else:
    copy_button.setIcon(QIcon('.\\pictures\\toolbar_light\\copy_light.png'))
copy_button.setIconSize(copy_button.size())
copy_button.setStyleSheet('border:0;padding:0')
copy_button.setToolTip('复制')

# 创建工具栏滑出动画
toolbar_animation = QPropertyAnimation(tool_bar, b"geometry")
toolbar_animation.setDuration(500)  # 动画持续时间（毫秒）
toolbar_animation.setStartValue(QRect(-700, height - 130, 700, 100))  # 初始位置
toolbar_animation.setEndValue(QRect(-10, height - 130, 700, 100))  # 结束位置
toolbar_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

# 创建按钮滑出动画
close_button_animation = QPropertyAnimation(close_button, b"geometry")
close_button_animation.setDuration(500)  # 动画持续时间（毫秒）
close_button_animation.setStartValue(QRect(-780, height - 117, 70, 70))  # 初始位置
close_button_animation.setEndValue(QRect(600, height - 117, 70, 70))  # 结束位置
close_button_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

ocr_button_animation = QPropertyAnimation(ocr_button, b"geometry")
ocr_button_animation.setDuration(500)  # 动画持续时间（毫秒）
ocr_button_animation.setStartValue(QRect(-680, height - 117, 70, 70))  # 初始位置
ocr_button_animation.setEndValue(QRect(500, height - 117, 70, 70))  # 结束位置
ocr_button_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

copy_button_animation = QPropertyAnimation(copy_button, b"geometry")
copy_button_animation.setDuration(500)  # 动画持续时间（毫秒）
copy_button_animation.setStartValue(QRect(-580, height - 117, 70, 70))  # 初始位置
copy_button_animation.setEndValue(QRect(400, height - 117, 70, 70))  # 结束位置
copy_button_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

#插件栏滑出动画
plugin_area_animation = QPropertyAnimation(plugin_area, b"geometry")
plugin_area_animation.setDuration(500)
plugin_area_animation.setStartValue(QRect(-700,height -126, 370, 90))
plugin_area_animation.setEndValue(QRect(15,height -126, 370, 90))
plugin_area_animation.setEasingCurve(QEasingCurve.InOutQuad)

# 创建工具栏收回动画
toolbar_retract_animation = QPropertyAnimation(tool_bar, b"geometry")
toolbar_retract_animation.setDuration(500)  # 动画持续时间（毫秒）
toolbar_retract_animation.setStartValue(QRect(-10, height - 130, 700, 100))  # 初始位置
toolbar_retract_animation.setEndValue(QRect(-700, height - 130, 700, 100))  # 结束位置
toolbar_retract_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

#插件栏收回动画
plugin_area_retract_animation = QPropertyAnimation(plugin_area, b"geometry")
plugin_area_retract_animation.setDuration(500)
plugin_area_retract_animation.setStartValue(QRect(15,height -126, 370, 90))
plugin_area_retract_animation.setEndValue(QRect(-700,height -126, 370, 90))
plugin_area_retract_animation.setEasingCurve(QEasingCurve.InOutQuad)
# 创建按钮收回动画
close_button_retract_animation = QPropertyAnimation(close_button, b"geometry")
close_button_retract_animation.setDuration(500)  # 动画持续时间（毫秒）
close_button_retract_animation.setStartValue(QRect(600, height - 117, 70, 70))  # 初始位置
close_button_retract_animation.setEndValue(QRect(-780, height - 117, 70, 70))  # 结束位置
close_button_retract_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

ocr_button_retract_animation = QPropertyAnimation(ocr_button, b"geometry")
ocr_button_retract_animation.setDuration(500)  # 动画持续时间（毫秒）
ocr_button_retract_animation.setStartValue(QRect(500, height - 117, 70, 70))  # 初始位置
ocr_button_retract_animation.setEndValue(QRect(-680, height - 117, 70, 70))  # 结束位置
ocr_button_retract_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线

copy_button_retract_animation = QPropertyAnimation(copy_button, b"geometry")
copy_button_retract_animation.setDuration(500)  # 动画持续时间（毫秒）
copy_button_retract_animation.setStartValue(QRect(400, height - 117, 70, 70))  # 初始位置
copy_button_retract_animation.setEndValue(QRect(-580, height - 117, 70, 70))  # 结束位置
copy_button_retract_animation.setEasingCurve(QEasingCurve.InOutQuad)  # 缓动曲线


def close_toolbar():
    toolbar_retract_animation.start()
    close_button_retract_animation.start()
    ocr_button_retract_animation.start()
    copy_button_retract_animation.start()
    plugin_area_retract_animation.start()
    # 在所有动画结束后关闭应用程序
    toolbar_retract_animation.finished.connect(app.quit)
    close_button_retract_animation.finished.connect(app.quit)
    ocr_button_retract_animation.finished.connect(app.quit)
    copy_button_retract_animation.finished.connect(app.quit)

if __name__ == '__main__':
    data_process()
    GUI.show()
    toolbar_animation.start()  # 启动工具栏滑出动画
    close_button_animation.start()  # 启动关闭按钮滑出动画
    ocr_button_animation.start()  # 启动OCR按钮滑出动画
    copy_button_animation.start()  # 启动复制按钮滑出动画
    plugin_area_animation.start()  #启动插件栏滑出动画
    sys.exit(app.exec_())