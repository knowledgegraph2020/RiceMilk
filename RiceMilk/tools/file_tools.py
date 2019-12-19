import os


def convert_to_file(link, main_title, dt, content, path):
    if not os.path.exists(path):
        os.makedirs(path)
    merge_path = path + '/' + main_title.strip()
    with open(merge_path, mode='w+') as f:
        f.write(link + "\n")
        f.write(main_title + "\n")
        f.write(dt + "\n")
        f.write(content)
