import os
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--window-size=1920,1080")  # 無頭模式，不顯示瀏覽器視窗

folder = input("請輸入下載目錄 (./expo/xxx): ")
path = './expo/' + folder
num = int(input("輸入下載張數 (10 -> 100張):"))


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'}

# LS1 https://www.flickr.com/photos/akevchiu/galleries/72157722210730785/

# 博覽館下載
url= 'https://www.flickr.com/photos/akevchiu/galleries/72157722210730785/'

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
tags = soup.find_all('div', class_='photo-container')
# print(tags)

photo = []
for tag in tags:
	item = 'https://www.flickr.com/' + tag.a['href']
	# print(item)
	photo.append(item)

os.makedirs(path, exist_ok=True)   # 產生目錄作為存放位置

for num in photo:
	r = requests.get(num, headers=headers)   	# 開始抓圖片
	soup = BeautifulSoup(r.text, 'html.parser')
	
	tags = soup.find_all('div', class_='height-controller enable-zoom')

	try:
		for tag in tags:
			source = tag.find('img', class_='main-photo')['src']	# 圖片的網址
			title = tag.find('img', class_='main-photo')['alt']   # 圖片的標題

			src ='https:' + source
			print(src)
			print(title)
			# exit()
			fn = source.split('/')[-1]

			with open(path + '/' + fn , 'wb') as f:
				f.write(requests.get(src, headers=headers, timeout=10).content)
	except Exception as e:
		print(f'Error: {e}')

print(f'總共下載 {len(photo)} 張圖片')



