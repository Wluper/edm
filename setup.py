from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    longDescription = fh.read()

setup(

    # >>>> SETUP <<<<
    name                            = 'edm',
    version                         = '0.0.4',
    description                     = 'Tools for assessing the difficulty of datasets for machine learning models',
    long_description                = longDescription,
    long_description_content_type   = "text/markdown",
    url                             = 'https://github.com/Wluper/edm',
    # package_index                   = '',
    author                          = 'Ed Collins',
    author_email                    = 'ed@wluper.com',
    license                         = 'GPL v2',

    # >>>> Actual packages, data and scripts <<<<
    packages      = find_packages(),

    # >>>> Requirements <<<<
    install_requires= [
        "numpy"
    ],
    python_requires='~=3.3'
)
