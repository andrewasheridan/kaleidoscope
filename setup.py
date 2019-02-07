import subprocess

from setuptools import find_packages
from setuptools import setup

PACKAGE_NAME = 'kaleidoscope/'


def generate_version_file():
    """Generate `__version.py` using the `VERSION` file"""
    filename = "__version__"
    with open("VERSION") as f:
        version = f.read().strip()

    path = PACKAGE_NAME + filename + ".py"
    with open(path, "w") as f:
        f.write('{}="{}"'.format(filename, version))

    print("Generating {}: {}".format(path, version))
    return version


def generate_git_info_file(command, filename):

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    output = output.decode().strip()

    if error:
        print(error)

    if process.returncode != 0:
        raise AssertionError(
            "Could not read git information, check directory"
        )

    path = PACKAGE_NAME + filename + ".py"
    with open(path, "w") as f:
        f.write('{} = """{}"""'.format(filename, output))

    print("Generating {}: {}".format(path, output))


def generate_git_branch_file():
    generate_git_info_file(command="git symbolic-ref -q HEAD",
                           filename="__branch__")


def generate_git_log_file():
    generate_git_info_file(command='git log -n1 --pretty="%h%n%s%n--%n%an%n%ae%n%ai"',
                           filename="__gitlog__")


def get_description():
    def get_description_lines():
        seen_desc = False

        with open('README.md') as f:
            for line in f:
                if seen_desc:
                    if line.startswith('##'):
                        break
                    line = line.strip()
                    if line:
                        yield line
                elif line.startswith('## Description'):
                    seen_desc = True

    return ' '.join(get_description_lines())


__version__ = generate_version_file()
generate_git_branch_file()
generate_git_log_file()

setup(
    name="kaleidoscope",
    version=__version__,
    description="Interface for Kaleidoscope",
    long_description=get_description(),
    url="https://github.com/andrewasheridan/kaleidoscope",
    author="Andrew Sheridan",
    author_email="sheridan@berkeley.edu",
    license="MIT",
    package_dir={'kaleidoscope': 'kaleidoscope'},
    packages=find_packages(),

)
