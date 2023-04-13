import time
import csv
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


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

def scroll(driver):

    SCROLL_PAUSE_TIME = 3
    i = 0
    while (i < 1):
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

def save_ids_to_csv(ids):
    # Open the CSV file for writing
    with open('C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\id_pr0gramm.csv', 'w', newline='') as f:
        # Create a CSV writer object
        writer = csv.writer(f)
        
        # Write the IDs to the CSV file
        writer.writerows([[id] for id in ids])

def save_urls_to_csv(url_list):
    # Open the CSV file for writing
    with open('C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\urls_pr0gramm.csv', 'w', newline='') as f:
        # Create a CSV writer object
        writer = csv.writer(f)
        
        # Write the IDs to the CSV file
        writer.writerows([[url] for url in url_list])

opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

driver.get(url)
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'stream-row')))

soup = scroll(driver)

ids, new_soup = getRows(soup)

url_list = [f'https://pr0gramm.com/new/{id}' for id in ids]

save_ids_to_csv(ids)

save_urls_to_csv(url_list)