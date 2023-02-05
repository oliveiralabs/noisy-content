import json

import requests


def get_array_from_json():
    with open('myinstants.json') as f:
        return json.load(f)


def download(url, out_file):
    response = requests.get(url)
    with open(out_file, 'wb') as f:
        f.write(response.content)


def main():
    array = get_array_from_json()
    for item in array:
        print(f'>>>> {item["title"]}')
        url = f'https://www.myinstants.com{item["url"]}'
        out_file = f'../raw-sounds/myinstants/{item["title"]}.mp3'
        download(url, out_file)


if __name__ == '__main__':
    main()
