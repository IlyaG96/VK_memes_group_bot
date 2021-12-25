from dotenv import load_dotenv
import requests
import pathlib
import os


def get_xkcd_response():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_comic(photo_path, photo_link):

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


def send_photo(photo_path, upload_url):
    print(1)

    with open(f"{photo_path}/photo.png", "rb") as file:
        files = {
            "file1": file,
        }
        response = requests.post(url=upload_url, files=files)
        response.raise_for_status()

    return response.json()


def save_photo(vk_token, user_id, group_id, vk_api_version, vk_hash, photo, server):

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
    answer = response.json()

    return answer


def post_photo(vk_token, user_id, group_id, vk_hash):

    payload = {
        "access_token": vk_token,
        "user_id": user_id,
        "group_id": group_id,
        "hash": vk_hash,
        "v": "5.131",
    }
    url = "https://api.vk.com/method/wall.post"
    response = requests.post(url, params=payload)
    response.raise_for_status()
    answer = response.json()

    return answer


def main():

    # environment vars
    load_dotenv()
    photo_path = os.getenv("PHOTO_PATH")
    group_id = os.getenv("VK_GROUP_ID")
    user_id = os.getenv("VK_USER_ID")
    vk_token = os.getenv("VK_TOKEN")
    vk_api_version = os.getenv("VK_API_VERSION")

    # information from xkcd
    xkcd_response = get_xkcd_response()
    photo_link = xkcd_response["img"]
    photo_title = xkcd_response["safe_title"]
    photo_description = xkcd_response["alt"]

    upload_url = get_vk_response(vk_token, group_id, vk_api_version)["response"]["upload_url"]
    downloaded_photo_params = send_photo(photo_path, upload_url)
    vk_hash = downloaded_photo_params["hash"]
    photo = downloaded_photo_params["photo"]
    server = downloaded_photo_params["server"]

    save_photo(vk_token, user_id, group_id, vk_api_version, vk_hash, photo, server)


main()


