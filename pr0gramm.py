from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests

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

def getMetaData(dynamicContentSoup):

    # Get source
    img_element = dynamicContentSoup.find('img', {'class': 'item-image-actual'})
    img_src = img_element.get('src')

    # Get tags
    meme_tags_html = dynamicContentSoup.find_all('a', {'class': 'tag-link'})
    meme_tags = []
    for tag in meme_tags_html:
        meme_tags.append(tag.text)     

    # Get time
    item_details = dynamicContentSoup.find(class_='item-details')
    time_element = item_details.find('a', class_='time')
    meme_date = time_element.get('title')

    # Get author
    author = dynamicContentSoup.find('a', class_='user')

    # Get upvotes and downvotes
    item_vote_div = dynamicContentSoup.find('div', class_='item-vote')
    score_span = item_vote_div.find('span', class_='score')
    score_contents = score_span.get('title')
    upvote_string, downvote_string = score_contents.split(', ')
    upvote = int(''.join(filter(str.isdigit, upvote_string)))
    downvote = int(''.join(filter(str.isdigit, downvote_string)))

    return img_src, author, meme_tags, meme_date, upvote, downvote

def iterateIdList(ids):
    #metadaten list
    memes_source = []
    meme_tags = []
    memes_date = []
    memes_author = []
    memes_upvotes = []
    memes_downvotes = []
    img_src, meme_tags, meme_date, upvote, downvote = getMetaData(dynamicContentSoup)

opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

driver.get(url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stream-row')))

# Set the URL of the website you want to retrieve
url = 'https://pr0gramm.com/new/5630296'

driver.get(url)

# Get the HTML source code of the webpage
dynamicContent = driver.page_source
dynamicContentSoup = BeautifulSoup(dynamicContent,"html.parser")

img_src, meme_tags, meme_date, meme_upvote, meme_downvote = getMetaData(dynamicContentSoup)

# Close the web driver
driver.close()







