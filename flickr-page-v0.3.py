import requests
import os
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

while True:
    base_url = input("輸入url的連結:（預設值 https://www.flickr.com/photos/akevchiu/): ")
    if base_url != '':
        break
    
folder = input("請輸入下載目錄名稱 (./Expo/xxx): ")
path = '../Expo/' + folder
p1 = int(input("請輸入圖片下載(上)範圍 page p1: "))
p2 = int(input("輸入(下)範圍 page p2: "))


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}


options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1920,1080")  # 無頭模式，不顯示瀏覽器窗口


# 所有相片
for n in range(p1, p2+1):
    
    url = base_url + f'page{n}/'  # 分頁
    print(f'*** {url}', end='\n')
    
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_content = driver.page_source

    soup = BeautifulSoup(html_content, 'html.parser')
    tags = soup.find_all('a', class_='overlay')
    # print(tags)
    
    photo = []
    for tag in tags:
        item = 'https://www.flickr.com/' + tag['href'] + 'sizes/k'    # 圖片的大小
        # print(item)
        photo.append(item)	
    print(photo)
    # breakpoint()

    print('-'*30)
    
    os.makedirs(path, exist_ok=True)

    for url in photo:
        r = requests.get(url , headers=headers)   	
        soup = BeautifulSoup(r.text, 'html.parser')  # 網頁解析

        tags = soup.find_all('div', id='allsizes-photo')  # 擷取圖片
        try:
            for tag in tags:                
                print(f'{tag.img["src"]}')    
                file = tag.img['src']   # 圖片的網址
                fn = file.split('/')[-1]   # 圖片名稱

                with open(path + '/' + fn , 'wb') as f:
                    f.write( requests.get( file, headers=headers, timeout=10).content )   # 存取圖片
        except Exception as e:
            print(f'Error: {e}')

    print(f'總共下載 {len(photo)} 張圖片',end='\n')

    driver.quit()


