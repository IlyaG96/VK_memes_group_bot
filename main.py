import requests
import pathlib

photo_path = "/Users/ilyagabdrakhmanov/PycharmProjects/VK_memes_group_bot/photos"

def download_comic(photo_path):
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    response_info = response.json()
    title = response_info.get("safe_title")
    photo_link = response_info.get("img")
    description = response_info.get("alt")

    photo_resp = requests.get(photo_link)
    pathlib.Path(photo_path).mkdir(parents=True, exist_ok=True)


    with open(f"{photo_path}/photo.png", mode="wb") as file:

        file.write(photo_resp.content)


download_comic(photo_path)