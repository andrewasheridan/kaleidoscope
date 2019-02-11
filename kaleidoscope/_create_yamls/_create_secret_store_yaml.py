from . import _yaml_creation as yc


def create_secret_store_yaml():
    secret_store_yaml = yc.load_yaml_template(path="yaml_templates/secret_store_template.yaml")
    yc.write_yaml_file(yaml=secret_store_yaml, path='secret_store.yaml')
