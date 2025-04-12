import win32gui
import win32ui
import win32con
from PIL import Image
from PyQt5.QtWidgets import QApplication, QDesktopWidget


app = QApplication([])  # 初始化一个QApplication实例

# 获取桌面及设置
hdesktop = win32gui.GetDesktopWindow()
desktop = QDesktopWidget()# 创建一个QDesktopWidget实例来获取屏幕信息  
width = desktop.screenGeometry().width()    # 获取屏幕的宽度和高度
height = desktop.screenGeometry().height() 
left = desktop.screenGeometry().left()# 获取主屏幕的左上角坐标
top = desktop.screenGeometry().top()        
app.quit()# 关闭应用

# 创建设备描述表及位图
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)
mem_dc = img_dc.CreateCompatibleDC()
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# 截图至内存设备描述表
mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)

# 将Bitmap数据转换为PIL Image对象并保存为JPEG
# 首先创建一个BytesIO对象来接收位图数据
bmp_data = screenshot.GetBitmapBits(True)
img = Image.frombuffer('RGB', (width, height), bmp_data, 'raw', 'BGRX', 0, 1)

# 保存为JPEG
img.save('.\\cache\\screenshot.jpg', 'JPEG')

# 内存释放
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())