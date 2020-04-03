import os


def convert_to_file(link, main_title, dt, content, path):
    if not os.path.exists(path):
        os.makedirs(path)
    merge_path = path + '/' + main_title.strip() + '.txt'
    with open(merge_path, mode='w+') as f:
        f.write(link + "\n")
        f.write(main_title + "\n")
        f.write(dt + "\n")
        f.write(content)


def add_to_exist_file(link, main_title, dt, content, path):
    
    with open(path, 'w+') as f:
        f.write(link + "\n")
        f.write(main_title + "\n")
        f.write(dt + "\n")
        f.write(content+ "\n")