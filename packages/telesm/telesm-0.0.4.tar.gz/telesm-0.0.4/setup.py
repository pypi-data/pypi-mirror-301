from setuptools import setup, find_packages

setup(
    name='telesm',
    version='0.0.4',
    description='A command-line dictionary app using WordNet',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Pedram Behroozi',
    author_email='pedrambehroozi@gmail.com',
    url='https://github.com/pedrambehroozi/telesm',
    packages=find_packages(),
    install_requires=['nltk'],
    entry_points={
        'console_scripts': [
            'telesm=telesm.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)