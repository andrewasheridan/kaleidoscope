
def load_yaml_template(loc='yaml_templates/queue-maker-template.yaml'):
    with open(loc) as f:
        yaml = [line for line in f]
        return yaml


def add_env_var_to_yaml(yaml, name, value):
    new_env_var_name = f"      - name: {name}\n"
    new_env_var_key = f"        value: {value}\n"
    env_index = get_index_of_row_label(yaml, "env:")
    yaml.insert(env_index + 1, new_env_var_name)
    yaml.insert(env_index + 2, new_env_var_key)

    return yaml


def get_index_of_row_label(yaml, label):
    for i, line in enumerate(yaml):
        if line.strip().startswith(label):
            return i


def write_yaml_file(yaml, filename='queue-maker-pod.yaml'):
    with open(filename, "w") as f:
        f.writelines(yaml)


queue_maker_yaml = load_yaml_template(loc='queue-maker-template.yaml')
queue_maker_yaml = add_env_var_to_yaml(queue_maker_yaml, "ORIGIN_S3", "s3://chainsaw-dogs-and-cats\n")
write_yaml_file(queue_maker_yaml, filename='queue-maker-pod-test.yaml')
