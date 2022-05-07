import pathlib
import random
import subprocess

import requests
from loguru import logger

from functions import (
    get_image_from_yandex,
    load_url_content,
    get_image_category,
    set_wallpaper,
)

if __name__ == "__main__":
    try:
        logger.add("./logs/file_1.log", rotation='1 day')
        logger.info("Стартуем!")
        headers = {
            "acept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }

        # get_image_from_yandex()
        main_url = "https://wall.alphacoders.com/random.php"
        logger.info("Получаем главную страницу!")
        main_soup = load_url_content(main_url, headers)
        logger.info("Получаем ид обоев!")
        image_ides = get_image_category(
            main_soup,
            conteiner_for_links="span",
            class_for_links="btn btn-primary btn-block download-button",
            get_item="data-id",
        )
        i = random.randint(0, len(image_ides))
        data_item = image_ides[0].get("data-id")
        data_type = image_ides[0].get("data-type")
        data_server = image_ides[0].get("data-server")
        json_url = "https://api.alphacoders.com/content/get-download-link"
        payloads = {
            "content_id": data_item,
            "content_type": "wallpaper",
            "file_type": data_type,
            "image_server": data_server,
        }
        response = requests.post(json_url, data=payloads, headers=headers)
        response = requests.get(response.json()["link"])
        path = pathlib.Path(pathlib.Path.cwd(), "1.jpg")
        with open(path, "wb") as f:
            f.write(response.content)
        logger.info("Оппа заебись!")
        set_wallpaper(path)
        print("end")
    except Exception as e:
        print(e)
