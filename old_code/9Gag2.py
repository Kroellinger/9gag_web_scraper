from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import requests
import csv
#1450

image_ids = []
image_titels = []
images_creation = []
image_sources = []
image_tags = []
image_upvotes = []
image_downvotes = []
image_authors = []
counter = 1


banned_authors = []

PATH = "C:\Program Files\chromedriver.exe"
url = 'https://9gag.com/tag/germany'

def getInfoArticle(article):
    prefix = "jsid-post-"
    articleId = article.get("id")[len(prefix):]
    image_post = article.find('div', class_="image-post post-view")
    image_creation_time = article.find('span', class_="ui-post-creator__creation")



    if not(articleId in image_ids) and image_post and image_creation_time:
        image_ids.append(articleId)
        global counter 
        counter = counter + 1
        #get post, author and creationTime
        image_author = article.find('a', class_="ui-post-creator__author")
        time_text = image_creation_time.text

        #get title
        a_tag = article.find('a', {'class': 'badge-evt badge-track'})
        h2_tag = a_tag.find('h2')
        title = h2_tag.text.strip()

        #get tags
        tags_div = article.find('div', class_='ui-post-tags')
        tag_elements = tags_div.find_all('a')
        tags = [tag.text.strip() for tag in tag_elements]

        #get up and downvotes
        vote_ul = article.find('ul', class_='btn-vote')
        upvote_span = vote_ul.find('a', class_='up').find('span')
        downvote_span = vote_ul.find('a', class_='down').find('span')
        try:
            upvote_count = float(upvote_span.text.strip('K')) * 1000 if 'K' in upvote_span.text else float(upvote_span.text)
        except ValueError:
            upvote_count = 0

        try:
            downvote_count = float(downvote_span.text.strip('K')) * 1000 if 'K' in downvote_span.text else float(downvote_span.text)
        except ValueError:
            downvote_count = 0

        #get image source       
        img_element = image_post.find('img')
        src_value = img_element['src']
    
        if image_author and not(image_author.text.strip() in banned_authors) and not(src_value.startswith("https://miscmedia")): 
            image_titels.append(title)
            image_sources.append(src_value)
            image_authors.append(image_author)
            images_creation.append(time_text)
            image_upvotes.append(upvote_count)
            image_downvotes.append(downvote_count)
            image_tags.append(tags)

def collectArticleIds(driver):
    SCROLL_PAUSE_TIME = 0.5
    i = 0
    while (i < 750):
        i += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        source = driver.page_source
        soup = BeautifulSoup(source,"html.parser")

        articles = soup.select('article[id^="jsid-post-"]')
        for article in articles:
            getInfoArticle(article)

def downloadImages():
    save_dir = r'C:\Users\ASUS\OneDrive\Desktop\articleInfo\9gag_images'
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

def saveCsv():

    #Directory path
    dir_path = r'C:\Users\ASUS\OneDrive\Desktop\articleInfo'

    # Create the directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


    # create a list of tuples where each tuple represents a row
    rows = zip(image_ids, images_creation, image_sources, image_titels, image_tags, image_upvotes, image_downvotes)

    # write the rows to a CSV file
    with open("C:/Users/ASUS/OneDrive/Desktop/articleInfo/image_data.csv", "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["image_id", "image_creation", "image_source", "image_titels", "image_tags", "image_upvotes", "image_downvotes"])
        for row in rows:
            writer.writerow(row)

def getComments():
    links = []
    individual_posts = []
    comments = []
    for i, id in enumerate(image_ids):
        url = "https://9gag.com/gag/" + id + "#comment"
        links.append(url)
        response = requests.get(url)
        html_content = response.text
        individual_posts.append(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        elements = soup.find_all('div', class_='comment-list-item__text')
        post_comments = []
        for element in elements:
            print(element.text)
            post_comments.append(element.text)
        comments.append(post_comments)
        print(comments)
        i += 1


opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

driver.get(url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'post-view')))

collectArticleIds(driver)
saveCsv()
downloadImages()
#getComments()



def dostuff():
    articles = soup.select('article[id^="jsid-post-"]')

    soup = soup.prettify()

    with open("image_sources.html", "w", encoding="utf-8") as file:
        for image_source in image_sources:
            file.write(image_source)
            file.write('\n\n')

    with open("individual_posts.html", "w", encoding="utf-8") as file:
        for individual_post in individual_posts:
            file.write(individual_post)
            file.write('\n\n')

driver.quit()


