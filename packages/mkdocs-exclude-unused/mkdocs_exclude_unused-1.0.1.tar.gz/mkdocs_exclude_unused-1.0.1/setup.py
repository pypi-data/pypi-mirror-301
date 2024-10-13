import os.path
import setuptools
from setuptools import setup

def read(name):
    mydir = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(mydir, name)).read()


setuptools.setup(
    name='mkdocs-exclude-unused',
    version='1.0.1',
    packages=['mkdocs_exclude_unused'],
    url='https://github.com/michal2612/mkdocs-exclude-unused',
    license='MIT',
    author='Michal Domanski',
    description='Simple plugin to exclude notused .md files from docs folder',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=['mkdocs'],

    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-exclude-unused = mkdocs_exclude_unused:ExcludeUnused',
        ]
    },
)