'''匯入套件'''
import json, os, time, re
from urllib import parse
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import random

'''放置 古騰堡計劃 中文書 metadata 的資訊'''
listData = []

'''中文書的網址'''
url = 'https://www.gutenberg.org/browse/languages/zh'

'''設定標頭'''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

# 取得中文書的主要連結
def getMainLinks():
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.text, "lxml")
    a_elms = soup.select('li.pgdbetext a')
    for a in a_elms:
        listData.append({
            "title": a.text,
            "link": "https://www.gutenberg.org" + a.get('href')
        })
        
# 取得中文書的內文連結
def getSubLinks():
  
    for i in range(len(listData)):
        urlNum = (listData[i]['link']).split('ebooks/')[1]
        linkurl = f"https://www.gutenberg.org/files/{urlNum}/{urlNum}-0.txt"
        if 'sub_link' not in listData:
            listData[i]['sub_link'] = linkurl


def writeTxt():
    
    folderPath = "gutenberg_chinese_txt"
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
                             
    for i in range(len(listData)):
        time.sleep(random.randint(1,2))
        response = requests.get(listData[i]['sub_link'], headers = headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "lxml")
        elms = soup.select_one('body')
        strContent = elms.get_text()
        
        regex = r'[\u4E00-\u9FFF，。：「」；、？！『』]+'
        match = re.findall(regex, strContent)
        text = " ".join(match)
    
        fileName = f"{listData[i]['title']}.txt"
        fileName = fileName.replace("\r"," ")
        fileName = fileName.replace("/"," ")

        # 將小說內容存到 txt 中
        fp = open(f"{folderPath}/{fileName}", "w", encoding="utf-8")
        fp.write(text)
        fp.close()

    
    
if __name__ == "__main__":
    time1 = time.time()
    getMainLinks()
    getSubLinks()
    writeTxt()
    print(f"執行總花費時間: {time.time() - time1}")