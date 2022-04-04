import pathlib
import random
import subprocess
import time
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from functions import load_url_content, get_image_category, check_connection

if __name__ == '__main__':
    headers = {
        'acept': '*/*',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    #path to the image
    path = pathlib.Path(pathlib.Path.cwd(), '3.jpg')
    internet = False
    print('Начинаем загрузку картинки...')
    while not internet:
        internet = check_connection(internet)
    while True:
        try:
            image_links = []
            url = 'https://yandex.ru'
            url_images = 'https://yandex.ru/images'
            soup = load_url_content(url_images, headers)
            print("Получил ссылки на рубрики")
            link = get_image_category(soup)[0]
            soup = load_url_content(url+link, headers)
            links_of_images = soup.find_all('a', class_="serp-item__link")
            count_of_links = len(links_of_images)
            link_image = links_of_images[random.randint(0, count_of_links)]
            image_links.append(link_image.get('href'))
            link = image_links[0]
            session = HTMLSession()
            r = session.get(url=url+link)
            r.html.render()
            soup = BeautifulSoup(r.html.html, 'lxml')
            link = soup.find('img', class_="MMImage-Origin").get('src')
            r = requests.get(url=link)
            with open(path, 'wb') as f:
                f.write(r.content)
            time.sleep(3)
            # set new background of system
            picture_path = path
            subprocess.Popen(
                "DISPLAY=:0 GSETTINGS_BACKEND=dconf /usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}".format(
                    picture_path), shell=True)
            print("Закончил!")
            break
        except Exception as e:
            print(e)
            print('Спим 10сек')
            time.sleep(10)
