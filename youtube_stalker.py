import json
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from googleapiclient.discovery import build

API_KEY = 'AIzaSyBf5jc18A_fem2smLg4zkjCeqxttrSepN8'
CHANEL_ID = 'UC-lHJZR3Gqxm24_Vd_AJ5Yw'
BASE_URL = 'https://www.youtube.com/watch?v='
SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search?'
URL = BASE_URL + 'key={}&chanelId={}&part=snippet,id&order=date&maxResults=1'.format(API_KEY, CHANEL_ID)

youtube = build('youtube', 'v3', developerKey=API_KEY)

def check_for_vids():
    findVids = youtube.channels().list(part='contentDetails', id=CHANEL_ID).execute()
    vidID = findVids["items"][0]['contentDetails']['relatedPlaylists']['uploads']
    listNew = youtube.playlistItems().list(part='snippet',playlistId=vidID, maxResults=1).execute()
    selectVid = listNew['items'][0]['snippet']['resourceId']['videoId']

    exists = False
    with open('videoid.json', 'r') as f:
        data = json.loads(f.read())
        if data['videoId'] != selectVid:
            print(f'New video with id: [ {selectVid} ] is out')
            chrome_options = ChromeOptions()
            chrome_options.add_experimental_option('detach', True)
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome('./drivers/chromedriver', options=chrome_options)
            driver.get(BASE_URL+selectVid)
            exists = True
    
    if exists:
        with open('videoid.json', 'w') as f:
            data = {'videoId':selectVid}
            json.dump(data, f)

try:
    while True:
        check_for_vids()
        print('Checking for new releases.')
        time.sleep(30)
except KeyboardInterrupt:
    print('\n++Stopped++')
