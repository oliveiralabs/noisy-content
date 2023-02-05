import json
import os

result = []
ignored_dirs = ["gen-index.py", ".idea", ".git", ".gitignore", "index.html", "index.json"]

folders = [f for f in os.listdir('../content') if f not in ignored_dirs]

for folder in folders:
    print(f'Folder --> "{folder}"')
    with open(f'../content/{folder}/info.json', 'r') as file:
        data = json.load(file)

    obj = {
        'name': data['name'],
        'folder': folder
    }

    result.append(obj)

with open('../index.json', 'w') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

# subprocess.call(['convert', file_path, '-resize', '150', file_path])
