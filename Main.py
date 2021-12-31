import os
import requests
from bs4 import BeautifulSoup
import sys
from yt_dlp import YoutubeDL


put_thumbnail = True

if len(sys.argv) == 1:
    url = input('Enter url: ')
elif len(sys.argv) == 2:
    url = sys.argv[1]
else:
    url = sys.argv[1]
    if str(sys.argv[2]) == 'nt':
        put_thumbnail = False


while True:

    htmlrequest = requests.get(url)
    document = BeautifulSoup(htmlrequest.text, 'html.parser')
    title = document.find('title').string.replace(" - YouTube", "").replace("|", "").replace("?", "").replace("\\", "").replace("/", "")
    thumbnail_link = document.find("link", rel="image_src")['href']
    thumbnail = requests.get(thumbnail_link, stream=True)

    finished_downloading = False
    while finished_downloading == False:
        try:
            ydl_opts = {'format': '140', 'outtmpl': f'{title}.m4a'}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
            finished_downloading = True
        except:
            pass

    print('Converting to mp3...')
    if put_thumbnail:
        with open('thumbnail.jpg', 'wb') as f:
            f.write(thumbnail.content)
        add_thumbnail = ' -i thumbnail.jpg -map 0:0 -map 1:0 -id3v2_version 3 -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\"'
    else:
        add_thumbnail = ''

    command = f'ffmpeg -y -i "{title}.m4a" -hide_banner -loglevel error{add_thumbnail} "{title}.mp3"'
    os.system(command)
    os.remove(f'{title}.m4a')
    try:
        os.remove('thumbnail.jpg')
    except:
        pass

    print(f'\n\nFinished downloading {title}')
    url = input('\nEnter another url to download another or press enter to exit: ')
    if url == (""):
        sys.exit()
    else:
        os.system('cls')