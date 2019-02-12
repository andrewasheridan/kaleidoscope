import pkg_resources


def load_yaml_template(path):

    if pkg_resources.resource_exists('kaleidoscope', path):
        path = pkg_resources.resource_filename('kaleidoscope', path)
        with open(path) as f:
            yaml = [line for line in f]
            return yaml
    else:
        raise IOError(f"File '{path}' not found")


def get_index_of_row_label(yaml, label):
    for i, line in enumerate(yaml):
        if line.strip().startswith(label):
            return i


def write_yaml_file(yaml, path):
    with open(path, "w") as f:
        f.writelines(yaml)
