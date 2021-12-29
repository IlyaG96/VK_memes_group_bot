from dotenv import load_dotenv
from random import randint
import requests
import pathlib
import os


def count_xkcd_comics():

    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()

    total_comics = response.json()["num"]

    return total_comics


def fetch_comic_description(total_comics):

    comic_number = randint(1, total_comics)
    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)

    return response.json()


def download_comic(photo_path, photo_link):
    photo = requests.get(photo_link)
    pathlib.Path(photo_path).mkdir(parents=True, exist_ok=True)

    with open(f"{photo_path}/photo.png", mode="wb") as file:
        file.write(photo.content)


def get_vk_response(vk_token, group_id, vk_api_version):

    payload = {
        "access_token": vk_token,
        "v": vk_api_version,
        "group_id": group_id
    }
    url = "https://api.vk.com/method/photos.getWallUploadServer"

    response = requests.get(url, params=payload)

    return response.json()


def send_to_server(photo_path, upload_url):

    with open(f"{photo_path}/photo.png", "rb") as file:
        files = {
            "file1": file,
        }
        response = requests.post(url=upload_url, files=files)
        response.raise_for_status()

    return response.json()


def save_on_server(photo_path, upload_url, vk_token, user_id, group_id, vk_api_version):

    downloaded_photo_params = send_to_server(photo_path, upload_url)

    vk_hash = downloaded_photo_params["hash"]
    photo = downloaded_photo_params["photo"]
    server = downloaded_photo_params["server"]

    payload = {
        "access_token": vk_token,
        "user_id": user_id,
        "group_id": group_id,
        "hash": vk_hash,
        "photo": photo,
        "server": server,
        "v": vk_api_version,
    }
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    response = requests.post(url, params=payload)
    response.raise_for_status()

    return response.json()


def post_photo(vk_token, user_id, group_id, vk_api_version, photo_path, upload_url, photo_description, photo_title):

    server_response = save_on_server(photo_path, upload_url, vk_token, user_id, group_id, vk_api_version)

    message = f"{photo_title}\n\n" \
              f"{photo_description}\n\n" \
              f"by https://xkcd.com"

    for answer in server_response["response"]:
        media_id = answer["id"]

    payload = {
        "access_token": vk_token,
        "owner_id": -int(group_id),
        "v": vk_api_version,
        "attachments": f"photo{user_id}_{media_id}",
        "message": message
    }
    url = "https://api.vk.com/method/wall.post"
    response = requests.post(url, params=payload)
    response.raise_for_status()

    return response.json()


def remove_comic(photo_path):
    file_to_rem = pathlib.Path(f"{photo_path}/photo.png")
    file_to_rem.unlink()


def main():

    load_dotenv()
    photo_path = os.getenv("PHOTO_PATH")
    group_id = os.getenv("VK_GROUP_ID")
    user_id = os.getenv("VK_USER_ID")
    vk_token = os.getenv("VK_TOKEN")
    vk_api_version = os.getenv("VK_API_VERSION")

    total_comics = count_xkcd_comics()
    comic_description = fetch_comic_description(total_comics)
    photo_title = comic_description["safe_title"]
    photo_description = comic_description["alt"]
    photo_link = comic_description["img"]

    download_comic(photo_path, photo_link)

    upload_url = get_vk_response(vk_token, group_id, vk_api_version)["response"]["upload_url"]
    post_photo(vk_token, user_id, group_id, vk_api_version, photo_path, upload_url, photo_description, photo_title)
    remove_comic(photo_path)


if __name__ == '__main__':
    main()
