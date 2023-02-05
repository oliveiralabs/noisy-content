import os
import re
import shutil
import unicodedata


def has_special_char(sound_title):
    pattern = re.compile("[^A-Za-z0-9\s]+")
    return pattern.match(sound_title)

def remove_accents(str_with_accent):
    str_process = unicodedata.normalize("NFD", str_with_accent)
    str_process = str_process.encode("ascii", "ignore")
    str_process = str_process.decode("utf-8")
    return str_process

def replace_multiple_spaces(string):
    return re.sub(' +', ' ', string)


def main():
    raw_folder = '../raw-sounds/myinstants-ogg/'

    for file in os.listdir(raw_folder):
        sound_title = file.replace('.ogg', '')

        if has_special_char(sound_title):
            str_without_accents = remove_accents(sound_title)
            sound_title_sanitized = re.sub('[^A-Za-z0-9\s]+', '', str_without_accents)

            result = replace_multiple_spaces(sound_title_sanitized)
            new_file_name = f'{result}.ogg'
            shutil.move(f'{raw_folder}{file}', f'../raw-sounds/myinstants-sanitized/{new_file_name}')

            print(f'Old -> {file} --- New -> {new_file_name}')
        else:
            shutil.move(f'{raw_folder}{file}', f'../raw-sounds/myinstants-sanitized/{file}')


if __name__ == '__main__':
    main()
