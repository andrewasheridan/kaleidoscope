from . import _yaml_creation as yc


def _update_parallelism_in_job(yaml, num):
    i = yc.get_index_of_row_label(yaml, "parallelism")
    yaml[i] = f"  parallelism: {num}\n"
    return yaml


def create_job_yaml(num_workers=10):
    job_yaml = yc.load_yaml_template(path="yaml_templates/job_template.yaml")
    job_yaml = _update_parallelism_in_job(job_yaml, num_workers)
    yc.write_yaml_file(yaml=job_yaml, path='job.yaml')
