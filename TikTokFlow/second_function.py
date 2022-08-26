from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from tempfile import mkdtemp
import re
import validators

url = "https://www.tiktok.com/@mercedesbenz/video/7130649149950807301?is_from_webapp=v1&item_id=7130649149950807301"

# Converts stats of format [string int/bs4.element][K/M/B] into a float 
def toInt(listIn):
    newItems = []
    d = { 'K' : 1, 'M' : 3, 'B' : 6}
    for item in listIn:
        itemText = item
        if type(item) not in (str, int):
            itemText = item.text
        if itemText[-1] in d:
            num, power = itemText[:-1], itemText[-1]
            newItems.append(float(num) * (1000 ** d[power]))
        else:
            try:
                newItems.append(float(itemText))
            except ValueError:
                newItems.append(None)
    # print("[INFO] newItems:", newItems)
    return newItems

# Uses Regex to extract the TikTok account name from the url
# If it cannot be detected, the name is default to "unnamedAccount"
def getAccountName(accountUrl):
    try:
        found = re.search('@(.+?)[?]', accountUrl)
        return found.group(1)
    except AttributeError:
        return "unnamedAccount"


def test(event=None, context=None):
    try:
        videoUrl = str(event["url"])
    except KeyError:
        return "[UNSUCCESSFUL] Please enter a url"
    
    valid = validators.url(videoUrl) and videoUrl.startswith("https://www.tiktok.com/@")
    if valid:
        start = time.time()
    
        options = webdriver.ChromeOptions()
        options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        chrome = webdriver.Chrome("/opt/chromedriver",
                                options=options)
        
        chrome.get(videoUrl)                    
        time.sleep(5)
        soup = BeautifulSoup(chrome.page_source, "html.parser")

        try:
            src = soup.find(class_="xgplayer-container").find('video').get('src')
        except AttributeError:
            src = "None"
        
        try:
            caption = soup.find(class_="tiktok-j6dmhd-ImgPoster e1yey0rl1").get('alt')
        except AttributeError:
            caption = "None"
        
        # videos = pd.DataFrame({'Video URL':src, 'Caption':caption, 'Views':0, 'Likes':toInt(likes), 
        #                     'Comments':toInt(comments), 'Shares':toInt(shares)})
        likesCommentsSharesTxt = soup.findAll(class_="tiktok-wxn977-StrongText edu4zum2")
        likesCommentsShares = []
        print(likesCommentsSharesTxt[0].text)

        try:
            likesCommentsShares.append(likesCommentsSharesTxt[0].text)
        except IndexError:
            likesCommentsShares.append(None)

        try:
            likesCommentsShares.append(likesCommentsSharesTxt[1].text)
        except IndexError:
            likesCommentsShares.append(None)

        try:
            likesCommentsShares.append(likesCommentsSharesTxt[2].text)
        except IndexError:
            likesCommentsShares.append(None)

        likesCommentsSharesInt = toInt(likesCommentsShares)

        chrome.quit()
        soup.decompose()

        end = time.time()
        print("[INFO] took", end-start, "and", end-start-5, "without sleep.")
        return (caption, src, likesCommentsSharesInt[0], likesCommentsSharesInt[1], likesCommentsSharesInt[2])

print(test({"url":url}))
