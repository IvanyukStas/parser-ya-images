import os
import platform
import pathlib
import random
import subprocess
import time

from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup


def load_url_content(url: str, headers: dict) -> BeautifulSoup:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    with open("index.html", "w") as f:
        f.write(r.text)
    return soup


def get_image_category(
    soup,
    conteiner_for_links="a",
    class_for_links="Link PopularRequestList-Preview",
    get_item="href",
):
    category_links = []
    if isinstance(soup, BeautifulSoup):
        for link in soup.find_all(conteiner_for_links, class_=class_for_links):
            category_links.append(link)
    return category_links


def check_connection(internet):
    try:
        subprocess.check_call(["ping", "-c 1", "www.google.ru"])
        print("Internet is up again!")
        internet = True
    except subprocess.CalledProcessError:
        print("Internet is still down :(")
    return internet


def get_image_from_yandex():
    headers = {
        "acept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }
    path = pathlib.Path(pathlib.Path.cwd(), "3.jpg")
    internet = False
    print("Начинаем загрузку картинки...")
    while not internet:
        internet = check_connection(internet)
    while True:
        try:
            image_links = []
            url = "https://yandex.ru"
            url_images = "https://yandex.ru/images"
            soup = load_url_content(url_images, headers)
            print("Получил ссылки на рубрики")
            link = get_image_category(soup)[0]
            print("Загрузил первую ссылку на рубрику")
            soup = load_url_content(url + link, headers)
            links_of_images = soup.find_all("a", class_="serp-item__link")
            print("Спарсил ссылки на картинки")
            count_of_links = len(links_of_images)
            link_image = links_of_images[random.randint(0, count_of_links)]
            image_links.append(link_image.get("href"))
            link = image_links[0]
            print("Запускаю ьраузер для получения картинки")
            session = HTMLSession()
            r = session.get(url=url + link)
            r.html.render()
            soup = BeautifulSoup(r.html.html, "lxml")
            session.close()
            print("Закрыли сессию")
            print("Сварили суп")
            with open("index.html", "w") as f:
                f.write(r.html.html)
            link = soup.find("img", class_="MMImage-Origin").get("src")
            print("Получили картинку")
            print(link)
            r = requests.get(url="https:" + link)
            with open(path, "wb") as f:
                f.write(r.content)
            print("Сохранили картинку")
            time.sleep(3)
            # set new background of system
            picture_path = path
            subprocess.Popen(
                "DISPLAY=:0 GSETTINGS_BACKEND=dconf /usr/bin/gsettings set org.gnome.desktop.background picture-uri file://{0}".format(
                    picture_path
                ),
                shell=True,
            )
            print("Закончил!")
            break
        except Exception as e:
            print(e)
            print("Спим 10сек")
            time.sleep(10)


def set_wallpaper(path):
    # Check the operating system
    system_name = platform.system().lower()
    if system_name == "linux":
        command = f"gsettings set org.gnome.desktop.background picture-uri file:{path}"
        os.system(command)
