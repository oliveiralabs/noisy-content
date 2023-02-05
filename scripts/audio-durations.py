import os
import subprocess


def get_duration(file_path):
    print(f'Measuring time: "{file_path.split("/")[-2:-1][0]}"')
    result = subprocess.run(["ffmpeg", "-i", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stderr.decode()
    if "Duration" in output:
        time = output.split("Duration: ")[1].split(",")[0]
        h, m, s = time.split(':')
        duration = int(h) * 3600 + int(m) * 60 + float(s)
        return duration
    else:
        return 0


def get_ogg_files(dir_path):
    ogg_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(".ogg"):
                file_path = os.path.join(root, file)
                ogg_files.append(file_path)
    return ogg_files


def sort_by_duration(ogg_files):
    return sorted(ogg_files, key=lambda x: get_duration(x), reverse=True)


def main():
    dir_path = '/home/antonio/Documents/oliveira-labs/noisy-sounds/content'
    ogg_files = get_ogg_files(dir_path)
    ogg_files_sorted = sort_by_duration(ogg_files)
    for file in ogg_files_sorted:
        duration = int(get_duration(file))
        minutes, seconds = divmod(duration, 60)
        print(f"{minutes}:{seconds} - {os.path.basename(os.path.dirname(file))}")


if __name__ == '__main__':
    main()
