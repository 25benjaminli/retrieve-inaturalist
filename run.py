import requests
from bs4 import BeautifulSoup
import selenium as se
from selenium import webdriver
import os
from PIL import Image
import time
URL = "https://www.inaturalist.org/taxa/324242-Oscillatoria/browse_photos"

browser = webdriver.ChromeOptions()
browser.add_argument('headless')
browser = webdriver.Chrome(options=browser)

browser.get(URL)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(0.5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(0.5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(0.5)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

soup = BeautifulSoup(browser.page_source, "html.parser")

# soup.prettify()
"""
cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos-51218764-medium-jpg
cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos-51218785-medium-jpg
cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos-51218801-medium-jpg
"""
# print(soup.findAll('div'))
# print(len(soup.find_all('div')))

results = soup.find_all('div', id=lambda x: x and x.startswith('cover-image-https-inaturalist-open-data-s-3-amazonaws-com-photos'))

# print(results)

for result in results:
    url = result["style"].split('url(')[1].split(')')[0].replace('\"', '')
    print(url)
    img = requests.get(url)
    print(type(img))
    file = open(f'images/{url.split("/")[-2]}-{url.split("/")[-1]}', 'wb')
    file.write(img.content)
    file.close()