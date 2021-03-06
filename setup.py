from setuptools import setup

# Pull version from source without importing
# since we can't import something we haven't built yet :)
exec(open('simpleloadtest/__version__.py').read())

setup(
    # Needed for dependency graph on GitHub
    install_requires=['numpy==1.*'],

    # Package version - taken from code, cannot be in setup.cfg file
    version=__version__,
)
