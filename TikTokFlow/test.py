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
        found = re.search('@(.+?)/', accountUrl)
        found2 = re.search('id=(.*)', accountUrl)
        print(found)
        name = found.group(1)
        id = found2.group(1)
        return name + id + "VidInfo.csv"
    except AttributeError:
        return "unnamedAccountVidInfo.csv"


def test(event=None, context=None):
    try:
        videoUrl = str(event["url"])
    except KeyError:
        return "[UNSUCCESSFUL] Please enter a url"
    
    valid = validators.url(videoUrl) and videoUrl.startswith("https://www.tiktok.com/@")
    if valid:
        start = time.time()
    
        options = webdriver.ChromeOptions()
        # options.binary_location = '/opt/chrome/chrome'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        # options.add_argument("--window-size=1280x1696")
        # options.add_argument("--single-process")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-dev-tools")
        # options.add_argument("--no-zygote")
        # options.add_argument(f"--user-data-dir={mkdtemp()}")
        # options.add_argument(f"--data-path={mkdtemp()}")
        # options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        # options.add_argument("--remote-debugging-port=9222")
        # chrome = webdriver.Chrome("/opt/chromedriver",
                                # options=options)
        
        driver = webdriver.Chrome("chromedriver.exe", options=options)
        driver.get(videoUrl)
                              
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

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
        print("[INFO] likesCommentsSharesTxt:", likesCommentsSharesTxt)

        try:
            likesCommentsShares.append(likesCommentsSharesTxt[0].text)
            print("[INFO] index 0", likesCommentsSharesTxt[0])
        except IndexError:
            likesCommentsShares.append(None)

        try:
            likesCommentsShares.append(likesCommentsSharesTxt[1].text)
            print("[INFO] index 1", likesCommentsSharesTxt[1])
        except IndexError:
            likesCommentsShares.append(None)

        try:
            likesCommentsShares.append(likesCommentsSharesTxt[2].text)
            print("[INFO] index 2", likesCommentsSharesTxt[2])
        except IndexError:
            likesCommentsShares.append(None)

        likesCommentsSharesInt = toInt(likesCommentsShares)

        driver.quit()
        soup.decompose()

        end = time.time()
        print("[INFO] took", end-start, "and", end-start-5, "without sleep.")
        return (caption, src, likesCommentsSharesInt[0], likesCommentsSharesInt[1], likesCommentsSharesInt[2])


import cv2


def getInfo(capIn):
    size = (int(capIn.get(3)), int(capIn.get(4)))
    frames = (capIn.get(5), capIn.get(7))

    print("[INFO] Fps:", frames[0], "Frame count:", frames[1])
    return [frames, size]

# import botocore.vendored.requests.packages.urllib3 as urllib3

def anotherTest(event, context=None):
    try:
        videoUrl = str(event["url"])
    except KeyError:
        return "[UNSUCCESSFUL] Please enter a url"
    
    valid = validators.url(videoUrl) and videoUrl.startswith("https://v16-webapp.tiktok.com") and ("type=video_mp4" in videoUrl)
    if valid:
        start = time.time()



        # accountName = getAccountName(videoUrl)
        # fileName = accountName + 'VidInfo.csv'

        bucket = "tiktok-mp4-output"
        key = "nameFromS3Storage"

        # s3 = boto3.client('s3')
        # http = urllib3.PoolManager()
        # s3.upload_fileobj(http.request('GET', url, preload_content=False), bucket, key)

        # s3_resource = boto3.resource('s3')
        # s3_resource.Object(bucket, fileName).put(Body=csv_buffer.getvalue())

        video = "I WILL RETURN"
        end = time.time()
        print("[INFO] took", end-start, "and", end-start-5, "without sleep.")
        return "SUCCESSFULLY SAVED AT", bucket, "AS", key


from io import StringIO
import boto3


def testDownload(event):
    try:
        videoUrl = str(event["url"])
    except KeyError:
        return "[UNSUCCESSFUL] Please enter a url"
    
    valid = validators.url(videoUrl) and videoUrl.startswith("https://v16-webapp.tiktok.com") and ("type=video_mp4" in videoUrl)
    if valid:
        start = time.time()


    bucket = "tiktok-mp4-output"
    s3_client = boto3.client('s3')

    cap = cv2.VideoCapture(url)
    s3_client.upload_file(cap, bucket, videoUrl)

    end = time.time()
    print("[INFO] took", end-start, "and", end-start-5, "without sleep.")


# print(test({"url":url}))

# print(getAccountName(url))
src = "https://v16-webapp.tiktok.com/a767d7f7b13f8390d4220edc3aabeb9a/62fd5562/video/tos/maliva/tos-maliva-ve-0068c799-us/2798f0a1b76e4e6f9199b6bb54573af0/?a=1988&ch=0&cr=0&dr=0&lr=tiktok_m&cd=0%7C0%7C1%7C0&cv=1&br=2762&bt=1381&cs=0&ds=3&ft=gKSYZ8Yuo0PD1l7yAsg9weY2O5LiaQ2D~k8&mime_type=video_mp4&qs=0&rc=ZWVnaTxpO2dpNGg0OGVnOUBpMzZxNTU6ZmRlZTMzZzczNEAtYl9gXjU2NTExMS8uMTJjYSNmYDIucjRnLmNgLS1kMS9zcw%3D%3D&l=20220817145344010190218222182631E4&btag=80000"
testDownload({"url":src})