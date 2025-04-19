from paddleocr import PaddleOCR
import json
from os import system
from GUI import read_file_to_list
import subprocess

config = open('config.json')
config_dict = json.load(config)
config.close()


# 模型路径下必须含有model和params文件
ocr = PaddleOCR(show_log=True,use_gpu=False)
if config_dict['MR'] == "True" :
    ocr = PaddleOCR(det_model_dir = ".\\models\\Multilingual_PP-OCRv3_det_infer")
if config_dict['FR'] == "True" :
    ocr = PaddleOCR(det_model_dir = ".\\models\\ch_PP-OCRv3_det_slim_infer")


img_path = '.\\cache\\screenshot.jpg'
anime_process = subprocess.Popen(['python', 'anime.py'],stdin=subprocess.PIPE,text=True)
result = ocr.ocr(img_path)
print(result)
position_file=open('.\\cache\\positions.txt','w')
for unit in result:
    for info in unit:
        for xy in info[0]:
            for position in xy:
                position_file.write(str(position)+'\n')
                #格式化坐标
position_file.close()

contents_file=open('.\\cache\\contents.txt','w')
contents = []
for unit in result:
    for info in unit:
        for content in info[1]:
            contents.append(content)#格式化内容

for i in range(0,len(contents)):
    if i < len(contents):
        contents.pop(i+1)
for content in contents:
    contents_file.write(content+'\n')#提取内容
contents_file.close()


word_widths = []
words_heights = []
words_R = []
words_D = []
def arrange_words():  # 字符位置计算
    global word_widths
    global words_heights
    global words_R
    global words_D
    global positions
    positions = read_file_to_list('.\\cache\\positions.txt','utf-8',True)
    for i in range(0,int(len(positions)),8):
        width = positions[i + 2] - positions[i]
        height = positions[i + 5] - positions[i + 1]
        word_R = positions[i]
        word_D = positions[i + 1]
        word_widths.append(width)
        words_heights.append(height)
        words_R.append(word_R)
        words_D.append(word_D)
anime_process.stdin.write('exit\n')
anime_process.stdin.flush()
anime_process.communicate()
system('GUI.py')