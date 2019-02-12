from . import _yaml_creation as yc


def create_poll_yaml():
    poll_yaml = yc.load_yaml_template(path="yaml_templates/poll_template.yaml")
    yc.write_yaml_file(yaml=poll_yaml, path='poll.yaml')
