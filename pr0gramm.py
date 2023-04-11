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

def downloadImages():
    save_dir = r'C:\Users\ASUS\OneDrive\Desktop\articleInfo\pr0gramm_images'
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

def scroll(driver):
    SCROLL_PAUSE_TIME = 0.1
    i = 0
    while (i < 2):
        i += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

    source = driver.page_source
    soup = BeautifulSoup(source,"html.parser")
    return soup

def getRows(soup):
    # find the <div> element with ID "stream"
    stream_div = soup.find('div', id='stream')

    # find all <div> elements with class "stream-row" that are descendants of `stream_div`
    stream_rows = stream_div.find_all('div', class_='stream-row')

    # create a new BeautifulSoup object with only the `stream_rows` elements
    new_soup = BeautifulSoup('<html><body></body></html>', 'html.parser')
    body_tag = new_soup.body
    ids = []
    for row in stream_rows:
        body_tag.append(row)
        # find all <a> elements with class "silent thumb" that are descendants of `stream_row`
        silent_thumb_links = row.find_all('a', class_='silent thumb')

        # extract the `id` attribute value of each `a` element and add it to a list
        
        for link in silent_thumb_links:
            id = link['id']
            id_number = id.replace("item-", "")
            ids.append(id_number)
    return ids, new_soup

def element_has_class(driver, locator, class_name):
    element = driver.find_element(*locator)
    if class_name in element.get_attribute("class"):
        return element
    else:
        return False

def waitForElements(driver):
    # wait up to 10 seconds time in item-details
    wait = WebDriverWait(driver, 10)
    item_details_locator = (By.CLASS_NAME, 'item-details')
    item_details_element = wait.until(EC.visibility_of_element_located(item_details_locator))
    time_locator = (By.CLASS_NAME, 'time')
    time_element = wait.until(lambda driver: element_has_class(driver, (By.XPATH, './/a[@class="time"]'), 'time'))

    # Wait up to 10 seconds for tag-link
    wait = WebDriverWait(driver, 10)
    tag_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tag-link')))

    # Wait up to 10 seconds for score
    wait = WebDriverWait(driver, 10)
    score_span = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'score')))

def getMetaData(dynamicContentSoup):

    #metadaten list
    memes_date = []
    memes_author = []
    memes_upvotes = []
    memes_downvotes = []

    # Get tags
    memes_tags = dynamicContentSoup.find_all('a', {'class': 'tag-link'})
    for tag_link in memes_tags:
        print(tag_link.string)

    # Get time
    item_details = dynamicContentSoup.find(class_='item-details')
    time_element = item_details.find('a', class_='time')

    # Get author
    author = dynamicContentSoup.find('a', class_='user')


    # Get upvotes and downvotes
    score_span = soup.find('span', class_='score')
    print(score_span)
    score_contents = score_span.contents[0]
    upvote_string, downvote_string = score_contents.split(', ')
    upvote = int(''.join(filter(str.isdigit, upvote_string)))
    downvote = int(''.join(filter(str.isdigit, downvote_string)))

    print(upvote)
    print(downvote)
    
    return memes_tags, time_element

opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

driver.get(url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stream-row')))

soup = scroll(driver)

ids, new_soup = getRows(soup)



# Set the URL of the website you want to retrieve
url = 'https://pr0gramm.com/new/5630296'

driver.get(url)

waitForElements(driver)
# Get the HTML source code of the webpage
dynamicContent = driver.page_source
dynamicContentSoup = BeautifulSoup(dynamicContent,"html.parser")

getMetaData(dynamicContentSoup)

# Close the web driver
driver.close()





# Write the HTML content to a file with the desired name
filename = 'dynamicPr0grammSite.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(dynamicContentSoup.prettify())

# save the new soup as an HTML file
filename = 'stream_rows.html'
with open(filename, 'w', encoding='utf-8') as f:
    f.write(str(new_soup))





