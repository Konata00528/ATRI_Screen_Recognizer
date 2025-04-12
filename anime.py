#file:d:\python\ATRI_Screen_Recognizer\anime.py
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLabel, QWidget
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QBrush, QMovie
import sys
import threading

class RoundedWindow(QWidget):
    def __init__(self, parent=None):
        super(RoundedWindow, self).__init__(parent)
        self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.radius = 20

        # 添加GIF动图
        self.gif_label = QLabel(self)
        self.movie = QMovie(".\\pictures\\loading.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.start()

        label = QLabel('识别中...', self)
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 100, 150, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawRoundedRect(self.rect(), self.radius, self.radius)

    def resizeEvent(self, event):
        # 调整GIF标签的大小以适应窗口
        self.gif_label.setGeometry(10, 0, self.width(), int(self.height() * 0.8))
        super().resizeEvent(event)

def listen_ocr():
    while True:
        line = sys.stdin.readline().strip()
        if line == 'exit':
            ani_app.quit()
            break

ani_app = QApplication(sys.argv)
window = RoundedWindow()

desktop = QDesktopWidget()
screen_geometry = desktop.screenGeometry()
width = screen_geometry.width()
height = screen_geometry.height()
left = screen_geometry.left()
top = screen_geometry.top()

window.setGeometry(width // 2 - 75, height, 150, 150)

animation = QPropertyAnimation(window, b"geometry")
animation.setDuration(500)
animation.setStartValue(QRect(width // 2 - 75, height, 150, 150))
animation.setEndValue(QRect(width // 2 - 75, height // 2 - 75, 150, 150))
animation.setEasingCurve(QEasingCurve.InOutQuad) 

window.show()
animation.start()
threading.Thread(target=listen_ocr, daemon=True).start()
ani_app.exec_()