from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = "C:\Program Files\chromedriver.exe"
url = 'https://pr0gramm.com/new/!%20meme' 
DEFAULT_WAIT_TIME = 2

def element_has_class(driver, locator, class_name):
    element = driver.find_element(*locator)
    if class_name in element.get_attribute("class"):
        return element
    else:
        return False
    
def waitForElements(driver):
    # wait up to 10 seconds time in item-details
    wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)
    item_details_locator = (By.CLASS_NAME, 'item-details')
    item_details_element = wait.until(EC.visibility_of_element_located(item_details_locator))
    time_locator = (By.CLASS_NAME, 'time')
    time_element = wait.until(lambda driver: element_has_class(driver, (By.XPATH, './/a[@class="time"]'), 'time'))

    # Wait up to 10 seconds for tag-link
    wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)
    tag_link = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tag-link')))

    # Wait up to 10 seconds for score
    wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)
    score_span = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'score')))

    # Wait up to 10 seconds for the element to be present
    wait = WebDriverWait(driver, DEFAULT_WAIT_TIME)
    locator = (By.CLASS_NAME, 'item-image-actual')
    element = wait.until(EC.presence_of_element_located(locator))    

def get_html_from_links(driver):
    # Open the CSV file and read the links
    with open('C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\urls_pr0gramm.csv', 'r') as f:
        reader = csv.reader(f)
        links = [row[0] for row in reader]
    
    j = 0
    # Process links in batches of 1000
    #51865
    #58910 + 5872
    for i in range(64782, len(links), 1000):
        batch = links[i:i+1000]

        # Create an empty list to store the HTML code blocks for this batch
        html_blocks = []

        # Iterate through the links in this batch and retrieve the HTML from each link
        for link in batch:
            j += 1
            print(j)
            print(link)
            driver.get(link)
            #waitForElements(driver)
            html = driver.page_source
            html_blocks.append(html)

        # Create or open the JSON file for writing
        with open('C:\\Users\\ASUS\\OneDrive\\Desktop\\articleInfo\\pr0grammJson.json', 'a+') as f:
            # Load any existing JSON data from the file
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

            # Append the new HTML blocks to the existing data
            data += html_blocks

            # Write the data back to the file
            f.seek(0)
            json.dump(data, f, indent=4)

    
opts = Options()
opts.add_argument("user-agent=whatever you want")
driver = webdriver.Chrome(PATH,chrome_options=opts)

get_html_from_links(driver)

# Close the webdriver
driver.quit()


