import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import sys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



PATH = "C:\Program Files\chromedriver.exe"

opts = Options()
opts.add_argument("user-agent=whatever you want")

driver = webdriver.Chrome(PATH,chrome_options=opts)

# data = input("Search: ")
# n = int(input("Number: "))

#url = f'https://9gag.com/search?query={data}'
url1 = 'https://9gag.com/tag/germany'

driver.get(url1)

print("Search URL:",url1, "\n")

"""
SCROLL_PAUSE_TIME = 5

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
flag = 5
while (flag>0):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    flag = flag - 1
    print(flag)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# driver.execute_script("window.scrollBy(0, document.body.scrollHeight)","")
# time.sleep(10)
"""

wait = WebDriverWait(driver, 10)

element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'post-view')))

#source = driver.execute_script("return document.documentElement.outerHTML")
source = driver.page_source
# driver.page_source

driver.quit()

soup = BeautifulSoup(source,"lxml")
soup = soup.prettify()

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='UTF-8', buffering=1)
element = soup.select_one("/html/body/div[2]/div/div[1]/div[2]/div[1]/section/div[1]/article[1]/div[1]/div/div/a/div/ picture/img")

if element:
    print(element["src"])
else:
    print("Element not found.")

with open("output4.html", "w", encoding="utf-8") as f:
    f.write(str(soup))
'''
# print(soup.prettify())

global TITLE,MEDIA,LINKS
TITLE = []
MEDIA = []
LINKS = []

for media in soup.findAll("div", class_="post-container"):
    # print(media.source,"\n")
    # try:
    #     print('Type: ', media.source.get('type'))
    #     print('Image: ', media.source.get('srcset'))
    #     print('Video: ',media.source.get('src'),"\n")
    # except:
    #     pass
    try:
        video = str(media.source.get('type'))
        video = video.split(";")[0]
        diff = str(media)

        if diff.find("post-text-container") > 1:
            flag = 1
        else:
            flag = 0

        image = media.source.get('type')
        # print(video, "\n")
        # print(image, "\n")
    except:
        pass

    if video == "video/mp4":
        # print(media.source.get("src"), "\n")
        try:
            video_link = media.source.get('src')
        except:
            pass

        if video_link not in LINKS:
            LINKS.append(video_link)
        else:
            pass

    if image == "image/webp" and flag == 1:
        # print(media.img.get("src"), "\n")
        try:
            image_link = media.source.get('srcset')
        except:
            pass

        if image_link not in LINKS:
            LINKS.append(image_link)
        else:
            pass

    else:
        pass


for i in range(len(LINKS)):
    print(LINKS[i])
    download = requests.get(LINKS[i])
    if LINKS[i].find(".mp4") > 1:
        with open("C:/Users/User/Downloads/Memes/Meme{}.mp4".format(i), "wb") as file:
            file.write(download.content)
    else:
        with open("C:/Users/User/Downloads/Memes/Meme{}.jpg".format(i), "wb") as file:
            file.write(download.content)

    print()
    '''