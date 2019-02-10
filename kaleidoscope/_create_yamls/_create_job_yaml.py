from . import _yaml_creation as yc


def add_env_var_to_yaml(yaml, name, value):
    new_env_var_name = f"        - name: {name}\n"
    new_env_var_key = f"          value: {value}\n"
    env_index = yc.get_index_of_row_label(yaml, "env:")
    yaml.insert(env_index + 1, new_env_var_name)
    yaml.insert(env_index + 2, new_env_var_key)

    return yaml


def _update_parallelism_in_job(yaml, num):
    i = yc.get_index_of_row_label(yaml, "parallelism")
    yaml[i] = f"  parallelism: {num}\n"
    return yaml


def create_job_yaml(origin_s3_bucket, destination_s3_bucket, num_workers=10):
    job_yaml = yc.load_yaml_template(path="yaml_templates/job_template.yaml")
    job_yaml = _update_parallelism_in_job(job_yaml, num_workers)
    job_yaml = add_env_var_to_yaml(job_yaml, "ORIGIN_S3", f"{origin_s3_bucket}")
    job_yaml = add_env_var_to_yaml(job_yaml, "DESTINATION_S3", f"{destination_s3_bucket}")

    yc.write_yaml_file(yaml=job_yaml, path='job.yaml')
