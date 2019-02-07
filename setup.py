import subprocess


def generate_version_file():
    """Generate `__version.py` using the `VERSION` file"""

    with open("VERSION") as f:
        __version__ = f.read().strip()

    with open("src/__version__.py", "w") as f:
        f.write('__version__="{}"'.format(__version__))

    print("Generating src/__version__.py: {}".format(__version__))


def generate_git_info_file(command, file, direc='src/'):

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    output = output.decode().strip()

    if error:
        print(error)

    if process.returncode != 0:
        raise AssertionError(
            "Could not read git information, check directory"
        )

    path = direc + file + ".py"
    with open(path, "w") as f:
        f.write('{} = """{}"""'.format(file, output))

    print("Generating {}: {}".format(path, output))


def generate_git_branch_file():
    generate_git_info_file(command="git symbolic-ref -q HEAD",
                           file="__branch__")


def generate_git_log_file():
    generate_git_info_file(command='git log -n1 --pretty="%h%n%s%n--%n%an%n%ae%n%ai"',
                           file="__gitlog__")


generate_version_file()
generate_git_branch_file()
generate_git_log_file()
