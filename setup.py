
def generate_version_file():
    """Generate `__version.py` using the `VERSION` file"""

    with open("VERSION") as VERSION:
        __version__ = VERSION.read().strip()

    with open("src/__version__.py", "w") as version:
        version.write('__version__="{}"'.format(__version__))

    print("Generating src/__version__.py: {}".format(__version__))


generate_version_file()
