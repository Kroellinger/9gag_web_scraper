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

image_ids = []
images_creation = []
image_sources = []
image_tags = []
image_upvotes = []
image_downvotes = []
image_authors = []
counter = 1

PATH = "C:\Program Files\chromedriver.exe"
url = 'https://pr0gramm.com/new/!%20meme'

def getInfoArticle(article):

    prefix = "jsid-post-"
    articleId = article.get("id")[len(prefix):]
    image_post = article.find('div', class_="image-post post-view")
    image_creation_time = article.find('span', class_="ui-post-creator__creation")



    if not(articleId in image_ids) and image_post and image_creation_time:
        image_ids.append(articleId)
        global counter # add this line
        counter = counter + 1
        print(counter)
        #get post, author and creationTime
        image_author = article.find('a', class_="ui-post-creator__author")
        time_text = image_creation_time.text

        #get tags
        tags_div = article.find('div', class_='ui-post-tags')
        tag_elements = tags_div.find_all('a')
        tags = [tag.text.strip() for tag in tag_elements]

        #get up and downvotes
        vote_ul = article.find('ul', class_='btn-vote')
        upvote_span = vote_ul.find('a', class_='up').find('span')
        downvote_span = vote_ul.find('a', class_='down').find('span')
        print(upvote_span.text)
        print(articleId)
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
            image_sources.append(src_value)
            image_authors.append(image_author)
            images_creation.append(time_text)
            image_upvotes.append(upvote_count)
            image_downvotes.append(downvote_count)
            image_tags.append(tags)

def collectArticleIds(driver):
    SCROLL_PAUSE_TIME = 1
    i = 0
    while (i < 2):
        i += 1
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        source = driver.page_source
        soup = BeautifulSoup(source,"html.parser")
        
        

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
    rows = zip(image_ids, images_creation, image_sources, image_tags, image_upvotes, image_downvotes)

    # write the rows to a CSV file
    with open("C:/Users/ASUS/OneDrive/Desktop/articleInfo/image_data.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["image_id", "image_creation", "image_source", "image_tags", "image_upvotes", "image_downvotes"])
        for row in rows:
            writer.writerow(row)

opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

driver.get(url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stream-row')))

SCROLL_PAUSE_TIME = 1
i = 0
while (i < 4):
    i += 1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

source = driver.page_source
soup = BeautifulSoup(source,"html.parser")

# find the <div> element with ID "stream"
stream_div = soup.find('div', id='stream')

# find all <div> elements with class "stream-row" that are descendants of `stream_div`
stream_rows = stream_div.find_all('div', class_='stream-row')


# create a new BeautifulSoup object with only the `stream_rows` elements
new_soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
body_tag = new_soup.body
for row in stream_rows:
    body_tag.append(row)
    # find all <a> elements with class "silent thumb" that are descendants of `stream_row`
    silent_thumb_links = row.find_all('a', class_='silent thumb')

    # extract the `id` attribute value of each `a` element and add it to a list
    ids = []
    for link in silent_thumb_links:
        ids.append(link['id'])

    print(ids)

# save the new soup as an HTML file
filename = 'stream_rows.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(str(new_soup))

# Assuming `soup` is the BeautifulSoup object you want to save
filename = 'pr0gramm.html'

# Save the prettified HTML code to a file
with open(filename, 'w', encoding='utf-8') as f:
    f.write(str(soup))



