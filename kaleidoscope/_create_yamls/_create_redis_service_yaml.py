from . import _yaml_creation as yc


def create_redis_service_yaml():
    redis_service_yaml = yc.load_yaml_template(path="yaml_templates/redis_service_template.yaml")
    yc.write_yaml_file(yaml=redis_service_yaml, path='redis_service.yaml')
