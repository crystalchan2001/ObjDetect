from selenium import webdriver
from bs4 import BeautifulSoup
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
import time

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
            newItems.append(float(itemText))
    # print("[INFO] newItems:", newItems)
    return newItems

def handler(event=None, context=None):
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

    start = time.time()

    chrome.get(event["account"])
    soup = BeautifulSoup(chrome.page_source, "html.parser")
    time.sleep(5)
    
    divWrapperList = soup.findAll(class_="tiktok-yz6ijl-DivWrapper e1cg0wnj1")
    viewsList = soup.findAll(class_="video-count tiktok-1p23b18-StrongVideoCount e148ts222")

    urlList = []
    for div in divWrapperList:
        urlList.append(div.find('a').get('href'))

    chrome.quit()
    soup.decompose()

    end = time.time()

    print("[INFO] took", end-start, "to complete")
    # print("[INFO] urlList length:", len(urlList))
    # print("urlList:", urlList[0])


    return (urlList, toInt(viewsList))
