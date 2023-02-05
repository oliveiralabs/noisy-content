import json
import os
import shutil
import subprocess

import requests
import requests.utils
from slugify import slugify

from env import api_key


def request_tenor(sound_name):
    endpoint = 'https://tenor.googleapis.com/v2/search'
    client_key = "my-apps"
    search_term = requests.utils.quote(sound_name)

    url = f'{endpoint}?q={search_term}&key={api_key}&client_key={client_key}&limit=1'
    print(f'Request tenor: GET {url}')
    r = requests.get(url)

    if r.status_code == 200:
        response = json.loads(r.content)
        if len(response['results']) > 0:
            gif_url = response['results'][0]['media_formats']['nanogif']['url']
            img_url = response['results'][0]['media_formats']['nanogifpreview']['url']
        else:
            print(f'>>>>>>>>>>>>>>>>>>>>>>> Gif fallback! >>>>>> {sound_name}')
            gif_url = 'https://media.tenor.com/3f87UxkcPREAAAAS/troll-troll-face.gif'
            img_url = 'https://media.tenor.com/3f87UxkcPREAAAAT/troll-troll-face.png'
    else:
        raise Exception(f'Request fail: {r.status_code} {r.content}')

    return gif_url, img_url


def create_folder(folder_name):
    path = f'../content/{folder_name}'
    if not os.path.exists(path):
        os.makedirs(path)


def download_gif_and_img(sound_name):
    gif_url, img_url = request_tenor(sound_name)

    print(f'Downloading gif: {gif_url}')
    download(gif_url, "gif.gif")

    print(f'Downloading img: {img_url}')
    download(img_url, "image.gif")

    subprocess.call(['convert', 'image.gif', 'image.png'])

    os.remove('image.gif')

    shutil.move('gif.gif', f'../content/{sound_name}')
    shutil.move('image.png', f'../content/{sound_name}')


def download(url, out_file_name):
    response = requests.get(url)
    with open(out_file_name, 'wb') as f:
        f.write(response.content)

def create_info_json(file_path, sound_name):
    data = {"name": sound_name}
    with open(f'{file_path}/info.json', "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False)


def main():
    raw_folder = '../raw-sounds/2/'

    for file in os.listdir(raw_folder):
        print(f'>> File {file}')
        sound_name = file.replace('.ogg', '')
        folder_name_slug = slugify(sound_name)

        if os.path.isdir(f'../content/{folder_name_slug}'):
            print(f'Directory {file} already exists, skipping')
            continue

        create_folder(folder_name_slug)
        create_info_json(f'../content/{folder_name_slug}', sound_name)

        shutil.copy(f'{raw_folder}{file}', f'../content/{folder_name_slug}')

        # Renomeia pra sound.ogg
        shutil.move(f'../content/{folder_name_slug}/{file}', f'../content/{folder_name_slug}/sound.ogg')
        download_gif_and_img(folder_name_slug)


if __name__ == '__main__':
    main()
