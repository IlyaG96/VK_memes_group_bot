from dotenv import load_dotenv
from random import randint
from pathlib import Path
import requests
import pathlib
import os


class VkException(Exception):
    pass


def check_for_errors(response):

    if response.get('error'):
        error_code = response['error']['error_code']
        error_msg = response['error']['error_msg']
        msg = f"Ошибка! Код ошибки: '{error_code}', текст ошибки: '{error_msg}'"

        raise VkException(msg)


def get_xkcd_last_comic_id():

    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    last_comic_id = response.json()["num"]

    return last_comic_id


def chose_random_number(last_comic_id):
    comic_number = randint(1, last_comic_id)

    return comic_number


def fetch_comic_description(comic_number):

    url = f"https://xkcd.com/{comic_number}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    answer = response.json()

    return answer


def download_comic(photo_link, path_to_photo):

    response = requests.get(photo_link)
    response.raise_for_status()

    with open(path_to_photo, mode="wb") as file:
        file.write(response.content)


def get_vk_upload_url(vk_token, group_id, vk_api_version):

    payload = {
        "access_token": vk_token,
        "v": vk_api_version,
        "group_id": group_id
    }
    url = "https://api.vk.com/method/photos.getWallUploadServer"
    response = requests.get(url, params=payload)
    response.raise_for_status()

    answer = response.json()
    check_for_errors(answer)

    return answer


def send_to_server(path_to_photo, upload_url):

    with open(path_to_photo, "rb") as file:
        files = {
            "file1": file,
        }
        response = requests.post(url=upload_url, files=files)
    response.raise_for_status()
    answer = response.json()
    check_for_errors(answer)

    return answer


def save_on_server(vk_token,
                   user_id,
                   group_id,
                   vk_api_version,
                   vk_hash,
                   photo,
                   server):

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
    check_for_errors(answer)

    return answer


def write_message(photo_title, photo_description):

    message = f"{photo_title}\n\n" \
              f"{photo_description}\n\n" \
              f"by https://xkcd.com"

    return message


def post_photo(vk_token, user_id, group_id, vk_api_version, message, media_id):

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
    answer = response.json()
    check_for_errors(answer)

    return answer


def post_comic_on_wall(vk_token,
                       group_id,
                       vk_api_version,
                       path_to_photo,
                       photo_title,
                       photo_description):

    vk_response = get_vk_upload_url(vk_token, group_id, vk_api_version)
    upload_url = vk_response["response"]["upload_url"]
    user_id = vk_response["response"]["user_id"]

    downloaded_photo_params = send_to_server(path_to_photo, upload_url)
    vk_hash = downloaded_photo_params["hash"]
    photo = downloaded_photo_params["photo"]
    server = downloaded_photo_params["server"]

    server_response = save_on_server(vk_token,
                                     user_id,
                                     group_id,
                                     vk_api_version,
                                     vk_hash,
                                     photo,
                                     server)
    media_id = server_response["response"][0]["id"]
    message = write_message(photo_title, photo_description)

    post_photo(vk_token, user_id, group_id, vk_api_version, message, media_id)


def main():

    load_dotenv()
    photo_path = os.getenv("PHOTO_PATH", default="./photos")
    group_id = os.getenv("VK_GROUP_ID")
    vk_token = os.getenv("VK_TOKEN")
    vk_api_version = os.getenv("VK_API_VERSION", default=5.131)
    pathlib.Path(photo_path).mkdir(parents=True, exist_ok=True)

    last_comic_id = get_xkcd_last_comic_id()
    comic_number = chose_random_number(last_comic_id)
    comic_description = fetch_comic_description(comic_number)
    photo_title = comic_description["safe_title"]
    photo_description = comic_description["alt"]
    photo_link = comic_description["img"]
    file_name = os.path.basename(photo_link)
    path_to_photo = Path(photo_path, file_name)
    download_comic(photo_link, path_to_photo)

    try:
        post_comic_on_wall(vk_token,
                           group_id,
                           vk_api_version,
                           path_to_photo,
                           photo_title,
                           photo_description)
    finally:
        path_to_photo.unlink()


if __name__ == '__main__':
    main()
