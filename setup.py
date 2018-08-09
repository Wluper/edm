from setuptools import setup, find_packages

setup(

    # >>>> SETUP <<<<
    name          ='edm',
    version       ='0.0.1',
    description   ='Tools for assessing the difficulty of datasets for machine learning models',
    url           ='',
    package_index ='',
    author        ='Ed Collins',
    author_email  ='ed@wluper.com',
    license       ='MIT',

    # >>>> Actual packages, data and scripts <<<<
    packages      = find_packages(),

    # >>>> Requirements <<<<
    install_requires= [
        "numpy"
    ],
    python_requires='~=3.3'
)
