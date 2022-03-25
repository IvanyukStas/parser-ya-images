import pathlib
import subprocess
import time
import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

from functions import load_url_content, get_image_category

if __name__ == '__main__':
    headers = {
        'acept': '*/*',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    url = 'https://yandex.ru/images'
    path = pathlib.Path(pathlib.Path.cwd(), '3.jpg')
    print('Начинаем загрузку картинки...')
    while True:
        try:
            soup = load_url_content(url, headers)
            url = 'https://yandex.ru'
            print("Получил ссылки на рубрики")
            link = get_image_category(soup)[0]
            soup = load_url_content(url+link, headers)
            image_links =[]
            for link in soup.find_all('a', class_="serp-item__link")[:1]:
                image_links.append(link.get('href'))
            link = image_links[0]
            session = HTMLSession()
            r = session.get(url=url+link)
            r.html.render()
            soup = BeautifulSoup(r.html.html, 'lxml')
            link = soup.find('img', class_="MMImage-Origin").get('src')
            r = requests.get(url=link)
            with open(path, 'wb') as f:
                f.write(r.content)
            time.sleep(5)
            picture_path = path
            subprocess.Popen(
                "DISPLAY=:0 GSETTINGS_BACKEND=dconf /usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}".format(
                    picture_path), shell=True)
            print("Закончил!")
            break
        except Exception as e:
            print(e)
