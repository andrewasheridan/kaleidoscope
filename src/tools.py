from itertools import takewhile

def get_image_name_from_path(path):
    s = path[::-1]
    return "".join(takewhile(lambda x: x != "/", s))[::-1]

def new_image_name(base_image_name, char):
    # assumes base_image_name only has one `.` before the extension
    image_name = base_image_name.split(".")
    new_image_name = image_name[0] + char + "." + image_name[1]
    return new_image_name
    