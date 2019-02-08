def load_yaml_template(loc):
    with open(loc) as f:
        yaml = [line for line in f]
        return yaml


def get_index_of_row_label(yaml, label):
    for i, line in enumerate(yaml):
        if line.strip().startswith(label):
            return i


def update_parallelism_in_job(yaml, num):
    i = get_index_of_row_label(yaml, "parallelism")
    yaml[i] = f"  parallelism: {num}\n"
    return yaml


def write_yaml_file(yaml, filename):
    with open(filename, "w") as f:
        f.writelines(yaml)


job_yaml = load_yaml_template(loc="yaml_templates/job_template.yaml")
write_yaml_file(yaml=job_yaml, filename='job-test.yaml')
