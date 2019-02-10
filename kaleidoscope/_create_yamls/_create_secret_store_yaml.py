from . import _yaml_creation as yc


def create_secret_store_yaml():
    job_yaml = yc.load_yaml_template(path="yaml_templates/secret_store_template.yaml")
    yc.write_yaml_file(yaml=job_yaml, path='secret_store.yaml')
