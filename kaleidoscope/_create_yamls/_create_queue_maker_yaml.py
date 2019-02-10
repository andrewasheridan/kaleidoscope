from .import _yaml_creation as yc


def add_env_var_to_yaml(yaml, name, value):
    new_env_var_name = f"      - name: {name}\n"
    new_env_var_key = f"        value: {value}\n"
    env_index = yc.get_index_of_row_label(yaml, "env:")
    yaml.insert(env_index + 1, new_env_var_name)
    yaml.insert(env_index + 2, new_env_var_key)

    return yaml


def create_queue_maker_yaml(origin_s3_bucket="s3://chainsaw-dogs-and-cats"):

    queue_maker_yaml = yc.load_yaml_template(path='yaml_templates/queue-maker-template.yaml')
    queue_maker_yaml = add_env_var_to_yaml(queue_maker_yaml, "ORIGIN_S3", f"{origin_s3_bucket}\n")
    yc.write_yaml_file(queue_maker_yaml, path='queue-maker-pod.yaml')
