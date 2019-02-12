from . import _yaml_creation as yc


def create_redis_master_yaml():
    redis_yaml = yc.load_yaml_template(path="yaml_templates/redis_master_template.yaml")
    yc.write_yaml_file(yaml=redis_yaml, path='redis_master.yaml')
