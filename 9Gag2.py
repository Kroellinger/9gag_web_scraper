from bs4 import BeautifulSoup
from selenium import webdriver
import sys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from lxml import etree
import requests
import os


PATH = "C:\Program Files\chromedriver.exe"
opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)
url1 = 'https://9gag.com/tag/germany'

driver.get(url1)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'post-view')))

source = driver.page_source
soup = BeautifulSoup(source,"html.parser")

SCROLL_PAUSE_TIME = 1
image_articels = []
image_ids = []
image_posts = []
image_sources = []
banned_authors = []
images_creation = []
i = 0
while (i < 1):
    i += 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    source = driver.page_source
    soup = BeautifulSoup(source,"html.parser")
    #elements = soup.select('article[id^="jsid-post-"] .image-post.post-view')

    articles = soup.select('article[id^="jsid-post-"]')
    for article in articles:
        articleId = article.get("id")
        image_post = article.find('div', class_="image-post post-view")
        image_author = article.find('a', class_="ui-post-creator__author")
        
        if image_post:
            img_element = image_post.find('img')
            src_value = img_element['src']
     
        if image_post and image_author and not(articleId in image_ids) and not(image_author.text.strip() in banned_authors) and not(src_value.startswith("https://miscmedia")): 
            prefix = "jsid-post-"
            articleId = articleId[len(prefix):]
            image_ids.append(articleId)

            image_articels.append(article)
            image_posts.append(image_post)

            image_sources.append(src_value)
            image_creation = article.find('span', class_='ui-post-creator__creation')
            images_creation.append(image_creation)



links = []
individual_posts = []
comments = []
for i, id in enumerate(image_ids):
    url = "https://9gag.com/gag/" + id + "#comment"
    links.append(url)
    response = requests.get(url)
    print(url)
    html_content = response.text
    individual_posts.append(html_content)
    soup = BeautifulSoup(html_content, 'html.parser')
    elements = soup.find_all('div', class_='comment-list-item__text')
    post_comments = []
    for element in elements:
        print(element)
        post_comments.append(element.text)
    comments.append(post_comments)

    
       




    #parent_elements = [element.find_parents("article", id=lambda x: x and x.startswith("jsid-post-")) for element in elements]
    i += 1


articles = soup.select('article[id^="jsid-post-"]')
#articles = soup.find_all(class_="image-post post-view")

soup = soup.prettify()



#dom = etree.HTML(str(soup))
#print(dom.xpath("//article[starts-with(@id, 'jsid-post-')]"))

with open("articles.html", "w", encoding="utf-8") as file:
    for article in image_articels:
        file.write(article.prettify())
        file.write('\n\n')

with open("image_posts.html", "w", encoding="utf-8") as file:
    for post in image_posts:
        file.write(post.prettify())
        file.write('\n\n')

with open("image_sources.html", "w", encoding="utf-8") as file:
    for image_source in image_sources:
        file.write(image_source)
        file.write('\n\n')

with open("individual_posts.html", "w", encoding="utf-8") as file:
    for individual_post in individual_posts:
        file.write(individual_post)
        file.write('\n\n')


driver.quit()

save_dir = "9gag_images"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# download and save images
i = 0
for img_source in image_sources:
    save_path = os.path.join(save_dir, f"image{i}.jpg")
    response = requests.get(img_source)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    i += 1