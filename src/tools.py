from itertools import takewhile

def get_image_name_from_path(path):
    s = path[::-1]
    s = "".join(takewhile(lambda x: x != "/", s))[::-1]
    return s

def new_image_name(base_image_name, char):
    # assumes base_image_name only has one `.` before the extension
    image_name = base_image_name.split(".")
    new_image_name = image_name[0] + char + "." + image_name[1]
    return new_image_name
    
def save_obj(obj, filename, dir = 's3_keys/'):
    with open(dir + filename + ".pickle", "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(path):
    with open(path, "rb") as f:
        return pickle.load(f)

