import subprocess

import requests
from bs4 import BeautifulSoup


def load_url_content(url: str, headers: dict) -> BeautifulSoup:
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    with open('index.html', 'w') as f:
        f.write(r.text)
    return soup

def get_image_category(soup):
    category_links = []
    if isinstance(soup, BeautifulSoup):
        for link in soup.find_all('a', class_="Link PopularRequestList-Preview"):
            category_links.append(link.get('href'))
    return category_links

def check_connection(internet):
    try:
        subprocess.check_call(["ping", "-c 1", "www.google.ru"])
        print("Internet is up again!")
        internet = True
    except subprocess.CalledProcessError:
        print("Internet is still down :(")
    return internet