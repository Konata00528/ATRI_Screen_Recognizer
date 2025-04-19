import json
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID
import os
from GUI import read_file_to_list
import subprocess

content_file= open(r'.\cache\contents.txt','w',encoding='utf-8')
location_file= open(r'.\cache\locations.txt','w',encoding='utf-8')

config = open('config.json')
config_dict = json.load(config)
config.close()
result = None
anime_process = subprocess.Popen(['python', 'anime.py'],stdin=subprocess.PIPE,text=True)
def ocr_result_callback(img_path: str, results: dict):
    global result
    result = results

ocr_manager = OcrManager(r'.\OCR')
ocr_manager.SetExePath(r'.\OCR\WeChatOCR\WeChatOCR.exe')
ocr_manager.SetUsrLibDir(r'.\OCR')
ocr_manager.SetOcrResultCallback(ocr_result_callback)
ocr_manager.StartWeChatOCR()
ocr_manager.DoOCRTask(r'.\cache\screenshot.jpg')
while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
    pass
ocr_manager.KillWeChatOCR()

#格式化输出
for primary_item in result['ocrResult']:
    content_file.write(primary_item['text']+'\n')
content_file.close()

for primary_item in result['ocrResult']:
    location_file.write(str(primary_item['location']['left'])+'\n')
    location_file.write(str(primary_item['location']['top'])+'\n')
    location_file.write(str(primary_item['location']['right'])+'\n')
    location_file.write(str(primary_item['location']['bottom'])+'\n')




anime_process.stdin.write('exit\n')
anime_process.stdin.flush()
anime_process.communicate()