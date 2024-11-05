import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from src.extract_cards_data import get_card_data


def get_path_dir_list():
    with open("data/path_list.json", "r") as file:
        path_list = json.load(file)

    path_dirs = []
    for path in path_list:
        print(f"Getting path dir from {path['name']}")
        path_dirs.append(path["path_dir"])
    return path_dirs


def extract_data_from_path(path_dir):
    data = []
    for path in path_dir:
        print(f"Extracting data from {path}")
        data += get_card_data(html_path=path)

    with open("data/cards_extracted.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"Data extraction finished. {len(data)} cards extracted.")

    return data


def download_image_from_url(url, file_name):
    import requests

    response = requests.get(url)
    with open(file_name, "wb") as file:
        file.write(response.content)


def _download_image(card):
    print(f"Downloading {card['name']}...")
    safe_name = re.sub(
        r"[^a-zA-Z0-9_]", "_", card["name"].replace(" ", "_").replace(".", "")
    )
    path = "static/{}_{}.png".format(safe_name, card["slug"])

    if os.path.exists(path):
        print(f"File {path} already exists, skipping")
        return

    download_image_from_url(card["illustration_img_url"], path)
    print(f"Downloaded {card['name']}")


def _batch_download_images(card_list, batch_size=5):
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for i in range(0, len(card_list), batch_size):
            batch = card_list[i : i + batch_size]
            executor.map(_download_image, batch)

            print(f"Downloaded batch {i // batch_size + 1}")
            time.sleep(0.5)


def delete_files_with_special_chars(directory="static"):
    valid_pattern = re.compile(r"^[a-zA-Z0-9._-]+$")

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if not valid_pattern.match(filename):
            os.remove(file_path)
            print(f"Deleted file with special characters: {filename}")

    print("Completed check for special characters in filenames.")


if __name__ == "__main__":
    DOWNLOAD_IMAGES = True
    CHECK_SPECIAL_CHARS = False
    path_dir_list = get_path_dir_list()
    card_list = extract_data_from_path(path_dir_list)
    print("Data extraction finished")

    if DOWNLOAD_IMAGES:
        if CHECK_SPECIAL_CHARS:
            delete_files_with_special_chars("static")

        _batch_download_images(card_list)
        print("Images downloaded")
